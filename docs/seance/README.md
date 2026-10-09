# Consignes de séance

Ce dossier contient **un fichier par séance** : `seance-01.md`, `seance-02.md`, etc.

L'enseignant ajoute le fichier correspondant **après chaque séance**. Un fichier absent
signifie donc une chose très simple : *cette séance n'a pas encore eu lieu*. Ce n'est pas
une erreur, et ce n'est pas un oubli de votre part.

## À quoi sert un fichier de séance

La consigne remise en séance (`seance-0N.md`) est le cours du jour : elle explique, elle
pose des questions, elle demande de comparer des options. Ce fichier est l'autre moitié :
une **liste de travail**. Il contient

- les étapes, dans l'ordre, avec leur durée ;
- ce qu'il faut faire à chaque étape, en 2 à 4 points ;
- la **commande qui prouve** que l'étape est terminée ;
- la définition de terminé de la journée, en cases à cocher ;
- les ADR du jour ;
- les pièges qui coûtent le plus cher, en séance ;
- le plan B si le temps manque.

## Mode d'emploi

1. Ouvrez le fichier du jour au début de la séance, gardez-le ouvert.
2. Cochez au fil de l'eau, et **faites un commit** à chaque fin d'étape. Une case cochée non
   commitée est une case que vous oublierez de cocher.
3. En fin de journée, ne cochez que ce que vous pouvez **montrer**. Une case cochée
   sans preuve est pire qu'une case vide : elle vous donne une fausse confiance jusqu'à la
   soutenance.
4. Remplacez la date et votre équipe en tête du fichier, puis poussez.

## Règle d'or

> Une case cochée vaut une démonstration qui marche.
> « J'ai écrit le code » n'est pas « ça marche ».
> « Le test passe chez moi » n'est pas « le test passe ».

Si vous n'avez pas pu faire une étape, ne la cochez pas, mais **écrivez pourquoi** dans le
README du projet, dans la section « ce qui n'est pas prêt ». Une limite annoncée et
justifiée ne coûte aucun point ; une case vide sans explication en coûte.

## Vue d'ensemble

Ce dossier ne contient que des séances qui **ont eu lieu**. Le titre d'une séance est
annoncé dans [`../ROADMAP.md`](../ROADMAP.md) ; son contenu n'apparaît qu'ici, le jour
venue.

| Séance | Fichier | Statut |
|---|---|---|
| 1 — Du notebook à une application | `seance-01.md` | ☑ |
| 2 — Exécuter partout | `seance-02.md` | *à venir* |
| 3 — Livrer en continu | `seance-03.md` | *à venir* |
| 4 — Fiabiliser les données et tracer l'entraînement | `seance-04.md` | *à venir* |
| 5 — Exécuter par lots | `seance-05.md` | *à venir* |
| 6 — Traiter les événements en temps réel | `seance-06.md` | *à venir* |
| 7 — Superviser et alerter | `seance-07.md` | *à venir* |
| 8 — Durcir avant la soutenance | `seance-08.md` | *à venir* |
| 9 — Soutenance | `seance-09.md` | *à venir* |

Légende : ☑ la liste est dans ce dossier · *à venir* elle sera remise en séance.

Une ligne marquée *à venir* ne vous empêche pas d'avancer : elle vous empêche de deviner.
Ce que vous devez faire aujourd'hui est écrit dans le fichier du jour, et nulle part
ailleurs.