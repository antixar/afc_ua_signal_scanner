from pathlib import Path
from typing import Tuple, Optional

from .client import Client
from .paths import DIRECTORY_AUTH_PATH
# from .paths import WHO_AM_I as DIRECTORY_AUTH_PATH
from .store_base import StoreBase
from .utils import Singleton


class StoreContact(StoreBase, metaclass=Singleton):

    @property
    def store_path(self) -> Path:
        return self.store_folder / "contacts.ini"

    async def get(self, name: str, client: Client) -> Tuple[Optional[str], Optional[str]]:
        data, err = await client.get(DIRECTORY_AUTH_PATH)
        raise Exception(f"{data} => {err}")
