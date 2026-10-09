"""Racine de composition : le seul endroit qui connaît les classes concrètes.

Séance 1 — TODO : implémenter.

Ce module assemble les couches :

```text
abstractions/OrderStore            ← implémenté par → infrastructure/…
abstractions/ModelRepository       ← implémenté par → infrastructure/…
      ↓                                        ↓
application/PredictEligibility  ← reçoit des abstractions, pas des classes
      ↓
api/routers/predictions      ← reçoit des cas d'usage via Depends
```

Conséquence : `api/` et `application/` n'importent **jamais** `infrastructure`. Changer
de base de données, c'est modifier ce fichier, et un seul test.

TODO (session 1)
---------------
1. `build_container(...)` (ou `get_container()`) : instancier la configuration, les
   adaptateurs et les cas d'usage, une seule fois par processus ;
2. `load_model()` : charger l'artefact produit par le notebook (cellule 43) et le
   construire en `EligibilityPredictor`. Doit-il échouer au démarrage si le fichier est
   absent ? Rappelez-vous la différence entre `/health` et `/health/ready` ;
3. fournir les objets au bon moment : le lifespan de FastAPI est le bon endroit pour
   charger/relâcher, pas l'import du module ;
4. si l'application doit fonctionner avec plusieurs implémentations selon
   l'environnement (`local` / `test` / `prod`), c'est ici que se prend la décision.
   C'est exactement ce que fait une « factory » : elle choisit en fonction d'un
   paramètre, et rien d'autre dans le code n'a à savoir.
"""

from __future__ import annotations

from .abstractions.model_repository import ModelRepository
from .abstractions.order_store import OrderStore


class Container:
    """Assemblage des objets de l'application.

    TODO (session 1): declare the attributes you need (settings, order_store,
    model_repository, use cases) and add a property or accessor for each one.
    A dataclass is a good fit here: it makes the assembled graph explicit.
    """

    # TODO (session 1): declare the attributes.
    ...


def build_container() -> Container:
    """Build the object graph of the application.

    TODO (session 1): implement. Choose here which implementations to use.

    This function is where you plug in the technical choices: which `OrderStore`,
    which `ModelRepository`, in which environment. Nowhere else.
    """
    raise NotImplementedError


def get_order_store() -> OrderStore:
    """Return the configured OrderStore implementation."""
    raise NotImplementedError


def get_model_repository() -> ModelRepository:
    """Return the configured ModelRepository implementation."""
    raise NotImplementedError