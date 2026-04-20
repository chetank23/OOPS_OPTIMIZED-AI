from __future__ import annotations

import random
from functools import lru_cache
from typing import Any, NamedTuple

try:
    from sklearn.ensemble import IsolationForest
except ModuleNotFoundError:
    IsolationForest = None

DEFAULT_GST_RATE = 18.0
MODEL_RANDOM_STATE = 42


class ModelBundle(NamedTuple):
    model: Any
    min_score: float
    max_score: float


def _coerce_amount(value: Any, field_name: str) -> float:
    try:
        amount = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a numeric value.") from exc

    if amount < 0:
        raise ValueError(f"{field_name} cannot be negative.")

    return round(amount, 2)


def _build_training_dataset() -> list[list[float]]:
    rng = random.Random(MODEL_RANDOM_STATE)
    gst_rates = [5.0, 12.0, 18.0, 28.0]
    samples: list[list[float]] = []

    # A deterministic synthetic baseline keeps the anomaly detector predictable
    # even when there is no historical training data available yet.
    for rate in gst_rates:
        for _ in range(80):
            taxable_value = rng.uniform(1000.0, 250000.0)
            gst_amount = taxable_value * rate / 100.0
            gross_amount = taxable_value + gst_amount
            jitter = rng.uniform(-0.025, 0.025)

            samples.append(
                [
                    round(gross_amount * (1 + jitter), 2),
                    round(gst_amount * (1 + jitter), 2),
                    round(rate, 2),
                ]
            )

    return samples


def _build_feature_vector(invoice_amount: float, gst_amount: float) -> list[float]:
    if invoice_amount <= 0:
        raise ValueError("invoice_amount must be greater than zero.")

    if gst_amount < 0:
        raise ValueError("gst_amount cannot be negative.")

    if gst_amount > invoice_amount:
        raise ValueError("gst_amount cannot be greater than invoice_amount.")

    taxable_value = max(invoice_amount - gst_amount, 1.0)
    implied_rate = (gst_amount / taxable_value) * 100.0 if taxable_value else DEFAULT_GST_RATE

    return [
        round(invoice_amount, 2),
        round(gst_amount, 2),
        round(implied_rate, 2),
    ]


@lru_cache(maxsize=1)
def _get_model_bundle() -> ModelBundle:
    if IsolationForest is None:
        raise RuntimeError(
            "scikit-learn is required for anomaly detection. Install dependencies from requirements.txt."
        )

    training_dataset = _build_training_dataset()
    model = IsolationForest(
        n_estimators=200,
        contamination=0.08,
        random_state=MODEL_RANDOM_STATE,
    )
    model.fit(training_dataset)

    training_scores = model.score_samples(training_dataset)
    return ModelBundle(
        model=model,
        min_score=float(min(training_scores)),
        max_score=float(max(training_scores)),
    )


def _normalize_risk_score(score: float, model_bundle: ModelBundle) -> float:
    if model_bundle.max_score == model_bundle.min_score:
        return 0.0

    normalized = (model_bundle.max_score - score) / (model_bundle.max_score - model_bundle.min_score)
    normalized = max(0.0, min(1.0, normalized))
    return round(normalized, 4)


def detect_anomaly(data: dict) -> dict:
    """Return anomaly metadata for an invoice amount and GST amount pair."""

    invoice_amount = _coerce_amount(data.get("invoice_amount"), "invoice_amount")
    gst_amount = _coerce_amount(data.get("gst_amount"), "gst_amount")
    feature_vector = _build_feature_vector(invoice_amount, gst_amount)

    model_bundle = _get_model_bundle()
    prediction = model_bundle.model.predict([feature_vector])[0]
    anomaly_score = float(model_bundle.model.score_samples([feature_vector])[0])

    return {
        "anomaly": bool(prediction == -1),
        "risk_score": _normalize_risk_score(anomaly_score, model_bundle),
    }
