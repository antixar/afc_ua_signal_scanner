import configparser
import re
from pathlib import Path
from .utils import Singleton, Logger
import base64
import ujson as json
from .key_helper import KeyPair, KeyHelper, SignedPreKeyRecord, PreKeyRecord
import pickle
from typing import Optional

RE_KEY = re.compile("^KEY_([A-Z]+)_([A-Z0-9_]+)$")


class Store(Logger, metaclass=Singleton):

    def __init__(self):
        self.__config = configparser.ConfigParser()
        if self.config_path.exists():
            self.__config.read(str(self.config_path))
        
        self.__sessions = configparser.ConfigParser()
        if self.session_path.exists():
            self.__sessions.read(str(self.session_path))

    @property
    def store_folder(self):
        folder = Path.home() / ".py_signalapp"
        if not folder.exists():
            folder.mkdir()
        return folder
        
    @property
    def config_path(self) -> Path:
        return self.store_folder / "config.ini"

    @property
    def session_path(self) -> Path:
        return self.store_folder / "sessions.ini"


    def __getattr__(self, key):
        if not key.startswith("KEY_"):
            return self.__getattribute__(key)
        option1, option2 = self.__key2option(key)
        if not option1:
            raise Exception(f"incorrect key: {key}")
        if option1 not in self.__config or option2 not in self.__config[option1]:
            return None
        res = self.__config[option1][option2]
        if res and res.isdigit():
            return int(res)
        if res and res.upper() == "NONE":
            return None
        return res

    def __setattr__(self, key, value):

        if not key.startswith("KEY_"):
            return super().__setattr__(key, value)
        return self.__save(key, value)

    def __save(self, key, value):
        if str(getattr(self, key)) == str(value):
            return
        option1, option2 = self.__key2option(key)
        if option1 not in self.__config:
            self.__config[option1] = {}
        self.__config[option1][option2] = str(value)
        with open(str(self.__store_file), "w") as f:
            self.__config.write(f)


    def __delattr__(self, key):
        if not key.startswith("KEY_"):
            return super().__delattr__(key)
        option1, option2 = self.__key2option(key)
        if option1 not in self.__config:
            return
        elif option2 not in self.__config[option1]:
            return
        del self.__config[option1][option2]
        if not len(self.__config[option1]):
            del self.__config[option1]
        with open(str(self.__store_file), "w") as f:
            self.__config.write(f)

    def __str__(self):
        resp = []
        for section in self.__config.sections():
            for option in self.__config[section]:
                key = f"KEY_{section}_{option}".upper()
                resp.append(f"{key} => {self.__config[section][option]}")
               
        return "\n".join(resp)

    @classmethod
    def __key2option(cls, key):
        m = RE_KEY.match(key)
        if not m:
            return None, None
        return m.group(1).lower().title(), m.group(2).lower()

    
 
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
    def identity_key_pair(self) -> Optional[KeyPair]:
        return self.__str2key(self.KEY_KEYS_IDENTITY_PAIR)

    @property
    def signed_pre_key(self) -> Optional[SignedPreKeyRecord]:
        return self.__str2key(self.KEY_KEYS_SIGNED_PRE_KEY)
    
    def get_pre_key(self, key_id) -> Optional[PreKeyRecord]:
        return self.__str2key(getattr(self, f"KEY_PREKEYS_{key_id}"))
 
    
    def remove(self):
        if self.config_path.exists():
            self.config_path.unlink()
            self.__config = configparser.ConfigParser()
        if self.session_path.exists():
            self.session_path.unlink()
            self.__sessions = configparser.ConfigParser()