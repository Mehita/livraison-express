"""Tests de contrat des implémentations de `OrderStore`.

Séance 1 — TODO : implémenter.

Quand vous écrirez un vrai adaptateur (PostgreSQL, Redis, SQLite...), vous répéterez
les mêmes tests à chaque fois. L'idée est de les écrire **une fois**, contre
l'ABC, et de les exécuter pour toutes les implémentations.

C'est un test d'inversion : au lieu d'écrire « mon adaptateur fait ce que je veux »,
on écrit « tout adaptateur fait ce que l'application exige ».

TODO (session 1)
---------------
1. Écrire une classe de test de contrat, réutilisable :

   .. code-block:: python

      class OrderStoreContractTests:
          # Contract every OrderStore implementation must satisfy.

          def make_store(self) -> OrderStore:
              raise NotImplementedError

          def test_save_then_get_returns_the_same_order(self) -> None:
              ...

          def test_get_unknown_returns_none(self) -> None:
              ...

          def test_save_is_idempotent(self) -> None:
              ...

2. Puis une sous-classe par implémentation :

   .. code-block:: python

      class TestInMemoryOrderStore(OrderStoreContractTests):
          def make_store(self) -> OrderStore:
              return InMemoryOrderStore()

   PYTEST ne collecte pas une classe dont le nom ne commence pas par `Test`, donc la
   classe de contrat n'est exécutée qu'à travers les sous-classes : c'est voulu.

3. Ajouter vos propres adaptateurs au fur et à mesure des séances, en ajoutant une
   sous-classe de deux lignes. Si votre adaptateur échoue à un test de contrat, ce n'est
   pas le test qu'il faut corriger : c'est l'adaptateur, ou c'est l'ABC qu'il faut
   préciser.

Le même fichier accueillera, plus tard, les contrats de `ModelRepository` (séance 3),
`ExperimentTracker` (séance 4), `EventStream` (séance 6) et `MetricsRecorder` (séance 7).
Un fichier de contrats par session, ou un seul qui grossit ? Décidez et justifiez.
"""

from __future__ import annotations

# TODO (session 1): implement the contract tests and their subclass for
# InMemoryOrderStore.