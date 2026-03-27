import re

def extract_fields(text):
    # Normalize text
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    # Handle OCR mistakes (IMPORTANT)
    text = text.replace("GST1N", "GSTIN")
    text = text.replace("Inv No", "Invoice No")

    # GSTIN
    gstin_match = re.search(
        r"GSTIN\s*[:\-]?\s*([0-9A-Z]{15})",
        text,
        re.IGNORECASE
    )

    # Invoice number
    invoice_match = re.search(
        r"Invoice\s*No\s*[:\-]?\s*(\w+)",
        text,
        re.IGNORECASE
    )

    # Date
    date_match = re.search(r"\d{2}/\d{2}/\d{4}", text)

    # Amount
    amount_match = re.search(
        r"(Total|Amount|Grand Total)\s*[:\-₹]?\s*(\d+)",
        text,
        re.IGNORECASE
    )

    return {
        "gstin": gstin_match.group(1) if gstin_match else None,
        "invoice_no": invoice_match.group(1) if invoice_match else None,
        "date": date_match.group(0) if date_match else None,
        "amount": float(amount_match.group(2)) if amount_match else None
    }