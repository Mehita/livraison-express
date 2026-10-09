"""Tests unitaires du prédicteur (assertions de la cellule 39 du notebook).

Ces tests ne chargent aucun modèle : ils utilisent la fixture `fake_model`.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import timedelta

import pytest

from livraison_express.domain.entities import OrderFeatures, Prediction
from livraison_express.domain.exceptions import InvalidOrderError
from livraison_express.domain.predictor import EligibilityPredictor


def test_predict_returns_a_prediction(
    sample_order: OrderFeatures, fake_model: object
) -> None:
    """The predictor returns a coherent prediction for a valid order."""
    predictor = EligibilityPredictor(fake_model, threshold=0.5, model_version="1.0.0")

    prediction = predictor.predict(sample_order)

    assert isinstance(prediction, Prediction)
    assert prediction.decision in {"oui", "non"}
    assert isinstance(prediction.express_eligible, bool)
    assert 0 <= prediction.probability <= 1
    assert prediction.model_version


def test_missing_feature_raises_a_domain_error(
    sample_order: OrderFeatures, fake_model: object
) -> None:
    """An order missing a mandatory feature raises a domain exception."""
    predictor = EligibilityPredictor(fake_model, threshold=0.5, model_version="1.0.0")
    incomplete = replace(sample_order, distance_km=None)

    with pytest.raises(InvalidOrderError):
        predictor.predict(incomplete)


def test_threshold_is_honoured(sample_order: OrderFeatures, fake_model: object) -> None:
    """The decision threshold changes the outcome, it is not hardcoded."""
    lenient = EligibilityPredictor(fake_model, threshold=0.2, model_version="1.0.0")
    strict = EligibilityPredictor(fake_model, threshold=0.8, model_version="1.0.0")

    assert lenient.predict(sample_order).decision == "oui"
    assert strict.predict(sample_order).decision == "non"


def test_prediction_has_a_timestamp(
    sample_order: OrderFeatures, fake_model: object
) -> None:
    """The prediction is dated with a timezone-aware timestamp."""
    predictor = EligibilityPredictor(fake_model, threshold=0.5, model_version="1.0.0")

    predicted_at = predictor.predict(sample_order).predicted_at

    assert predicted_at.tzinfo is not None
    assert predicted_at.utcoffset() == timedelta(0)


def test_model_version_is_not_hardcoded(
    sample_order: OrderFeatures, fake_model: object
) -> None:
    """The version comes from the constructor, not from a literal in the code."""
    predictor = EligibilityPredictor(fake_model, threshold=0.5, model_version="9.9.9")

    assert predictor.predict(sample_order).model_version == "9.9.9"
