import asyncio
import aiohttp
from .client import Client, T
from typing import Tuple, Optional
import ujson
from .settings import TEXT_SECURE_SERVER_URL
from urllib.parse import urljoin

def generateRegistrationID():
	return randint(1, 2^32) & 0x3fff

def generatePassword():
    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
    return base64.b64encode(bytes(password, 'utf-8'))







class HttpClient(Client):
    def __init__(self, url: str= TEXT_SECURE_SERVER_URL):
        super().__init__(url=url)
        self._lock = asyncio.Lock()
        self._session = None
        return None

    @classmethod
    async def instance(cls: T, *args, **kwargs) -> Tuple[Optional[T], Optional[str]]:
        inst = cls(*args, **kwargs)
        inst._session = aiohttp.ClientSession(headers=inst._headers, json_serialize=ujson.dumps,  raise_for_status=False)
        return inst, None


            
    async def __send(self, method: str, path: str, headers: dict) -> Tuple[Optional[dict], Optional[str]]:
        full_url = urljoin(self._url, path)
        params = {
           "url": urljoin(self._url, path),
           
           "headers": headers,
           "ssl_context": self._ssl_context,
           "method": method,
        }
        
        resp = await self._session.request(**params)
        self.logger.warning(resp)
        if resp.status != 200:
            return None, f"request error: [{resp.status}] {str(await resp.text())}"
        raise Exception(resp)




    async def get(self, path: str, headers: dict=None) -> Tuple[Optional[dict], Optional[str]]:
        return await self.__send("GET", path, headers)


    async def stop(self):
        if self._session:
            await self._session.close()

