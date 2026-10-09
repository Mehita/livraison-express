"""Tests de la CLI : codes de sortie exploitables, sans serveur."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import pytest

from livraison_express.bootstrap import Container, build_container
from livraison_express.cli import EXIT_FAILURE, EXIT_OK, EXIT_USAGE, build_parser, main
from livraison_express.config import Settings
from livraison_express.domain.entities import OrderFeatures


def _container(tmp_path: Path) -> Container:
    return build_container(
        Settings(
            environment="test",
            model_path=str(tmp_path / "model.joblib"),
            model_threshold=0.5,
            model_version="1.0.0",
            order_store_dsn=f"sqlite:///{tmp_path / 'orders.db'}",
            log_level="INFO",
        )
    )


def _write_order(tmp_path: Path, order: OrderFeatures) -> Path:
    path = tmp_path / "order.json"
    path.write_text(json.dumps(asdict(order)), encoding="utf-8")
    return path


def test_parser_requires_a_subcommand() -> None:
    with pytest.raises(SystemExit):
        build_parser().parse_args([])


def test_train_then_predict_succeed(
    tmp_path: Path, sample_order: OrderFeatures, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["train"], _container(tmp_path)) == EXIT_OK

    order_file = _write_order(tmp_path, sample_order)
    assert main(["predict", "--file", str(order_file)], _container(tmp_path)) == EXIT_OK

    assert '"express_eligible"' in capsys.readouterr().out


def test_predict_without_model_fails_with_a_non_zero_code(
    tmp_path: Path, sample_order: OrderFeatures
) -> None:
    order_file = _write_order(tmp_path, sample_order)

    assert main(["predict", "--file", str(order_file)], _container(tmp_path)) == EXIT_FAILURE


def test_predict_with_unreadable_file_is_a_usage_error(tmp_path: Path) -> None:
    missing = tmp_path / "absent.json"

    assert main(["predict", "--file", str(missing)], _container(tmp_path)) == EXIT_USAGE
