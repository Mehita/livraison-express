"""Adaptateur SQLite de l'abstraction `OrderStore` (ADR-0001).

Un fichier SQLite, créé au premier usage. Choix provisoire : un seul écrivain à la fois,
donc une seule instance de l'API. Au-delà, on remplace cet adaptateur (voir ADR-0001).
"""

from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path

from ...abstractions.order_store import OrderStore
from ...domain.entities import FEATURE_COLUMNS, OrderFeatures
from ...domain.exceptions import InvalidOrderError

_PREFIX = "sqlite:///"
_COLUMNS = ("order_id", *FEATURE_COLUMNS)


def _path_from_dsn(dsn: str) -> str:
    """Accept `sqlite:///./orders.db` or a plain path."""
    return dsn.removeprefix(_PREFIX)


class SqliteOrderStore(OrderStore):
    """Store orders in a SQLite file, one row per `order_id`."""

    def __init__(self, dsn: str) -> None:
        self._path = _path_from_dsn(dsn)
        Path(self._path).parent.mkdir(parents=True, exist_ok=True)
        # Colonnes sans type déclaré : SQLite garde le type Python (int reste int).
        columns = ", ".join(
            f"{name} TEXT PRIMARY KEY" if name == "order_id" else name for name in _COLUMNS
        )
        with closing(self._connect()) as conn, conn:
            conn.execute(f"CREATE TABLE IF NOT EXISTS orders ({columns})")

    def _connect(self) -> sqlite3.Connection:
        # Une connexion par opération : FastAPI exécute les routes dans plusieurs threads.
        return sqlite3.connect(self._path)

    def save(self, order: OrderFeatures) -> None:
        """Insert or replace the order: idempotent thanks to the PRIMARY KEY."""
        if order.order_id is None:
            raise InvalidOrderError("order_id obligatoire pour enregistrer une commande")
        placeholders = ", ".join("?" for _ in _COLUMNS)
        values = [getattr(order, name) for name in _COLUMNS]
        with closing(self._connect()) as conn, conn:
            conn.execute(
                f"INSERT OR REPLACE INTO orders ({', '.join(_COLUMNS)}) VALUES ({placeholders})",
                values,
            )

    def get(self, order_id: str) -> OrderFeatures | None:
        """Return the stored order, or None if the identifier is unknown."""
        with closing(self._connect()) as conn:
            row = conn.execute(
                f"SELECT {', '.join(_COLUMNS)} FROM orders WHERE order_id = ?", (order_id,)
            ).fetchone()
        if row is None:
            return None
        return OrderFeatures(**dict(zip(_COLUMNS, row, strict=True)))
