from .settings import TEXT_SECURE_WEBSOCKET_API
from .listener import Listener


async def signal_listen(**kwargs: dict):
    async for msg in Listener().listen(ws_link=TEXT_SECURE_WEBSOCKET_API, **kwargs):
        yield msg

