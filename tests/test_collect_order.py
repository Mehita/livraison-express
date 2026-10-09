"""Tests du cas d'usage de collecte : on teste l'orchestration, pas le stockage."""

from __future__ import annotations

from dataclasses import replace

import pytest

from livraison_express.application.collect_order import CollectOrder
from livraison_express.domain.entities import OrderFeatures
from livraison_express.domain.exceptions import OrderNotFoundError
from livraison_express.infrastructure.dev.in_memory_order_store import InMemoryOrderStore


def test_execute_stores_the_order_and_returns_its_id(
    sample_order: OrderFeatures, order_store: InMemoryOrderStore
) -> None:
    """The returned identifier is the key under which the order can be read back."""
    order_id = CollectOrder(order_store).execute(sample_order)

    assert order_id.startswith("CMD-")
    assert order_store.get(order_id) is not None


def test_execute_keeps_the_given_order_id(
    sample_order: OrderFeatures, order_store: InMemoryOrderStore
) -> None:
    """An order that already has an identifier keeps it."""
    order = replace(sample_order, order_id="CMD-000042")

    assert CollectOrder(order_store).execute(order) == "CMD-000042"


def test_same_order_id_twice_is_idempotent(
    sample_order: OrderFeatures, order_store: InMemoryOrderStore
) -> None:
    """A retry returns the same identifier and creates no duplicate."""
    use_case = CollectOrder(order_store)
    order = replace(sample_order, order_id="CMD-000042")

    first = use_case.execute(order)
    second = use_case.execute(order)

    assert first == second
    assert order_store.count() == 1


def test_get_returns_the_stored_order(
    sample_order: OrderFeatures, order_store: InMemoryOrderStore
) -> None:
    """Reading back gives the order that was collected."""
    use_case = CollectOrder(order_store)
    order_id = use_case.execute(sample_order)

    assert use_case.get(order_id).order_id == order_id


def test_get_unknown_order_raises_not_found(order_store: InMemoryOrderStore) -> None:
    """An unknown identifier is a domain error, not None."""
    with pytest.raises(OrderNotFoundError):
        CollectOrder(order_store).get("CMD-INCONNU")
