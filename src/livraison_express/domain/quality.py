"""Résultat d'un contrôle qualité sur des données.

Séance 4 — ce fichier est introduit en Séance 4 (consigne de la séance 4), il n'est pas
nécessaire en Séance 1. Sa signature fait partie du squelette dès le début pour que la
structure cible reste visible.

Le notebook contient déjà l'implémentation de référence :

- cellule 14 : `validate_dataset(df)` lève la première erreur trouvée (un seul message) ;
- cellule 18 : `clean_orders_data(df)` nettoie silencieusement (doublons, NaN, bornage).

En production, un contrôle qualité doit être capable de **tout** dire, pas seulement la
première erreur : `DataQualityReport` agrège les violations pour être exploitable
dans une supervision (séance 7).
"""

from __future__ import annotations

from dataclasses import dataclass, field

# TODO (session 4): declare the types below.
#
# DataQualityReport: the result of a validation (valid: bool, violations: list[str],
#     checked_rows: int, ...) so a batch job can decide, log and alert.
# DataQualityRule: one check (name, predicate) — this is how you make validation
#     extensible without modifying the validator each time (Open/Closed).
# QualitySeverity: enum (warning vs blocking). A rule can warn without blocking,
#     others must block the pipeline: make the difference explicit.
#
# Reuse from the notebook: cell 14 lists the required columns and the valid ranges.
# Those rules are data, not code: they belong in the DataQualityRule objects.