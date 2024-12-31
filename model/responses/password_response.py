from model.responses.vault_response import VaultResponse


class PasswordResponse(VaultResponse):
    url: str
    email: str
    password: str
