import argparse
import asyncio
import functools
import logging
import re
import signal
import sys

from signal_api.account_manager import AccountManager
from signal_api.device_manager import DeviceManager
from signal_api.http_client import HttpClient
from signal_api.paths import CREATE_ACCOUNT_SMS_PATH, KEEPALIVE_PATH, WHO_AM_I
from signal_api.store import Store
from signal_api.ws_client import WsClient

# from protos import WhisperTextProtocol_pb2 as text_protocol
LOGGER = logging.getLogger(__name__)


def check_phone_format(arg_value, re_phone=re.compile(r"^\+[0-9]{12}$")):
    if not re_phone.match(arg_value):
        raise argparse.ArgumentTypeError(
            "invalid phone number. Correct format: +231111111111"
        )
    return arg_value


def check_pin_format(arg_value, re_pin=re.compile(r"^[0-9]{4}$")):
    if not re_pin.match(arg_value):
        raise argparse.ArgumentTypeError(
            "invalid pin. Correct format: 1234"
        )
    return arg_value


async def main():

    parser = argparse.ArgumentParser(
        description="Options for setup of Signal settings and running of its modes"
    )

    # Optional positional argument
    parser.add_argument(
        "-a",
        "--account",
        nargs=1,
        type=check_phone_format,
        help='An account value (phone number with land code)"',
    )
    parser.add_argument(
        "--captcha",
        nargs='?',
        type=str,
        help='Captcha token from https://signalcaptchas.org/registration/generate.html',
    )
    parser.add_argument(
        "--code",
        nargs='?',
        type=str,
        help='Code of verification',
    )
    parser.add_argument(
        "--device",
        # nargs='?',
        action='store_true',
        help='Registration of a new device',
    )
    parser.add_argument(
        "--pin",
        nargs='?',
        type=check_pin_format,
        help='Pin of verification',
    )
    # Required positional argument
    parser.add_argument(
        "command",
        nargs=1,
        help="A command for this this tool. Available values:",
        choices=["register"],
    )

    args = parser.parse_args()

    if not args.account:
        # try to load this value from a local score
        args.account = Store().KEY_ACCOUNT_PHONE_NUMBER
        if not args.account:
            raise SystemExit(
                "Not found an account phone number. Please input it with the '-a' option"
            )
    else:
        Store().KEY_ACCOUNT_PHONE_NUMBER = args.account[0]
    command = args.command[0]
  
    if command == "register":
        params = {
            "code":args.code or None,
            "pin": args.pin or None,
            "captcha_token":args.captcha or None
        }
        manager = DeviceManager() if args.device else AccountManager()
        err = await manager.register_with_verification_code(**params)
        if err:
            SystemExit("Can't register your account, try with captcha token again")

    raise Exception(Store().KEY_ACCOUNT_PHONE_NUMBER)
    print(parser.print_help())
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
