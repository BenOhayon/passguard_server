from fastapi import APIRouter
from fastapi.responses import JSONResponse

from model.repositories.users_repo import UserRepository
from model.entities.login_input import LoginInput
from model.entities.user import User
from model.exceptions import PassGuardAPIException
from utils import HttpStatusCodes

auth_router = APIRouter()
user_repository = UserRepository.get_instance()


# [POST] api/v1/auth/login
@auth_router.post(
    path='/login',
    tags=["Authentication"]
)
def login(login_input: LoginInput):
    result = user_repository.login(login_input.username, login_input.password)
    if not isinstance(result, str):
        return JSONResponse(status_code=HttpStatusCodes.OK.value, content=result)
    else:
        raise PassGuardAPIException(status_code=HttpStatusCodes.NOT_FOUND.value, error_message=result)


# [POST] api/v1/auth/register
@auth_router.post(
    path='/register',
    tags=["Authentication"]
)
def register(new_user: User):
    result = user_repository.register(new_user.username, new_user.password, email=new_user.email)
    if not isinstance(result, str):
        return JSONResponse(status_code=HttpStatusCodes.CREATED.value, content=result)
    else:
        raise PassGuardAPIException(status_code=HttpStatusCodes.BAD_REQUEST.value, error_message=result)
