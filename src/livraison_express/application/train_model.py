"""Cas d'usage : entraîner le modèle d'éligibilité.

Séance 1 — TODO : implémenter.

C'est le cas d'usage « Entraînement du modèle » du tableau des éléments à industrialiser.
Il est **hors du chemin de la requête HTTP** : l'entraînement se produit dans un job
(`python -m livraison_express train`, ou plus tard une CI), jamais quand un client
appelle l'API. Un service qui réentraîne à la demande est un service qui tombe.

La quasi-totalité de ce cas d_usage existe déjà dans le notebook, il s'agit de le
déplacer en trois morceaux séparés par des frontières :

| Étape | Cellules | Devient |
|---|---|---|
| 1. construire la pipeline | 20, 22, 24 | `build_model()` : une fonction pure, aucun effet de bord |
| 2. entraîner et évaluer | 26, 28, 29, 30 | `TrainEligibilityModel.execute()` |
| 3. persister | 41 | l'implémentation du `ModelRepository` |

C'est exactement le découpage demandé par les principes du cours : une responsabilité
par classe/méthode, et aucune dépendance inutile (l'évaluation n'écrit pas dans le
registre de modèle, la construction de pipeline ne lit pas de données).

TODO (session 1)
---------------
1. `build_model(random_state)`: move notebook cells 20, 22 and 24 here.
   It must be a **pure function**: same inputs, same pipeline, no I/O, no global state.
   Test it directly — this is the easiest thing to test in the whole project.
2. `TrainEligibilityModel.execute()`: move cells 22, 26, 28-30 here.
   Use the `ModelRepository` abstraction to save the model and its model card (cell 55).
   - Where do the metrics go? Into the `ModelCard` (which becomes `GET /v1/model`)?
   - Notebook cell 26 logs to MLflow: that is another collaborator, delivered in
     session 4 (`ExperimentTracker`). For now, either return the metrics, or print
     them, but do not import MLflow directly here — that would couple this use case
     to a specific tracking tool.
3. What is the input of this use case: a `DataFrame`? A path to a dataset?
   Decide, and note that the answer changes what you can test.
"""

from __future__ import annotations

from ..abstractions.model_repository import ModelRepository


class TrainEligibilityModel:
    """Entraîne le modèle de prédiction et le rend disponible au service.

    Collaborateurs
    --------------
    model_repository : destination des artefacts (cellule 41).
    dataset : source des données d'entraînement. TODO (session 1): the notebook
    generates them synthetically (cell 8, `generate_orders_dataset`). In production
    this is an existing dataset: where does it come from? Make it a collaborator
    (a new abstraction) rather than an import, or your use case will not be testable
    without generating 6000 rows.

    TODO (session 1): declare the fields and implement `execute`.
    """

    def __init__(self, model_repository: ModelRepository) -> None:
        # TODO (session 1): store the collaborators.
        raise NotImplementedError

    def execute(self) -> None:
        """Train the model, evaluate it, then persist it with its model card.

        TODO (session 1): move notebook cells 22, 26, 28-30 and 41 here.

        Order matters: evaluate BEFORE saving, and never save a model you did not
        evaluate. A model saved without its metrics is an artifact nobody can defend.
        """
        raise NotImplementedError


def build_model(random_state: int = 42) -> object:
    """Build the scikit-learn pipeline, without fitting it.

    Move notebook cells 20, 22 and 24 here.

    Pure function of its argument: no file access, no randomness that is not seeded,
    no global variable. This is the function you will unit-test, and the one that lets
    the training script and the API agree on the same features.

    TODO (session 1): implement. Use the constants declared in `domain/entities.py`
    (FEATURE_COLUMNS, NUMERIC_FEATURES, CATEGORICAL_FEATURES) instead of redefining
    the lists from cell 20 (DRY).

    Note: `train_test_split` belongs to the *training* case (step 2), not here. The
    pipeline does not need to know about splits.
    """
    raise NotImplementedError