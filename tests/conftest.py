"""Fixtures partagées par les tests.

Les tests doivent être rapides et hermétiques : aucun modèle réel, aucune base.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from fastapi.testclient import TestClient

from livraison_express.api.app import create_app
from livraison_express.bootstrap import Container, build_container
from livraison_express.config import Settings
from livraison_express.domain.entities import OrderFeatures
from livraison_express.domain.predictor import EligibilityPredictor
from livraison_express.infrastructure.dev.in_memory_order_store import InMemoryOrderStore


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
    return InMemoryOrderStore()


@pytest.fixture
def container(tmp_path: Path, fake_model: FakeModel) -> Container:
    """Return a test container: in-memory store, fake model loaded (probability 0.6)."""
    settings = Settings(
        environment="test",
        model_path=str(tmp_path / "model.joblib"),
        model_threshold=0.5,
        model_version="1.0.0",
        order_store_dsn="unused-in-test",
        log_level="INFO",
    )
    test_container = build_container(settings)
    test_container.predictor = EligibilityPredictor(
        model=fake_model, threshold=0.5, model_version="1.0.0"
    )
    return test_container


@pytest.fixture
def api_client(container: Container) -> TestClient:
    """Return a TestClient for the application, with test dependencies."""
    return TestClient(create_app(container))
