import os
from typing import Union
from fastapi import Request
from bson import ObjectId
from db.db_connector import db
from model.exceptions import PassGuardAPIException
from model.parsers.db_response_parser import parse_db_response
import jwt

from utils import HttpStatusCodes


class UserRepository:
    __create_key = object()

    @classmethod
    def get_instance(cls):
        return UserRepository(cls.__create_key)

    def __init__(self, create_key):
        if create_key == UserRepository.__create_key:
            self.users_collection = db["users"]

    def fetch_all_users(self):
        all_users = self.users_collection.find()
        return [parse_db_response(user) for user in all_users]

    def fetch_user(self, username: str, password: str):
        requested_user = self.users_collection.find_one({"username": username})
        if requested_user is not None:
            parsed_user = parse_db_response(requested_user)
            if parsed_user['password'] != password:
                return f"Wrong password for {username}"
            *user_result, password = parsed_user.items()
            return user_result
        return "User was not found"

    def create_user(self, username: str, email: str, password: str):
        requested_user = self.users_collection.find_one({"username": username})
        if requested_user is not None:
            new_user = {
                "username": username,
                "email": email
            }
            self.users_collection.insert_one({**new_user, "password": password})
            return new_user
        return "User already exists"

    def update_user(self, user_id: str, updated_user_data: dict):
        updated_user = {
            "_id": ObjectId(user_id),
            **updated_user_data
        }
        return self.users_collection.replace_one({"_id": ObjectId(user_id)}, updated_user)

    def delete_user(self, item_id: str):
        requested_item = self.users_collection.find_one({"_id": ObjectId(item_id)})
        if requested_item is not None:
            self.users_collection.delete_one({"_id": ObjectId(item_id)})
        return requested_item

    def register(self, username: str, password: str, **more_user_data) -> Union[dict, str]:
        existing_user = self.users_collection.find_one({"username": username})
        if existing_user is None:
            token = jwt.encode(
                payload={"username": username, "password": password, **more_user_data},
                key=os.getenv('JWT_SECRET_KEY'),
                algorithm="HS256"
            )
            self.users_collection.insert_one({
                "username": username,
                "password": password,
                **more_user_data
            })
            return {
                "username": username,
                **more_user_data,
                "token": token
            }
        return "User already exists"

    def login(self, username: str, password: str):
        requested_user = self.users_collection.find_one({"username": username})
        if requested_user is not None:
            parsed_user = parse_db_response(requested_user)
            if password == parsed_user['password']:
                user_id, username, password, *rest = parsed_user.items()
                more_user_data = {k: v for k, v in rest}
                token = jwt.encode(
                    payload={"username": username, "password": password, **more_user_data},
                    key=os.getenv('JWT_SECRET_KEY'),
                    algorithm=os.getenv('JWT_ALGORITHM')
                )
                return {
                    "id": user_id[1],
                    "username": username[1],
                    **more_user_data,
                    "token": token
                }
            return "Wrong password"
        return "User was not found"

    def user_exists(self, username: str):
        user = self.users_collection.find_one({"username": username})
        return user is not None
