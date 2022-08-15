import asyncio
import base64
import json
import logging
import pathlib
import random
import socket
import ssl
import string
import time
import websockets
from async_timeout import timeout, timeout_at
from google.protobuf.message import DecodeError
from random import randint
from typing import Iterator, Optional, Tuple, Type, TypeVar
from urllib.parse import urlparse
from websockets.exceptions import InvalidHandshake
from websockets.legacy.client import WebSocketClientProtocol

from .protos import WebSocketResources_pb2 as ws_resources
from .utils import Singleton, Logger

T = TypeVar("T", bound="Client")


class Client(Logger, metaclass=Singleton):
    _inited_clses = {}

    def __init__(self):
        return

    def unique_log_id(self) -> str:
        return self._url

    async def create(self, url: str):
        self._url = url
        self._headers = {
            "Host": urlparse(url).netloc,
            "User-Agent": "Signal-Desktop/1.2.3",
        }
        self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        pem_file = pathlib.Path(__file__).with_name("cert.pem")
        self._ssl_context.load_verify_locations(pem_file)
        return None

    @classmethod
    async def instance(cls: T, *args, **kwargs) -> Tuple[Optional[T], Optional[str]]:
        inst = cls()
        if not Client._inited_clses.get(cls):
            err = await inst.create(*args, **kwargs)
            if err:
                return None, err
            Client._inited_clses[cls] = True
        return inst, None

    async def get(
            self, path: str, headers: dict = None
    ) -> Tuple[Optional[dict], Optional[str]]:
        raise NotImplementedError

    async def stop(self):
        raise NotImplementedError
