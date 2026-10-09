"""`ModelRepository` de développement : le `.joblib` du notebook, chargé une fois.

Implémentation de référence de l'abstraction `ModelRepository`.

Le notebook (cellule 41) écrit `express_delivery_model.joblib` dans `artifacts/`.
Cet adaptateur charge ce fichier et le garde en mémoire. C'est exactement ce que fait
un service de production au démarrage, et la cellule 43 du notebook (`joblib.load`)
en montre le code.

Ce fichier est **fourni**. Il illustre deux décisions importantes :

- le modèle est chargé **une fois** au démarrage, pas à chaque requête ;
- l'absence de modèle n'est pas fatale : elle est signalée, et l'API répond 503 sur les
  prédictions tant qu'il n'y a rien à prédire.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import joblib

from ...abstractions.model_repository import ModelRepository
from ...domain.entities import ModelCard
from ...domain.exceptions import ModelNotAvailableError

logger = logging.getLogger(__name__)


class FileModelRepository(ModelRepository):
    """Load and store the model artifact on the local filesystem.

    This is ADR-0000 in code: a local directory, explicitly provisional. See
    docs/decisions/ADR-0000-example-model-artefacts.md.
    """

    def __init__(self, model_path: str) -> None:
        """Build the repository for a given artifact path.

        Args:
            model_path: path to the .joblib file written by notebook cell 41.
        """
        self._model_path = Path(model_path)
        self._model: object | None = None
        self._model_card: ModelCard | None = None

    def save(self, model: object, model_card: ModelCard) -> None:
        """Persist the model artifact and its model card.

        Notebook reference: cell 41 (joblib.dump + metrics.json + features.json).

        Writes exactly what the notebook writes, next to the artifact, so that the
        student can compare both sides. The model card is stored as JSON because it is
        data, not code; the model is stored with joblib because sklearn pipelines are
        code.

        Note on the coupling: this reads `model_card.metrics` and `model_card.features`,
        the two fields required by `ModelCardSchema` in `docs/api/openapi.yml`. Those
        fields belong to the `ModelCard` you declare in `domain/entities.py` (session 3),
        so `save()` only becomes callable after session 3. That is expected, not a bug.
        """
        self._model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, self._model_path)
        self._model_path.with_suffix(".metrics.json").write_text(
            json.dumps(model_card.metrics, indent=2, sort_keys=True)
        )
        self._model_path.with_suffix(".features.json").write_text(
            json.dumps(model_card.features, indent=2)
        )
        self._model = model
        self._model_card = model_card

    def load(self, version: str) -> object:
        """Return the loaded model.

        The `version` argument is accepted to respect the abstraction, but ignored:
        this implementation keeps one artifact, so there is nothing to select. This
        is a limitation to state in your ADR when you implement the real one.
        """
        if not self._model_path.exists():
            raise ModelNotAvailableError(
                f"Model artifact not found: {self._model_path}. "
                "Run notebook cell 41 first, or `python -m livraison_express train`."
            )
        model = joblib.load(self._model_path)
        self._model = model
        return model

    def load_if_available(self) -> object | None:
        """Load the artifact if it exists, return None otherwise.

        Behaviour expected at startup: log a warning and continue, so the process stays
        up and `/health/ready` can report the model as missing.

        Note: a missing file is handled, a **corrupted** file is not. Letting the
        exception propagate is deliberate — a corrupted artifact is a different
        incident than a missing one, and it must be visible at startup.
        """
        if not self._model_path.exists():
            logger.warning("No model artifact at %s", self._model_path)
            return None
        model = self.load("")
        logger.info("Model artifact loaded from %s", self._model_path)
        return model