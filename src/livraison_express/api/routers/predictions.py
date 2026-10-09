"""Routeur : prédictions.

`POST /v1/predictions` est la cellule 34 du notebook exposée en HTTP. Le routeur convertit
et délègue : la logique de décision est dans le domaine, pas ici.

Le modèle absent n'est pas géré par un `if` : le fournisseur de dépendance lève
`ModelNotAvailableError`, que `errors.py` traduit en 503.

`/batch` et `/{order_id}` arrivent en séance 5 : on ne les écrit pas maintenant (YAGNI).
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from ...application.predict_eligibility import PredictEligibility
from ..dependencies import get_predict_eligibility_use_case
from ..mappers import to_order, to_prediction_schema
from ..schemas import OrderFeaturesSchema
from ..schemas import Prediction as PredictionSchema

router = APIRouter(prefix="/v1/predictions", tags=["predictions"])


@router.post("", response_model=PredictionSchema, response_model_exclude_none=True)
def create_prediction(
    order: OrderFeaturesSchema,
    use_case: PredictEligibility = Depends(get_predict_eligibility_use_case),
) -> PredictionSchema:
    """Predict the express eligibility of one order (synchronous)."""
    return to_prediction_schema(use_case.execute(to_order(order)))
