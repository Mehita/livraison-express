"""Traduction des exceptions en réponses HTTP.

Séance 1 — TODO : implémenter.

Ce module implémente le principe « une erreur métier n'est pas une erreur serveur ».

| Exception du domaine            | Code HTTP | Un code d'erreur stable |
|---------------------------------|-----------|-------------------------|
| `InvalidOrderError`             | 422       | `validation_error`      |
| `ModelNotAvailableError`        | 503       | `model_unavailable`     |
| erreur du client HTTP           | 400/404   | ...                     |

Les codes d'erreur sont un **contrat** : un client branche son monitoring dessus, on
ne les change pas sans faire majorer la version de l'API. Les messages, eux, sont
libres et destinés à l'humain.

TODO (session 1)
---------------
1. enregistrer un `app.exception_handler` par famille d'erreur du domaine ;
2. produire le corps `ErrorResponse` défini dans `docs/api/openapi.yml` ;
3. vérifier le cas ValidationError de Pydantic : FastAPI renvoie déjà 422, mais avec
   SON format de corps. Les deux formats doivent correspondre au contrat, donc il
   faut peut-être surcharger ce handler aussi (et c'est le genre de détail qui fait
   échouer un test d'intégration sur une API censée respecter son contrat) ;
4.logger l'erreur avec un identifiant de corrélation, et renvoyer cet identifiant au
   client : c'est ce qui permet de retrouver la requête dans les logs (séance 7).

`ValidationError` de Pydantic n'est pas une erreur métier : ne l'attrapez pas dans le
domain, elle est dans la couche API.
"""

# TODO (session 1): declare the handlers here.
#
# Expected shape:
#
#   from fastapi import FastAPI, Request
#   from fastapi.responses import JSONResponse
#
#   def register_exception_handlers(app: FastAPI) -> None:
#       @app.exception_handler(InvalidOrderError)
#       async def handle_invalid_order(request: Request, exc: InvalidOrderError) -> JSONResponse:
#           ...