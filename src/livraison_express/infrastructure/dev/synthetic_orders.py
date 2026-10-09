"""Générateur de commandes de développement (cellule 8 du notebook).

Le notebook synthétise 6 000 commandes avec une graine fixe : c'est ce qui le rend
exécutable sans source externe, et ce qui rend les tests reproductibles. La logique de
score (pénalités de zone et de météo, bonus premium, sigmoïde) est identique à celle de
la cellule 8, pour que les métriques restent comparables à celles du notebook.

Le `DataFrame` pandas reste un détail de génération : il ne sort pas de ce module.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ...domain.entities import FEATURE_COLUMNS, LabeledOrder, OrderFeatures

ZONE_PENALTY = {"centre": 0, "proche_banlieue": 0.10, "banlieue": 0.25, "rurale": 0.45}
WEATHER_PENALTY = {"normal": 0, "pluie": 0.10, "neige": 0.25, "orage": 0.30}


def _generate_frame(n_rows: int, random_state: int) -> pd.DataFrame:
    """Build the synthetic dataset exactly as notebook cell 8 does."""
    rng = np.random.default_rng(random_state)

    order_date = pd.date_range(start="2025-01-01", end="2025-12-31", periods=n_rows)

    hour = rng.integers(7, 23, size=n_rows)
    day_of_week = pd.Series(order_date).dt.dayofweek.to_numpy()
    weekend = (day_of_week >= 5).astype(int)

    data = pd.DataFrame(
        {
            "order_id": [f"CMD-{i:06d}" for i in range(1, n_rows + 1)],
            "order_date": order_date,
            "hour": hour,
            "day_of_week": day_of_week,
            "weekend": weekend,
            "distance_km": np.round(rng.gamma(shape=2.0, scale=4.0, size=n_rows), 2),
            "order_value_eur": np.round(rng.uniform(10, 250, size=n_rows), 2),
            "weight_kg": np.round(rng.uniform(0.2, 25, size=n_rows), 2),
            "stock_available": rng.binomial(1, 0.85, size=n_rows),
            "preparation_time_min": np.round(
                rng.normal(loc=25, scale=10, size=n_rows).clip(5, 90), 1
            ),
            "carrier_capacity": np.round(rng.uniform(0.2, 1.0, size=n_rows), 2),
            "weather": rng.choice(
                ["normal", "pluie", "neige", "orage"], size=n_rows, p=[0.65, 0.20, 0.10, 0.05]
            ),
            "delivery_zone": rng.choice(
                ["centre", "proche_banlieue", "banlieue", "rurale"],
                size=n_rows,
                p=[0.30, 0.30, 0.25, 0.15],
            ),
            "customer_type": rng.choice(["standard", "premium"], size=n_rows, p=[0.80, 0.20]),
        }
    )

    zone_penalty = data["delivery_zone"].map(ZONE_PENALTY)
    weather_penalty = data["weather"].map(WEATHER_PENALTY)
    customer_bonus = (data["customer_type"] == "premium").astype(int) * 0.15

    # Score latent simulant une décision métier
    score = (
        2.5
        - 0.18 * data["distance_km"]
        - 0.035 * data["preparation_time_min"]
        - 0.035 * data["weight_kg"]
        - zone_penalty
        - weather_penalty
        + 1.8 * data["stock_available"]
        + 1.3 * data["carrier_capacity"]
        + customer_bonus
        - 0.40 * data["weekend"]
        - 0.08 * np.maximum(data["hour"] - 18, 0)
    )
    probability = 1 / (1 + np.exp(-score))
    data["express_eligible"] = rng.binomial(1, probability)
    return data


def _to_labeled_orders(data: pd.DataFrame) -> list[LabeledOrder]:
    columns = ["order_id", *FEATURE_COLUMNS]
    return [
        LabeledOrder(
            order=OrderFeatures(**{name: row[name] for name in columns}),
            express_eligible=bool(row["express_eligible"]),
        )
        for row in data.to_dict("records")
    ]


def generate_labeled_orders(n_rows: int = 6000, random_state: int = 42) -> list[LabeledOrder]:
    """Generate orders with their known outcome (used to train the model)."""
    return _to_labeled_orders(_generate_frame(n_rows, random_state))


def generate_orders_dataset(n_rows: int = 6000, random_state: int = 42) -> list[OrderFeatures]:
    """Generate orders without the outcome (used to feed the API locally)."""
    return [labeled.order for labeled in generate_labeled_orders(n_rows, random_state)]
