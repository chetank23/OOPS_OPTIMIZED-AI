from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any, Callable

from fastapi import UploadFile

from schemas import (
    AIResult,
    DuplicateInvoiceSummary,
    InvoiceFields,
    InvoiceValidationResult,
    ProcessInvoiceResponse,
    ReconciliationResult,
    ReconciliationSummary,
    ValidatedInvoiceData,
)
from services.anomaly import detect_anomaly
from services.extractor import extract_fields
from services.ocr import extract_text
from services.reconciler import reconcile
from services.report import generate
from services.validator import validate_invoice
from storage import get_all, save_invoice, save_result

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
SUPPORTED_CONTENT_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/jpg",
    "image/png",
}
DEFAULT_GST_RATE = 18.0
AMOUNT_FIELDS = ("amount", "taxable_value", "cgst", "sgst", "igst", "gst_amount")
CORE_FIELDS = ("gstin", "invoice_no", "date", "amount")


class PipelineStageError(Exception):
    """Raised when one stage of the invoice pipeline cannot complete safely."""

    def __init__(self, stage: str, message: str, status_code: int = 422) -> None:
        super().__init__(message)
        self.stage = stage
        self.message = message
        self.status_code = status_code


class InvoiceProcessingPipeline:
    """Coordinates the end-to-end GST invoice processing workflow."""

    def __init__(
        self,
        *,
        ocr_service: Callable[[bytes, str], str] = extract_text,
        extractor_service: Callable[[str], dict[str, Any]] = extract_fields,
        validation_service: Callable[[dict[str, Any]], dict[str, Any]] = validate_invoice,
        reconciliation_service: Callable[[list[dict[str, Any]]], dict[str, Any]] = reconcile,
        anomaly_service: Callable[[dict[str, Any]], dict[str, Any]] = detect_anomaly,
        report_service: Callable[[list[dict[str, Any]]], str] = generate,
        load_records: Callable[[], list[dict[str, Any]]] = get_all,
        persist_invoice: Callable[[dict[str, Any]], None] = save_invoice,
        persist_result: Callable[[dict[str, Any]], None] = save_result,
    ) -> None:
        self.ocr_service = ocr_service
        self.extractor_service = extractor_service
        self.validation_service = validation_service
        self.reconciliation_service = reconciliation_service
        self.anomaly_service = anomaly_service
        self.report_service = report_service
        self.load_records = load_records
        self.persist_invoice = persist_invoice
        self.persist_result = persist_result

    async def process_uploaded_invoice(self, file: UploadFile) -> ProcessInvoiceResponse:
        filename = self._validate_upload(file)
        file_bytes = await self._read_upload(file)

        logger.info("Processing invoice upload: %s", filename)

        raw_text = self._run_ocr(file_bytes, filename)
        fields = self._run_extraction(raw_text)
        validated_data = self._run_validation(fields)
        invoice_record, reconciliation_result = self._run_reconciliation(filename, validated_data)
        ai_result = self._run_anomaly(validated_data.fields)

        invoice_record["ai_result"] = ai_result.model_dump()
        invoice_record["reconciliation_result"] = reconciliation_result.model_dump()

        report_path = self._run_report(invoice_record)
        invoice_record["report"] = report_path

        response = ProcessInvoiceResponse(
            validated_data=validated_data,
            reconciliation_result=reconciliation_result,
            ai_result=ai_result,
            report=report_path,
        )

        self._persist(invoice_record, response.model_dump())
        logger.info("Completed invoice processing for %s", filename)
        return response

    async def _read_upload(self, file: UploadFile) -> bytes:
        try:
            file_bytes = await file.read()
        except Exception as exc:
            logger.exception("Failed to read uploaded file %s", file.filename)
            raise PipelineStageError(
                "file_validation",
                "Unable to read uploaded invoice.",
                status_code=400,
            ) from exc

        if not file_bytes:
            raise PipelineStageError(
                "file_validation",
                "Uploaded invoice is empty.",
                status_code=400,
            )

        return file_bytes

    def _validate_upload(self, file: UploadFile) -> str:
        filename = file.filename or "invoice"
        suffix = Path(filename).suffix.lower()
        content_type = (file.content_type or "").lower()

        if suffix not in SUPPORTED_EXTENSIONS and content_type not in SUPPORTED_CONTENT_TYPES:
            raise PipelineStageError(
                "file_validation",
                "Only PDF, PNG, JPG, and JPEG invoices are supported.",
                status_code=400,
            )

        return filename

    def _run_ocr(self, file_bytes: bytes, filename: str) -> str:
        try:
            raw_text = self.ocr_service(file_bytes, filename)
        except Exception as exc:
            logger.exception("OCR failed for %s", filename)
            raise PipelineStageError("ocr", "OCR failed for the uploaded invoice.", status_code=500) from exc

        if not raw_text or not raw_text.strip():
            raise PipelineStageError("ocr", "OCR did not return any text.", status_code=422)

        return raw_text

    def _run_extraction(self, raw_text: str) -> InvoiceFields:
        try:
            extracted_data = self.extractor_service(raw_text)
        except Exception as exc:
            logger.exception("Field extraction failed")
            raise PipelineStageError("extraction", "Field extraction failed.") from exc

        if not isinstance(extracted_data, dict):
            raise PipelineStageError("extraction", "Field extraction returned an invalid payload.", status_code=500)

        if not any(extracted_data.get(field) not in (None, "") for field in CORE_FIELDS):
            raise PipelineStageError("extraction", "No structured invoice fields could be extracted.")

        normalized_fields = dict(extracted_data)
        for field_name in AMOUNT_FIELDS:
            normalized_fields[field_name] = self._coerce_amount(normalized_fields.get(field_name))

        invoice_amount = normalized_fields.get("amount")
        gst_amount = normalized_fields.get("gst_amount")
        gst_amount_source = normalized_fields.get("gst_amount_source")

        # Prefer explicit tax values from the extractor and only estimate when OCR text
        # does not expose any tax amounts.
        if gst_amount is None:
            gst_amount, gst_amount_source = self._extract_gst_amount_fallback(raw_text, invoice_amount)

        normalized_fields["invoice_amount"] = invoice_amount
        normalized_fields["gst_amount"] = gst_amount
        normalized_fields["gst_amount_source"] = gst_amount_source

        return InvoiceFields.model_validate(normalized_fields)

    def _run_validation(self, fields: InvoiceFields) -> ValidatedInvoiceData:
        try:
            validation_payload = self.validation_service(fields.model_dump())
        except Exception as exc:
            logger.exception("Validation failed for invoice %s", fields.invoice_no)
            raise PipelineStageError("validation", "Validation failed.") from exc

        if not isinstance(validation_payload, dict):
            raise PipelineStageError("validation", "Validation returned an invalid payload.", status_code=500)

        validation_result = InvoiceValidationResult.model_validate(validation_payload)
        return ValidatedInvoiceData(fields=fields, validation=validation_result)

    def _run_reconciliation(
        self,
        filename: str,
        validated_data: ValidatedInvoiceData,
    ) -> tuple[dict[str, Any], ReconciliationResult]:
        current_record = {
            "filename": filename,
            "fields": validated_data.fields.model_dump(),
            "validation": validated_data.validation.model_dump(),
        }

        try:
            historical_records = self.load_records()
            reconciliation_summary = self.reconciliation_service(historical_records + [current_record])
        except Exception as exc:
            logger.exception("Reconciliation failed for %s", filename)
            raise PipelineStageError("reconciliation", "Reconciliation failed.", status_code=500) from exc

        current_key = (
            current_record["fields"].get("gstin"),
            current_record["fields"].get("invoice_no"),
        )
        duplicates: list[DuplicateInvoiceSummary] = []

        for record in reconciliation_summary.get("matched", []):
            if record is current_record:
                continue

            record_fields = record.get("fields", {})
            record_key = (record_fields.get("gstin"), record_fields.get("invoice_no"))
            if record_key == current_key:
                duplicates.append(
                    DuplicateInvoiceSummary(
                        filename=record.get("filename"),
                        gstin=record_fields.get("gstin"),
                        invoice_no=record_fields.get("invoice_no"),
                    )
                )

        return current_record, ReconciliationResult(
            status=current_record.get("reconciliation_status", "unknown"),
            duplicates=duplicates,
            summary=ReconciliationSummary(
                matched=len(reconciliation_summary.get("matched", [])),
                mismatched=len(reconciliation_summary.get("mismatched", [])),
            ),
        )

    def _run_anomaly(self, fields: InvoiceFields) -> AIResult:
        if fields.invoice_amount is None or fields.gst_amount is None:
            raise PipelineStageError(
                "anomaly_detection",
                "Invoice amount and GST amount are required for anomaly detection.",
            )

        try:
            ai_payload = self.anomaly_service(
                {
                    "invoice_amount": fields.invoice_amount,
                    "gst_amount": fields.gst_amount,
                }
            )
        except Exception as exc:
            logger.exception("Anomaly detection failed for invoice %s", fields.invoice_no)
            raise PipelineStageError(
                "anomaly_detection",
                "AI anomaly detection failed.",
            ) from exc

        if not isinstance(ai_payload, dict):
            raise PipelineStageError(
                "anomaly_detection",
                "AI anomaly detection returned an invalid payload.",
                status_code=500,
            )

        return AIResult.model_validate(ai_payload)

    def _run_report(self, invoice_record: dict[str, Any]) -> str:
        try:
            report_path = self.report_service([invoice_record])
        except Exception as exc:
            logger.exception("Report generation failed for %s", invoice_record.get("filename"))
            raise PipelineStageError("reporting", "Report generation failed.", status_code=500) from exc

        if not report_path or str(report_path).startswith("Error generating report"):
            raise PipelineStageError("reporting", "Report generation failed.", status_code=500)

        return report_path

    def _persist(self, invoice_record: dict[str, Any], response_payload: dict[str, Any]) -> None:
        try:
            self.persist_invoice(invoice_record)
            self.persist_result(response_payload)
        except Exception as exc:
            logger.exception("Failed to persist processed invoice data for %s", invoice_record.get("filename"))
            raise PipelineStageError(
                "storage",
                "Failed to persist processed invoice data.",
                status_code=500,
            ) from exc

    @staticmethod
    def _coerce_amount(value: Any) -> float | None:
        if value in (None, ""):
            return None

        if isinstance(value, (int, float)):
            return round(float(value), 2)

        normalized = re.sub(r"[^0-9.]", "", str(value))
        if not normalized:
            return None

        try:
            return round(float(normalized), 2)
        except ValueError:
            return None

    def _extract_gst_amount_fallback(self, raw_text: str, invoice_amount: float | None) -> tuple[float | None, str]:
        normalized_text = re.sub(r"\s+", " ", raw_text.replace("\n", " "))
        amount_pattern = r"([0-9][0-9,]*(?:\.\d{1,2})?)"

        component_matches = re.findall(
            rf"(?:CGST|SGST|IGST)(?:\s+Amount)?(?:\s*@?\s*\d{{1,2}}(?:\.\d+)?%)?\s*[:=\-]?\s*(?:Rs\.?|INR|{chr(8377)})?\s*{amount_pattern}",
            normalized_text,
            re.IGNORECASE,
        )
        component_amounts = [self._coerce_amount(value) for value in component_matches]
        component_amounts = [value for value in component_amounts if value is not None]
        if component_amounts:
            return round(sum(component_amounts), 2), "tax_components"

        direct_match = re.search(
            rf"\b(?:GST|Tax)\b(?:\s+Amount)?\s*[:=\-]?\s*(?:Rs\.?|INR|{chr(8377)})?\s*{amount_pattern}",
            normalized_text,
            re.IGNORECASE,
        )
        if direct_match:
            direct_amount = self._coerce_amount(direct_match.group(1))
            if direct_amount is not None:
                return direct_amount, "direct_match"

        if invoice_amount is None:
            return None, "unavailable"

        rate_match = re.search(
            r"(\d{1,2}(?:\.\d+)?)\s*%\s*\b(?:GST|Tax)\b",
            normalized_text,
            re.IGNORECASE,
        )
        if rate_match:
            rate = float(rate_match.group(1))
            estimated = invoice_amount * rate / (100.0 + rate)
            return round(estimated, 2), f"inferred_from_{rate:g}_percent_rate"

        estimated = invoice_amount * DEFAULT_GST_RATE / (100.0 + DEFAULT_GST_RATE)
        return round(estimated, 2), "estimated_default_18_percent"
