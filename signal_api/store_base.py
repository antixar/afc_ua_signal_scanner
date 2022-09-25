import base64
import configparser

import re
import ujson as json
from pathlib import Path
from typing import Optional

from .utils import Logger
from .utils import Singleton

RE_KEY = re.compile("^KEY_([A-Z]+)_([A-Z0-9_]+)$")

class StoreBase(Logger, metaclass=Singleton):

    def __init__(self):
        self.__storage = configparser.ConfigParser()
        if self.store_path.exists():
            self.__storage.read(str(self.store_path))


    @property
    def store_folder(self):
        folder = Path.home() / ".py_signalapp"
        if not folder.exists():
            folder.mkdir()
        return folder

    @property
    def store_path(self) -> Path:
        pass


    def __getattr__(self, key):
        if not key.startswith("KEY_"):
            return self.__getattribute__(key)
        option1, option2 = self.__key2option(key)
        if not option1:
            raise Exception(f"incorrect key: {key}")
        if option1 not in self.__storage or option2 not in self.__storage[option1]:
            return None
        res = self.__storage[option1][option2]
        if res and res.isdigit():
            return int(res)
        if res and res.upper() == "NONE":
            return None
        return res

    def __setattr__(self, key, value):
        if not key.startswith("KEY_"):
            return super().__setattr__(key, value)
        return self.save_key_value(key, value)

    def save_key_value(self, key, value):
        if str(getattr(self, key)) == str(value):
            return
        option1, option2 = self.__key2option(key)
        if option1 not in self.__storage:
            self.__storage[option1] = {}
        self.__storage[option1][option2] = str(value)
        with open(str(self.store_path), "w") as f:
            self.__storage.write(f)

    def __delattr__(self, key):
        if not key.startswith("KEY_"):
            return super().__delattr__(key)
        option1, option2 = self.__key2option(key)
        if option1 not in self.__storage:
            return
        elif option2 not in self.__storage[option1]:
            return
        del self.__storage[option1][option2]
        if not len(self.__storage[option1]):
            del self.__storage[option1]
        with open(str(self.__store_file), "w") as f:
            self.__storage.write(f)

    def __str__(self):
        resp = []
        for section in self.__storage.sections():
            for option in self.__storage[section]:
                key = f"KEY_{section}_{option}".upper()
                resp.append(f"{key} => {self.__storage[section][option]}")

        return "\n".join(resp)

    @classmethod
    def __key2option(cls, key):
        m = RE_KEY.match(key)
        if not m:
            return None, None
        return m.group(1).lower().title(), m.group(2).lower()


  

    def clean(self):
        if self.store_path.exists():
            self.store_path.unlink()
            self.__storage = configparser.ConfigParser()
        return
