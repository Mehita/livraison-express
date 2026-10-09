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
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: Literal["local", "test", "prod"]
    model_path: str
    model_threshold: float = Field(gt=0, lt=1)
    order_store_dsn: str
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()