# GST Invoice AI Backend Submission

## Deliverables

- FastAPI app: [main.py](./main.py)
- AI anomaly module: [services/anomaly.py](./services/anomaly.py)
- Supporting services:
  - [services/ocr.py](./services/ocr.py)
  - [services/extractor.py](./services/extractor.py)
  - [services/validator.py](./services/validator.py)
  - [services/reconciler.py](./services/reconciler.py)
  - [services/report.py](./services/report.py)
- Tests:
  - [tests/test_extractor.py](./tests/test_extractor.py)
  - [tests/test_main.py](./tests/test_main.py)
  - [tests/test_report.py](./tests/test_report.py)

## Implemented Pipeline

`OCR -> Extract -> Validate -> Reconcile -> AI -> Report`

Endpoint:

`POST /process-invoice`

Accepts:

- invoice image upload
- invoice PDF upload

Returns:

```json
{
  "validated_data": {},
  "reconciliation_result": {},
  "ai_result": {
    "anomaly": false,
    "risk_score": 0.0
  },
  "report": "reports/report_YYYYMMDD_HHMMSS.csv"
}
```

## AI Module

[services/anomaly.py](./services/anomaly.py) uses `sklearn.ensemble.IsolationForest` and exposes:

```python
def detect_anomaly(data: dict) -> dict
```

Input keys:

- `invoice_amount`
- `gst_amount`

Output:

```json
{
  "anomaly": false,
  "risk_score": 0.0
}
```

## Run

From `GST_HELPER/backend`:

```powershell
& '..\.venv\Scripts\python.exe' -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Health check:

```powershell
curl.exe http://127.0.0.1:8000/health
```

Process an invoice:

```powershell
curl.exe -X POST http://127.0.0.1:8000/process-invoice -F "file=@D:\path\to\invoice.png"
```

## Test

From `GST_HELPER`:

```powershell
& '.\.venv\Scripts\python.exe' -m pytest backend\tests -q -p no:cacheprovider
```

Current result:

`10 passed`

## Notes

- The extractor preserves full invoice numbers such as `INV-2024-001`.
- Tax fields such as `Taxable Value`, `CGST`, `SGST`, and `IGST` are parsed and exported in reports.
- The pipeline falls back to estimated GST only when explicit tax values are missing in OCR text.
