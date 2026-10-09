# ADR-0000 — Exemple : où stocker les artefacts du modèle

> Fichier d'exemple, fourni avec le squelette. Il sert de modèle de format et de niveau de
> détail. Il ne décrit pas une décision à prendre : la vôtre, pour le stockage des commandes,
> est attendue dès la Séance 1.

- Statut : Accepted
- Date : 01/01/2025
- Séance : 1

## Contexte

La cellule 41 du notebook écrit trois fichiers dans `notebooks/artifacts/` :

- `express_delivery_model.joblib` : la pipeline scikit-learn entraînée ;
- `metrics.json` : les métriques de la run d'évaluation ;
- `features.json` : la version du modèle, la cible et la liste des variables utilisées.

L'API doit pouvoir recharger ce modèle au démarrage (cellule 43) sans réentraîner à chaque
redéploiement. On a donc besoin d'un endroit où lire et écrire ces artefacts, partagé entre la
machine qui entraîne et celle qui sert les prédictions.

Contraintes : le modèle fait quelques Mo, il est écrit peu souvent et lu très souvent, il doit
pouvoir être identifié par une version, et le format doit rester un `.joblib` pour réutiliser
le code du notebook tel quel.

## Options considérées

| Option | Avantages | Inconvénients |
|---|---|---|
| A. Répertoire local `artifacts/` sur chaque machine | Aucun service à installer, réutilise directement le code de la cellule 41 | Chaque redéploiement doit repartir du modèle, pas de versionnage fiable, pas de partage entre entraîneurs |
| B. Système de fichiers réseau (NFS) partagé | Partage simple entre les deux machines | Pas de versionnage, accès concurrents pénibles, pas de métadonnées |
| C. Registre d'objets avec versionnage (type MLflow Model Registry ou équivalent) | Versionnage natif, métadonnées et métriques attachées, promotion possible entre environnements | Service supplémentaire à maintenir, une dépendance de plus au chargement |

## Décision

Nous retenons **A** pour les séances 1 et 2 : le répertoire local, parce qu'à ce stade
l'application est déployée sur une seule machine et qu'aucun besoin de partage n'est établi.
Cette décision est explicitement **provisoire** : le passage à C est l'objet de la Séance 3,
qui introduit la CI/CD et la traçabilité des versions de modèle.

## Conséquences

- La cellule 41 du notebook est réutilisable telle quelle, sans réécriture.
- Chaque version du modèle doit être identifiée explicitement (`MODEL_VERSION`, déjà défini
  dans la cellule 5) et écrite dans `features.json`.
- Le chargement doit être tolérant à l'absence de modèle au démarrage : l'API doit répondre
  `503` sur `/v1/predictions` tant que le modèle n'est pas chargé, et le signaler sur
  `/health/ready`. C'est le comportement attendu de la sonde de disponibilité.
- Le jour où le déploiement devient multi-machine, cette ADR devra être markée
  `Superseded by ADR-000X` et une nouvelle décision écrite.