# `abstractions/` — les besoins du domaine envers l'extérieur

Ce dossier ne contient **aucune technologie**, seulement des classes abstraites (ABC) qui
décrivent ce que l'application attend d'une brique externe.

## Règle de dépendance

```text
        api  →  application  →  abstractions  ←  infrastructure
                            ↘        domain  ↗
```

- `domain`, `application` et `abstractions` **n'importent jamais** `infrastructure`.
- `infrastructure` **implémente** les abstractions de ce dossier.
- Seuls `bootstrap.py` (la racine de composition) et les tests importent `infrastructure`.

C'est le principe d'inversion de dépendance (le « D » de SOLID). Concrètement : votre
`PredictEligibility` reçoit un `ModelRepository`, pas un `joblib`. Il ne sait pas que le
modèle vient d'un fichier, il sait qu'il peut demander un modèle.

Conséquence pratique : pour changer de base de données, on écrit **un** nouveau
implémentant dans `infrastructure/` et on change **une** ligne dans `bootstrap.py`.
Aucun code métier n'est touché.

## Ajouter une abstraction

Quand un cas d'usage a besoin d'une nouvelle brique (un broker en séance 6, un système de
métriques en séance 7) :

1. Déclarez l'ABC ici, avec les signatures et les erreurs attendues documentées.
2. N'écrivez pas l'implémentation ici : elle va dans `infrastructure/`.
3. Documentez le besoin dans le cas d'usage, et le choix dans un ADR.

## Les abstractions livrées avec le squelette

| Fichier | Séance | Besoin exprimé |
|---|---|---|
| `order_store.py` | 1 | Conserver les commandes collectées |
| `model_repository.py` | 1 | Conserver et recharger le modèle entraîné |

Les suivantes sont livrées par le squelette de leur séance (voir `docs/squelettes/`) :
`quality.py` et `experiment_tracker.py` (séance 4), `prediction_store.py` et
`batch_scheduler.py` (séance 5), `event_stream.py` (séance 6), `metrics.py`,
`alert_sink.py` et `drift_detector.py` (séance 7).