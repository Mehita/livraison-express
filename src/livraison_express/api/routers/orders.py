"""Routeur : collecte des commandes.

Séance 1 — TODO : implémenter.

Deux endpoints : `POST /v1/orders` (collecte) et `GET /v1/orders/{order_id}` (lecture).

Ce routeur est l'exemple le plus simple de la séparation des couches : il convertit
une requête HTTP en `OrderFeatures`, appelle le cas d'usage `CollectOrder`, et convertit
le résultat en `OrderAccepted`. Ni le modèle, ni le format de stockage n'apparaissent ici.

Deux points d'attention :

1. **Code 202 et non 201.** Le contrat renvoie 202 : la commande est acceptée, la
   prédiction n'est pas faite. Une.created (201) dirait « votre ressource est créée »
   sans dire si elle est déjà prédite. Écrivez la conséquence de ce choix dans votre ADR.
2. **Conversion des schémas.** `OrderFeaturesSchema` → `OrderFeatures` (domain) puis
   retour. Ne renvoyez jamais un schéma Pydantic « tel quel » si le domaine a son propre
   type : ce sont deux contrats qui évoluent séparément.

TODO (session 1)
---------------
- implémenter les deux handlers ;
- `status_code=202` explicite sur le POST (FastAPI ne le devine pas) ;
- documenter et vérifier que les 422 (commande invalide) et les 404 (commande inconnue)
  correspondent au format d'erreur du contrat.
"""

from __future__ import annotations

# TODO (session 1): declare the router and the two handlers.
#
# Expected shape:
#
#   router = APIRouter(prefix="/v1/orders", tags=["orders"])
#
#   @router.post("", response_model=OrderAccepted, status_code=status.HTTP_202_ACCEPTED)
#   def create_order(
#       order: OrderFeaturesSchema,
#       use_case: CollectOrder = Depends(get_collect_order_use_case),
#   ) -> OrderAccepted: ...
#
#   @router.get("/{order_id}", response_model=OrderFeaturesSchema)
#   def get_order(order_id: str, ...) -> OrderFeaturesSchema: ...