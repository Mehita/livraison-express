"""Cas d'usage : prédire l'éligibilité express d'une commande."""

from __future__ import annotations

from ..domain.entities import OrderFeatures, Prediction, assign_order_id
from ..domain.predictor import EligibilityPredictor


class PredictEligibility:
    """Prédit l'éligibilité express d'une commande.

    Orchestre et ne calcule pas : le calcul vit dans `EligibilityPredictor`. Ce cas
    d'usage garantit seulement que la commande a un identifiant, puis délègue.
    """

    def __init__(self, predictor: EligibilityPredictor) -> None:
        self._predictor = predictor

    def execute(self, order: OrderFeatures) -> Prediction:
        """Return the eligibility prediction for one order."""
        return self._predictor.predict(assign_order_id(order))
