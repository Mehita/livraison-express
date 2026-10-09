"""Générateur de commandes de développement.

Séance 1 — TODO : compléter depuis la cellule 8 du notebook.

`generate_orders_dataset()` du notebook synthétise 6 000 commandes avec une graine
fixe (`random_state=42`). C'est ce qui rend le notebook exécutable sans source de
données externe, et c'est ce qui permet à vos tests d'être reproductibles.

TODO (session 1)
---------------
Déplacer le corps de la cellule 8 ici, en respectant trois points :

1. **Le type de retour.** Le notebook renvoie un `DataFrame` pandas. Cette fonction
   doit renvoyer une liste de `OrderFeatures`, sinon elle attire pandas dans le
   domaine. Le `DataFrame` reste un détail de la génération, il ne doit pas sortir
   de cette fonction.
2. **La reproductibilité.** `rng = np.random.default_rng(random_state)` avec la graine
   en paramètre : deux appels avec la même graine donnent le même jeu de données.
   C'est ce qui vous permettra d'écrire un test non flaky plus tard.
3. **La graine.** 42 par défaut (valeur de la cellule 3), mais toujours en paramètre.

Ce module sert à trois choses : peupler l'API en local (`POST /v1/orders` avec un corps
généré), entraîner le modèle (cas d'usage `TrainEligibilityModel`) et écrire des tests
sans base de données.
"""

from __future__ import annotations

from ...domain.entities import OrderFeatures


def generate_orders_dataset(n_rows: int = 6000, random_state: int = 42) -> list[OrderFeatures]:
    """Generate a synthetic list of orders.

    Notebook reference: cell 8 (`generate_orders_dataset`).

    TODO (session 1): move the body of cell 8 here.

    The scoring logic of cell 8 (zone penalty, weather penalty, customer bonus, the
    sigmoid that produces `express_eligible`) is the one that makes the synthetic data
    learnable: keep it identical, otherwise your metrics will differ from the notebook's
    and you will spend an hour wondering why.
    """
    raise NotImplementedError