"""Le prédicteur : le cœur métier de l'application (cellule 34 du notebook)."""

from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd

from .entities import FEATURE_COLUMNS, OrderFeatures, Prediction
from .exceptions import InvalidOrderError


class EligibilityPredictor:
    """Prédit l'éligibilité d'une commande à la livraison express.

    Le modèle, le seuil et la version sont injectés au constructeur : un test peut donc
    fournir un faux modèle, sans joblib ni scikit-learn.
    """

    def __init__(self, model: object, threshold: float, model_version: str) -> None:
        self._model = model
        self._threshold = threshold
        self._model_version = model_version

    def predict(self, order: OrderFeatures) -> Prediction:
        """Return the eligibility prediction for one order."""
        values = {name: getattr(order, name, None) for name in FEATURE_COLUMNS}
        missing = sorted(name for name, value in values.items() if value is None)
        if missing:
            raise InvalidOrderError(f"Variables manquantes : {missing}")

        input_df = pd.DataFrame([values])
        probability = float(self._model.predict_proba(input_df)[0, 1])
        eligible = probability >= self._threshold

        return Prediction(
            order_id=order.order_id,
            express_eligible=bool(eligible),
            decision="oui" if eligible else "non",
            probability=round(probability, 4),
            model_version=self._model_version,
            predicted_at=datetime.now(timezone.utc),
        )
