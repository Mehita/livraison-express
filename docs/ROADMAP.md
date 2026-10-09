# Feuille de route du projet

Ce fichier est votre **fil rouge**. Il sert à deux choses :

1. savoir **où vous en êtes** dans le projet ;
2. savoir **où trouver ce qu'il reste à faire aujourd'hui**.

Il ne contient volontairement **ni le contenu des séances à venir, ni la liste des
décisions techniques à prendre**. Vous y suivez ce que vous avez déjà fait, et ce que
vous devez faire est écrit dans la liste de travail du jour.

## Comment l'utiliser

| Quand | Quoi |
|---|---|
| Le matin de la séance | ouvrir `docs/seance/seance-0N.md` : c'est votre liste de travail |
| Pendant la séance | cocher au fil de l'eau, et **faire un commit** à chaque fin d'étape |
| En fin de séance | cocher ce qui est **vérifié**, pousser, puis passer la ligne de séance ici à ☒ |
| Quand vous ne savez plus quoi faire | rouvrir la dernière worklist suivie : elle contient les étapes, la commande qui prouve chaque étape, le plan B et ce qui ne peut pas être sacrifié |

Deux règles qui rendent ce fichier utile, et pas décoratif :

- **une case cochée vaut une démonstration qui marche.** « J'ai écrit le code » n'est pas
  « ça marche » ; « le test passe chez moi » n'est pas « le test passe » ;
- **ce qui n'est pas fait est écrit quelque part.** Une limite annoncée et justifiée dans
  le README ne coûte aucun point. Une case vide sans explication en coûte.

## Où j'en suis

| Séance | Liste de travail | Statut |
|---|---|---|
| 1 — Du notebook à une application | `docs/seance/seance-01.md` | ☐ |
| 2 — Exécuter partout | `docs/seance/seance-02.md` | *sera distribuée en séance* |
| 3 — Livrer en continu | `docs/seance/seance-03.md` | *sera distribuée en séance* |
| 4 — Fiabiliser les données et tracer l'entraînement | `docs/seance/seance-04.md` | *sera distribuée en séance* |
| 5 — Exécuter par lots | `docs/seance/seance-05.md` | *sera distribuée en séance* |
| 6 — Traiter les événements en temps réel | `docs/seance/seance-06.md` | *sera distribuée en séance* |
| 7 — Superviser et alerter | `docs/seance/seance-07.md` | *sera distribuée en séance* |
| 8 — Durcir avant la soutenance | `docs/seance/seance-08.md` | *sera distribuée en séance* |
| 9 — Soutenance | `docs/seance/seance-09.md` | *sera distribuée en séance* |

Légende : ☐ pas commencée · ☑ en cours · ☒ terminée.

Une liste de travail qui n'existe pas encore n'est pas un oubli : elle est remise avec la
séance correspondante. Le jour où vous en avez besoin, elle est là.

## Le parcours

Les séances sont **séquentielles**. Chaque séance suppose ce que vous avez fait avant,
et chaque liste de travail commence par « ce que vous devez savoir faire à la fin » : c'est
le seul document qui décrit votre journée.

Trois conséquences utiles :

- **ne cherchez pas à anticiper** en lutant les fichiers des autres séances : ce qu'on vous
  fera faire dépendra de ce que vous aurez terminé ;
- **si vous êtes en retard**, chaque liste de travail comporte une section « plan B » qui
  dit explicitement ce qui ne peut pas être sacrifié et ce qui peut attendre. Une séance
  peut déborder sur une journée, c'est prévu et ce n'est pas un échec ;
- **si une séance vous a échappé**, rouvrez sa liste de travail : elle est faite pour être
  lue trois jours plus tard, en diagonale. Reprenez par « ce que vous devez savoir faire à
  la fin », puis par la définition de terminé.

## Le journal des décisions

`docs/decisions/` contient vos **ADR** (*Architecture Decision Records*) : un fichier par
décision technique structurée, daté, court. Le format est dans
`docs/decisions/README.md`, et `docs/decisions/ADR-0000-example-model-artefacts.md` est un
exemple complet.

- une décision = un fichier. N'en écrivez pas trois pour la même décision ;
- le **numéro** de chaque décision vous est donné dans la liste de travail du jour ;
  ne renumérotez pas, ne sautez pas de numéro ;
- une ADR = dix lignes, pas dix pages : contexte, options, décision, pourquoi, conséquences,
  et ce qu'il faudrait surveiller.

Une décision écrite vaut des points même si ce n'est pas le choix que le jury aurait fait.
Une décision non écrite est invisible.

## Ce que le jury regardera

La grille complète est remise avec la consigne de la dernière séance. En résumé :
**15 points sur le dépôt**, évalué à l'aveugle avant la soutenance (le code ne doit porter ni
nom ni pseudonyme), et **5 points le jour J**.

Trois remarques :

- le README est lu **avant** le code : c'est lui qui décide si le démarrage sera réputé
  reproductible ;
- les ADR sont lus **avant** la démonstration ;
- une limite annoncée (« nous n'avons pas implémenté ceci, voici pourquoi ») est valorisée ;
  la même limite découverte pendant la démo ne l'est pas.

## Références

| Document | Ce qu'on y trouve |
|---|---|
| `docs/seance/seance-0N.md` | **votre liste de travail du jour** : étapes, vérifications, ADR du jour, plan B |
| `docs/api/openapi.yml` | le contrat de l'API : il ne change pas, votre implémentation s'y conforme |
| `docs/decisions/README.md` | comment écrire une ADR |
| `docs/decisions/ADR-0000-example-model-artefacts.md` | un exemple complet, à imiter |
| `notebooks/project_test_v1_final_final2.ipynb` | la référence : le code à porter vient de là |

Vos propres documents s'ajoutent au fur et à mesure, au fil des séances.