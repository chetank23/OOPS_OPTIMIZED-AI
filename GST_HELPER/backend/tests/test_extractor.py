from pathlib import Path
import sys


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from services.extractor import extract_fields


def test_extract_fields_preserves_full_invoice_number_and_amount():
    text = (
        "GSTIN: 29ABCDE1234F2Z5 "
        "Invoice No: INV-2024-001 "
        "Date: 25/03/2024 "
        "Grand Total: Rs. 12,500.75"
    )

    fields = extract_fields(text)

    assert fields["gstin"] == "29ABCDE1234F2Z5"
    assert fields["invoice_no"] == "INV-2024-001"
    assert fields["date"] == "25/03/2024"
    assert fields["amount"] == 12500.75


def test_extract_fields_normalizes_ocr_aliases_and_slash_invoice_numbers():
    text = (
        "GST1N: 18AABCT1234H1Z0 "
        "Invoice Number: ab/24-25/009 "
        "Date: 26-03-2024 "
        "Total Amount: 98,000"
    )

    fields = extract_fields(text)

    assert fields["gstin"] == "18AABCT1234H1Z0"
    assert fields["invoice_no"] == "AB/24-25/009"
    assert fields["date"] == "26-03-2024"
    assert fields["amount"] == 98000.0


def test_extract_fields_parses_tax_components_and_taxable_value():
    text = (
        "GSTIN: 29ABCDE1234F2Z5 "
        "Invoice No: INV-2024-010 "
        "Date: 27/03/2024 "
        "Taxable Value: 100000 "
        "CGST 9%: 9000 "
        "SGST 9%: 9000 "
        "Grand Total: 118000"
    )

    fields = extract_fields(text)

    assert fields["taxable_value"] == 100000.0
    assert fields["cgst"] == 9000.0
    assert fields["sgst"] == 9000.0
    assert fields["igst"] is None
    assert fields["gst_amount"] == 18000.0
    assert fields["gst_amount_source"] == "tax_components"
