import aiohttp
import asyncio
import hashlib
import platform
import random
import string
import ujson
from datetime import date
from typing import Optional, Tuple
from urllib.parse import urljoin

from .client import Client, T
from .settings import TEXT_SECURE_SERVER_URL, CONTACT_DISCOVERY_URL
from .store import Store

DEFAULT_DEVICE_ID = 1

PLATFORM_STRINGS = {
    'win32': 'Windows',
    'darwin': 'macOS',
    'linux': 'Linux',
};


class HttpClient(Client):
    store = Store()

    async def create(self, url: str = TEXT_SECURE_SERVER_URL) -> Optional[str]:
        self._lock = asyncio.Lock()
        err = await super().create(url=url)
        if err:
            return err
        self._session = aiohttp.ClientSession(
            # headers=self._headers,
            json_serialize=ujson.dumps,
            raise_for_status=False
        )
        return None

    def __createAuthHeader(self) -> str:
        login = str(self.store.config.KEY_ACCOUNT_UUID or self.store.config.KEY_ACCOUNT_PHONE_NUMBER)
        login = self.store.config.KEY_ACCOUNT_PHONE_NUMBER
        # if self.store.config.KEY_ACCOUNT_DEVICE_ID and self.store.config.KEY_ACCOUNT_DEVICE_ID != DEFAULT_DEVICE_ID:
        #     login += "." + self.store.config.KEY_ACCOUNT_DEVICE_ID
        # login += ".1"
        # raise Exception(aiohttp.BasicAuth(login, self.__encode_password(login)).encode())
        return aiohttp.BasicAuth(login, self.store.config.password)

    async def __send(
            self, method: str, path: str, headers: dict = None, body: dict = None
    ) -> Tuple[Optional[dict], Optional[str]]:
        full_url = urljoin(self._url, path)
        if not headers:
            headers = {}
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            "User-Agent": self.__get_user_agent()
        }

        params = {
            "url": full_url,
            "headers": headers,
            "ssl_context": self._ssl_context,
            "method": method,
            "auth": self.__createAuthHeader(),
            "skip_auto_headers": ("User-Agent", "Content-Type"),

        }

        self.logger.info("params: {}", params)
        if method in ["PUT", "POST"] and body:
            params["json"] = body
            self.logger.info("body: {}", body)
        # raise Exception(params)
        resp = await self._session.request(**params)
        self.logger.warning(resp.headers)
        if resp.status != 200:
            return None, f"request error: {full_url} => [{resp.status}] {str(await resp.text())}"
        if not resp.headers["Content-Length"]:
            return None, None
        body = await resp.text()
        if resp.headers.get("Content-Type") == "application/json":
            body = ujson.loads(body)
            print(str(body))
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

    def __get_user_agent(self, app_version="1.2.3"):
        platform_name = PLATFORM_STRINGS.get((platform.system() or '').lower(), None)
        release = platform.release()
        res = f"Signal-Desktop/{app_version}"
        if platform_name:
            res += f" {platform_name} {release}"
        return res


class ContactClient(HttpClient):
    async def create(self) -> Optional[str]:
        return await super().create(url=CONTACT_DISCOVERY_URL)
