"""Cas d'usage : collecter une commande à prédire.

Séance 1 — TODO : implémenter.

C'est le cas d'usage « Collecte de données » du tableau des éléments à industrialiser.

La question de conception centrale de ce cas d'usage : **quand** prédire ?

- à la réception de la commande (synchrone, réponse immédiate à l'appelant) ;
- de façon différée (la commande est stockée, la prédiction est calculée plus tard) ;
- les deux.

Le contrat OpenAPI de `POST /v1/orders` répond **202 Accepted** : la commande est
acceptée, la prédiction est déjà partie ailleurs. C'est un choix d'architecture, pas
une commodité : le chemin de code que vous écrivez ici doit être compatible avec le fait
que la prédiction n'est pas disponible au retour de la requête.

TODO (session 1)
---------------
1. declare the fields (`order_store` is mandatory; is anything else needed?);
2. `execute`: validate the order, persist it, return what the API needs
   (`OrderAccepted`: an `order_id`);
3. what happens if the same `order_id` is submitted twice? The `OrderStore` contract
   says `save` is idempotent: the API returns 202 again, or 409? Argue it.
"""

from __future__ import annotations

from ..abstractions.order_store import OrderStore
from ..domain.entities import OrderFeatures


class CollectOrder:
    """Enregistre une commande à prédire.

    Collaborateurs
    --------------
    order_store : la persistance des commandes.

    TODO (session 1): implement `execute`, and add a second method to read an order
    back (used by `GET /v1/orders/{order_id}`). Should reading be a method of this
    same class, or another use case? Argue it.
    """

    def __init__(self, order_store: OrderStore) -> None:
        # TODO (session 1): store the collaborator.
        raise NotImplementedError

    def execute(self, order: OrderFeatures) -> str:
        """Persist one order and return its identifier.

        TODO (session 1):
        - generate an `order_id` when the incoming order has none
          (format of the notebook: `CMD-000001`, see cell 8);
        - let the store validate the order, or validate it yourself? Argue it.
        """
        raise NotImplementedError