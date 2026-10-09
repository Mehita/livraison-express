"""Injection des dépendances : comment un routeur obtient ses cas d'usage.

Séance 1 — TODO : implémenter.

Un routeur ne doit jamais écrire `OrderStore()` ni `Predictor(...)`. Si c'est le cas,
le test du routeur exige une base de données, et l'infrastructure fuit dans l'API.

Le mécanisme idiomatique avec FastAPI est `Depends`, qui appelle une fonction «
fournisseur » (provider) au lieu d'instancier la dépendance dans le handler. Deux
questions à trancher :

1. Les fournisseurs doivent-ils être des singletons (`lru_cache`) ? Si une requête
   recharge le `.joblib` de 20 Mo, l'API s'effondre. Que se passe-t-il si le modèle
   change en cours de route (séance 3) ?
2. Comment les tests remplacent-ils les vrais objets ? Il faut un point de substitution
   unique, sinon chaque test doit réécrire le câblage.

TODO (session 1)
---------------
- `get_order_store()`, `get_model_repository()`, `get_predictor()` : écrire des
  fournisseurs qui lisent l'assemblage produit par `bootstrap.py` ;
- `get_predict_eligibility_use_case()` : construire le cas d'usage avec ses
  collaborateurs, ici ou dans `bootstrap.py` ? Une seule des deux (DRY) ;
- `get_settings_dep()` si nécessaire.
"""

from __future__ import annotations

# TODO (session 1): declare the FastAPI dependencies here.
# Example of the expected shape:
#
#   from fastapi import Depends
#
#   def get_order_store() -> OrderStore:
#       return ...
#
# Then in a router:
#
#   @router.post("/v1/predictions", response_model=Prediction)
#   def predict(
#       order: OrderFeaturesSchema,
#       use_case: PredictEligibility = Depends(get_predict_eligibility_use_case),
#   ) -> PredictionSchema:
#       ...
#
# Keep this module free of FastAPI route definitions: it is the wiring, not the web.