from enum import Enum
from fastapi import Depends, APIRouter


class VaultItemType(Enum):
    PASSWORD = "password"
    NOTE = "note"
    PAYMENT_METHOD = "payment_method"


class HttpStatusCodes(Enum):
    OK = 200
    CREATED = 201
    UPDATED = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    SERVER_ERROR = 500


def add_middleware_to_router(router: APIRouter, middleware_function):
    for route in router.routes:
        route.dependencies.append(Depends(middleware_function))


def encode_jwt(payload, encryption_key):
    pass
