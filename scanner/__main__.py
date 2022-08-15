import asyncio
import functools
import logging
import signal
import sys

from signal_api.http_client import HttpClient
from signal_api.paths import CREATE_ACCOUNT_SMS_PATH, KEEPALIVE_PATH, WHO_AM_I
from signal_api.store import Store
from signal_api.ws_client import WsClient

# from protos import WhisperTextProtocol_pb2 as text_protocol
LOGGER = logging.getLogger(__name__)


async def main():
    print(id(Store()))
    print(id(Store()))
    Store().KEY_TEST_VALUE_DDDD = 1111
    Store().KEY_TESTRRRRR_VALUE_DDDD = 1111
    del Store().KEY_TEST_VALUE_DDDD
    raise Exception
    http_client, err = await HttpClient.instance()
    res, err = await http_client.get("/v1/accounts/me")
    if err:
        LOGGER.warning(err)
    try:
        ws_client, err = await WsClient.instance()
        if err:
            raise SystemExit(err)
        # await ws_client.get(CREATE_ACCOUNT_SMS_PATH % ("111", "android"))
        # await ws_client.get("/v1/accounts/me")
        await ws_client.stop()
    except asyncio.CancelledError:
        LOGGER.warning("You pressed Ctrl+C!")
        sys.exit(0)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
