# ADR-0001 — Stocker les commandes collectées

- Statut : Accepted
- Date : 09/10/2026
- Séance : 1

## Contexte

(À écrire : le besoin et les contraintes. Une commande est écrite une fois et lue
plusieurs fois, `save` doit être idempotent sur order_id, les données doivent survivre
à un redémarrage, aucune infrastructure à installer en séance 1.)

## Options considérées

| Option | Avantages | Inconvénients |
|---|---|---|
| A. En mémoire | | |
| B. SQLite | | |
| C. PostgreSQL | | |
| D. Redis | | |

## Décision

(À écrire : l'option retenue et pourquoi, en précisant qu'elle est provisoire.)

## Conséquences

(À écrire : ce que ça simplifie, ce que ça complique, ce qui se passe si la base est
indisponible au démarrage, comment on gère deux écritures simultanées sur le même
order_id, et quand passer à PostgreSQL.)
