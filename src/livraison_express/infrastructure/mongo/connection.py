"""Ce que les adaptateurs MongoDB ont en commun : lire l'URI, traduire les pannes."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from pymongo import MongoClient
from pymongo.errors import ConfigurationError, PyMongoError

from ...domain.exceptions import OrderStoreUnavailableError


def database_name(dsn: str) -> str:
    """Read the database from `mongodb://host:port/database` (it is required)."""
    try:
        return MongoClient(dsn, connect=False).get_default_database().name
    except ConfigurationError as error:
        # Le message ne cite pas le DSN : il peut contenir un mot de passe.
        raise ValueError("L'URI MongoDB doit nommer la base : mongodb://hôte:port/base") from error


@contextmanager
def unavailable_as_domain_error() -> Iterator[None]:
    """Translate MongoDB's connection errors into the domain's vocabulary."""
    try:
        yield
    except PyMongoError as error:
        raise OrderStoreUnavailableError(f"MongoDB ne répond pas : {error}") from error
