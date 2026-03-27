import re

def is_valid_gstin(gstin):
    if not gstin:
        return False
    pattern = r"^\d{2}[A-Z]{5}\d{4}[A-Z]\dZ\d$"
    return re.match(pattern, gstin) is not None


def validate_invoice(data):
    issues = []

    # GSTIN validation
    if not is_valid_gstin(data["gstin"]):
        issues.append("Invalid GSTIN")

    # Invoice number check
    if not data["invoice_no"]:
        issues.append("Missing Invoice Number")

    # Date check
    if not data["date"]:
        issues.append("Invalid or Missing Date")

    # Amount check (IMPORTANT FIX)
    if data["amount"] is None or data["amount"] <= 0:
        issues.append("Missing or Invalid Amount")

    # Risk scoring
    risk_score = min(len(issues) * 25, 100)

    return {
        "status": "valid" if not issues else "invalid",
        "issues": issues,
        "risk_score": risk_score
    }

    return {
        "status": "valid" if not issues else "invalid",
        "issues": issues,
        "risk_score": risk_score
    }