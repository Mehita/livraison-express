# eligibilite-livraison-express

Application de prédiction d'éligibilité à la livraison express, construite à partir du
notebook `notebooks/project_test_v1_final_final2.ipynb`.

Vous ne partez pas d'une page blanche : le squelette applicatif est fourni. Votre travail
consiste à **implémenter** les classes abstraites, à **câbler** les couches entre elles et à
**choisir** les briques techniques dont l'application a besoin.

## Démarrage

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
pip install -e .
```

Puis, dans l'ordre :

1. Exécutez le notebook `notebooks/project_test_v1_final_final2.ipynb` de bout en bout.
   Il produit `notebooks/artifacts/express_delivery_model.joblib`, dont l'application a besoin.
2. Ouvrez `docs/seance/seance-01.md` : c'est votre liste de travail du jour.
3. Suivez la consigne (`seance-0N.md`), qui est remise en séance par l'enseignant.
4. `docs/ROADMAP.md` sert à vous repérer dans le projet, pas à anticiper les séances.

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