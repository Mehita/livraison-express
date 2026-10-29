# Contribuer à eligibilite-livraison-express

Merci de votre intérêt ! Ce document explique comment proposer une modification.

## Installation

```bash
git clone https://github.com/Mehita/livraison-express.git
cd livraison-express
uv venv .venv --python 3.13          # ou : python3.13 -m venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env                 # puis remplir les valeurs (voir le README)
uv pip install -e .
python -m livraison_express train    # produit le modèle utilisé par l'API
```

## Organisation des branches (GitFlow)

| Branche | Rôle | Part de | Fusionne dans |
|---|---|---|---|
| `main` | versions livrées, chaque commit est une version taguée | | |
| `develop` | intégration du travail en cours | `main` | |
| `feature/<sujet>` | un sujet, une branche | `develop` | `develop` |
| `release/<x.y.z>` | préparer une version | `develop` | `main` et `develop` |
| `hotfix/<x.y.z>` | corriger un bug urgent en production | `main` | `main` et `develop` |

**Personne ne pousse directement sur `main` ni sur `develop`** : tout passe par une
Pull Request.

## Proposer une modification

1. Partez de `develop` à jour : `git switch develop && git pull`.
2. Créez une branche : `git switch -c feature/<sujet>`.
3. Faites des commits petits, un par étape, avec un message qui dit **pourquoi**.
4. Vérifiez en local (voir ci-dessous).
5. Poussez : `git push -u origin feature/<sujet>`.
6. Ouvrez une Pull Request **vers `develop`**, en décrivant le problème résolu et la
   manière de le vérifier.
7. Attendez la revue et le passage de la CI, puis fusionnez.

## Conventions de commit

Format : `type(portée): résumé qui dit pourquoi`.

| Type | Usage |
|---|---|
| `feat` | nouvelle fonctionnalité |
| `fix` | correction de bug |
| `docs` | documentation uniquement |
| `test` | ajout ou correction de tests |
| `refactor` | changement interne sans effet visible |
| `chore` | outillage, dépendances, configuration |

Exemple : `fix(api): renvoyer 422 et non 500 quand une variable est hors bornes`.

## Avant d'ouvrir une Pull Request

```bash
pytest          # tous les tests doivent passer, sans test ignoré
ruff check .    # aucune alerte
```

La règle de dépendance est vérifiée par un test (`tests/test_architecture.py`) :
`domain`, `application`, `abstractions` et `api` n'importent jamais `infrastructure`,
et les routeurs n'importent pas `joblib`.

Une Pull Request est prête quand :

- [ ] les tests et `ruff` passent ;
- [ ] les nouveaux comportements ont un test ;
- [ ] un choix technique important est expliqué dans une ADR (`docs/decisions/`) ;
- [ ] le README est mis à jour si la manière de démarrer ou d'utiliser le projet change ;
- [ ] aucun secret n'est ajouté (`.env` n'est jamais versionné).

## Publier une version

1. `git switch -c release/<x.y.z> develop` : dernières corrections et numéro de version.
2. Fusion dans `main` par Pull Request, puis tag `v<x.y.z>` : la publication de la release
   déclenche la construction de l'image Docker.
3. Fusion de `main` dans `develop` pour que les corrections de la release ne soient pas
   perdues.

## Autres documents

- [Code de conduite](CODE_OF_CONDUCT.md)
- [Politique de sécurité](SECURITY.md) : ne signalez **jamais** une faille par une issue
  publique.
- [Licence MIT](LICENSE)
