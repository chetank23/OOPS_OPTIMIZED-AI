import os
from datetime import datetime

import pandas as pd


def _flatten_item(item: dict) -> dict:
    fields = item.get("fields", {})
    validation = item.get("validation", {})
    reconciliation = item.get("reconciliation_result", {})
    ai_result = item.get("ai_result", {})

    return {
        "filename": item.get("filename", ""),
        "gstin": fields.get("gstin", ""),
        "invoice_no": fields.get("invoice_no", ""),
        "date": fields.get("date", ""),
        "taxable_value": fields.get("taxable_value", 0),
        "cgst": fields.get("cgst", 0),
        "sgst": fields.get("sgst", 0),
        "igst": fields.get("igst", 0),
        "gst_amount": fields.get("gst_amount", 0),
        "gst_amount_source": fields.get("gst_amount_source", ""),
        "amount": fields.get("amount", 0),
        "validation_status": validation.get("status", ""),
        "validation_risk_score": validation.get("risk_score", 0),
        "issues": "|".join(validation.get("issues", [])),
        "reconciliation_status": reconciliation.get("status", item.get("reconciliation_status", "")),
        "duplicate_count": len(reconciliation.get("duplicates", [])),
        "ai_anomaly": ai_result.get("anomaly", ""),
        "ai_risk_score": ai_result.get("risk_score", ""),
    }


def generate(data):
    try:
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"reports/report_{timestamp}.csv"

        flattened = [_flatten_item(item) for item in data]

        if flattened:
            pd.DataFrame(flattened).to_csv(path, index=False)

        return path
    except Exception as e:
        print(f"Report Generation Error: {str(e)}")
        return f"Error generating report: {str(e)}"
