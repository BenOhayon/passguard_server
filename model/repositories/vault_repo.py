from bson import ObjectId
from db.db_connector import db
from model.parsers.db_response_parser import parse_db_response
from utils import VaultItemType
from cryptography.fernet import Fernet


class VaultRepository:
    __create_key = object()

    @classmethod
    def get_instance(cls):
        return VaultRepository(cls.__create_key)

    def __init__(self, create_key):
        if create_key == VaultRepository.__create_key:
            self.vault_collection = db["vault"]

    def fetch_all_vault_items(self):
        all_items = self.vault_collection.find()
        return [self.__parse_vault_item(item) for item in all_items]

    def fetch_vault_item(self, item_id):
        requested_item = self.vault_collection.find_one({"_id": ObjectId(item_id)})
        if requested_item is not None:
            return self.__parse_vault_item(requested_item)
        return None
    
    def __parse_vault_item(self, vault_item):
        parsed_item = parse_db_response(vault_item)
        if parsed_item["type"] == VaultItemType.PASSWORD.value:
            with open('encryption.txt', 'r') as file:
                encryption_key = file.read().strip()
                crypter = Fernet(encryption_key)
                encrypted_password = parsed_item["password"]
                decrypted_password = crypter.decrypt(bytes(encrypted_password, 'utf8'))
                parsed_item["password"] = str(decrypted_password, 'utf8')
        return parsed_item

    def create_password(self, name: str, folder: str, url: str, email: str, password: str):
        with open('encryption.txt', 'r') as file:
            encryption_key = file.read().strip()
            crypter = Fernet(encryption_key)
            encrypted_password = str(crypter.encrypt(bytes(password, 'utf8')), 'utf8')
        return self.__create_item(
            name,
            folder,
            VaultItemType.PASSWORD,
            url=url,
            email=email,
            password=encrypted_password
        )

    def update_vault_item(self, item_id: str, updated_item_data: dict):
        updated_item = {
            "_id": ObjectId(item_id),
            **updated_item_data
        }
        return self.vault_collection.replace_one({"_id": ObjectId(item_id)}, updated_item)

    def delete_vault_item(self, item_id: str):
        requested_item = self.vault_collection.find({"_id": ObjectId(item_id)})
        if requested_item is not None:
            self.vault_collection.delete_one({"_id": ObjectId(item_id)})
        return requested_item

    def __create_item(self, name: str, folder: str, item_type: VaultItemType, **item_data):
        new_password_item = {
            "name": name,
            "folder": folder,
            "type": item_type.value,
            **item_data
        }
        self.vault_collection.insert_one(new_password_item)
        return new_password_item
