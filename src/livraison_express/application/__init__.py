"""Couche application : les cas d'usage de l'application.

Un cas d'usage = une action métier que quelqu'un peut déclencher
(prédire une commande, entraîner le modèle, collecter une commande).
Il orchestre le domaine et les abstractions, il n'implémente aucune brique technique.

Dépendances autorisées : `domain` et `abstractions`. Jamais `infrastructure`, jamais `api`.
"""
