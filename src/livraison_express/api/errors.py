"""Traduction des exceptions en réponses HTTP, toutes au format `Error` du contrat.

| Exception                    | Code HTTP | `error`             |
|------------------------------|-----------|---------------------|
| `InvalidOrderError`          | 422       | `validation_error`  |
| validation Pydantic / FastAPI| 422       | `validation_error`  |
| `OrderNotFoundError`         | 404       | `order_not_found`   |
| `ModelNotAvailableError`     | 503       | `model_unavailable` |
| toute autre exception        | 500       | `internal_error`    |

Les codes `error` sont un contrat : un client branche son monitoring dessus. Les messages
sont libres. Une erreur métier n'est jamais une erreur serveur (500).
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ..domain.exceptions import InvalidOrderError, ModelNotAvailableError, OrderNotFoundError
from .schemas import ErrorResponse

logger = logging.getLogger(__name__)


def _error_response(
    status_code: int, code: str, message: str, details: list[str] | None = None
) -> JSONResponse:
    body = ErrorResponse(error=code, message=message, details=details or [])
    return JSONResponse(status_code=status_code, content=body.model_dump())


def register_exception_handlers(app: FastAPI) -> None:
    """Attach one handler per family of errors."""

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation(request: Request, exc: RequestValidationError):
        # FastAPI answers 422 with ITS body format: replace it by the contract's one.
        details = [
            f"{'.'.join(str(part) for part in error['loc'] if part != 'body')}: {error['msg']}"
            for error in exc.errors()
        ]
        return _error_response(422, "validation_error", "Commande invalide", details)

    @app.exception_handler(InvalidOrderError)
    async def handle_invalid_order(request: Request, exc: InvalidOrderError):
        return _error_response(422, "validation_error", str(exc))

    @app.exception_handler(OrderNotFoundError)
    async def handle_order_not_found(request: Request, exc: OrderNotFoundError):
        return _error_response(404, "order_not_found", str(exc))

    @app.exception_handler(ModelNotAvailableError)
    async def handle_model_unavailable(request: Request, exc: ModelNotAvailableError):
        return _error_response(503, "model_unavailable", str(exc))

    @app.exception_handler(Exception)
    async def handle_unexpected(request: Request, exc: Exception):
        logger.exception("Unhandled error on %s %s", request.method, request.url.path)
        return _error_response(500, "internal_error", "Erreur interne")
