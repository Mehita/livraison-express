# ADR-0004 : Source des données, MongoDB (base analytique) plutôt que PostgreSQL

- **Statut** : acceptée (à compléter après examen des données)
- **Date** : 2026-10-29
- **Remplace partiellement** : [ADR-0001](ADR-0001-stockage-des-commandes.md) (SQLite, provisoire)

## Contexte

L'entraînement et la prédiction doivent s'appuyer sur les vraies commandes de l'entreprise,
et non plus sur des données synthétiques ou sur SQLite. Deux bases existent :

| | PostgreSQL | MongoDB |
|---|---|---|
| Rôle | base de **production** de l'ERP, partagée avec une autre application critique | base **analytique**, réservée aux services Data |
| Historique | depuis 2015 | depuis 2023 (l'avant n'a pas été copié) |
| Alimentation | écrite par l'ERP (échange bilatéral) | copie en temps réel depuis PostgreSQL par un ETL, à sens unique |
| Points d'attention | schéma modifié en 2017 et 2023, plus mis à jour depuis 2023, administrateur parti | maintenue par un alternant bientôt en fin de contrat, sans authentification en local |

Contraintes : ne jamais risquer la production, ne pas faire confiance à la qualité des données,
et sachant que notre application **écrit** des commandes (`OrderStore.save`).

## Décision

- La source des données est **MongoDB** (base `livraison_express`, collection `orders`), lue
  avec `pymongo`.
- Une seule implémentation est ajoutée : `MongoOrderStore`, adaptateur de l'abstraction
  `OrderStore` (l'`OrderRepository` du cours), avec `save`, `get` et `get_all`. Les adaptateurs
  SQLite et mémoire restent pour le développement et les tests.
- L'application **n'accède jamais** à la base de production PostgreSQL.
- Les données lues sont **validées** par l'application avant l'entraînement : une ligne
  invalide est rejetée et comptée, jamais corrigée en silence.

## Alternatives écartées

| Option | Pourquoi pas |
|---|---|
| PostgreSQL de production, en direct | une erreur de notre code toucherait l'ERP, et notre API y écrirait des commandes ; le cours déconseille l'intégration directe en production |
| Réplique PostgreSQL en lecture seule | solution idéale (historique complet depuis 2015), mais elle n'existe pas et demande une infrastructure que nous n'avons pas ; gardée comme évolution |
| Rester sur SQLite | ne contient pas les vraies commandes de l'entreprise |

## Conséquences

- Aucun risque pour la production, et des données fraîches grâce à l'ETL en temps réel.
- L'historique commence en 2023 : le volume doit être **vérifié** avant tout entraînement.
- La base n'impose pas de schéma : la validation côté application est indispensable.
- Dépendance à un ETL maintenu par un alternant qui part : risque de continuité, à signaler
  au responsable.
- Pas d'authentification en local : tout environnement de production devra en prévoir une.
- Les commandes collectées par l'API ne seront pas écrites dans `orders`, qui est alimentée par
  l'ETL : une collection dédiée sera utilisée (à confirmer après examen des données).

## À vérifier dans les données

- [ ] Nombre de documents disponibles dans `orders` (suffisant pour entraîner ?).
- [ ] Les champs et leurs types correspondent à `OrderFeatures`, et le libellé
      d'éligibilité express est présent.
- [ ] Valeurs manquantes, doublons, valeurs hors des bornes du domaine.
