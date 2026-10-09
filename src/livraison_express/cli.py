"""Interface en ligne de commande : le point d'entrée non HTTP.

```bash
python -m livraison_express serve                      # démarre l'API
python -m livraison_express train                      # entraîne et sauvegarde le modèle
python -m livraison_express predict --file order.json  # prédiction locale, sans serveur
```

Toutes les opérations d'un projet ML ne sont pas des requêtes HTTP : l'entraînement est un
processus, pas un endpoint. Chaque sous-commande rend un code de sortie exploitable
(0 succès, non 0 échec) : un job de CI qui renvoie 0 après un échec d'entraînement est un
piège silencieux.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from .bootstrap import Container, build_container
from .domain.entities import OrderFeatures
from .domain.exceptions import DomainError

EXIT_OK = 0
EXIT_FAILURE = 1
EXIT_USAGE = 2


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser. Argument names are a public contract."""
    parser = argparse.ArgumentParser(prog="livraison_express")
    commands = parser.add_subparsers(dest="command", required=True)

    serve = commands.add_parser("serve", help="Démarre l'API HTTP")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)

    commands.add_parser("train", help="Entraîne le modèle et le sauvegarde")

    predict = commands.add_parser("predict", help="Prédit l'éligibilité d'une commande")
    predict.add_argument("--file", required=True, type=Path, help="Commande au format JSON")
    return parser


def _train(container: Container) -> int:
    card = container.train_model.execute()
    print(json.dumps({"model_version": card.model_version, "metrics": card.metrics}, indent=2))
    return EXIT_OK


def _predict(container: Container, path: Path) -> int:
    try:
        order = OrderFeatures(**json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError, TypeError) as error:
        print(f"Commande illisible ({path}) : {error}", file=sys.stderr)
        return EXIT_USAGE
    container.load_model()
    prediction = container.predict_eligibility().execute(order)
    print(
        json.dumps(
            {**asdict(prediction), "predicted_at": prediction.predicted_at.isoformat()}, indent=2
        )
    )
    return EXIT_OK


def _serve(host: str, port: int) -> int:
    import uvicorn  # imported here: `train` and `predict` do not need a web server

    uvicorn.run("livraison_express.api.app:create_app", factory=True, host=host, port=port)
    return EXIT_OK


def main(argv: list[str] | None = None, container: Container | None = None) -> int:
    """Run one subcommand and return its exit code.

    `container` can be injected (tests); by default it is built from the environment.
    """
    args = build_parser().parse_args(argv)
    if args.command == "serve":
        return _serve(args.host, args.port)
    container = container or build_container()
    try:
        if args.command == "train":
            return _train(container)
        return _predict(container, args.file)
    except DomainError as error:
        print(f"Erreur : {error}", file=sys.stderr)
        return EXIT_FAILURE
