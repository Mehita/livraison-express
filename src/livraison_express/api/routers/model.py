"""Routeur : métadonnées du modèle en service.

Séance 3 — ce routeur est livré par le squelette de la Séance 3, il n'est pas
nécessaire en Séance 1.

`GET /v1/model` expose la model card (cellule 55 du notebook) : version en service,
seuil de décision, variables utilisées, métriques, limites connues.

C'est l'endpoint qui répond à la question qu'on vous posera le premier jour d'un
incident : « quelle version tourne en production, et avec quelles métriques ? »
Sans lui, la réponse est dans un fichier `.joblib` sur un disque, ce qui n'est pas
une réponse.

TODO (séance 3)
---------------
- implémenter le handler ;
- décider si la version se lit dans l'artefact au démarrage ou si elle vient d'un
  registre (ModelRegistry) : le registre est l'objet de la séance 3 ;
- exposer aussi la liste des versions disponibles ?
"""

from __future__ import annotations

# TODO (session 3): declare the router.
#
# Expected shape:
#
#   router = APIRouter(prefix="/v1/model", tags=["model"])
#
#   @router.get("", response_model=ModelCardSchema)
#   def get_model_card(...) -> ModelCardSchema: ...