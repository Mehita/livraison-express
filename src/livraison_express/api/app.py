"""Assemblage de l'application FastAPI.

Séance 1 — TODO : implémenter.

`create_app()` est le seul endroit autorisé à importer à la fois `api` et
`infrastructure` : c'est la racine de composition (composition root). Partout ailleurs,
on dépend d'abstractions.

TODO (session 1)
---------------
1. `create_app()` : instancier `FastAPI(...)` avec les métadonnées de l'API
   (titre, version, description) issues de `docs/api/openapi.yml` ;
2. enregistrer les routeurs (`/health`, `/v1/orders`, `/v1/predictions`, `/v1/model`) ;
3. enregistrer les gestionnaires d'exceptions de `api/errors.py` ;
4. installer le middleware de logs structurés (voir `api/errors.py` ou createz
   `api/middleware.py`) : une ligne de log par requête, en JSON, avec la durée.

Ce que `create_app()` ne doit PAS contenir : de la logique métier, un accès direct à
une base de données, un `joblib.load` dans le handler. Le chargement du modèle se fait
une fois au démarrage, dans `bootstrap.py`.
"""

from __future__ import annotations

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Build the FastAPI application.

    TODO (session 1): implement. Signature and lifespan are already decided: the
    model is loaded once at startup and released at shutdown, so a request handler
    never pays for it.
    """
    raise NotImplementedError