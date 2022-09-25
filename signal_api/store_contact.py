from .utils import Singleton
from .store_base import StoreBase
from typing import Tuple, Optional
from .client import Client
from pathlib import Path

class StoreContact(StoreBase, metaclass=Singleton):
    
    @property
    def store_path(self) -> Path:
        return self.store_folder / "contacts.ini"

    async def get(self, name: str, client: Client) -> Tuple[Optional[str], Optional[str]]:
        return None, "aaaaaa"
        raise Exception("aaaaa")
        
