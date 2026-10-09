"""Routeur : prédictions.

Séance 1 — TODO : implémenter.

`POST /v1/predictions` est l'élément « Exposer une fonction de prédiction » du tableau
des éléments à industrialiser : c'est la cellule 34 du notebook, exposée en HTTP.

`POST /v1/predictions/batch` et `GET /v1/predictions/{order_id}` arrivent en séance 5,
avec la lecture de l'historique : ne les implémentez pas maintenant (YAGNI).

TODO (session 1)
---------------
- implémenter `POST /v1/predictions` ;
- `response_model=` doit être le schéma Pydantic de `api/schemas.py`, pas le type du
  domaine : c'est ce qui fait que FastAPI valide la réponse et documente l'API ;
- le schéma de la réponse a un champ `latency_ms` (séance 7 pour le remplir, mais le
  champ existe dès le contrat : votre réponse doit rester conforme dès la séance 1) ;
- gérer le cas « modèle pas chargé » : 503, via `ModelNotAvailableError` et
  `api/errors.py`, pas via un `if` dans le handler.

TODO (session 5): ajouter `POST /v1/predictions/batch` et `GET /v1/predictions/{order_id}`
lorsque le cas d'usage batch et le `PredictionStore` existeront.
"""

from __future__ import annotations

# TODO (session 1): declare the router and POST /v1/predictions.
#
# Expected shape:
#
#   router = APIRouter(prefix="/v1/predictions", tags=["predictions"])
#
#   @router.post("", response_model=PredictionSchema)
#   def create_prediction(
#       order: OrderFeaturesSchema,
#       use_case: PredictEligibility = Depends(get_predict_eligibility_use_case),
#   ) -> PredictionSchema: ...