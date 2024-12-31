from pydantic import BaseModel

from utils import VaultItemType


class VaultResponse(BaseModel):
    id: str
    name: str
    type: VaultItemType
    folder: str
