"""Adaptateur MongoDB de l'abstraction `OrderStore` (ADR-0004).

Une commande = un document. Le champ `_id` porte l'`order_id` : `save` remplace le document
au lieu d'en ajouter un, ce qui rend l'écriture idempotente. Les autres champs sont les
variables du modèle. Les commandes écrites par l'ETL (collection `orders`) sont lues, mais
rien ne garantit qu'elles soient complètes : un document incomplet est signalé par une
erreur du domaine, pas par une erreur de MongoDB.
"""

from __future__ import annotations

from typing import Any

from pymongo import MongoClient

from ...abstractions.order_store import OrderStore
from ...domain.entities import FEATURE_COLUMNS, OrderFeatures
from ...domain.exceptions import InvalidOrderError
from .connection import database_name, unavailable_as_domain_error


def _to_document(order: OrderFeatures) -> dict[str, Any]:
    return {name: getattr(order, name) for name in FEATURE_COLUMNS}


def _to_order(document: dict[str, Any]) -> OrderFeatures:
    missing = [name for name in FEATURE_COLUMNS if name not in document]
    if missing:
        raise InvalidOrderError(
            f"Commande {document.get('_id')} incomplète : champs manquants {', '.join(missing)}"
        )
    values = {name: document[name] for name in FEATURE_COLUMNS}
    return OrderFeatures(order_id=document["_id"], **values)


class MongoOrderStore(OrderStore):
    """Store orders in a MongoDB collection, one document per `order_id`."""

    def __init__(
        self,
        uri: str,
        database: str,
        collection: str = "orders",
        timeout_ms: int = 3000,
    ) -> None:
        # La connexion est paresseuse : MongoClient n'échoue qu'à la première requête.
        self._client: MongoClient = MongoClient(uri, serverSelectionTimeoutMS=timeout_ms)
        self._orders = self._client[database][collection]

    @classmethod
    def from_dsn(
        cls, dsn: str, collection: str = "orders", timeout_ms: int = 3000
    ) -> MongoOrderStore:
        """Build the store from `mongodb://host:port/database` (the database is required)."""
        return cls(dsn, database_name(dsn), collection, timeout_ms)

    def save(self, order: OrderFeatures) -> None:
        """Insert or replace the order: idempotent because `_id` is the order_id."""
        if order.order_id is None:
            raise InvalidOrderError("order_id obligatoire pour enregistrer une commande")
        with unavailable_as_domain_error():
            self._orders.replace_one({"_id": order.order_id}, _to_document(order), upsert=True)

    def get(self, order_id: str) -> OrderFeatures | None:
        """Return the stored order, or None if the identifier is unknown."""
        with unavailable_as_domain_error():
            document = self._orders.find_one({"_id": order_id})
        return None if document is None else _to_order(document)

    def get_all(self) -> list[OrderFeatures]:
        """Return every stored order."""
        with unavailable_as_domain_error():
            return [_to_order(document) for document in self._orders.find()]
