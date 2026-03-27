import json, os

INVOICE_FILE = "data/invoices.json"
RESULT_FILE = "data/results.json"

def init_storage():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(INVOICE_FILE):
        with open(INVOICE_FILE, "w") as f:
            json.dump([], f)

    if not os.path.exists(RESULT_FILE):
        with open(RESULT_FILE, "w") as f:
            json.dump([], f)


def save_invoice(data):
    with open(INVOICE_FILE, "r+") as f:
        items = json.load(f)
        items.append(data)
        f.seek(0)
        json.dump(items, f, indent=4)


def save_result(data):
    with open(RESULT_FILE, "r+") as f:
        items = json.load(f)
        items.append(data)
        f.seek(0)
        json.dump(items, f, indent=4)


def get_all():
    with open(INVOICE_FILE) as f:
        return json.load(f)