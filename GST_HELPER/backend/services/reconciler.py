def reconcile(invoices):
    seen = {}
    matched = []
    mismatched = []

    for inv in invoices:
        gstin = inv["fields"].get("gstin", "unknown")
        invoice_no = inv["fields"].get("invoice_no", "unknown")
        key = (gstin, invoice_no)

        if key in seen:
            inv["reconciliation_status"] = "duplicate"
            matched.append(inv)
        else:
            seen[key] = inv
            inv["reconciliation_status"] = "unique"
            mismatched.append(inv)

    return {
        "matched": matched,
        "mismatched": mismatched
    }