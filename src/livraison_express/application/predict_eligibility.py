"""Cas d'usage : prédire l'éligibilité express d'une commande.

Séance 1 — TODO : implémenter.

C'est le cas d'usage qui correspond à l'élément « Exposer une fonction de prédiction »
du tableau des éléments à industrialiser. C'est le cas d'usage le plus simple, et
c'est le meilleur endroit pour comprendre l'architecture : il fait trois choses et
seulement trois.

Exemple d'appel :

```python
use_case = PredictEligibility(predictor=predictor, order_store=store)
result = use_case.execute(OrderFeatures(hour=14, ...))
```
"""

from __future__ import annotations

from ..abstractions.order_store import OrderStore
from ..domain.entities import OrderFeatures, Prediction


class PredictEligibility:
    """Prédit l'éligibilité express d'une commande déjà connue.

    Collaborateurs
    --------------
    predictor : `EligibilityPredictor`, le calcul métier (cellule 34 du notebook).
    order_store : l'historique des prédictions. TODO (session 1) : decide whether the
    prediction must be persisted here (see the `Prediction` store of session 5) or
    whether that is another use case's responsibility. Both answers are defensible:
    argue yours in the ADR.

    Le calcul métier vit dans `domain/predictor.py`. Ce cas d'use n'a pas à le
    réécrire : il l'appelle, et il gère ce qui l'entoure (persistance, journalisation,
    erreurs). C'est la séparation du « qui décide » et du « qui calcule ».

    TODO (session 1): declare the fields and store the collaborators as private
    attributes. Follow the naming used in `docs/etudiant/src/livraison_express/`.
    """

    def __init__(self, predictor: object, order_store: OrderStore) -> None:
        # TODO (session 1): store the collaborators.
        raise NotImplementedError

    def execute(self, order: OrderFeatures) -> Prediction:
        """Return the eligibility prediction for one order.

        TODO (session 1): implement the orchestration:

        1. call the predictor (do NOT duplicate the model logic here);
        2. decide what to persist (prediction history?) and where;
        3. let the domain exceptions bubble up: `api/errors.py` translates them
           into HTTP status codes.

        What does this method NOT do? It does not know that HTTP exists, it does not
        know what a DataFrame is, it does not know that joblib is involved.
        If you need any of those, a collaborator is missing: name it, add it to the
        abstraction layer.
        """
        raise NotImplementedError