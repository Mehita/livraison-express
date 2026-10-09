"""Couche API : la livraison HTTP de l'application (FastAPI).

Cette couche traduit une requête HTTP en un appel de cas d'usage, et un résultat
(exception comprise) en une réponse HTTP conforme à `docs/api/openapi.yml`.
Elle ne contient aucune règle métier.

Dépendances autorisées : `application`, `domain`. Jamais `infrastructure`.
"""
