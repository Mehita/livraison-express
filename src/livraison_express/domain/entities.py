"""Types du domaine.

Séance 1 — TODO : compléter et transformer en dataclasses.

Ce module ne contient aucune dépendance technique : ni scikit-learn, ni pandas, ni
FastAPI. Les types y sont définis par leur *forme* (`OrderFeatures`), ce qui est
précisément ce qui permet de changer de base de données ou de format d'événement
sans toucher une seule ligne de logique métier (règle de dépendance inversée).

Le contrat exact de `OrderFeatures` est défini par `docs/api/openapi.yml` :
`OrderFeatures` y reprend exactement les `FEATURE_COLUMNS` de la cellule 20 du notebook.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

# TODO (session 1): declare the feature columns exactly as in notebook cell 20
# (FEATURE_COLUMNS, NUMERIC_FEATURES, CATEGORICAL_FEATURES) and expose them as
# module-level constants. They are the contract between the notebook, the
# validation, the model and the API: define them in ONE place and import them
# everywhere else (DRY).
#
# Expected content (adapt to the notebook, do not invent columns):
#   TARGET_COLUMN = "express_eligible"
#   FEATURE_COLUMNS: list[str]          # the 12 columns of cell 20
#   NUMERIC_FEATURES: list[str]
#   CATEGORICAL_FEATURES: list[str]


@dataclass(frozen=True)
class OrderFeatures:
    """Caractéristiques d'une commande, telles que requises par le modèle.

    Correspond au schéma `OrderFeatures` de `docs/api/openapi.yml`, donc aux
    variables de la cellule 20 du notebook.

    TODO (session 1): declare the fields. `order_id` is optional (the server
    generates it when it is missing, see POST /v1/orders). The categorical fields
    are closed sets (`Weather`, `DeliveryZone`, `CustomerType` in the OpenAPI file):
    decide whether to type them as `str` or as `Enum`, and justify the choice.
    """

    # TODO (session 1): declare the fields.
    ...


@dataclass(frozen=True)
class Prediction:
    """Résultat d'une prédiction : la sortie de la cellule 34 du notebook.

    TODO (session 1): declare the fields required by the `Prediction` schema of
    the OpenAPI file: order_id, express_eligible, decision, probability,
    model_version, predicted_at (and latency_ms from session 7).

    Note: the notebook returns a `dict`. A dataclass is better here because it
    states the contract once, and `api/schemas.py` converts it to the JSON contract.
    """

    # TODO (session 1): declare the fields.
    ...


@dataclass(frozen=True)
class OrderEvent:
    """Message produit et consommé par le flux temps réel (séance 6).

    TODO (session 6): declare the fields of the `OrderEvent` schema of the
    OpenAPI file: event_id, event_type, occurred_at, order, schema_version.
    The dataclass is declared here, in the domain layer, because the *contract*
    is a business concern: the transport (Kafka, Redis Streams, SQS...) is not.
    """

    # TODO (session 6): declare the fields.
    ...


@dataclass(frozen=True)
class ModelCard:
    """Métadonnées et métriques du modèle en service (cellule 55 du notebook).

    TODO (session 3): declare the fields of the `ModelCard` schema of the
    OpenAPI file.
    """

    # TODO (session 3): declare the fields.
    ...


# TODO (session 1): do we need a type for the model artifact itself
# (the scikit-learn Pipeline loaded from the .joblib)? If you add one,
# put it here and keep the scikit-learn import out of this module.
#
# TODO (session 1): `predicted_at` is a datetime, but the notebook cell 34 calls
# `datetime.utcnow()`, which is deprecated since Python 3.12. Use a timezone-aware
# `datetime.now(timezone.utc)` instead, and say why in your commit message.