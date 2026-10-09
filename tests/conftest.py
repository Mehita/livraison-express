"""Fixtures partagées par les tests.

Séance 1 — TODO : compléter.

Deux objectifs :

1. **Les tests doivent être rapides et hermétiques.** Un test qui touche une vraie base
   de données ou qui charge un vrai modèle de 20 Mo est un test lent et instable.
   C'est le rôle des adaptateurs de `infrastructure/dev/`.
2. **Un point de substitution unique.** Le même point doit servir aux tests unitaires
   (un faux prédicteur) et aux tests d'intégration (l'API complète). Sinon chaque test
   réécrit son câblage.

TODO (session 1)
---------------
- `sample_order` : une `OrderFeatures` valide, réutilisable (valeurs de la cellule 36) ;
- `fake_model` : un faux objet qui implémente l'interface attendue par
  `EligibilityPredictor` (une méthode `predict_proba`), sans scikit-learn. C'est le
  moyen de tester le prédicteur sans modèle ;
- `order_store` : une instance neuve d'`InMemoryOrderStore` par test ;
- `api_client` : un `TestClient` FastAPI dont les dépendances (`Depends`) sont
  remplacées par vos objets de test. `app.dependency_overrides` est l'outil prévu pour ça.
"""

from __future__ import annotations

import pytest

# TODO (session 1): declare the fixtures below and import what you need.
#
#   import sys
#   from pathlib import Path
#
#   import numpy as np
#   import pytest
#   from fastapi.testclient import TestClient
#
#   sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def sample_order() -> object:
    """Return one valid order (notebook cell 36)."""
    raise NotImplementedError


@pytest.fixture
def fake_model() -> object:
    """Return a stand-in for the scikit-learn pipeline.

    The notebook cell 34 calls `model.predict_proba(input_df)[0, 1]`. A fake object
    exposing the same method is enough to test the predictor: no joblib, no training.

    TODO (session 1): implement it. Decide whether the probability is fixed or
    parameterised (a fixed probability gives predictable tests, a parameterised one
    lets you test both sides of the threshold).
    """
    raise NotImplementedError


@pytest.fixture
def order_store() -> object:
    """Return a fresh InMemoryOrderStore, empty."""
    raise NotImplementedError


@pytest.fixture
def api_client() -> object:
    """Return a TestClient for the application, with test dependencies.

    TODO (session 1): implement it with `fastapi.testclient.TestClient` and
    `app.dependency_overrides`, so that no test needs a real database.
    """
    raise NotImplementedError