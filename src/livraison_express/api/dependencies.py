"""Injection des dépendances : comment un routeur obtient ses cas d'usage.

Le conteneur assemblé par `bootstrap.py` est posé sur `app.state` par `create_app`. Ce
module ne fait que le lire : un routeur n'écrit jamais `OrderStore()` ni `Predictor(...)`.

Point de substitution unique pour les tests : `create_app(container)`. Un test construit
son propre conteneur (faux modèle, store en mémoire) et le passe à `create_app`, sans
toucher au câblage.

`get_predict_eligibility_use_case` laisse remonter `ModelNotAvailableError` quand aucun
modèle n'est chargé : c'est `api/errors.py` qui la traduit en 503, pas un `if` dans le
routeur.
"""

from __future__ import annotations

from fastapi import Request

from ..application.collect_order import CollectOrder
from ..application.predict_eligibility import PredictEligibility


def get_collect_order_use_case(request: Request) -> CollectOrder:
    """Provide the order collection use case."""
    return request.app.state.container.collect_order


def get_predict_eligibility_use_case(request: Request) -> PredictEligibility:
    """Provide the prediction use case (raises ModelNotAvailableError without a model)."""
    return request.app.state.container.predict_eligibility()
