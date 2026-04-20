from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ErrorResponse(BaseModel):
    error: str
    stage: str


class InvoiceFields(BaseModel):
    """Normalized invoice fields returned by the extraction stage."""

    model_config = ConfigDict(extra="ignore")

    gstin: str | None = None
    invoice_no: str | None = None
    date: str | None = None
    taxable_value: float | None = None
    cgst: float | None = None
    sgst: float | None = None
    igst: float | None = None
    gst_amount: float | None = None
    gst_amount_source: str | None = None
    amount: float | None = None
    invoice_amount: float | None = None


class InvoiceValidationResult(BaseModel):
    status: str
    issues: list[str] = Field(default_factory=list)
    risk_score: float = 0


class ValidatedInvoiceData(BaseModel):
    fields: InvoiceFields
    validation: InvoiceValidationResult


class DuplicateInvoiceSummary(BaseModel):
    filename: str | None = None
    gstin: str | None = None
    invoice_no: str | None = None


class ReconciliationSummary(BaseModel):
    matched: int = 0
    mismatched: int = 0


class ReconciliationResult(BaseModel):
    status: str = "unknown"
    duplicates: list[DuplicateInvoiceSummary] = Field(default_factory=list)
    summary: ReconciliationSummary = Field(default_factory=ReconciliationSummary)


class AIResult(BaseModel):
    anomaly: bool
    risk_score: float


class ProcessInvoiceResponse(BaseModel):
    validated_data: ValidatedInvoiceData
    reconciliation_result: ReconciliationResult
    ai_result: AIResult
    report: str
