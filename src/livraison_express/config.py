"""Configuration de l'application, lue depuis l'environnement.

Séance 1 — TODO : compléter ce module.

Ce fichier implémente le principe « la configuration vient de l'environnement »
(12-factor) : aucun secret, aucune URL de base de données et aucun chemin de modèle
n'est écrit en dur dans le code. Les valeurs sont lues depuis l'environnement ou
depuis un fichier `.env` (voir `.env.example`).

Travail attendu
---------------
1. Compléter les champs de `Settings`. Aucune valeur par défaut n'est fournie :
   c'est à vous de décider, par exemple la valeur par défaut du seuil de décision
   (`MODEL_THRESHOLD`), et de le justifier si ce n'est pas 0.5 (cellule 31).
2. Implémenter `get_settings()` pour instancier `Settings`.
3. Vérifier que `get_settings()` est mis en cache (`lru_cache`) : l'objet doit être
   construit une seule fois par processus, pas à chaque requête.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration de l'application.

    Les noms de champs correspondent aux clés de `.env.example`. Avec
    `SettingsConfigDict(env_file=".env")`, pydantic lit les variables d'environnement
    en priorité sur le fichier `.env`.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # TODO (session 1): declare the settings below as typed fields, and choose
    # whether a default value is appropriate for each of them.
    #
    # environment: local | test | prod
    environment: str
    # Path to the .joblib file written by notebook cell 41.
    model_path: str
    # Decision threshold used to turn a probability into a yes/no (notebook cell 31).
    model_threshold: float
    # Connection string of the OrderStore implementation you choose.
    order_store_dsn: str
    # DEBUG | INFO | WARNING | ERROR
    log_level: str

    # TODO (session 1): declare the settings that *your* implementation needs.
    # A dataset URL? A broker address? A queue name? An API key?
    # They do not have to be the ones listed above.


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the application settings, built once per process.

    TODO (session 1): instanciate `Settings()`. The caching is already done by
    the decorator: do not remove it.
    """
    raise NotImplementedError(
        "Session 1: instantiate Settings() here. See config.py docstring."
    )