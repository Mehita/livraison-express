"""Tests de l'entraînement : la pipeline est pure, le cas d'usage évalue avant de ranger."""

from __future__ import annotations

from livraison_express.abstractions.model_repository import ModelRepository
from livraison_express.application.train_model import TrainEligibilityModel, build_model
from livraison_express.domain.entities import FEATURE_COLUMNS, ModelCard
from livraison_express.infrastructure.dev.synthetic_orders import generate_labeled_orders


class RecordingRepository(ModelRepository):
    """Faux dépôt : mémorise ce qu'on lui demande de ranger."""

    def __init__(self) -> None:
        self.saved: list[tuple[object, ModelCard]] = []

    def save(self, model: object, model_card: ModelCard) -> None:
        self.saved.append((model, model_card))

    def load(self, version: str) -> object:
        raise NotImplementedError


def _use_case(repository: RecordingRepository) -> TrainEligibilityModel:
    return TrainEligibilityModel(
        repository, lambda: generate_labeled_orders(800), model_version="9.9.9"
    )


def test_build_model_is_unfitted_and_deterministic() -> None:
    first, second = build_model(42), build_model(42)

    assert first is not second
    assert [name for name, _ in first.steps] == ["preprocessor", "classifier"]
    assert first.get_params()["classifier__random_state"] == 42
    assert not hasattr(first.named_steps["classifier"], "coef_")


def test_execute_saves_one_model_with_its_card() -> None:
    repository = RecordingRepository()

    card = _use_case(repository).execute()

    assert len(repository.saved) == 1
    saved_model, saved_card = repository.saved[0]
    assert saved_card is card
    assert card.model_version == "9.9.9"
    assert card.features == list(FEATURE_COLUMNS)
    assert set(card.metrics) == {"accuracy", "precision", "recall", "f1_score", "roc_auc"}
    assert hasattr(saved_model, "predict_proba")


def test_trained_model_learns_something() -> None:
    """The synthetic target is learnable: a model at chance level means a broken pipeline."""
    card = _use_case(RecordingRepository()).execute()

    assert card.metrics["roc_auc"] > 0.7


def test_same_seed_gives_the_same_metrics() -> None:
    assert _use_case(RecordingRepository()).execute().metrics == (
        _use_case(RecordingRepository()).execute().metrics
    )
