"""Routeur : collecte des commandes.

`POST /v1/orders` répond **202 Accepted** et non 201 : la commande est acceptée et rangée,
la prédiction n'est pas faite. Le routeur ne fait que convertir : requête HTTP ->
`OrderFeatures`, appel du cas d'usage `CollectOrder`, résultat -> `OrderAccepted`. Ni le
modèle ni le format de stockage n'apparaissent ici.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, status

from ...application.collect_order import CollectOrder
from ..dependencies import get_collect_order_use_case
from ..mappers import to_order, to_order_schema
from ..schemas import OrderAccepted, OrderFeaturesSchema

router = APIRouter(prefix="/v1/orders", tags=["orders"])


@router.post("", response_model=OrderAccepted, status_code=status.HTTP_202_ACCEPTED)
def create_order(
    order: OrderFeaturesSchema,
    use_case: CollectOrder = Depends(get_collect_order_use_case),
) -> OrderAccepted:
    """Collect one order (idempotent on `order_id`)."""
    return OrderAccepted(order_id=use_case.execute(to_order(order)))


@router.get("/{order_id}", response_model=OrderFeaturesSchema, response_model_exclude_none=True)
def get_order(
    order_id: str,
    use_case: CollectOrder = Depends(get_collect_order_use_case),
) -> OrderFeaturesSchema:
    """Read an order back (404 through OrderNotFoundError when unknown)."""
    return to_order_schema(use_case.get(order_id))
