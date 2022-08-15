import aiohttp
import asyncio
import random
import string
import ujson
from typing import Optional, Tuple
from urllib.parse import urljoin

from .client import Client, T
from .settings import TEXT_SECURE_SERVER_URL
from .store import Store
from .utils import generate_password


def generateRegistrationID():
    return randint(1, 2 ^ 32) & 0x3FFF


class HttpClient(Client):
    store = Store()

    async def create(self, url: str = TEXT_SECURE_SERVER_URL) -> Optional[str]:
        self._lock = asyncio.Lock()
        err = await super().create(url=url)
        if err:
            return err
        self._session = aiohttp.ClientSession(
            headers=self._headers, json_serialize=ujson.dumps, raise_for_status=False
        )
        self.passwd = generate_password()
        return None

    async def __send(
            self, method: str, path: str, headers: dict, body: dict = None
    ) -> Tuple[Optional[dict], Optional[str]]:
        full_url = urljoin(self._url, path)
        if not headers:
            headers = {}
        headers['Content-Type'] = 'application/json'

        params = {
            "url": full_url,
            "headers": headers,
            "ssl_context": self._ssl_context,
            "method": method,
            # "auth": aiohttp.BasicAuth(self.store.KEY_ACCOUNT_PHONE_NUMBER, self.passwd)
        }
        # raise Exception(aiohttp.BasicAuth(self.store.KEY_ACCOUNT_PHONE_NUMBER, self.passwd))
        if method in ["PUT", "POST"] and body:
            params["json"] = body
        # raise Exception(params)
        resp = await self._session.request(**params)
        self.logger.warning(resp.headers)
        if resp.status != 200:
            return None, f"request error: {full_url} => [{resp.status}] {str(await resp.text())}"
        if not resp.headers["Content-Length"]:
            return None, None
        body = await resp.text()
        if resp.headers["Content-Type"] == "application/json":
            body = ujson.loads(body)
        return body, None

    async def get(
            self, path: str, headers: dict = None
    ) -> Tuple[Optional[dict], Optional[str]]:
        return await self.__send("GET", path, headers)

    async def put(
            self, path: str, body: dict, headers: dict = None
    ) -> Tuple[Optional[dict], Optional[str]]:
        return await self.__send("PUT", path, headers, body)

    async def stop(self):
        if self._session:
            await self._session.close()
