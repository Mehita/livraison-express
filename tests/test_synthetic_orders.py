"""Tests du générateur de commandes : reproductible, fidèle à la cellule 8."""

from __future__ import annotations

from livraison_express.domain.entities import LabeledOrder, OrderFeatures
from livraison_express.infrastructure.dev.synthetic_orders import (
    generate_labeled_orders,
    generate_orders_dataset,
)


def test_same_seed_gives_the_same_orders() -> None:
    """Reproducibility: what makes the other tests non-flaky."""
    assert generate_labeled_orders(50, random_state=7) == generate_labeled_orders(
        50, random_state=7
    )


def test_different_seed_gives_different_orders() -> None:
    assert generate_labeled_orders(50, random_state=1) != generate_labeled_orders(
        50, random_state=2
    )


def test_default_size_is_the_notebook_one() -> None:
    assert len(generate_orders_dataset()) == 6000


def test_orders_are_domain_objects_with_ids() -> None:
    orders = generate_orders_dataset(5)

    assert all(isinstance(order, OrderFeatures) for order in orders)
    assert orders[0].order_id == "CMD-000001"
    assert orders[4].order_id == "CMD-000005"


def test_labeled_orders_carry_the_outcome_apart_from_the_order() -> None:
    labeled = generate_labeled_orders(20)

    assert all(isinstance(item, LabeledOrder) for item in labeled)
    assert all(isinstance(item.express_eligible, bool) for item in labeled)
    assert not hasattr(labeled[0].order, "express_eligible")


def test_both_outcomes_exist() -> None:
    """A training set with a single class could not train anything."""
    outcomes = {item.express_eligible for item in generate_labeled_orders(500)}

    assert outcomes == {True, False}
