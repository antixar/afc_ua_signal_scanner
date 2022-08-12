import asyncio
import functools
import logging
import signal
import signal
import sys

from signalapp.paths import CREATE_ACCOUNT_SMS_PATH, KEEPALIVE_PATH
from signalapp.ws_client import WsClient

# from protos import WhisperTextProtocol_pb2 as text_protocol
LOGGER = logging.getLogger(__name__)
# test = text_protocol.SignalMessage()
# test.ratchetKey = b'aaaaa'
# test.counter = 1
# test.previousCounter = 2
# test.ciphertext = b'bbbbb'

# with open('out.bin', 'wb') as f:
#    f.write(test.SerializeToString())


async def main():
    try:
        ws_client, err = await WsClient.instance()
        if err:
            raise SystemExit(err)
        await ws_client.get(CREATE_ACCOUNT_SMS_PATH % ("111", "android"))
        # await ws_client.get("/api/v1/sticker")
        await ws_client.stop()
    except asyncio.CancelledError:
        LOGGER.warning('You pressed Ctrl+C!')
        sys.exit(0)
        
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
