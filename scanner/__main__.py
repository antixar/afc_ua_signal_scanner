from signalapp import signal_listen
import asyncio, signal, sys, logging
import functools
import signal

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
        async for msg in signal_listen():
            LOGGER.warning(f"AAAAAA {msg}")
    except asyncio.CancelledError:
        LOGGER.warning('You pressed Ctrl+C!')
        sys.exit(0)
        
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
