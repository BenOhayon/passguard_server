from typing import Optional
from pydantic import BaseModel


class VaultItem(BaseModel):
    name: str
    folder: Optional[str]
