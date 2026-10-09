"""Tests unitaires du prédicteur.

Séance 1 — TODO : implémenter.

C'est le notebook qui donne la référence : la cellule 39 (`run_prediction_tests`)
contient déjà les assertions à reprendre. Elles sont portable telles quelles, il n'y a
que la construction des données qui change (un `OrderFeatures` au lieu d'un `dict`).

Ces tests ne doivent charger **aucun modèle** : ils utilisent la fixture `fake_model`.
C'est le bénéfice concret de l'inversion de dépendances, et c'est à cette séance que
vous devez le constater : la logique métier se teste sans scikit-learn, sans fichier,
sans base de données.
"""

from __future__ import annotations

# TODO (session 1): implement these tests.
#
# Tests to write, from notebook cell 39 (`run_prediction_tests`) and beyond:
#
# 1. test_predict_returns_a_prediction
#    decision in {"oui", "non"}, express_eligible is a bool, 0 <= probability <= 1,
#    model_version is present.
# 2. test_missing_feature_raises_a_domain_error
#    an order without `distance_km` raises a domain exception, NOT a ValueError.
#    Assert the exception TYPE, not the message.
# 3. test_threshold_is_honoured
#    same probability, two thresholds (0.2 and 0.8) → two different decisions.
#    This test does not exist in the notebook and it is the most valuable one:
#    it proves the threshold is a parameter and not a constant.
# 4. test_prediction_has_a_timestamp
#    predicted_at is timezone-aware. (Cell 34 uses the deprecated datetime.utcnow().
#    You are expected to fix that, so test it.)
# 5. test_model_version_is_not_hardcoded
#    the version comes from the model card / configuration, not from a literal in
#    the code.


def test_predict_returns_a_prediction(sample_order: object, fake_model: object) -> None:
    """The predictor returns a coherent prediction for a valid order."""
    raise NotImplementedError


def test_missing_feature_raises_a_domain_error(fake_model: object) -> None:
    """An order missing a mandatory feature raises a domain exception."""
    raise NotImplementedError


def test_threshold_is_honoured(sample_order: object, fake_model: object) -> None:
    """The decision threshold changes the outcome, it is not hardcoded."""
    raise NotImplementedError


def test_prediction_has_a_timestamp(sample_order: object, fake_model: object) -> None:
    """The prediction is dated with a timezone-aware timestamp."""
    raise NotImplementedError