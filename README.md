# eligibilite-livraison-express

Application de prédiction d'éligibilité à la livraison express, construite à partir du
notebook `notebooks/project_test_v1_final_final2.ipynb`.

Vous ne partez pas d'une page blanche : le squelette applicatif est fourni. Votre travail
consiste à **implémenter** les classes abstraites, à **câbler** les couches entre elles et à
**choisir** les briques techniques dont l'application a besoin.

## Démarrage

```bash
uv venv .venv --python 3.13          # ou : python3.13 -m venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env                 # puis remplir les valeurs (voir ci-dessous)
uv pip install -e .
python -m livraison_express train    # produit artifacts/express_delivery_model.joblib
python -m livraison_express serve    # API sur http://localhost:8000/docs
```

Valeurs à renseigner dans `.env` (aucune n'a de défaut : l'application refuse de démarrer
si l'une manque ou est invalide) :

| Clé | Exemple | Rôle |
|---|---|---|
| `ENVIRONMENT` | `local` | `local`, `test` ou `prod` (en `test`, les commandes sont en mémoire) |
| `MODEL_PATH` | `artifacts/express_delivery_model.joblib` | où `train` écrit et où l'API lit le modèle |
| `MODEL_THRESHOLD` | `0.5` | seuil de décision, entre 0 et 1 (cellule 31) |
| `MODEL_VERSION` | `1.0.0` | version du modèle, renvoyée dans chaque prédiction |
| `ORDER_STORE_DSN` | `sqlite:///./data/orders.db` | où sont rangées les commandes (ADR-0001) |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING` ou `ERROR` |

Sans `.joblib`, l'API démarre quand même : `/health` répond 200, `/health/ready` et
`/v1/predictions` répondent 503 (ADR-0002).

## Lancement

```bash
python -m livraison_express serve    # API sur http://localhost:8000
python -m livraison_express train    # entraînement + sauvegarde du modèle
python -m livraison_express predict --file order.json
```

La documentation interactive de l'API est disponible sur <http://localhost:8000/docs>.

## Tests et qualité

```bash
pytest
ruff check .
```

## Règles du projet

1. **Le notebook est la référence.** Chaque fonction à implémenter indique dans sa docstring la
   cellule du notebook qui contient la logique. Collez-la, puis adaptez-la : c'est le cœur de
   la méthode « du prototype à la production ».
2. **Aucune dépendance entrante.** `domain`, `application` et `abstractions` n'importent jamais
   `infrastructure` ni `api`. C'est la règle de dépendance (Dependency Inversion, principe SOLID).
3. **Aucun choix technique n'est imposé.** Quand une abstraction doit être implémentée, vous
   choisissez la brique (PostgreSQL, Redis, Kafka, Prometheus...) et vous justifiez le choix
   dans `docs/decisions/ADR-000X-*.md`.
4. **Une responsabilité par classe.** Si une méthode dépasse l'écran ou fait deux choses,
   elle est probablement à couper.
5. **YAGNI.** N'implémentez pas ce qui n'est pas demandé par la consigne du jour.

## Arborescence

```text
src/livraison_express/
├── config.py               # settings lus depuis l'environnement
├── domain/                 # règles métier, types, aucune dépendance technique
├── application/            # cas d'usage : un fichier = une action métier
├── abstractions/           # besoins du domaine envers l'extérieur (interfaces abstraites)
├── infrastructure/         # implémentations concrètes des abstractions
│   └── dev/                # adaptateurs de développement, remplaçables
└── api/                    # livraison HTTP (FastAPI)
├── bootstrap.py            # racine de composition : assemble tout
└── cli.py                  # points d'entrée en ligne de commande
```

## Documentation

| Chemin | Ce qu'on y trouve |
|---|---|
| `docs/seance/` | **votre liste de travail du jour** : étapes, vérifications, ADR du jour, plan B |
| `docs/ROADMAP.md` | où vous en êtes, mode d'emploi, journal des décisions |
| `docs/api/openapi.yml` | le contrat de l'API : il ne change pas |
| `docs/decisions/` | le format des ADR, et vos décisions |

Vous y ajouterez vos propres documents au fil des séances, au fur et à mesure des besoins.

## Journal de bord

`docs/decisions/` contient le format des ADR (Architecture Decision Records) : un fichier par
décision technique structurée. Une décision = un fichier. C'est court, c'est daté, et c'est
ce qu'on vous demandera à l'oral de la soutenance. Le numéro de chaque décision est donné
dans votre liste de travail du jour.

## Décisions d'architecture

- [ADR-0001 : stockage des commandes](docs/decisions/ADR-0001-stockage-des-commandes.md)
- [ADR-0002 : stockage du modèle](docs/decisions/ADR-0002-stockage-du-modele.md)

## Pourquoi `api/routers/predictions.py` n'a-t-il pas le droit d'importer `joblib` ?

(À écrire : trois lignes, avec tes mots.)

## Qui a fait quoi

(À écrire.)

## Limites assumées

- Les prédictions ne sont pas conservées en séance 1 : l'historique arrive en séance 5.
- SQLite (ADR-0001) et le répertoire local pour le modèle (ADR-0002) sont des choix
  provisoires, valables pour une seule instance de l'API.
- Les variables `weather`, `delivery_zone` et `customer_type` sont obligatoires dans
  `schemas.py` (le squelette leur donnait une valeur par défaut) : le contrat OpenAPI dit
  qu'une variable absente doit produire un 422.
- Le `/docs` généré par FastAPI affiche encore son format d'erreur 422 par défaut, alors
  que les réponses réelles suivent le format `{error, message, details}` du contrat.
- Le jeu de données est synthétique (cellule 8) : les métriques ne disent rien des
  performances sur de vraies commandes.
