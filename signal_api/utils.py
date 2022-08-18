import os
import random
import secrets
import sys
from dataclasses import dataclass
from loguru import logger
from typing import Any, Optional

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>[{time}]</green> # <level>{level} # {extra[class_name]} {extra[unique_id]} # {message}</level>",
    filter=lambda record: "class_logger" in record["extra"],
)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger:
    @dataclass
    class __Logger:
        class_name: str
        unique_id: str = None

        def __getattr__(self, key: str) -> Any:
            if not hasattr(logger, key):
                return self.__getattribute__(key)

            def intra(*args, **kwargs):
                params = {
                    "class_logger": True,
                    "class_name": self.class_name,
                    "unique_id": self.unique_id or "",
                }
                return getattr(logger.bind(**params), key)(*args, **kwargs)

            return intra

    def unique_log_id(self) -> str:
        return ""

    @property
    def logger(self):
        return self.__Logger(self.__class__.__name__, self.unique_log_id() or "")





