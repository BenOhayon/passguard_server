import os
import jwt
from dotenv import load_dotenv
from fastapi import Request
from model.exceptions import PassGuardAPIException
from model.repositories.users_repo import UserRepository
from utils import HttpStatusCodes

load_dotenv()
user_repository = UserRepository.get_instance()


def authenticate_user(request: Request):
    if 'X-Auth-Token' in request.headers:
        token = request.headers['X-Auth-Token']
        jwt_data = jwt.decode(
            jwt=token,
            key=os.getenv('JWT_SECRET_KEY'),
            algorithms="HS256"
        )
        user_exists = user_repository.user_exists(jwt_data["username"])
        if not user_exists:
            raise PassGuardAPIException(
                status_code=HttpStatusCodes.UNAUTHORIZED.value,
                error_message="User unauthorized"
            )
    else:
        raise PassGuardAPIException(
            status_code=HttpStatusCodes.UNAUTHORIZED.value,
            error_message="User unauthorized"
        )
