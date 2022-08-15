import configparser
import re
from pathlib import Path

from .utils import Singleton

RE_KEY = re.compile("^KEY_([A-Z]+)_([A-Z_]+)$")


class Store(metaclass=Singleton):
    def __init__(self):
        self.__store_file = Path.home() / ".singalapp_py"
        self.__config = configparser.ConfigParser()
        if self.__store_file.exists():
            self.__config.read(str(self.__store_file))

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
        return res

    def __setattr__(self, key, value):

        if not key.startswith("KEY_"):
            return super().__setattr__(key, value)
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

    @classmethod
    def __key2option(cls, key):
        m = RE_KEY.match(key)
        if not m:
            return None, None
        return m.group(1).lower().title(), m.group(2).lower()
