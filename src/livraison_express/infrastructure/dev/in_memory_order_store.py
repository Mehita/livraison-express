"""`OrderStore` de développement : un dictionnaire en mémoire.

Implémentation de référence de l'abstraction `OrderStore`.

Ce fichier est **fourni** et sert trois usages :

1. faire tourner l'application et les tests sans installer de base de données ;
2. montrer à quoi ressemble une implémentation : les dépendances injectées au
   constructeur, les erreurs du domaine, rien de spécifique à une technologie ;
3. servir de point de comparaison quand vous écrirez la vôtre.

Limites, à connaître (elles sont la raison d'être de la Séance 1) : les données sont
perdues au redémarrage, rien n'est partagé entre deux processus, et la recherche est
linéaire. C'est très bien pour un test unitaire, inacceptable en production.
"""

from __future__ import annotations

from ...abstractions.order_store import OrderStore
from ...domain.entities import OrderFeatures


class InMemoryOrderStore(OrderStore):
    """Store orders in a process-local dictionary.

    Notebook reference: none. This adapter exists only to run the application locally.
    """

    def __init__(self) -> None:
        """Build an empty store."""
        self._orders: dict[str, OrderFeatures] = {}

    def save(self, order: OrderFeatures) -> None:
        """Store one order, idempotently on order_id.

        Assigning to `self._orders[order_id]` is what makes `save` idempotent: saving
        the same order twice leaves a single entry. A real database needs an explicit
        constraint (PRIMARY KEY / ON CONFLICT) to obtain the same guarantee.
        """
        self._orders[order.order_id] = order

    def get(self, order_id: str) -> OrderFeatures | None:
        """Return the stored order, or None if it does not exist."""
        return self._orders.get(order_id)

    def count(self) -> int:
        """Return the number of stored orders (used by the health check)."""
        return len(self._orders)

    def clear(self) -> None:
        """Drop every stored order (used between two tests)."""
        self._orders.clear()