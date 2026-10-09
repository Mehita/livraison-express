"""Erreurs du domaine.

Séance 1 — TODO : compléter.

Deux questions à trancher dans ce cours :

1. Faut-il une hiérarchie d'exceptions par couche (`DomainError`, `ApplicationError`),
   ou une seule famille d'exceptions applicatives ?
   Une hiérarchie permet à la couche API de traduire chaque famille en un code HTTP
   différent : c'est ce que montre `api/errors.py`.
2. Quelle est la hiérarchie minimale qui reste utile (règle YAGNI) ?

Contrainte : la couche API ne doit jamais renvoyer une 500 pour une erreur métier.
Toute erreur attendue par le client doit exister ici et avoir un mapping HTTP déclaré.
"""


class DomainError(Exception):
    """Erreur de règle métier : la demande est invalide du point de vue du domaine."""


class ModelNotAvailableError(DomainError):
    """Le modèle n'est pas chargé, ou son artefact est illisible.

    Cas typique : l'API démarre avant que le fichier `.joblib` soit disponible.
    La sonde `/health/ready` doit pouvoir signaler ce cas sans lever d'exception.
    """


class InvalidOrderError(DomainError):
    """La commande reçue ne respecte pas le contrat de données attendu.

    Les variables manquantes ou hors domaine sont détectées par la cellule 14 du
    notebook (`validate_dataset`) : c'est le message d'erreur qui doit être remonté
    au client, pas une trace technique de scikit-learn.
    """


# TODO (session 1): add the errors you need (see docstring).
# DataQualityError and PredictionStoreError are used from session 4 and 5.