"""Le contrôle qualité dit tout (pas seulement la première erreur) et distingue le grave."""

from __future__ import annotations

from typing import Any

from livraison_express.domain.entities import CATEGORICAL_FEATURES, NUMERIC_FEATURES
from livraison_express.domain.quality import (
    ALLOWED_CATEGORIES,
    NUMERIC_RANGES,
    DataQualityReport,
    QualitySeverity,
    row_rule,
    validate,
)


def _record(**overrides: Any) -> dict[str, Any]:
    record = {
        "order_id": "CMD-000001",
        "hour": 14,
        "day_of_week": 2,
        "weekend": 0,
        "distance_km": 3.5,
        "order_value_eur": 89.9,
        "weight_kg": 2.4,
        "stock_available": 1,
        "preparation_time_min": 18.0,
        "carrier_capacity": 0.85,
        "weather": "normal",
        "delivery_zone": "centre",
        "customer_type": "standard",
        "express_eligible": 1,
    }
    record.update(overrides)
    return record


def _dataset(*extra: dict[str, Any]) -> list[dict[str, Any]]:
    """Two clean rows with both outcomes, plus the rows under test."""
    return [
        _record(order_id="CMD-A", express_eligible=1),
        _record(order_id="CMD-B", express_eligible=0),
        *extra,
    ]


def _names(report: DataQualityReport) -> set[str]:
    return {violation.rule for violation in report.violations}


def test_clean_data_is_valid() -> None:
    report = validate(_dataset())

    assert report.valid
    assert report.violations == ()
    assert report.checked_rows == 2


def test_no_data_is_not_valid() -> None:
    report = validate([])

    assert not report.valid
    assert report.checked_rows == 0
    assert "Aucune donnée" in report.summary()


def test_a_missing_feature_warns_but_does_not_block() -> None:
    """The model imputes missing features (median / most frequent): worth a warning only."""
    report = validate(_dataset(_record(order_id="CMD-C", distance_km=None)))

    assert report.valid
    assert _names(report) == {"missing_feature_value"}
    assert report.warnings[0].severity is QualitySeverity.WARNING


def test_a_nan_counts_as_missing() -> None:
    report = validate(_dataset(_record(order_id="CMD-C", weight_kg=float("nan"))))

    assert _names(report) == {"missing_feature_value"}


def test_a_missing_label_blocks() -> None:
    report = validate(_dataset(_record(order_id="CMD-C", express_eligible=None)))

    assert not report.valid
    assert "missing_label" in _names(report)


def test_an_invalid_label_blocks() -> None:
    report = validate(_dataset(_record(order_id="CMD-C", express_eligible="oui")))

    assert not report.valid
    assert "invalid_label" in _names(report)


def test_an_out_of_range_value_blocks_and_points_at_the_row() -> None:
    report = validate(_dataset(_record(order_id="CMD-C", hour=25)))

    assert not report.valid
    violation = report.blocking[0]
    assert violation.rule == "hour_out_of_range"
    assert violation.count == 1
    assert violation.first_row == 2


def test_a_negative_or_non_numeric_value_is_out_of_range() -> None:
    negative = validate(_dataset(_record(order_id="CMD-C", distance_km=-1.0)))
    text = validate(_dataset(_record(order_id="CMD-C", distance_km="abc")))

    assert "distance_km_out_of_range" in _names(negative)
    assert "distance_km_out_of_range" in _names(text)


def test_an_unknown_category_blocks() -> None:
    report = validate(_dataset(_record(order_id="CMD-C", weather="grele")))

    assert not report.valid
    assert "weather_not_allowed" in _names(report)


def test_duplicate_order_ids_warn_but_do_not_block() -> None:
    report = validate(_dataset(_record(order_id="CMD-A", express_eligible=1)))

    assert report.valid
    assert _names(report) == {"duplicate_order_id"}
    assert report.violations[0].first_row == 2


def test_a_single_outcome_blocks_training() -> None:
    only_ones = [_record(order_id="CMD-A"), _record(order_id="CMD-B")]

    report = validate(only_ones)

    assert not report.valid
    assert "label_has_one_class_only" in _names(report)


def test_the_report_lists_every_violation_not_only_the_first() -> None:
    report = validate(_dataset(_record(order_id="CMD-C", hour=25, delivery_zone="mars")))

    assert {"hour_out_of_range", "delivery_zone_not_allowed"} <= _names(report)


def test_a_rule_is_data_so_a_new_one_needs_no_change_to_the_validator() -> None:
    too_expensive = row_rule(
        "order_too_expensive",
        QualitySeverity.WARNING,
        "commande de plus de 200 euros",
        lambda record: record["order_value_eur"] > 200,
    )

    report = validate([_record(order_value_eur=250.0)], rules=(too_expensive,))

    assert _names(report) == {"order_too_expensive"}
    assert report.valid


def test_the_summary_names_the_rules_that_failed() -> None:
    summary = validate(_dataset(_record(order_id="CMD-C", hour=25))).summary()

    assert "BLOQUANT" in summary
    assert "hour_out_of_range" in summary


def test_every_model_variable_has_its_quality_rule() -> None:
    """Adding a variable to entities.py without a quality rule must fail here."""
    assert set(NUMERIC_RANGES) == set(NUMERIC_FEATURES)
    assert set(ALLOWED_CATEGORIES) == set(CATEGORICAL_FEATURES)
