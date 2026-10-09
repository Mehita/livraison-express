# Séance 1 — Du notebook à une application

> **Date** : ____/____ · **Équipe** : ____________________
> Durée : 7 h (2 h de cours, 5 h de TP) · ADR du jour : **ADR-0001**, **ADR-0002**
> Consigne complète remise en séance. Feuille de route : [`../ROADMAP.md`](../ROADMAP.md).

## Ce que vous devez savoir faire à la fin

Cinq résultats observables. Si vous les avez, la séance est réussie, quelle que soit la
beauté du code :

1. `POST /v1/predictions` renvoie une prédiction **conforme au contrat** `docs/api/openapi.yml`.
2. Le prédicteur vient du **notebook** (cellule 34), pas d'une réécriture au feeling.
3. `pytest` passe, sans `NotImplementedError` et sans test ignoré.
4. L'API démarre **même sans `.joblib`**, et le dit sur `/health/ready`.
5. Deux ADR écrits, avec au moins trois options comparées chacun.

## Avant de commencer

- [ ] Python 3.13 disponible (`python --version`), Docker **pas** nécessaire aujourd'hui.
- [ ] `README.md`, `docs/api/openapi.yml` et `src/livraison_express/abstractions/README.md` lus.
- [ ] `docs/ROADMAP.md` ouvert dans un onglet : c'est votre repère pour les 8 séances qui suivent.

## Étape 0 — Environnement (20 min)

- [ ] Environnement virtuel créé, dépendances runtime **et** dev installées.
- [ ] `.env` créé à partir de `.env.example`, et **jamais** commité (`git check-ignore .env`).
- [ ] Notebook exécuté de bout en bout.
- [ ] Les quatre artefacts sont présents : `express_delivery_model.joblib`, `features.json`,
      `metrics.json`, `batch_predictions.csv`.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
git check-ignore .env && echo "OK : .env est ignoré"

jupyter nbconvert --to notebook --execute --inplace notebooks/project_test_v1_final_final2.ipynb
ls notebooks/artifacts/
```

**À savoir** : la dernière cellule du notebook échoue (`input_dataframe is not defined`).
C'est normal, c'est un extrait d'illustration. **Les autres cellules doivent passer**, et
vos métriques doivent ressembler à `accuracy ≈ 0.75`, `f1 ≈ 0.83`, `roc_auc ≈ 0.85`. Si ce
n'est pas le cas, vérifiez `random_state=42` avant d'aller plus loin : tous les résultats
de la suite en dépendent.

## Étape 1 — Comprendre l'architecture (30 min)

- [ ] Réponse écrite (3 lignes) dans votre README à : *pourquoi
      `api/routers/predictions.py` n'a-t-il pas le droit d'importer `joblib` ?*
- [ ] Vous savez expliquer la règle de dépendance sans regarder : `domain` ne connaît ni
      `api`, ni `infrastructure`, ni `joblib`.

> Cette réponse vaut un point à la soutenance, et elle est lue avant votre code. Une
> phrase honnête (« parce que la dépendance irait dans le mauvais sens, et que le test du
> prédicteur chargerait alors le modèle ») suffit ; une phrase apprise par cœur ne suffit pas.

## Étape 2 — Configuration (25 min)

- [ ] `Settings` déclaré dans `config.py`, champs **sans valeur par défaut**.
- [ ] `get_settings()` implémenté et mis en cache (`lru_cache`).
- [ ] Le seuil de décision est justifié si vous ne prenez pas `0.5`.

```bash
python -c "from livraison_express.config import get_settings; print(get_settings())"
```

## Étape 3 — Domaine (1 h 15)

C'est le cœur de la séance. Ne passez pas vite : les séances 4, 5 et 6 reutilisent tout ce
qui est écrit ici.

- [ ] `TARGET_COLUMN`, `FEATURE_COLUMNS`, `NUMERIC_FEATURES`, `CATEGORICAL_FEATURES`
      déclarés **tels qu'ils sont en cellule 20**.
- [ ] `OrderFeatures` et `Prediction` déclarés, en dataclasses.
- [ ] `predict_eligibility()` : corps déplacé depuis la **cellule 34**.
- [ ] `datetime.now(timezone.utc)` et **pas** `datetime.utcnow()` (déprécié depuis 3.12).
- [ ] Les exceptions du domaine sont dans `domain/exceptions.py`, avec un nom justifié.

| Cellule 34 (notebook) | Votre application |
|---|---|
| `order_data: dict` | `OrderFeatures` |
| `FEATURE_COLUMNS` en dur | constante importée |
| `raise ValueError(...)` | erreur de `domain/exceptions.py` |
| retour `dict` | retour `Prediction` |

> **Piège le plus fréquent de la journée** : les listes de variables sont recopiées à
> trois endroits (notebook, API, modèle). Elles doivent exister **une seule fois**, dans
> `domain/entities.py`. Le test de non-régression du modèle de la séance 3 ne le pardonne
> pas.

## Étape 4 — Application (1 h)

- [ ] `PredictEligibility` orchestre et ne calcule pas.
- [ ] `CollectOrder` implémenté.
- [ ] `build_model(random_state=42)` est une **fonction pure** (cellules 20, 22, 24), et
      `test_build_model_returns_a_pipeline` passe.
- [ ] `TrainEligibilityModel.execute()` : entraîner, **évaluer, puis seulement sauvegarder**.
- [ ] Le CLI sort avec un **code non nul** en cas d'échec (indispensable en séance 5).

## Étape 5 — Infrastructure (45 min)

- [ ] Un `OrderStore` réel implémenté, un dossier par technique.
- [ ] Un `ModelRepository` réel implémenté.
- [ ] `load_if_available()` fonctionne : l'API démarre sans `.joblib`.
- [ ] Cellule 8 déplacée dans `synthetic_orders.py`, **en renvoyant des `OrderFeatures`**.

> Les adaptateurs de `infrastructure/dev/` vous sont fournis pour que l'application
> tourne tout de suite. Ce ne sont **pas** des solutions de production : données perdues
> au redémarrage, rien de partagé entre processus, recherche linéaire. C'est précisément
> ce que votre ADR-0001 doit expliquer.

## Étape 6 — API (1 h)

- [ ] `api/dependencies.py` : injection par `Depends`, aucun `if` de configuration en dur.
- [ ] `response_model=` prend toujours le schéma de `api/schemas.py`, **jamais** le type
      du domaine.
- [ ] `POST /v1/orders` répond **202**.
- [ ] `POST /v1/predictions` répond **503** si aucun modèle n'est chargé, via
      `ModelNotAvailableError`.
- [ ] `api/errors.py` mappe chaque erreur du domaine vers son code HTTP, au format
      `ErrorResponse`.
- [ ] Les paths de votre API sont **identiques** à ceux du contrat fourni (vérification
      ci-dessous).

```bash
curl -s localhost:8000/openapi.json > /tmp/vous.json
python -c "
import json, yaml
mine = json.load(open('/tmp/vous.json'))
ref = yaml.safe_load(open('docs/api/openapi.yml'))
print('paths identiques :', set(mine['paths']) == set(ref['paths']))
"
```

## Étape 7 — Tests (45 min)

- [ ] Les quatre fichiers de tests sont implémentés : aucun ne charge de modèle, aucune
      base n'est touchée.
- [ ] Les assertions viennent de la **cellule 39**.
- [ ] Aucun `skip`, aucun `xfail` : c'est une pénalité automatique en soutenance.
- [ ] `ruff check .` ne signale rien.

```bash
pytest
ruff check .
```

## Définition de terminé

Cochez **et vérifiez**. Une case cochée doit pouvoir être prouvée par la commande indiquée.

- [ ] `pytest` passe, sans `NotImplementedError` ni test ignoré → `pytest`
- [ ] `ruff check .` ne signale rien → `ruff check .`
- [ ] `GET /health` renvoie 200 → `curl -s -o /dev/null -w '%{http_code}\n' localhost:8000/health`
- [ ] `POST /v1/predictions` renvoie une prédiction conforme au contrat → `curl -X POST localhost:8000/v1/predictions -H 'Content-Type: application/json' -d @order.json`
- [ ] une commande invalide renvoie **422**, pas 500 → même commande avec `"hour": 25`
- [ ] `GET /v1/orders/{order_id}` renvoie **404** pour un identifiant inconnu → `curl -s -o /dev/null -w '%{http_code}\n' localhost:8000/v1/orders/CMD-999999`
- [ ] `python -m livraison_express train` produit un `.joblib` relançable
- [ ] l'API démarre **sans** `.joblib` et le signale sur `/health/ready` (503)
- [ ] `ADR-0001` et `ADR-0002` écrits, avec au moins 3 options comparées chacun
- [ ] aucune violation de la règle de dépendance :

```bash
grep -rn "infrastructure" src/livraison_express/{domain,application,abstractions,api} \
  && echo "VIOLATION" || echo "OK : aucune dépendance entrante"
```

> Cette dernière commande doit afficher `OK`. Si elle affiche `VIOLATION`, ce n'est pas
> grave : c'est exactement ce que la séance 1 cherche à faire apparaître.

## Les ADR du jour

Deux décisions, à écrire **avant** de coder : elles structurent votre implémentation.

| ADR | Sujet | Ce qu'il faut trancher |
|---|---|---|
| `ADR-0001-*.md` | Stockage des commandes | Quelle technologie ? Sur quels critères ? Que se passe-t-il si elle est indisponible au démarrage ? |
| `ADR-0002-*.md` | Stockage des artefacts de modèle | Quelle version provisoire, et **à quel moment** devient-elle caduc ? (l'exemple `ADR-0000` vous donne le format) |

Le format est dans `docs/decisions/README.md`, l'exemple complet dans
`docs/decisions/ADR-0000-example-model-artefacts.md`. Une ADR = un fichier, daté, en dix
lignes. Une décision = une ADR : n'en écrivez pas trois pour la même décision.

## Pièges qui coûtent le plus cher aujourd'hui

| Piège | Conséquence |
|---|---|
| Une modalité inconnue (`weather: "neige"`) renvoie 500 | Le modèle doit répondre **200** : `OneHotEncoder(handle_unknown="ignore")` (cellule 24) ignore la modalité. C'est la question 2 du jury. |
| `/health` dépend de la base de données | Une panne de la base déclenche des redémarrages de conteneurs en cascade. `/health` reste vert, toujours. |
| `/health/ready` renvoie 200 sans modèle | Le routeur envoie du trafic à un service qui ne peut pas prédire. |
| Les listes de variables dupliquées dans le modèle | La non-régression (séance 3) devient impossible à démontrer. |
| Le notebook rejoué sans `random_state=42` | Vos métriques ne correspondent plus, et la cellule 41 ne produit plus le même modèle. |

## Si le temps manque (plan B, moins de 2 h)

Priorité stricte : **étape 2 (config) → étape 3 (domaine) → `/v1/predictions` →
tests du prédicteur et de l'API**. Le reste est reporté.

Une API qui répond, avec un modèle chargé en mémoire et une suite de tests qui tourne,
vaut mieux qu'une architecture complète mais non fonctionnelle. Le jury le voit en deux
minutes ; un fichier non commité, non.

## Critères de la grille concernés aujourd'hui

Aujourd'hui, vous travaillez sur les points qui rapportent le plus au dépôt (15 points) :

| Critère de la grille | Où vous y touchez aujourd'hui |
|---|---|
| Reproductibilité de l'entraînement | étape 4, `train` relançable |
| Contrôle qualité des données | pas encore — c'est la séance 4 |
| Règle de dépendance | la commande `grep` de la définition de terminé |
| Tests | étape 7, aucun test ne charge de modèle |
| Justification des choix | les deux ADR du jour |
| Le projet démarre en une commande documentée | la section « Démarrage » de votre README |

## Avant de partir

- [ ] Un commit par étape, avec un message qui dit **pourquoi**.
- [ ] Votre README dit comment démarrer en 5 minutes, et qui a fait quoi.
- [ ] `docs/seance/seance-01.md` coché, avec la date en tête.
- [ ] La ligne « Séance 1 » est passée à ☒ dans [`../ROADMAP.md`](../ROADMAP.md).
- [ ] `ADR-0001` et `ADR-0002` sont présents dans `docs/decisions/`, avec le bon numéro dans
      leur nom de fichier.
- [ ] Le squelette de la séance 2 est appliqué quand il est distribué :
      `cp -r <supports>/docs/squelettes/seance-02/. .` puis
      `mkdir -p docs/seance && mv seance-02.md docs/seance/`