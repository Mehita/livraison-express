"""Couche infrastructure : les implémentations concrètes des abstractions.

C'est ici que se trouvent les choix techniques : base de données, broker, registre de
modèles, système de métriques. Chaque module implémente une ou plusieurs abstractions de
`abstractions/` et n'est importé que par `bootstrap.py`.

Dépendances autorisées : tout, y compris les bibliothèques externes.
"""
