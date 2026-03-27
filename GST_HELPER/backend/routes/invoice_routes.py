from fastapi import APIRouter, UploadFile, File
from typing import List
from services.ocr import extract_text
from services.extractor import extract_fields
from services.validator import validate_invoice
from services.reconciler import reconcile
from services.report import generate

from storage import save_invoice, save_result, get_all

router = APIRouter()


@router.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    print("🚀 UPLOAD API HIT")

    if not files:
        return {"error": "No files uploaded"}

    processed = []
    for f in files:
        try:
            content = await f.read()

            text = extract_text(content, f.filename)

            # DEBUG (VERY IMPORTANT)
            print("\n===== OCR TEXT =====\n", text)

            fields = extract_fields(text)
            print("Extracted Fields:", fields)

            validation = validate_invoice(fields)

            record = {
                "filename": f.filename,
                "fields": fields,
                "validation": validation
            }

            save_invoice(record)
            processed.append(record)
        except Exception as e:
            print(f"Error processing {f.filename}: {str(e)}")
            processed.append({
                "filename": f.filename,
                "error": str(e),
                "fields": {},
                "validation": {"status": "error", "issues": ["Processing failed"]}
            })

    # Reconciliation
    recon = reconcile(processed)

    save_result({
        "processed": processed,
        "reconciliation": recon
    })

    return {
        "processed": processed,
        "reconciliation": recon
    }


@router.get("/report")
def report():
    data = get_all()
    return {"file": generate(data)}