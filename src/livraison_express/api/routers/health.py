"""Routeur : sondes de vivacité et de disponibilité.

Séance 1 — TODO : implémenter.

La différence entre les deux sondes est l'une des distinctions les plus importantes
en exploitation, et elle est trop souvent oubliée :

| Sonde | Question | Dépendances | Usage |
|---|---|---|---|
| `/health` | le processus répond-il ? | aucune | l'orchestrateur redémarre le conteneur |
| `/health/ready` | le service peut-il traiter une requête ? | modèle chargé, dépendances joignables | l'orchestrateur arrête d'envoyer du trafic |

Conséquence à comprendre : si `/health` dépend de la base de données, un incident de la
base déclenche des redémarrages de conteneurs qui n'y peuvent rien. `/health` doit
répondre 200 même quand tout le reste est cassé.

`GET /health/ready` renvoie 503 quand le modèle n'est pas chargé : c'est le comportement
attendu au démarrage, avant que `bootstrap.py` n'ait chargé l'artefact, et après un
incident de disque.

TODO (session 1)
---------------
- implémenter les deux handlers et leurs schémas de réponse (`HealthStatus`,
  `ReadinessStatus`) ;
- écrire un test qui vérifie que `/health` renvoie 200 même quand les dépendances sont
  dans le rouge (voir `tests/test_api_predictions.py` pour le modèle de test) ;
- la réponse doit-elle exposer la version ? Comparez avec le contrat OpenAPI.
"""

from __future__ import annotations

# TODO (session 1): declare the router here.
#
# Expected shape:
#
#   from fastapi import APIRouter, Response, status
#
#   router = APIRouter(tags=["health"])
#
#   @router.get("/health", response_model=HealthStatus)
#   def get_health() -> HealthStatus: ...
#
#   @router.get("/health/ready", response_model=ReadinessStatus)
#   def get_readiness(response: Response) -> ReadinessStatus: ...