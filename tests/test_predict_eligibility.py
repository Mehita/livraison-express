"""Tests du cas d'usage de prédiction : on teste l'orchestration, pas le modèle."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

import pytest

from livraison_express.application.predict_eligibility import PredictEligibility
from livraison_express.domain.entities import OrderFeatures, Prediction
from livraison_express.domain.exceptions import InvalidOrderError


class RecordingPredictor:
    """Faux prédicteur : mémorise la commande reçue, renvoie un résultat prévu."""

    def __init__(self, error: Exception | None = None) -> None:
        self.received: OrderFeatures | None = None
        self._error = error

    def predict(self, order: OrderFeatures) -> Prediction:
        self.received = order
        if self._error is not None:
            raise self._error
        return Prediction(
            order_id=order.order_id,
            express_eligible=True,
            decision="oui",
            probability=0.9,
            model_version="1.0.0",
            predicted_at=datetime.now(UTC),
        )


def test_execute_delegates_to_the_predictor(sample_order: OrderFeatures) -> None:
    """The use case delegates the computation to the predictor."""
    predictor = RecordingPredictor()

    prediction = PredictEligibility(predictor).execute(sample_order)

    assert predictor.received is not None
    assert prediction.decision == "oui"
    assert prediction.order_id == predictor.received.order_id


def test_execute_assigns_an_order_id_when_missing(sample_order: OrderFeatures) -> None:
    """The use case does not persist the prediction: it guarantees an order_id."""
    predictor = RecordingPredictor()
    use_case = PredictEligibility(predictor)

    use_case.execute(sample_order)
    assert predictor.received is not None
    assert predictor.received.order_id.startswith("CMD-")

    use_case.execute(replace(sample_order, order_id="CMD-000042"))
    assert predictor.received.order_id == "CMD-000042"


def test_domain_errors_are_not_swallowed(sample_order: OrderFeatures) -> None:
    """A domain error raised by the predictor reaches the API layer unchanged."""
    predictor = RecordingPredictor(error=InvalidOrderError("variable manquante"))

    with pytest.raises(InvalidOrderError):
        PredictEligibility(predictor).execute(sample_order)
