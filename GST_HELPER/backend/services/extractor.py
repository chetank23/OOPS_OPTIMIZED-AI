import re


CURRENCY_PATTERN = r"(?:Rs\.?|INR|\u20B9)?"
AMOUNT_PATTERN = r"([0-9][0-9,]*(?:\.\d{1,2})?)"


def _parse_amount(value: str | None) -> float | None:
    if not value:
        return None

    return float(value.replace(",", ""))


def _normalize_text(text: str) -> str:
    normalized = text.replace("\n", " ")
    normalized = re.sub(r"\s+", " ", normalized)

    corrections = {
        "GST1N": "GSTIN",
        "Inv No": "Invoice No",
        "Inv. No": "Invoice No",
        "Invoice Number": "Invoice No",
        "Invoice #": "Invoice No",
    }

    for source, target in corrections.items():
        normalized = normalized.replace(source, target)

    return normalized.strip()


def _extract_invoice_number(text: str) -> str | None:
    patterns = [
        r"Invoice\s*No\s*[:\-]?\s*([A-Z0-9][A-Z0-9/_-]*)",
        r"\bInv(?:oice)?\s*(?:No|Number|#)\s*[:\-]?\s*([A-Z0-9][A-Z0-9/_-]*)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip(" .,:;").upper()

    return None


def _extract_labeled_amount(text: str, *labels: str) -> float | None:
    combined_labels = "|".join(labels)
    pattern = (
        rf"\b(?:{combined_labels})\b"
        rf"(?:\s*@?\s*\d{{1,2}}(?:\.\d+)?%)?"
        rf"\s*[:=\-]?\s*{CURRENCY_PATTERN}\s*{AMOUNT_PATTERN}"
    )

    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return None

    return _parse_amount(match.group(1))


def _extract_amount(text: str) -> float | None:
    return _extract_labeled_amount(
        text,
        r"Grand\s+Total",
        r"Invoice\s+Total",
        r"Total\s+Amount",
        r"Total",
        r"Amount",
    )


def _extract_tax_details(text: str) -> dict:
    taxable_value = _extract_labeled_amount(
        text,
        r"Taxable\s+Value",
        r"Taxable\s+Amount",
        r"Sub\s*Total",
    )
    cgst = _extract_labeled_amount(text, r"CGST(?:\s+Amount)?")
    sgst = _extract_labeled_amount(text, r"SGST(?:\s+Amount)?")
    igst = _extract_labeled_amount(text, r"IGST(?:\s+Amount)?")
    direct_gst_amount = _extract_labeled_amount(
        text,
        r"GST(?:\s+Amount)?",
        r"Tax(?:\s+Amount)?",
    )

    component_amounts = [amount for amount in (cgst, sgst, igst) if amount is not None]
    if component_amounts:
        gst_amount = round(sum(component_amounts), 2)
        gst_amount_source = "tax_components"
    elif direct_gst_amount is not None:
        gst_amount = direct_gst_amount
        gst_amount_source = "direct_match"
    else:
        gst_amount = None
        gst_amount_source = None

    return {
        "taxable_value": taxable_value,
        "cgst": cgst,
        "sgst": sgst,
        "igst": igst,
        "gst_amount": gst_amount,
        "gst_amount_source": gst_amount_source,
    }


def extract_fields(text):
    text = _normalize_text(text)

    gstin_match = re.search(
        r"GSTIN\s*[:\-]?\s*([0-9A-Z]{15})",
        text,
        re.IGNORECASE,
    )

    date_match = re.search(r"\b\d{2}[/-]\d{2}[/-]\d{4}\b", text)

    return {
        "gstin": gstin_match.group(1).upper() if gstin_match else None,
        "invoice_no": _extract_invoice_number(text),
        "date": date_match.group(0) if date_match else None,
        "amount": _extract_amount(text),
        **_extract_tax_details(text),
    }
