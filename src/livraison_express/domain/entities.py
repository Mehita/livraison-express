"""Types du domaine.

Ce module ne contient aucune dépendance technique : ni scikit-learn, ni pandas, ni
FastAPI. Les types y sont définis par leur *forme* (`OrderFeatures`), ce qui permet de
changer de base de données ou de format d'événement sans toucher à la logique métier
(règle de dépendance inversée).

Le contrat exact de `OrderFeatures` est défini par `docs/api/openapi.yml` :
il reprend exactement les `FEATURE_COLUMNS` de la cellule 20 du notebook.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from uuid import uuid4

# Variables du modèle (cellule 20 du notebook). Déclarées ICI, une seule fois :
# l'API, le modèle et les tests les importent (DRY).
TARGET_COLUMN = "express_eligible"

NUMERIC_FEATURES = [
    "hour",
    "day_of_week",
    "weekend",
    "distance_km",
    "order_value_eur",
    "weight_kg",
    "stock_available",
    "preparation_time_min",
    "carrier_capacity",
]

CATEGORICAL_FEATURES = [
    "weather",
    "delivery_zone",
    "customer_type",
]

FEATURE_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES


@dataclass(frozen=True)
class OrderFeatures:
    """Caractéristiques d'une commande, telles que requises par le modèle.

    Correspond au schéma `OrderFeatures` de `docs/api/openapi.yml`. `order_id` est
    facultatif : le serveur le génère s'il est absent. Les variables catégorielles sont
    des `str` : le domaine ne connaît pas la liste fermée des valeurs, c'est la couche
    API qui fait respecter le contrat.
    """

    hour: int
    day_of_week: int
    weekend: int
    distance_km: float
    order_value_eur: float
    weight_kg: float
    stock_available: int
    preparation_time_min: float
    carrier_capacity: float
    weather: str
    delivery_zone: str
    customer_type: str
    order_id: str | None = None


@dataclass(frozen=True)
class Prediction:
    """Résultat d'une prédiction : la sortie de la cellule 34 du notebook.

    `latency_ms` du contrat est ajouté à la séance 7 (YAGNI).
    """

    order_id: str | None
    express_eligible: bool
    decision: str
    probability: float
    model_version: str
    predicted_at: datetime


@dataclass(frozen=True)
class OrderEvent:
    """Message du flux temps réel (séance 6).

    TODO (session 6): declare the fields of the `OrderEvent` schema.
    """

    ...


@dataclass(frozen=True)
class ModelCard:
    """Métadonnées et métriques du modèle en service (cellule 55 du notebook).

    TODO (session 3): declare the fields of the `ModelCard` schema.
    """

    ...


def assign_order_id(order: OrderFeatures) -> OrderFeatures:
    """Return the order with an identifier: the one it has, or a generated one."""
    if order.order_id is not None:
        return order
    return replace(order, order_id=f"CMD-{uuid4().hex[:8].upper()}")
