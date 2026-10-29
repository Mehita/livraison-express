# Politique de sécurité

## Versions prises en charge

| Version | Corrections de sécurité |
|---|---|
| 1.0.x | oui |
| < 1.0 | non |

## Signaler une vulnérabilité

**N'ouvrez pas d'issue publique** pour une faille de sécurité.

Utilisez le signalement privé de GitHub : onglet **Security** du dépôt, puis
**Report a vulnerability**. Indiquez si possible :

- la version concernée et la manière de reproduire le problème ;
- l'impact que vous imaginez (fuite de données, déni de service, exécution de code...) ;
- une suggestion de correction, si vous en avez une.

## Ce que vous pouvez attendre

- un accusé de réception sous **7 jours** ;
- une première évaluation (faille confirmée ou non) sous **14 jours** ;
- une correction publiée dans une version de correctif (`hotfix`), puis une mention
  dans le journal des changements, sauf si vous préférez rester anonyme.

## Périmètre et bonnes pratiques du projet

- Aucun secret n'est stocké dans le dépôt : `.env` est exclu par `.gitignore`, et seul
  `.env.example` (sans valeur) est versionné.
- La configuration est lue depuis l'environnement et validée au démarrage : une valeur
  manquante ou invalide empêche l'application de démarrer.
- Les entrées de l'API sont validées par un contrat strict (`docs/api/openapi.yml`) :
  toute variable inconnue ou hors bornes est refusée avec un code 422.
- Le modèle (`.joblib`) est chargé depuis un chemin que vous contrôlez : ne chargez jamais
  un fichier de modèle venant d'une source que vous ne maîtrisez pas, car le format
  `joblib` (comme `pickle`) peut exécuter du code à la lecture.
