import base64
import configparser
import pickle
import re
import ujson as json
from pathlib import Path
from typing import Optional
import secrets
from .key_helper import KeyPair, KeyHelper, SignedPreKeyRecord, PreKeyRecord
from .store_base import StoreBase
from .utils import Singleton
import pickle


class StoreConfig(StoreBase, metaclass=Singleton):


    @property
    def store_path(self) -> Path:
        return self.store_folder / "config.ini"

    def __key2str(self, key):
        return base64.b64encode(pickle.dumps(key)).decode('utf-8')

    def __str2key(self, data) -> object:
        if not data:
            return None
        return pickle.loads(base64.b64decode(data))

    def generate_keys(self):

        identity_key_pair = KeyHelper.generate_key_pair()
        self.KEY_KEYS_IDENTITY_PAIR = self.__key2str(identity_key_pair)

        signed_pre_key = KeyHelper.generate_signed_pre_key(identity_key_pair, 0)
        self.KEY_KEYS_SIGNED_PRE_KEY = self.__key2str(signed_pre_key)

        for k in KeyHelper.generate_pre_keys(0, 100):
            self.__save(f"KEY_PREKEYS_{k.id}", self.__key2str(k))
        return

    @property
    def password(self):
        if not self.KEY_ACCOUNT_PASSWD:
            self.KEY_ACCOUNT_PASSWD = secrets.token_urlsafe(18)
        return self.KEY_ACCOUNT_PASSWD
