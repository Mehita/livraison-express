"""Tests de l'API HTTP.

Séance 1 — TODO : implémenter.

Ce sont des tests d'intégration légers : ils traversent toute la pile (routeur →
cas d'usage → domaine) mais avec des doublures pour les dépendances externes. Ils ne
doivent jamais exiger une base de données ni un modèle entraîné.

Ce qu'ils vérifient, au-delà du simple « ça renvoie 200 » :

- le **contrat** : le corps de la réponse correspond à `docs/api/openapi.yml` ;
- les **codes d'erreur** : 422 pour une commande invalide, 404 pour une commande
  inconnue, 503 quand le modèle est absent. Une API qui renvoie 500 sur une erreur
  métier est une API cassée ;
- l'**isolation** : un test ne doit pas polluer le suivant (utilisez les fixtures).

TODO (séance 1)
--------------
1. test_predict_returns_200_and_a_valid_body — valeurs de la cellule 36.
2. test_predict_returns_422_on_invalid_order — retirez `distance_km`.
3. test_predict_returns_503_when_the_model_is_missing — remplacez le modèle par None
   via `app.dependency_overrides` et vérifiez le code ET le corps d'erreur.
4. test_health_returns_200 — et, si vous avez implémenté `/health/ready`,
   `test_readiness_returns_503_when_the_model_is_missing`.
5. test_collect_order_returns_202 — vérifiez aussi que l'ordre est relisible.
6. test_response_matches_the_openapi_contract — comparez les clés du JSON retourné
   avec le schéma `Prediction` de `docs/api/openapi.yml`. C'est le test qui valide
   votre interprétation du contrat, et il vous évitera des surprises le jour de la
soutenance.

TODO (session 3): ajouter un test sur GET /v1/model.
TODO (session 7): ajouter un test sur la présence des métriques exposées.
"""

from __future__ import annotations

# TODO (session 1): implement these tests.
#
# Expected shape:
#
#   from fastapi.testclient import TestClient
#
#   def test_predict_returns_200_and_a_valid_body(api_client: TestClient) -> None:
#       response = api_client.post("/v1/predictions", json=VALID_ORDER)
#       assert response.status_code == 200
#       body = response.json()
#       assert body["decision"] in {"oui", "non"}
#       assert 0.0 <= body["probability"] <= 1.0


def test_predict_returns_200_and_a_valid_body() -> None:
    """POST /v1/predictions answers 200 with a contract-compliant body."""
    raise NotImplementedError


def test_predict_returns_422_on_invalid_order() -> None:
    """POST /v1/predictions answers 422 when a feature is missing."""
    raise NotImplementedError


def test_predict_returns_503_when_the_model_is_missing() -> None:
    """POST /v1/predictions answers 503 when no model is loaded."""
    raise NotImplementedError


def test_health_returns_200() -> None:
    """GET /health answers 200 even when the dependencies are down."""
    raise NotImplementedError


def test_collect_order_returns_202() -> None:
    """POST /v1/orders answers 202 and the order is readable afterwards."""
    raise NotImplementedError


def test_response_matches_the_openapi_contract() -> None:
    """The response body matches the Prediction schema of docs/api/openapi.yml."""
    raise NotImplementedError