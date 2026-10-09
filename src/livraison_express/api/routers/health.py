"""Routeur : sondes de vivacité et de disponibilité.

| Sonde | Question | Dépendances | Usage |
|---|---|---|---|
| `/health` | le processus répond-il ? | aucune | l'orchestrateur redémarre le conteneur |
| `/health/ready` | peut-il traiter une requête ? | modèle chargé, store joignable | l'orchestrateur coupe le trafic |

`/health` ne dépend de rien : si elle dépendait de la base, un incident de base
déclencherait des redémarrages de conteneurs qui n'y peuvent rien. Elle répond 200 même
quand tout le reste est cassé. `/health/ready` répond 503 tant que le modèle n'est pas chargé.
"""

from __future__ import annotations

from fastapi import APIRouter, Request, Response

from ..metadata import API_VERSION, SERVICE_NAME
from ..schemas import HealthStatus, ReadinessStatus

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthStatus)
def get_health() -> HealthStatus:
    """Liveness: the process answers."""
    return HealthStatus(service=SERVICE_NAME, version=API_VERSION)


@router.get("/health/ready", response_model=ReadinessStatus)
def get_readiness(request: Request, response: Response) -> ReadinessStatus:
    """Readiness: 200 only if a prediction can be served, 503 otherwise."""
    container = request.app.state.container
    checks = {
        "model": "loaded" if container.model_ready else "missing",
        "order_store": _order_store_status(container),
    }
    ready = all(value in {"loaded", "reachable"} for value in checks.values())
    if not ready:
        response.status_code = 503
    return ReadinessStatus(
        status="ready" if ready else "not_ready", checks=checks, version=API_VERSION
    )


def _order_store_status(container) -> str:
    """Probe the store with a harmless read; any failure means 'unreachable'."""
    try:
        container.order_store.get("__readiness_probe__")
    except Exception:
        return "unreachable"
    return "reachable"
