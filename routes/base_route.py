from fastapi import APIRouter

from routes.auth_route import auth_router
from routes.vault_route import vault_router

base_router = APIRouter()
base_router.include_router(vault_router, prefix="/v1/vault", tags=["Vault"])
base_router.include_router(auth_router, prefix="/v1/auth", tags=["Authentication"])
