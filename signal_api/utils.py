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


def generate_registration_id(extended_range: Optional[bool] = False) -> int:
    # Generate a registration ID.  Clients should only do this once, at install time.

    # :param str extended_range: By default (false), the generated registration
    #                            ID is sized to require the minimal possible protobuf
    #                            encoding overhead. Specify true if the caller needs
    #                            the full range of MAX_INT at the cost of slightly
    #                            higher encoding overhead.
    # :return: the generated registration ID.

    sr = random.SystemRandom()
    if extended_range:
        return sr.randint(0, sys.maxint - 1) + 1
    return sr.randint(0, 16380) + 1


def generate_signaling_key() -> str:
    # generate random a 32 byte AES key and a 20 byte Hmac256 key and concatenate them.
    aes_key_32 = secrets.token_urlsafe(32)
    hmac_key_20 = secrets.token_urlsafe(20)
    return aes_key_32 + hmac_key_20


def generate_password():
    return secrets.token_urlsafe(16)
