"""Cas d'usage : collecter une commande à prédire et la relire.

`POST /v1/orders` répond 202 : la commande est acceptée et rangée, la prédiction
viendra plus tard. Ce cas d'usage ne prédit donc rien : il n'a pas besoin du modèle,
ce qui lui permet de fonctionner même quand `/health/ready` répond 503.
"""

from __future__ import annotations

from ..abstractions.order_store import OrderStore
from ..domain.entities import OrderFeatures, assign_order_id
from ..domain.exceptions import OrderNotFoundError


class CollectOrder:
    """Enregistre une commande et permet de la relire.

    Collaborateur : `order_store`, la persistance (injectée, jamais construite ici).
    """

    def __init__(self, order_store: OrderStore) -> None:
        self._order_store = order_store

    def execute(self, order: OrderFeatures) -> str:
        """Persist one order and return its identifier.

        Re-submitting the same `order_id` is not an error: `save` is idempotent, so the
        caller gets the same identifier again (a client that retries after a timeout
        must not be punished by a 409).
        """
        order = assign_order_id(order)
        self._order_store.save(order)
        return order.order_id

    def get(self, order_id: str) -> OrderFeatures:
        """Return a stored order, or raise OrderNotFoundError (mapped to 404)."""
        order = self._order_store.get(order_id)
        if order is None:
            raise OrderNotFoundError(f"Commande inconnue : {order_id}")
        return order
