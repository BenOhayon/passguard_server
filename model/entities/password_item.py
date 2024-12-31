from model.entities.vault_item import VaultItem


class PasswordItem(VaultItem):
    url: str
    email: str
    password: str
