"""Interface en ligne de commande : le point d'entrée non HTTP.

Séance 1 — TODO : implémenter.

```bash
python -m livraison_express serve                      # démarre l'API
python -m livraison_express train                      # entraîne et sauvegarde le modèle
python -m livraison_express predict --file order.json  # prédiction en local, sans serveur
```

Pourquoi une CLI en plus de l'API ? Parce que toutes les opérations d'un projet ML ne
sont pas des requêtes HTTP : l'entraînement, l'évaluation et les jobs batch sont des
processus, pas des endpoints. Exposer un `POST /train` serait une erreur
d'architecture, pas une fonctionnalité.

TODO (session 1)
---------------
1. implémenter le parsing d'arguments avec `argparse` (sous-commandes) ;
2. `train` : appeler `TrainEligibilityModel.execute()` ;
3. `predict` : lire un fichier JSON, appeler `PredictEligibility.execute()`,
   afficher le résultat (JSON lisible par une machine ET lisible par un humain) ;
4. `serve` : appeler uvicorn sur l'objet d'application de `api/app.py` ;
5. chaque sous-commande doit rendre un code de sortie exploitable (0 succès, non 0 échec) :
   un job en CI qui renvoie 0 après un échec de l'entraînement est un piège silencieux.

TODO (sessions 5 et 6): ajouter `batch` (séance 5) et `consume` (séance 6), qui seront
des processus de longue durée, pas des requêtes.
"""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser.

    TODO (session 1): declare the subcommands `serve`, `train` and `predict`, with
    their options. Note that a CLI is a public contract too: name your arguments now
    and keep them stable.
    """
    raise NotImplementedError


def main() -> int:
    """Entry point of the CLI.

    TODO (session 1): dispatch to the right subcommand and return an exit code.
    `if __name__ == "__main__":` is handled by the `__main__.py` at the root of the
    package (already provided).
    """
    raise NotImplementedError