from datetime import datetime
from pathlib import Path
import sys


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from services import report


def test_generate_report_includes_tax_and_ai_fields(monkeypatch):
    captured = {}

    class FixedDateTime:
        @classmethod
        def now(cls):
            return datetime(2026, 4, 18, 9, 30, 0)

    def fake_to_csv(self, path, index=False):
        captured["path"] = path
        captured["index"] = index
        captured["rows"] = self.to_dict(orient="records")
        captured["columns"] = list(self.columns)

    monkeypatch.setattr(report, "datetime", FixedDateTime)
    monkeypatch.setattr(report.pd.DataFrame, "to_csv", fake_to_csv, raising=False)

    report_path = report.generate(
        [
            {
                "filename": "invoice.png",
                "fields": {
                    "gstin": "29ABCDE1234F2Z5",
                    "invoice_no": "INV-2024-001",
                    "date": "25/03/2024",
                    "taxable_value": 100000.0,
                    "cgst": 9000.0,
                    "sgst": 9000.0,
                    "igst": None,
                    "gst_amount": 18000.0,
                    "gst_amount_source": "tax_components",
                    "amount": 118000.0,
                },
                "validation": {
                    "status": "valid",
                    "risk_score": 0,
                    "issues": [],
                },
                "reconciliation_result": {
                    "status": "unique",
                    "duplicates": [],
                },
                "ai_result": {
                    "anomaly": False,
                    "risk_score": 0.08,
                },
            }
        ]
    )

    assert report_path == "reports/report_20260418_093000.csv"
    assert captured["path"] == report_path
    assert captured["index"] is False
    assert captured["columns"] == [
        "filename",
        "gstin",
        "invoice_no",
        "date",
        "taxable_value",
        "cgst",
        "sgst",
        "igst",
        "gst_amount",
        "gst_amount_source",
        "amount",
        "validation_status",
        "validation_risk_score",
        "issues",
        "reconciliation_status",
        "duplicate_count",
        "ai_anomaly",
        "ai_risk_score",
    ]
    assert captured["rows"] == [
        {
            "filename": "invoice.png",
            "gstin": "29ABCDE1234F2Z5",
            "invoice_no": "INV-2024-001",
            "date": "25/03/2024",
            "taxable_value": 100000.0,
            "cgst": 9000.0,
            "sgst": 9000.0,
            "igst": None,
            "gst_amount": 18000.0,
            "gst_amount_source": "tax_components",
            "amount": 118000.0,
            "validation_status": "valid",
            "validation_risk_score": 0,
            "issues": "",
            "reconciliation_status": "unique",
            "duplicate_count": 0,
            "ai_anomaly": False,
            "ai_risk_score": 0.08,
        }
    ]
