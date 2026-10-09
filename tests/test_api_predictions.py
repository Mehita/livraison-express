"""Tests de l'API HTTP : toute la pile (routeur -> cas d'usage -> domaine), sans modèle réel.

Ils vérifient le contrat `docs/api/openapi.yml` et les codes d'erreur : une erreur métier
ne doit jamais produire un 500.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from fastapi.testclient import TestClient

from livraison_express.api.app import create_app
from livraison_express.bootstrap import Container

CONTRACT = Path(__file__).resolve().parent.parent / "docs" / "api" / "openapi.yml"

VALID_ORDER = {
    "hour": 14,
    "day_of_week": 2,
    "weekend": 0,
    "distance_km": 3.5,
    "order_value_eur": 89.9,
    "weight_kg": 2.4,
    "stock_available": 1,
    "preparation_time_min": 18,
    "carrier_capacity": 0.85,
    "weather": "normal",
    "delivery_zone": "centre",
    "customer_type": "premium",
}


def test_predict_returns_200_and_a_valid_body(api_client: TestClient) -> None:
    """POST /v1/predictions answers 200 with a contract-compliant body."""
    response = api_client.post("/v1/predictions", json=VALID_ORDER)

    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "oui"  # fake model: probability 0.6 >= threshold 0.5
    assert body["express_eligible"] is True
    assert 0.0 <= body["probability"] <= 1.0
    assert body["model_version"] == "1.0.0"
    assert body["order_id"].startswith("CMD-")


def test_predict_returns_422_on_invalid_order(api_client: TestClient) -> None:
    """POST /v1/predictions answers 422, in the contract's error format."""
    order = {key: value for key, value in VALID_ORDER.items() if key != "distance_km"}

    response = api_client.post("/v1/predictions", json=order)

    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "validation_error"
    assert any("distance_km" in detail for detail in body["details"])


def test_predict_rejects_unknown_and_missing_categorical_fields(api_client: TestClient) -> None:
    """The contract says: any missing or extra variable is a 422."""
    extra = {**VALID_ORDER, "colour": "red"}
    no_weather = {key: value for key, value in VALID_ORDER.items() if key != "weather"}

    assert api_client.post("/v1/predictions", json=extra).status_code == 422
    assert api_client.post("/v1/predictions", json=no_weather).status_code == 422


def test_predict_returns_503_when_the_model_is_missing(container: Container) -> None:
    """POST /v1/predictions answers 503 and the error body when no model is loaded."""
    container.predictor = None
    client = TestClient(create_app(container))

    response = client.post("/v1/predictions", json=VALID_ORDER)

    assert response.status_code == 503
    assert response.json()["error"] == "model_unavailable"


def test_health_returns_200(container: Container) -> None:
    """GET /health answers 200 even when the model is missing."""
    container.predictor = None
    client = TestClient(create_app(container))

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_readiness_is_200_with_a_model_and_503_without(container: Container) -> None:
    """GET /health/ready tells the orchestrator whether to send traffic."""
    ready = TestClient(create_app(container)).get("/health/ready")
    container.predictor = None
    not_ready = TestClient(create_app(container)).get("/health/ready")

    assert ready.status_code == 200
    assert ready.json()["status"] == "ready"
    assert not_ready.status_code == 503
    assert not_ready.json()["status"] == "not_ready"
    assert not_ready.json()["checks"]["model"] == "missing"


def test_collect_order_returns_202(api_client: TestClient) -> None:
    """POST /v1/orders answers 202 and the order is readable afterwards."""
    response = api_client.post("/v1/orders", json=VALID_ORDER)

    assert response.status_code == 202
    body = response.json()
    assert body["status"] == "accepted"
    read_back = api_client.get(f"/v1/orders/{body['order_id']}")
    assert read_back.status_code == 200
    assert read_back.json()["distance_km"] == VALID_ORDER["distance_km"]


def test_collect_order_works_without_a_model(container: Container) -> None:
    """Collection does not depend on the model: it stays up while predictions answer 503."""
    container.predictor = None
    client = TestClient(create_app(container))

    assert client.post("/v1/orders", json=VALID_ORDER).status_code == 202


def test_unknown_order_returns_404(api_client: TestClient) -> None:
    """GET /v1/orders/{id} answers 404 with the contract's error format."""
    response = api_client.get("/v1/orders/CMD-INCONNU")

    assert response.status_code == 404
    assert response.json()["error"] == "order_not_found"


def test_response_matches_the_openapi_contract(api_client: TestClient) -> None:
    """The response body matches the Prediction schema of docs/api/openapi.yml."""
    contract = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    schema = contract["components"]["schemas"]["Prediction"]

    body = api_client.post("/v1/predictions", json=VALID_ORDER).json()

    assert set(schema["required"]) <= set(body)
    assert set(body) <= set(schema["properties"])
    assert body["decision"] in schema["properties"]["decision"]["enum"]


def test_paths_of_the_app_are_declared_in_the_contract(api_client: TestClient) -> None:
    """Every route exposed by FastAPI exists in the contract (no invented endpoint)."""
    contract_paths = set(yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))["paths"])

    app_paths = set(api_client.get("/openapi.json").json()["paths"])

    assert app_paths <= contract_paths
