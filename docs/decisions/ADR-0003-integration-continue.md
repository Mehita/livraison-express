# ADR-0003 : Intégration continue, outils de qualité et publication de l'image

- **Statut** : acceptée
- **Date** : 2026-10-29

## Contexte

Chaque modification doit être vérifiée automatiquement avant d'entrer dans `develop` ou
`main`. L'énoncé suggère `pytest` et `pylint`. Le projet utilise déjà `ruff` (configuré
dans `pyproject.toml`), et `CONTRIBUTING.md` demande de lancer `pytest` et `ruff check .`
avant chaque Pull Request.

Une règle simple : la CI doit lancer **les mêmes commandes** que celles d'un développeur,
sinon un code peut passer en local et échouer en CI, ou l'inverse.

## Décision

- Un workflow `CI` (`.github/workflows/ci.yml`) lance `ruff check .` puis `pytest` à chaque
  push sur `main` ou `develop` et à chaque Pull Request vers ces branches, sur Python 3.13,
  avec les dépendances de `requirements.txt` et `requirements-dev.txt` (cache `pip`).
- Le linter est **`ruff` seul** : `pylint` n'est pas ajouté.
- Un second workflow, `Release image`, construit l'image Docker et la publie sur
  GitHub Container Registry (`ghcr.io`) quand une release est publiée. Il utilise le
  `GITHUB_TOKEN` fourni par GitHub (aucun mot de passe stocké) et des droits minimaux
  (`packages: write` uniquement pour ce workflow). L'image est construite pour `linux/amd64`.

## Alternatives écartées

| Option | Pourquoi pas |
|---|---|
| `pylint` seul | second outil de configuration, plus lent, nombreuses remarques de style (docstrings, noms) sans valeur ici ; ne remplace pas le tri des imports |
| `ruff` + `pylint` | double emploi sur l'essentiel des règles, et deux sources de vérité à entretenir |
| `flake8` + `isort` + `black` | trois outils pour ce que `ruff` fait seul |

## Conséquences

- Une seule configuration de qualité (`pyproject.toml`), une exécution en moins d'une seconde.
- Pas de contrôle de conception de type `pylint` (complexité, duplication). Il pourra être
  ajouté plus tard, en étape non bloquante, si le besoin apparaît.
- Les règles `ruff` actives sont limitées à `E4, E7, E9, F, I` : toute extension se
  décide et se documente.
- La CI a déjà prouvé son utilité : elle a révélé que les tests importaient `PyYAML`, qui
  n'était installé qu'indirectement par `uvicorn[standard]`. La dépendance est maintenant
  déclarée dans `requirements-dev.txt`, car seuls les tests l'utilisent.
- La publication de l'image dépend d'une release : elle ne sera validée en conditions
  réelles qu'à la première release.
