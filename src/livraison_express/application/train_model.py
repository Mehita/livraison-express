"""Cas d'usage : entraîner le modèle d'éligibilité.

Hors du chemin de la requête HTTP : l'entraînement se fait dans un job
(`python -m livraison_express train`), jamais quand un client appelle l'API.

Le notebook est découpé en trois morceaux séparés par des frontières :

| Étape | Cellules | Devient |
|---|---|---|
| construire la pipeline | 20, 22, 24 | `build_model()` : fonction pure |
| entraîner et évaluer | 22, 26, 28 | `TrainEligibilityModel.execute()` |
| persister | 41, 55 | le `ModelRepository` injecté |

MLflow (cellule 26) n'est pas importé ici : le suivi d'expériences sera un collaborateur
distinct à la séance 4 (`ExperimentTracker`).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ..abstractions.model_repository import ModelRepository
from ..domain.entities import (
    CATEGORICAL_FEATURES,
    FEATURE_COLUMNS,
    NUMERIC_FEATURES,
    LabeledOrder,
    ModelCard,
)


def build_model(random_state: int = 42) -> Pipeline:
    """Build the scikit-learn pipeline, without fitting it (notebook cells 20-24).

    Pure function: no file access, no global state, same arguments -> same pipeline.
    """
    numeric_transformer = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, NUMERIC_FEATURES),
            ("categorical", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )
    classifier = LogisticRegression(
        max_iter=1000, class_weight="balanced", random_state=random_state
    )
    return Pipeline(steps=[("preprocessor", preprocessor), ("classifier", classifier)])


class TrainEligibilityModel:
    """Entraîne le modèle, l'évalue, puis le range avec sa fiche d'identité.

    Collaborateurs
    --------------
    model_repository : destination des artefacts (cellule 41).
    load_orders : fournit les commandes passées avec leur résultat. C'est une fonction
        injectée et non un import : en production les données ne seront plus synthétiques,
        et le test n'a pas besoin de générer 6 000 lignes.
    """

    def __init__(
        self,
        model_repository: ModelRepository,
        load_orders: Callable[[], list[LabeledOrder]],
        model_version: str,
        random_state: int = 42,
    ) -> None:
        self._model_repository = model_repository
        self._load_orders = load_orders
        self._model_version = model_version
        self._random_state = random_state

    def execute(self) -> ModelCard:
        """Train, evaluate, then persist. Never saves a model that was not evaluated."""
        features, target = self._to_training_frame(self._load_orders())
        x_train, x_test, y_train, y_test = train_test_split(
            features, target, test_size=0.20, random_state=self._random_state, stratify=target
        )

        model = build_model(self._random_state)
        model.fit(x_train, y_train)

        y_pred = model.predict(x_test)
        y_proba = model.predict_proba(x_test)[:, 1]
        metrics = {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "precision": float(precision_score(y_test, y_pred, zero_division=0)),
            "recall": float(recall_score(y_test, y_pred, zero_division=0)),
            "f1_score": float(f1_score(y_test, y_pred, zero_division=0)),
            "roc_auc": float(roc_auc_score(y_test, y_proba)),
        }

        card = ModelCard(
            model_version=self._model_version, features=list(FEATURE_COLUMNS), metrics=metrics
        )
        self._model_repository.save(model, card)
        return card

    @staticmethod
    def _to_training_frame(orders: list[LabeledOrder]) -> tuple[pd.DataFrame, pd.Series]:
        rows = [{name: asdict(item.order)[name] for name in FEATURE_COLUMNS} for item in orders]
        target = pd.Series([int(item.express_eligible) for item in orders], name="express_eligible")
        return pd.DataFrame(rows, columns=FEATURE_COLUMNS), target
