"""Racine de composition : le seul endroit qui connaît les classes concrètes.

```text
abstractions/OrderStore            ← implémenté par → infrastructure/…
abstractions/ModelRepository       ← implémenté par → infrastructure/…
      ↓                                        ↓
application/PredictEligibility  ← reçoit des abstractions, pas des classes
      ↓
api/routers/predictions      ← reçoit des cas d'usage via Depends
```

`api/` et `application/` n'importent jamais `infrastructure`. Changer de base de données,
c'est modifier `_build_order_store` ici, et rien d'autre.

Le modèle est chargé une seule fois, au démarrage (`Container.load_model`), jamais à la
requête. Son absence n'est pas fatale : l'API démarre, `/health/ready` répond 503 et les
prédictions aussi (voir ADR-0002).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from functools import lru_cache

from .abstractions.model_repository import ModelRepository
from .abstractions.order_store import OrderStore
from .application.collect_order import CollectOrder
from .application.predict_eligibility import PredictEligibility
from .application.train_model import TrainEligibilityModel
from .config import Settings, get_settings
from .domain.exceptions import ModelNotAvailableError
from .domain.predictor import EligibilityPredictor
from .infrastructure.dev.in_memory_model_repository import FileModelRepository
from .infrastructure.dev.in_memory_order_store import InMemoryOrderStore
from .infrastructure.dev.synthetic_orders import generate_labeled_orders
from .infrastructure.sqlite.sqlite_order_store import SqliteOrderStore

logger = logging.getLogger(__name__)


@dataclass
class Container:
    """Le graphe d'objets de l'application, assemblé une fois par processus."""

    settings: Settings
    order_store: OrderStore
    model_repository: ModelRepository
    collect_order: CollectOrder
    train_model: TrainEligibilityModel
    predictor: EligibilityPredictor | None = None

    @property
    def model_ready(self) -> bool:
        """True once a model has been loaded (drives `/health/ready`)."""
        return self.predictor is not None

    def load_model(self) -> None:
        """Load the model artifact if it exists; stay up without it otherwise.

        A missing file is expected (nobody ran `train` yet) and is only reported.
        A corrupted file is a different incident: the exception is not caught.
        """
        try:
            model = self.model_repository.load(self.settings.model_version)
        except ModelNotAvailableError as error:
            logger.warning("Model not loaded, predictions will answer 503: %s", error)
            self.predictor = None
            return
        self.predictor = EligibilityPredictor(
            model=model,
            threshold=self.settings.model_threshold,
            model_version=self.settings.model_version,
        )
        logger.info("Model %s loaded", self.settings.model_version)

    def predict_eligibility(self) -> PredictEligibility:
        """Return the prediction use case.

        Raises:
            ModelNotAvailableError: no model is loaded (mapped to HTTP 503).
        """
        if self.predictor is None:
            raise ModelNotAvailableError("Aucun modèle chargé : lancez `train` puis redémarrez.")
        return PredictEligibility(self.predictor)


def _build_order_store(settings: Settings) -> OrderStore:
    """Factory: choose the OrderStore from the environment, nothing else knows."""
    if settings.environment == "test":
        return InMemoryOrderStore()
    return SqliteOrderStore(settings.order_store_dsn)


def build_container(settings: Settings | None = None) -> Container:
    """Build the object graph. Tests pass their own `settings`."""
    settings = settings or get_settings()
    order_store = _build_order_store(settings)
    model_repository = FileModelRepository(settings.model_path)
    return Container(
        settings=settings,
        order_store=order_store,
        model_repository=model_repository,
        collect_order=CollectOrder(order_store),
        train_model=TrainEligibilityModel(
            model_repository,
            load_orders=generate_labeled_orders,
            model_version=settings.model_version,
        ),
    )


@lru_cache(maxsize=1)
def get_container() -> Container:
    """Return the process-wide container (the model is loaded once, at startup)."""
    return build_container()
