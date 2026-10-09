"""Couche abstractions : les besoins du domaine envers l'extérieur.

Une abstraction décrit *ce que* l'application attend d'une brique externe
(stocker une commande, conserver un modèle, publier un événement, mesurer une latence),
jamais *comment* cette brique fonctionne. Les implémentations concrètes vivent dans
`infrastructure`.

Dépendances autorisées : la bibliothèque standard uniquement.
"""
