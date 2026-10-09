# ADR-0002 — Stocker le modèle entraîné et ses métadonnées

- Statut : Accepted
- Date : 09/10/2026
- Séance : 1

## Contexte

L'application doit pouvoir sauvegarder le modèle entraîné pour l'utiliser lors des prédictions, sans avoir à le re entraîner à chaque démarrage.
Il faut également conserver quelques informations sur le modèle, comme sa date d'entraînement, ses performances et sa version.
Pour la séance 1, la solution doit être simple à mettre en place et ne pas nécessiter d'infrastructure supplémentaire.

## Options considérées

| Option                              | Avantages                 | Inconvénients |
|---                                  |---                        |---            |
| A. Répertoire local `artifacts/`    | Simple à mettre en place, facile d'accès, aucune infrastructure supplémentaire| Permet de stocker les fichiers à distance et de les conserver durablement

| B. Stockage objet (type S3)         | Permet de stocker les fichiers à distance et de les conserver durablement| Nécessite une configuration et un service supplémentaire

| C. Registre de modèles (type MLflow)| Permet de suivre les versions des modèles, leurs performances et leurs paramètres| Demande une configuration supplémentaire et peut être trop complexe pour commencer 

| D. Git LFS / DVC                    | Permet de versionner les modèles ou de suivre les données et les artefacts du projet| Nécessite une configuration et une gestion supplémentaires 

## Décision

J'ai choisi le répertoire local artifacts/ pour la séance 1. Cette solution permet de sauvegarder le modèle entraîné et ses métadonnées sans ajouter de complexité au projet.
Cette décision est provisoire. 

## Conséquences

Le modèle peut être chargé au démarrage de l'application et réutilisé pour effectuer des prédictions sans être re entraîné à chaque fois.
Les fichiers doivent être conservés dans un emplacement stable et sauvegardés. Il faudra également vérifier qu'un modèle existe et qu'il est valide avant de lancer les prédictions.
Si le modèle est absent ou inutilisable, l'application devra signaler une erreur plutôt que de produire des prédictions incorrectes.
À terme, MLflow pourra être ajouté pour faciliter le suivi des expériences, des performances et des différentes versions du modèle.