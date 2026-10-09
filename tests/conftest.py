"""Fixtures partagées par les tests.

Les tests doivent être rapides et hermétiques : aucun modèle réel, aucune base.
"""

from __future__ import annotations

import numpy as np
import pytest

from livraison_express.domain.entities import OrderFeatures


class FakeModel:
    """Faux pipeline : expose `predict_proba` avec une probabilité fixe."""

    def __init__(self, probability: float) -> None:
        self._probability = probability

    def predict_proba(self, data: object) -> np.ndarray:
        return np.array([[1 - self._probability, self._probability]])


@pytest.fixture
def sample_order() -> OrderFeatures:
    """Return one valid order (notebook cell 36)."""
    return OrderFeatures(
        hour=14,
        day_of_week=2,
        weekend=0,
        distance_km=3.5,
        order_value_eur=89.90,
        weight_kg=2.4,
        stock_available=1,
        preparation_time_min=18,
        carrier_capacity=0.85,
        weather="normal",
        delivery_zone="centre",
        customer_type="premium",
    )


@pytest.fixture
def fake_model() -> FakeModel:
    """Return a stand-in for the scikit-learn pipeline (probability fixed at 0.6)."""
    return FakeModel(probability=0.6)


@pytest.fixture
def order_store() -> object:
    """Return a fresh InMemoryOrderStore, empty."""
    raise NotImplementedError


@pytest.fixture
def api_client() -> object:
    """Return a TestClient for the application, with test dependencies."""
    raise NotImplementedError
