# ADR — Architecture Decision Records

Une décision technique = **un fichier**. On écrit une ADR quand on choisit une brique dont le
choix n'est pas évident, et avant de l'intégrer (pas après, sinon c'est un justificatif).

## Format

```text
docs/decisions/
├── README.md
├── ADR-0000-example-model-artefacts.md   <- exemple fourni, fourni avec le modèle
├── ADR-0001-<slug>.md                   <- à vous
└── ADR-0002-<slug>.md
```

Nommage : `ADR-<numéro à 4 chiffres>-<slug en kebab-case>.md`, numérotation séquentielle.

## Gabarit

```markdown
# ADR-000X — <Titre de la décision, à l'infinitif ou au groupe nominal>

- Statut : Proposed | Accepted | Superseded by ADR-000Y
- Date : JJ/MM/AAAA
- Séance : N

## Contexte

Quel est le besoin ? Qu'est-ce qui le déclenche ? Quelles contraintes
(périmètre, données, compétences de l'équipe, budget, exploitation) ?

## Options considérées

| Option | Avantages | Inconvénients |
|---|---|---|
| A. ... | | |
| B. ... | | |
| C. ... | | |

## Décision

Nous retenons **A** parce que ...

## Conséquences

- Ce que cette décision simplifie
- Ce qu'elle complique ou rend impossible
- Ce qu'il faudra refaire le jour où ...
```

## Règles

1. Trois options minimum. « On a choisi Postgres » n'est pas une décision, c'est un résultat :
   on veut le raisonnement qui mène à Postgres, et les deux autres pistes écartées.
2. Une décision par fichier. Ne pas empiler cinq choix dans une seule ADR.
3. Une ADR superseded n'est jamais supprimée, on change son statut et on la remplace.
4. L'ADR est relue à la soutenance : un fichier écrit en Séance 1 et jamais mis à jour
   alors que l'implémentation a changé, ça se voit.

## Modèle de dépôt

La consigne de chaque séance indique les ADR attendues. Le fichier `ADR-0000-example-model-artefacts.md`
est un exemple complet : lisez-le pour le format et le niveau de détail attendus.