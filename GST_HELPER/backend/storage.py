from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
INVOICE_FILE = DATA_DIR / "invoices.json"
RESULT_FILE = DATA_DIR / "results.json"


class StorageError(Exception):
    """Raised when invoice persistence cannot be completed safely."""


def init_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for file_path in (INVOICE_FILE, RESULT_FILE):
        if not file_path.exists():
            _write_items(file_path, [])


def save_invoice(data: dict[str, Any]) -> None:
    items = _read_items(INVOICE_FILE)
    items.append(data)
    _write_items(INVOICE_FILE, items)


def save_result(data: dict[str, Any]) -> None:
    items = _read_items(RESULT_FILE)
    items.append(data)
    _write_items(RESULT_FILE, items)


def get_all() -> list[dict[str, Any]]:
    return _read_items(INVOICE_FILE)


def _read_items(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            payload = json.load(file)
    except json.JSONDecodeError as exc:
        raise StorageError(f"{path.name} contains invalid JSON.") from exc
    except OSError as exc:
        raise StorageError(f"Unable to read {path.name}.") from exc

    if not isinstance(payload, list):
        raise StorageError(f"{path.name} must store a JSON array.")

    return payload


def _write_items(path: Path, items: list[dict[str, Any]]) -> None:
    try:
        with path.open("w", encoding="utf-8") as file:
            json.dump(items, file, indent=4)
    except OSError as exc:
        raise StorageError(f"Unable to write {path.name}.") from exc
