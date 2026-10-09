# `infrastructure/` — ici, vous choisissez

Ce dossier contient les **implémentations concrètes** des abstractions de
`abstractions/`. C'est le seul endroit du projet où l'on parle de PostgreSQL, de Redis,
de Kafka, de Prometheus ou d'un chemin sur un disque.

Le squelette fournit `dev/` : deux implémentations en mémoire, volatiles, pour faire
tourner l'application et les tests sans rien installer. Elles ne sont pas des solutions
de production et vous n'êtes pas obligés de les garder.

## Ce qui est fourni

| Fichier | Rôle |
|---|---|
| `dev/in_memory_order_store.py` | `OrderStore` en mémoire : un dictionnaire. |
| `dev/in_memory_model_repository.py` | `ModelRepository` qui charge le `.joblib` produit par le notebook. |
| `dev/synthetic_orders.py` | Générateur de commandes, à compléter depuis la cellule 8. |

## Marche à suivre pour implémenter une abstraction

Pour chaque abstraction que vous devez rendre concrète :

1. Créer un sous-dossier par technique : `infrastructure/postgres/`,
   `infrastructure/redis/`, `infrastructure/kafka/`. Une technique = un dossier.
2. Y écrire les classes qui implémentent l'ABC. **Une seule responsabilité par classe** :
   une classe qui ouvre la connexion, une classe qui exécute les requêtes.
3. Choisir ce qu'on expose. Une méthode `save` qui renvoie un `sqlite3.Error` fait fuiter
   la technologie dans l'application : convertissez en `domain/exceptions.py`.
4. Câbler dans `bootstrap.py`, et rien ailleurs.
5. Écrire l'ADR correspondant : au moins trois options comparées.
6. Tester deux choses, qui sont deux niveaux de test différents :
   - **le contrat** : ma classe respecte-t-elle l'ABC ? (test abstrait, réutilisable)
   - **le comportement** : mon adaptateur fait-il ce qu'on attend ? (test concret)

## Ce qu'on attend de vous à chaque séance

| Séance | Implémentations à produire |
|---|---|
| 1 | un `OrderStore` réel, un `ModelRepository` réel, une justification écrite |
| 4 | le suivi d'expériences derrière `ExperimentTracker` |
| 5 | la persistance des prédictions, l'ordonnanceur du batch |
| 6 | le producteur et le consommateur d'événements |
| 7 | les métriques, les alertes, la détection de dérive |
| 8 | vos propres choix, cette fois sans filet : redondance, reprise, cache |

## Deux règles qui restent valables toutes les séances

1. **Rien d'implémenté ici n'est importé par `domain`, `application`, `abstractions` ou
   `api`.** Si vous vous sentez obligé de le faire, c'est qu'une abstraction manque :
   ajoutez-la dans `abstractions/`.
2. **Une dépendance externe = une décision.** Si vous ajoutez une bibliothèque à
   `requirements.txt`, elle apparaît dans une ADR.