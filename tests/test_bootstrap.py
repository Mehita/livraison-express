"""Tests du câblage : on vérifie les choix pris dans `bootstrap.py`."""

from __future__ import annotations

from pathlib import Path

import pytest

from livraison_express.bootstrap import build_container
from livraison_express.config import Settings
from livraison_express.domain.entities import OrderFeatures
from livraison_express.domain.exceptions import ModelNotAvailableError
from livraison_express.infrastructure.dev.in_memory_order_store import InMemoryOrderStore
from livraison_express.infrastructure.sqlite.sqlite_order_store import SqliteOrderStore


def _settings(tmp_path: Path, environment: str = "test") -> Settings:
    return Settings(
        environment=environment,
        model_path=str(tmp_path / "model.joblib"),
        model_threshold=0.5,
        model_version="1.0.0",
        order_store_dsn=f"sqlite:///{tmp_path / 'orders.db'}",
        log_level="INFO",
    )


def test_container_starts_without_a_model_file(tmp_path: Path) -> None:
    """ADR-0002: no .joblib is not a crash, it is a 503 later."""
    container = build_container(_settings(tmp_path))

    container.load_model()

    assert container.model_ready is False
    with pytest.raises(ModelNotAvailableError):
        container.predict_eligibility()


def test_collecting_orders_works_without_a_model(
    tmp_path: Path, sample_order: OrderFeatures
) -> None:
    """202 does not need the model: collection stays up while predictions are down."""
    container = build_container(_settings(tmp_path))

    order_id = container.collect_order.execute(sample_order)

    assert container.collect_order.get(order_id).order_id == order_id


def test_train_then_serve_round_trip(tmp_path: Path, sample_order: OrderFeatures) -> None:
    """The artifact written by `train` is the one loaded at startup."""
    settings = _settings(tmp_path)
    build_container(settings).train_model.execute()

    served = build_container(settings)
    served.load_model()
    prediction = served.predict_eligibility().execute(sample_order)

    assert served.model_ready is True
    assert prediction.model_version == "1.0.0"
    assert 0.0 <= prediction.probability <= 1.0


def test_order_store_is_chosen_from_the_environment(tmp_path: Path) -> None:
    """The factory is the only place that knows which OrderStore runs where."""
    assert isinstance(build_container(_settings(tmp_path, "test")).order_store, InMemoryOrderStore)
    assert isinstance(build_container(_settings(tmp_path, "local")).order_store, SqliteOrderStore)
