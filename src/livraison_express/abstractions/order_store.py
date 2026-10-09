"""Abstraction : où l'application range les commandes qu'elle collecte.

Séance 1 — TODO : implémenter un adaptateur dans `infrastructure/`.

C'est la brique « collecte de données » du tableau des éléments à industrialiser.
Le besoin est simple et la réponse technique ne l'est pas : une commande est écrite
une fois et lue potentiellement plusieurs fois (page de surveillance, ré-exécution du
batch, analyse après incident). Le choix du support (PostgreSQL, Redis, SQLite,
fichiers, API existante) dépend de ce que vous avez, de la fréquence de lecture,
de la durée de conservation et de vos contraintes d'exploitation.

Ne partez pas du choix : partez du besoin.

Ce que la couche application exige d'un support de stockage est listé ci-dessous.
Toute solution qui ne tient pas ces promesses ne convient pas, quelle qu'elle soit.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..domain.entities import OrderFeatures


class OrderStore(ABC):
    """Persistance des commandes collectées.

    Contrat attendu par la couche application :

    - `save` est **idempotent** sur `order_id` : ré-enregistrer la même commande
      ne doit pas créer de doublon (la cellule 18 du notebook supprime les doublons,
      autant ne pas les créer) ;
    - `get` renvoie `None` pour un identifiant inconnu, et ne lève pas d'exception ;
    - les noms d'erreurs à lever sont ceux de `domain/exceptions.py`, pas ceux de la
      bibliothèque de stockage utilisée (PostgreSQL, Redis...) : l'application ne
      doit pas connaître le vocabulaire de sa base.

    TODO (session 1): implement a concrete adapter in infrastructure/ (or reuse the
    dev one, but justify it), and write the rationale in
    docs/decisions/ADR-0001-*.md.

    Questions to answer in the ADR:
    - Quel volume, quelle fréquence d'écriture, quelle durée de conservation ?
    - Pourquoi ce support plutôt qu'un autre (au moins trois options comparées) ?
    - Que se passe-t-il si la base est indisponible au démarrage de l'API ?
    - Comment gérez-vous les écritures concurrentes sur un même `order_id` ?
    """

    @abstractmethod
    def save(self, order: OrderFeatures) -> None:
        """Persist one order.

        Idempotent on `order_id`.
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, order_id: str) -> OrderFeatures | None:
        """Return the stored order, or None if it does not exist."""
        raise NotImplementedError

    # TODO (session 1): declare the other methods your use cases need, with their
    # docstring. Typical needs: listing orders (pagination for a back-office),
    # iterating over the orders to predict (batch), deleting them (right to erasure),
    # counting them (supervision).
    #
    # Watch out: a method that returns a pandas DataFrame leaks the technology into
    # the abstraction. Return domain types (OrderFeatures), and convert inside the
    # adapter.

    # TODO (session 4): you will need a method to read the orders to predict
    # (see batch_predict_orders, notebook cell 46). Add it when you need it,
    # not before (YAGNI).