from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from typing_extensions import Annotated

from middlewares import authenticate_user
from model.entities.password_item import PasswordItem
from model.repositories.vault_repo import VaultRepository
from model.exceptions import PassGuardAPIException
from utils import HttpStatusCodes, add_middleware_to_router

vault_router = APIRouter()
vault_repository = VaultRepository.get_instance()


# [GET] api/v1/vault
@vault_router.get(
    path='/',
    status_code=HttpStatusCodes.OK.value
)
def get_all_vault_items(_: Annotated[str, None, Header(alias="X-Auth-Token")] = None):
    return JSONResponse(
        status_code=HttpStatusCodes.OK.value,
        content=vault_repository.fetch_all_vault_items()
    )


# [GET] api/v1/vault/{item_id}
@vault_router.get(
    path='/{item_id}',
    responses={HttpStatusCodes.OK.value: {}, HttpStatusCodes.NOT_FOUND.value: {}}
)
def get_vault_item(item_id: str, _: Annotated[str, None, Header(alias="X-Auth-Token")] = None):
    requested_item = vault_repository.fetch_vault_item(item_id)
    if requested_item is not None:
        return JSONResponse(
            status_code=HttpStatusCodes.OK.value,
            content=requested_item
        )
    else:
        raise PassGuardAPIException(
            status_code=HttpStatusCodes.NOT_FOUND.value,
            error_message="Vault item was not found"
        )


# [POST] api/v1/vault/passwords
@vault_router.post(
    path='/passwords',
    response_model=PasswordItem,
    status_code=HttpStatusCodes.CREATED.value
)
def create_password_item(password_item: PasswordItem, _: Annotated[str, None, Header(alias="X-Auth-Token")] = None):
    return JSONResponse(
        status_code=HttpStatusCodes.CREATED.value,
        content=vault_repository.create_password(
            password_item.name,
            password_item.folder,
            password_item.url,
            password_item.email,
            password_item.password
        )
    )


# [PUT] api/v1/vault/{item_id}
@vault_router.put(
    path='/{item_id}',
    status_code=HttpStatusCodes.UPDATED.value
)
def update_vault_item(item_id: str, updated_item_data: dict, _: Annotated[str, None, Header(alias="X-Auth-Token")] = None):
    vault_repository.update_vault_item(item_id, updated_item_data)
    return JSONResponse(
        status_code=HttpStatusCodes.UPDATED.value,
        content={
            "id": item_id,
            **updated_item_data
        }
    )


# [DELETE] api/v1/vault/{item_id}
@vault_router.delete(
    path='/{item_id}'
)
def delete_password_item(item_id: str, _: Annotated[str, None, Header(alias="X-Auth-Token")] = None):
    requested_item = vault_repository.delete_vault_item(item_id)
    if requested_item is not None:
        return requested_item
    else:
        raise PassGuardAPIException(
            status_code=HttpStatusCodes.NOT_FOUND.value,
            error_message="Vault item was not found"
        )


add_middleware_to_router(vault_router, authenticate_user)
