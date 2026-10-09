"""Abstraction : où l'application range le modèle entraîné.

Séance 1 — TODO : implémenter un adaptateur dans `infrastructure/`.

Trois besoins distincts se cachent derrière cette abstraction, et les confondre est
l'erreur classique :

1. **Écrire** le modèle et ses métadonnées à l'entraînement (cellule 41 du notebook :
   `joblib.dump`, `metrics.json`, `features.json`) ;
2. **Lire** un modèle déjà entraîné au démarrage de l'API (cellule 43 :
   `joblib.load`) — c'est ce qui distingue un service de production d'un notebook ;
3. **Savoir quelle version est en service** et l'exposer (cellule 55 : la model card,
   endpoint `GET /v1/model`, séance 3).

Un service de prédiction ne doit jamais réentraîner un modèle au démarrage : il charge
un artefact produit ailleurs. Cette séparation entraînement / service est l'un des
fondamentaux de l'industrialisation, et elle se voit ici.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..domain.entities import ModelCard


class ModelRepository(ABC):
    """Stockage des artefacts du modèle et de ses métadonnées.

    TODO (session 1): implement a concrete adapter in infrastructure/ and write the
    rationale in docs/decisions/ADR-0002-*.md.

    ADR-0000 (fourni en exemple) traite explicitement le cas « répertoire local » :
    c'est une réponse acceptable en Séance 1 et en Séance 2, à condition de dire
    qu'elle est provisoire et de définir ce qu'elle devient à la Séance 3.

    Contrats attendus de toute implémentation :

    - `save` écrit le modèle **et** les métadonnées de façon cohérente entre elles
      (cellule 41 écrit trois fichiers : les trois doivent être cohérents, sinon
      on sert un modèle avec les features d'un autre) ;
    - `load` doit être tolérant à l'absence d'artefact : l'API doit démarrer quand même
      et signaler l'indisponibilité sur `/health/ready`, pas exploser au boot ;
    - les identifiants de version sont des chaînes opaques (`"1.0.0"`), comparez-les
      sans supposer d'ordre numérique.
    """

    @abstractmethod
    def save(self, model: object, model_card: ModelCard) -> None:
        """Persist a trained model and its model card.

        Notebook reference: cell 41 (joblib.dump + metrics.json + features.json).
        """
        raise NotImplementedError

    @abstractmethod
    def load(self, version: str) -> object:
        """Return the trained model for this version.

        Notebook reference: cell 43 (joblib.load).

        Raises:
            ModelNotAvailableError: if the artifact is missing or unreadable.
        """
        raise NotImplementedError

    # TODO (session 1): declare the other methods you need.
    # Typical: latest_version(), list_versions(), model_card(version).
    # Sessions 3 and 8 will need version history: implement it then, not now (YAGNI).

    # TODO (session 1): `object` as the model type is a placeholder. A scikit-learn
    # Pipeline is what comes out of cell 24. How do you want to express this without
    # importing scikit-learn in the abstraction? Options: a protocol, a type alias
    # in `domain/entities.py`, or leaving it as `object` and documenting it.
    # Decide, and defend the choice.

    # TODO (session 7): the `Prediction` import above is unused for now. Remove it if
    # you do not need it, and check that your linter (ruff) is happy.