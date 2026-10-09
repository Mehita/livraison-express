"""Schémas Pydantic : la traduction du contrat OpenAPI en types Python.

Ce fichier est **fourni**. Il correspond, champ par champ, à `docs/api/openapi.yml` :
c'est le contrat de l'API, écrit une seule fois.

Si vous modifiez ce fichier, vous modifiez le contrat : mettez les deux à jour et
justifiez-le dans un ADR. La comparaison entre le YAML et le `/openapi.json` généré par
FastAPI fait partie de la définition de terminé de chaque séance.

Deux erreurs à éviter, elles sont la raison d'être de ce fichier :

1. dupliquer les règles de validation entre le domaine et l'API (le domaine ne connaît
   pas Pydantic, l'API ne connaît pas la logique métier) ;
2. exposer un type du domaine tel quel dans une réponse HTTP : le format de sortie est
   un contrat public, il évolue indépendamment du modèle interne.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Weather(str, Enum):
    WEATHER_NORMAL = "normal"
    WEATHER_RAIN = "pluie"
    WEATHER_SNOW = "neige"
    WEATHER_STORM = "orage"


class DeliveryZone(str, Enum):
    ZONE_CENTRE = "centre"
    ZONE_NEAR_SUBURB = "proche_banlieue"
    ZONE_SUBURB = "banlieue"
    ZONE_RURAL = "rurale"


class CustomerType(str, Enum):
    TYPE_STANDARD = "standard"
    TYPE_PREMIUM = "premium"


class OrderFeaturesSchema(BaseModel):
    """Request body of POST /v1/orders and POST /v1/predictions.

    Mirrors the `OrderFeatures` component of docs/api/openapi.yml.
    """

    model_config = ConfigDict(extra="forbid")

    order_id: str | None = Field(default=None, examples=["CMD-000001"])
    hour: int = Field(ge=0, le=23, examples=[14])
    day_of_week: int = Field(ge=0, le=6, examples=[2])
    weekend: int = Field(ge=0, le=1, examples=[0])
    distance_km: float = Field(ge=0, examples=[3.5])
    order_value_eur: float = Field(ge=0, examples=[89.9])
    weight_kg: float = Field(ge=0, examples=[2.4])
    stock_available: int = Field(ge=0, le=1, examples=[1])
    preparation_time_min: float = Field(ge=0, examples=[18])
    carrier_capacity: float = Field(ge=0, le=1, examples=[0.85])
    weather: Weather = Weather.WEATHER_NORMAL
    delivery_zone: DeliveryZone = DeliveryZone.ZONE_CENTRE
    customer_type: CustomerType = CustomerType.TYPE_PREMIUM


class OrderAccepted(BaseModel):
    """Response body of POST /v1/orders (202)."""

    order_id: str
    status: str = "accepted"


class Prediction(BaseModel):
    """Response body of POST /v1/predictions.

    Mirrors the `Prediction` component of docs/api/openapi.yml.
    """

    order_id: str
    express_eligible: bool
    decision: str = Field(pattern="^(oui|non)$")
    probability: float = Field(ge=0, le=1)
    model_version: str
    predicted_at: datetime
    latency_ms: float | None = None


class BatchPredictionRequest(BaseModel):
    """Request body of POST /v1/predictions/batch."""

    orders: list[OrderFeaturesSchema] = Field(min_length=1, max_length=1000)


class BatchPredictionResponse(BaseModel):
    """Response body of POST /v1/predictions/batch."""

    predictions: list[Prediction]
    count: int


class ModelCardSchema(BaseModel):
    """Response body of GET /v1/model.

    Mirrors the `ModelCard` component of docs/api/openapi.yml.
    """

    project: str
    model_version: str
    model_type: str
    task: str
    target: str
    threshold: float
    trained_at: datetime | None = None
    features: list[str]
    metrics: dict[str, float] = Field(default_factory=dict)
    limitations: list[str] = Field(default_factory=list)


class HealthStatus(BaseModel):
    """Response body of GET /health."""

    status: str = "ok"
    service: str
    version: str


class ReadinessStatus(BaseModel):
    """Response body of GET /health/ready."""

    status: str
    checks: dict[str, str] = Field(default_factory=dict)
    version: str | None = None


class ErrorResponse(BaseModel):
    """Error body, returned by every endpoint of the API."""

    error: str
    message: str
    details: list[str] = Field(default_factory=list)