"""Conversions entre les schémas HTTP (Pydantic) et les types du domaine.

Deux contrats qui évoluent séparément : le format HTTP est public, le type du domaine est
interne. Les convertir à un seul endroit évite de dupliquer le mapping dans chaque routeur.
"""

from __future__ import annotations

from dataclasses import asdict

from ..domain.entities import OrderFeatures
from ..domain.entities import Prediction as DomainPrediction
from .schemas import OrderFeaturesSchema
from .schemas import Prediction as PredictionSchema


def to_order(schema: OrderFeaturesSchema) -> OrderFeatures:
    """HTTP request body -> domain order (enums become plain strings)."""
    return OrderFeatures(**schema.model_dump(mode="json"))


def to_order_schema(order: OrderFeatures) -> OrderFeaturesSchema:
    """Domain order -> HTTP response body."""
    return OrderFeaturesSchema(**asdict(order))


def to_prediction_schema(prediction: DomainPrediction) -> PredictionSchema:
    """Domain prediction -> HTTP response body."""
    return PredictionSchema(**asdict(prediction))
