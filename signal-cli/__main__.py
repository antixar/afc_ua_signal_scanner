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
from signal_api.session import Session
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
        help='An account value (phone number with land code)',
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
    parser.add_argument(
        "-r",
        "--receiver",
        nargs=1,
        type=check_phone_format,
        help='A receiver value (phone number with land code)',
    )
    parser.add_argument(
        "-m",
        "--message",
        nargs=1,
        type=str,
        help='A message value',
    )

    # Required positional argument
    parser.add_argument(
        "command",
        nargs=1,
        help="A command for this this tool. Available values:",
        choices=["register", "send"],
    )

    args = parser.parse_args()
    config = Store().config
    if not args.account:
        # try to load this value from a local score
        args.account = config.KEY_ACCOUNT_PHONE_NUMBER
        if not args.account:
            raise SystemExit(
                "Not found an account phone number. Please input it with the '-a' option"
            )
    else:
        if config.KEY_ACCOUNT_PHONE_NUMBER and config.KEY_ACCOUNT_PHONE_NUMBER != args.account[0]:
            config.clean()
        config.KEY_ACCOUNT_PHONE_NUMBER = args.account[0]
    command = args.command[0]

    if command == "register":
        params = {
            "code": args.code or None,
            "pin": args.pin or None,
            "captcha_token": args.captcha or None
        }
        manager = DeviceManager() if args.device else AccountManager()
        err = await manager.register_with_verification_code(**params)
        if err:
            raise SystemExit("Can't register your account, try with captcha token again")
    if command == "send":
        if not args.message:
            raise SystemExit("not set any message value")
        if not args.receiver:
            raise SystemExit("not set a receiver value")
        session = Session(args.receiver[0])
        for message in args.message:
            err = await session.send(message)
            if err:
                raise SystemExit(f"Can't send this message. {err}")
    LOGGER.info("finished...")
    return


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
