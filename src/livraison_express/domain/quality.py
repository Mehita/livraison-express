"""Contrôle qualité des données d'entraînement (séance 4).

Le notebook contient l'implémentation de référence : la cellule 14 (`validate_dataset`)
lève la première erreur trouvée, la cellule 18 (`clean_orders_data`) nettoie en silence.
En production, un contrôle doit pouvoir **tout** dire : `DataQualityReport` agrège toutes
les violations, pour que le job d'entraînement décide, journalise et alerte.

Trois idées structurent ce module :

- une règle est une **donnée** (`DataQualityRule` : nom, gravité, test) : ajouter une
  règle ne modifie pas `validate` (ouvert/fermé) ;
- la gravité est explicite (`QualitySeverity`) : un avertissement journalise, une
  violation bloquante arrête l'entraînement ;
- le module est du domaine pur : il travaille sur des dictionnaires, sans pandas ni
  MongoDB. C'est l'infrastructure qui lui apporte les données.

Les bornes ci-dessous reprennent celles du contrat d'API (`api/schemas.py`). Elles sont
écrites ici une seconde fois, volontairement : le domaine n'a pas le droit d'importer
la couche API.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any

from .entities import FEATURE_COLUMNS, TARGET_COLUMN

Record = Mapping[str, Any]

# Bornes (min, max) des variables numériques. `None` : pas de borne haute.
NUMERIC_RANGES: dict[str, tuple[float, float | None]] = {
    "hour": (0, 23),
    "day_of_week": (0, 6),
    "weekend": (0, 1),
    "distance_km": (0, None),
    "order_value_eur": (0, None),
    "weight_kg": (0, None),
    "stock_available": (0, 1),
    "preparation_time_min": (0, None),
    "carrier_capacity": (0, 1),
}

# Valeurs autorisées des variables catégorielles (celles du notebook, cellule 8).
ALLOWED_CATEGORIES: dict[str, tuple[str, ...]] = {
    "weather": ("normal", "pluie", "neige", "orage"),
    "delivery_zone": ("centre", "proche_banlieue", "banlieue", "rurale"),
    "customer_type": ("standard", "premium"),
}

_VALID_LABELS = (0, 1, True, False)


class QualitySeverity(Enum):
    """Gravité d'une règle : un avertissement journalise, une violation bloque."""

    WARNING = "warning"
    BLOCKING = "blocking"


@dataclass(frozen=True)
class DataQualityRule:
    """Une vérification. `offending_rows` renvoie les positions des lignes fautives."""

    name: str
    severity: QualitySeverity
    description: str
    offending_rows: Callable[[Sequence[Record]], Sequence[int]]


@dataclass(frozen=True)
class QualityViolation:
    """Une règle non respectée : combien de lignes, et où se trouve la première."""

    rule: str
    severity: QualitySeverity
    description: str
    count: int
    first_row: int


@dataclass(frozen=True)
class DataQualityReport:
    """Résultat d'un contrôle : toutes les violations, pas seulement la première."""

    checked_rows: int
    violations: tuple[QualityViolation, ...] = ()

    @property
    def blocking(self) -> tuple[QualityViolation, ...]:
        return tuple(v for v in self.violations if v.severity is QualitySeverity.BLOCKING)

    @property
    def warnings(self) -> tuple[QualityViolation, ...]:
        return tuple(v for v in self.violations if v.severity is QualitySeverity.WARNING)

    @property
    def valid(self) -> bool:
        """True si l'on peut entraîner : des données, et aucune violation bloquante."""
        return self.checked_rows > 0 and not self.blocking

    def summary(self) -> str:
        """Résumé lisible, fait pour les journaux."""
        if self.checked_rows == 0:
            return "Aucune donnée à contrôler"
        lines = [
            f"{self.checked_rows} lignes contrôlées : "
            f"{len(self.blocking)} violation(s) bloquante(s), {len(self.warnings)} alerte(s)"
        ]
        for violation in self.violations:
            label = "BLOQUANT" if violation.severity is QualitySeverity.BLOCKING else "ALERTE"
            lines.append(
                f"  [{label}] {violation.rule} : {violation.description} "
                f"({violation.count} ligne(s), première : {violation.first_row})"
            )
        return "\n".join(lines)


def _is_missing(value: Any) -> bool:
    return value is None or (isinstance(value, float) and math.isnan(value))


def row_rule(
    name: str,
    severity: QualitySeverity,
    description: str,
    is_violated_by: Callable[[Record], bool],
) -> DataQualityRule:
    """Build a rule from a test applied to each row on its own."""

    def offending_rows(records: Sequence[Record]) -> list[int]:
        return [index for index, record in enumerate(records) if is_violated_by(record)]

    return DataQualityRule(name, severity, description, offending_rows)


def _out_of_range(column: str, low: float, high: float | None) -> Callable[[Record], bool]:
    def is_violated(record: Record) -> bool:
        value = record.get(column)
        if _is_missing(value):
            return False  # une valeur absente n'est pas une valeur hors bornes
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            return True
        return value < low or (high is not None and value > high)

    return is_violated


def _not_allowed(column: str, allowed: tuple[str, ...]) -> Callable[[Record], bool]:
    def is_violated(record: Record) -> bool:
        value = record.get(column)
        return not _is_missing(value) and value not in allowed

    return is_violated


def _duplicate_order_ids(records: Sequence[Record]) -> list[int]:
    seen: set[Any] = set()
    duplicates: list[int] = []
    for index, record in enumerate(records):
        order_id = record.get("order_id")
        if _is_missing(order_id):
            continue
        if order_id in seen:
            duplicates.append(index)
        else:
            seen.add(order_id)
    return duplicates


def _label_has_one_class_only(records: Sequence[Record]) -> Sequence[int]:
    """Training (stratified split, ROC AUC) needs both outcomes in the data."""
    labels = {
        bool(record[TARGET_COLUMN])
        for record in records
        if not _is_missing(record.get(TARGET_COLUMN)) and record[TARGET_COLUMN] in _VALID_LABELS
    }
    return range(len(records)) if records and len(labels) < 2 else []


def _default_rules() -> tuple[DataQualityRule, ...]:
    blocking, warning = QualitySeverity.BLOCKING, QualitySeverity.WARNING
    rules = [
        row_rule(
            "missing_feature_value",
            warning,
            "variable absente (le modèle l'impute : médiane ou valeur la plus fréquente)",
            lambda record: any(_is_missing(record.get(column)) for column in FEATURE_COLUMNS),
        ),
        row_rule(
            "missing_label",
            blocking,
            "résultat réel (express_eligible) absent : impossible d'apprendre dessus",
            lambda record: _is_missing(record.get(TARGET_COLUMN)),
        ),
        row_rule(
            "invalid_label",
            blocking,
            "résultat réel différent de 0/1",
            lambda record: not _is_missing(record.get(TARGET_COLUMN))
            and record[TARGET_COLUMN] not in _VALID_LABELS,
        ),
    ]
    rules += [
        row_rule(
            f"{column}_out_of_range",
            blocking,
            f"{column} hors bornes ou non numérique (attendu : {low} à {high or 'sans limite'})",
            _out_of_range(column, low, high),
        )
        for column, (low, high) in NUMERIC_RANGES.items()
    ]
    rules += [
        row_rule(
            f"{column}_not_allowed",
            blocking,
            f"{column} hors des valeurs autorisées {list(allowed)}",
            _not_allowed(column, allowed),
        )
        for column, allowed in ALLOWED_CATEGORIES.items()
    ]
    rules += [
        DataQualityRule(
            "duplicate_order_id",
            warning,
            "identifiant de commande en double (les doublons faussent l'évaluation)",
            _duplicate_order_ids,
        ),
        DataQualityRule(
            "label_has_one_class_only",
            blocking,
            "un seul résultat présent dans les données : l'entraînement est impossible",
            _label_has_one_class_only,
        ),
    ]
    return tuple(rules)


DEFAULT_RULES: tuple[DataQualityRule, ...] = _default_rules()


def validate(
    records: Sequence[Record], rules: Sequence[DataQualityRule] = DEFAULT_RULES
) -> DataQualityReport:
    """Run every rule over the records and report all violations (never stops at the first)."""
    violations = []
    for rule in rules:
        rows = rule.offending_rows(records)
        if rows:
            violations.append(
                QualityViolation(rule.name, rule.severity, rule.description, len(rows), rows[0])
            )
    return DataQualityReport(checked_rows=len(records), violations=tuple(violations))
