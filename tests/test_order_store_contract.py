"""Tests de contrat des implémentations de `OrderStore`.

La classe `OrderStoreContractTests` est écrite une fois, contre l'ABC. Pytest ne la
collecte pas (son nom ne commence pas par `Test`) : elle ne tourne qu'à travers les
sous-classes, une par implémentation. Ajouter un adaptateur = deux lignes.
"""

from __future__ import annotations

import tempfile
from dataclasses import replace
from pathlib import Path

from livraison_express.abstractions.order_store import OrderStore
from livraison_express.domain.entities import OrderFeatures
from livraison_express.infrastructure.dev.in_memory_order_store import InMemoryOrderStore
from livraison_express.infrastructure.sqlite.sqlite_order_store import SqliteOrderStore


def _order(order_id: str) -> OrderFeatures:
    return OrderFeatures(
        hour=14,
        day_of_week=2,
        weekend=0,
        distance_km=3.5,
        order_value_eur=89.9,
        weight_kg=2.4,
        stock_available=1,
        preparation_time_min=12,
        carrier_capacity=0.85,
        weather="normal",
        delivery_zone="centre",
        customer_type="premium",
        order_id=order_id,
    )


class OrderStoreContractTests:
    """Contract every OrderStore implementation must satisfy."""

    def make_store(self) -> OrderStore:
        raise NotImplementedError

    def test_save_then_get_returns_the_same_order(self) -> None:
        store = self.make_store()
        order = _order("CMD-000001")

        store.save(order)

        assert store.get("CMD-000001") == order

    def test_get_unknown_returns_none(self) -> None:
        assert self.make_store().get("CMD-INCONNU") is None

    def test_save_is_idempotent(self) -> None:
        store = self.make_store()
        order = _order("CMD-000001")

        store.save(order)
        store.save(order)

        assert store.get("CMD-000001") == order

    def test_save_same_id_keeps_the_latest_version(self) -> None:
        store = self.make_store()
        store.save(_order("CMD-000001"))
        updated = replace(_order("CMD-000001"), distance_km=9.0)

        store.save(updated)

        assert store.get("CMD-000001") == updated


class TestInMemoryOrderStore(OrderStoreContractTests):
    def make_store(self) -> OrderStore:
        return InMemoryOrderStore()


class TestSqliteOrderStore(OrderStoreContractTests):
    def make_store(self) -> OrderStore:
        directory = Path(tempfile.mkdtemp())
        return SqliteOrderStore(str(directory / "orders.db"))

    def test_data_survives_a_new_instance(self) -> None:
        """What ADR-0001 buys over memory: a restart does not lose the orders."""
        path = str(Path(tempfile.mkdtemp()) / "orders.db")
        SqliteOrderStore(path).save(_order("CMD-000001"))

        assert SqliteOrderStore(path).get("CMD-000001") == _order("CMD-000001")
