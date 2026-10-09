"""Le prédicteur : le cœur métier de l'application.

Séance 1 — TODO : implémenter.

C'est la fonction `predict_order_eligibility` de la **cellule 34 du notebook**, à déplacer
telle quelle. Tout le TP du jour consiste à la rendre testable et à la brancher sur l'API.

Trois points de conception à traiter, ils sont la valeur pédagogique de cette séance :

1. **Le type d'entrée.** La cellule 34 attend un `dict` brut. Ici elle attend un
   `OrderFeatures` et renvoie un `Prediction`. Qui fait la conversion ?
   C'est à vous de décider où s'arrête la conversion `dict` → `OrderFeatures`
   (proposition : dans la couche API, `api/routers/predictions.py`).

2. **La dépendance au modèle.** La cellule 34 reçoit l'objet `model` en paramètre.
   Une classe, elle, reçoit ce modèle **au constructeur**. C'est ce qui la rend
   testable : un test lui passe un faux modèle, sans joblib ni MLflow.

3. **L'erreur sur variable manquante.** La cellule 34 lève `ValueError` avec la liste
   des variables manquantes. Une `ValueError` n'est pas une erreur métier : quelle
   erreur de `domain/exceptions.py` faut-il lever, et pourquoi (c'est la question qui
   distingue une 422 d'une 500) ?
"""

from __future__ import annotations

from .entities import OrderFeatures, Prediction


class EligibilityPredictor:
    """Prédit l'éligibilité d'une commande à la livraison express.

    Collaborateurs
    --------------
    model : l'artefact de modèle chargé (pipeline scikit-learn). Ce n'est pas un type
        du domaine, d'où son annotation en `object` : le domaine ignore scikit-learn.
        À affiner si vous introduisez un type d'artefact dans `domain/entities.py`.
    threshold : probabilité au-dessus de laquelle la commande est éligible
        (cellule 31 : le 0.5 par défaut est discutable, le choix se fait avec le métier).

    TODO (session 1): declare the fields of `__init__` and store the model and the
    threshold as private attributes (`_model`, `_threshold`).
    """

    def __init__(self, model: object, threshold: float) -> None:
        # TODO (session 1): store the model and the threshold.
        raise NotImplementedError

    def predict(self, order: OrderFeatures) -> Prediction:
        """Return the eligibility prediction for one order.

        TODO (session 1): move the body of notebook cell 34 here
        (`predict_order_eligibility`), with these adaptations:

        - build the scikit-learn input DataFrame with the FEATURE_COLUMNS of cell 20,
          from the dataclass fields instead of a dict;
        - raise a domain exception (`InvalidOrderError`) instead of `ValueError`;
        - return a `Prediction` dataclass instead of a dict;
        - keep the four outputs of the notebook: express_eligible, decision,
          probability, model_version (plus predicted_at).
        """
        raise NotImplementedError