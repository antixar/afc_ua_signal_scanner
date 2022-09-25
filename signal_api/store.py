import base64
import configparser
import pickle
import re
import ujson as json
from pathlib import Path
from typing import Optional
from .store_config import StoreConfig
from .store_contact import StoreContact


class Store:
    __config_store = StoreConfig()
    __contact_store = StoreContact()
    
    
    def clean(self):
        self.__config_store.clean()
        
    @property
    def config(self) -> StoreConfig:
        return self.__config_store
        
    @property
    def contact(self) -> StoreContact:
        return self.__contact_store