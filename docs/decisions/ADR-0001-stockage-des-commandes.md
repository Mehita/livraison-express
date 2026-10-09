# ADR-0001 — Stocker les commandes collectées

- Statut : Accepted
- Date : 09/10/2026
- Séance : 1

## Contexte

L'application doit enregistrer les commandes pour pouvoir les consulter plusieurs fois et les utiliser pour prédire si une livraison peut être effectuée le jour même.
Les données doivent être conservées après un redémarrage. La méthode save ne doit pas créer de doublons lorsqu'une commande avec le même order_id est enregistrée plusieurs fois.
Pour la séance 1, la solution doit être simple à mettre en place et ne nécessiter aucune infrastructure supplémentaire.



## Options considérées

| Option         | Avantages       | Inconvénients |
|---             |---              |---            |
| A. En mémoire  | Simple et Rapide| Données perdues au redémarrage|
| B. SQLite      |Simple, intégré à Python, conserve les données dans un fichier | Moins adapté à des écritures simultanées|
| C. PostgreSQL  |Robuste et peut fonctionner sur accès simultané | Nécessite un serveur et une configuration|
| D. Redis       |Très rapide pour accéder aux données| Pas le meilleur choix pour stocker des commandes durablement|

## Décision

Je choisis SQLite pour la séance 1. C'est une solution simple qui permet de conserver les commandes sans installer de serveur.
Cette décision est provisoire en fonction de l'évolution des demandes du projet.

## Conséquences

SQLite permet de conserver les données après un redémarrage et de démarrer le projet rapidement.
Si la base de données est indisponible au démarrage, l'application doit signaler l'erreur et ne pas démarrer normalement sans pouvoir accéder aux données.
Si deux sauvegardes concernent le même order_id, une contrainte d'unicité empêchera la création de doublons. 
Si plusieurs instances de l'application doivent accéder aux mêmes données ou si les écritures deviennent trop nombreuses, nous pourrons envisager de passer à PostgreSQL.
