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
from async_timeout import timeout, timeout_at
from google.protobuf.message import DecodeError
from random import randint
from typing import TypeVar, Type, Iterator, Optional, Tuple
from websockets.exceptions import InvalidHandshake
from websockets.legacy.client import WebSocketClientProtocol

from .protos import WebSocketResources_pb2 as ws_resources
from .settings import TEXT_SECURE_WEBSOCKET_API

T = TypeVar('T', bound='WsClient')
LOGGER = logging.getLogger(__name__)
PING_TIMEOUT = 5.0


def generateRegistrationID():
	return randint(1, 2^32) & 0x3fff

def generatePassword():
    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
    return base64.b64encode(bytes(password, 'utf-8'))







class WsClient:
    def __init__(self):
        self._count = 0
        self._in_queue = asyncio.Queue()
        self._stack = {}
        self._lock = asyncio.Lock()
        self._ws = None

    @classmethod
    async def instance(cls: T, ws_link: str = TEXT_SECURE_WEBSOCKET_API) -> Tuple[Optional[T], Optional[str]]:
        inst = cls()
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        pem_file = pathlib.Path(__file__).with_name("cert.pem")
        ssl_context.load_verify_locations(pem_file)
        try:
            inst._ws = await websockets.connect(ws_link, ssl=ssl_context)
        except (socket.gaierror, InvalidHandshake) as exc:
            return None, f"WS: {ws_link}, {exc}"
        # asyncio.ensure_future(inst._ping_pong())
        asyncio.ensure_future(inst._listen())

        return inst, None

    
    async def _listen(self):
        LOGGER.warning("start to listen...")
        async for msg in self._ws:
             resp = ws_resources.WebSocketMessage()
             try:
                resp.ParseFromString(msg)
             except DecodeError as exc:
                 print(f"Decode error: {exc}, {msg}")
                 continue
             if resp.type == ws_resources.WebSocketMessage.Type.RESPONSE:
                resp = resp.response
             else:
                 raise Exception(resp)

             LOGGER.warning("ggg %s" % resp)

             async with self._lock:
                 q = self._stack.pop(resp.id, None)
             if not q:
                 print(f"not found queue with id {resp.id}")
                 continue

             if resp.status != 200:
                 await q.put((None, f"request error: [{resp.status}] {str(resp.message)}"))
             else:
                 await q.put((resp.body, None))

            
    async def __send(self, method: str, path: str, headers: dict) -> Tuple[Optional[dict], Optional[str]]:
        req = ws_resources.WebSocketMessage()
        req.type = ws_resources.WebSocketMessage.Type.REQUEST
        q = asyncio.Queue(maxsize=1)
        async with self._lock:
            self._count += 1
            req.request.id = self._count
            self._stack[self._count] = q


        req.request.verb = method
        req.request.path = path
        if headers:
            req.request.headers = headers
        print(req)
        print(base64.b64encode(req.SerializeToString()))
        await self._ws.send(req.SerializeToString())

        try:
            async with timeout(1.5) as cm:
                await asyncio.sleep(2)
                return await q.get()
        except asyncio.TimeoutError:
            pass
        async with self._lock:
            self._stack.pop(self._count, None)
        return None, "Timeout error for 'send' operation"



    async def get(self, path: str, headers: dict=None) -> Tuple[Optional[dict], Optional[str]]:
        return await self.__send("GET", path, headers)


    async def stop(self):
        if self._ws:
            await self._ws.close()
            await self._ws.wait_closed()
