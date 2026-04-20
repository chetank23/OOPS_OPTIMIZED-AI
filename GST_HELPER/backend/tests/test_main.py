from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import main


@pytest.fixture
def client(monkeypatch):
    saved = {
        "invoices": [],
        "results": [],
    }
    report_path = str(BACKEND_DIR / "tests" / "report.csv")

    monkeypatch.setattr(main.pipeline, "load_records", lambda: [])
    monkeypatch.setattr(main.pipeline, "persist_invoice", lambda data: saved["invoices"].append(data))
    monkeypatch.setattr(main.pipeline, "persist_result", lambda data: saved["results"].append(data))
    monkeypatch.setattr(main.pipeline, "report_service", lambda data: report_path)

    with TestClient(main.app) as test_client:
        yield test_client, saved


def test_health_endpoint(client):
    api_client, _ = client

    response = api_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_process_invoice_success(client, monkeypatch):
    api_client, saved = client
    sample_text = (
        "GSTIN: 29ABCDE1234F2Z5 "
        "Invoice No: INV-2024-001 "
        "Date: 25/03/2024 "
        "Grand Total: 118000 "
        "GST Amount: 18000"
    )

    monkeypatch.setattr(main.pipeline, "ocr_service", lambda *_: sample_text)
    monkeypatch.setattr(main.pipeline, "anomaly_service", lambda data: {"anomaly": False, "risk_score": 0.12})

    response = api_client.post(
        "/process-invoice",
        files={"file": ("invoice.png", b"fake-image-content", "image/png")},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["validated_data"]["fields"]["invoice_no"] == "INV-2024-001"
    assert body["validated_data"]["fields"]["gst_amount"] == 18000.0
    assert body["validated_data"]["validation"]["status"] == "valid"
    assert body["reconciliation_result"]["status"] == "unique"
    assert body["ai_result"] == {"anomaly": False, "risk_score": 0.12}
    assert body["report"].endswith("report.csv")
    assert len(saved["invoices"]) == 1
    assert len(saved["results"]) == 1


def test_process_invoice_uses_tax_components_before_estimation(client, monkeypatch):
    api_client, _ = client
    sample_text = (
        "GSTIN: 29ABCDE1234F2Z5 "
        "Invoice No: INV-2024-010 "
        "Date: 27/03/2024 "
        "Taxable Value: 100000 "
        "CGST 9%: 9000 "
        "SGST 9%: 9000 "
        "Grand Total: 118000"
    )

    monkeypatch.setattr(main.pipeline, "ocr_service", lambda *_: sample_text)
    monkeypatch.setattr(main.pipeline, "anomaly_service", lambda data: {"anomaly": False, "risk_score": 0.08})

    response = api_client.post(
        "/process-invoice",
        files={"file": ("invoice.png", b"fake-image-content", "image/png")},
    )

    body = response.json()
    fields = body["validated_data"]["fields"]

    assert response.status_code == 200
    assert fields["taxable_value"] == 100000.0
    assert fields["cgst"] == 9000.0
    assert fields["sgst"] == 9000.0
    assert fields["igst"] is None
    assert fields["gst_amount"] == 18000.0
    assert fields["gst_amount_source"] == "tax_components"


def test_process_invoice_rejects_invalid_file_type(client):
    api_client, _ = client

    response = api_client.post(
        "/process-invoice",
        files={"file": ("invoice.txt", b"not-supported", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["stage"] == "file_validation"


def test_process_invoice_rejects_empty_upload(client):
    api_client, _ = client

    response = api_client.post(
        "/process-invoice",
        files={"file": ("empty.png", b"", "image/png")},
    )

    assert response.status_code == 400
    assert response.json()["stage"] == "file_validation"


def test_process_invoice_surfaces_anomaly_stage_input_error(client, monkeypatch):
    api_client, _ = client
    sample_text = (
        "GSTIN: 29ABCDE1234F2Z5 "
        "Invoice No: INV-2024-009 "
        "Date: 25/03/2024"
    )

    monkeypatch.setattr(main.pipeline, "ocr_service", lambda *_: sample_text)

    response = api_client.post(
        "/process-invoice",
        files={"file": ("invoice.png", b"fake-image-content", "image/png")},
    )

    assert response.status_code == 422
    assert response.json() == {
        "error": "Invoice amount and GST amount are required for anomaly detection.",
        "stage": "anomaly_detection",
    }
