"""Tests du cas d'usage de prédiction.

Séance 1 — TODO : implémenter.

Un test de cas d'usage ne teste pas le modèle : il teste l'**orchestration**. Est-ce que
le cas dusage appelle bien le prédicteur ? Est-ce qu'il persiste ce qu'il doit
persister ? Est-ce qu'il laisse remonter les erreurs du domaine au lieu de les
avaler ?

C'est le niveau de test qui a le meilleur rapport valeur / coût de ce projet, parce
qu'il tient en quelques lignes et qu'il casse dès qu'une règle d'orchestration bouge.
"""

from __future__ import annotations

# TODO (session 1): implement these tests.
#
# 1. test_execute_delegates_to_the_predictor
#    the use case calls the predictor and returns what it returns.
#    Use a fake predictor that records the call, or monkeypatch.
# 2. test_execute_persists_the_prediction
#    if you decided in the ADR to persist the prediction, assert it is readable
#    afterwards. If you decided NOT to persist it here, replace this test by a test
#    asserting the opposite — a decision has to be tested as well as a feature.
# 3. test_domain_errors_are_not_swallowed
#    if the predictor raises InvalidOrderError, `execute` propagates it (it does not
#    return None, it does not wrap it into a generic Exception). An application that
#    hides its errors cannot be monitored (session 7).
# 4. test_use_case_does_not_depend_on_the_technology
#    a test that only imports `application` + `abstractions` + `domain` and never
#    `infrastructure`... write it as an import guard with `ast` or run it as a
#    separate test file, see docs/decisions/README.md. A cheap way to enforce the
#    dependency rule is to grep the imports in CI (session 3).


def test_execute_delegates_to_the_predictor() -> None:
    """The use case delegates the computation to the predictor."""
    raise NotImplementedError


def test_execute_persists_the_prediction() -> None:
    """The prediction is persisted (or explicitly not, per the ADR)."""
    raise NotImplementedError


def test_domain_errors_are_not_swallowed() -> None:
    """A domain error raised by the predictor reaches the API layer unchanged."""
    raise NotImplementedError