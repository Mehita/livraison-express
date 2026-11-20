"""Une base de données injoignable doit donner un 503 propre, jamais une erreur 500."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from livraison_express.api.errors import register_exception_handlers
from livraison_express.domain.exceptions import OrderStoreUnavailableError


def test_unavailable_order_store_is_a_503_in_the_contract_format() -> None:
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/boom")
    def boom() -> None:
        raise OrderStoreUnavailableError("MongoDB ne répond pas : mot de passe=secret")

    response = TestClient(app).get("/boom")

    assert response.status_code == 503
    assert response.json()["error"] == "order_store_unavailable"
    assert "secret" not in response.text
