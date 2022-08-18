import os
import random
import secrets
import sys
from dataclasses import dataclass
from loguru import logger
from typing import Any, Optional
from x3dh.implementations import KeyPairCurve25519


class KeyPair(KeyPairCurve25519):
    pass

class KeyHelper:

    @staticmethod
    def generate_registration_id(extended_range: Optional[bool] = False) -> int:
        # Generate a registration ID.  Clients should only do this once, at install time.

        # :param str extended_range: By default (false), the generated registration
        #                            ID is sized to require the minimal possible protobuf
        #                            encoding overhead. Specify true if the caller needs
        #                            the full range of MAX_INT at the cost of slightly
        #                            higher encoding overhead.
        # :return: the generated registration ID.

        sr = random.SystemRandom()
        if extended_range:
            return sr.randint(0, sys.maxint - 1) + 1
        return sr.randint(0, 16380) + 1

    @staticmethod
    def generate_signaling_key() -> str:
        # generate random a 32 byte AES key and a 20 byte Hmac256 key and concatenate them.
        aes_key_32 = secrets.token_urlsafe(32)
        hmac_key_20 = secrets.token_urlsafe(20)
        return aes_key_32 + hmac_key_20


    @staticmethod
    def generate_identity_key_pair() -> KeyPair:
        # Generate an identity key pair.  Clients should only do this once, at install time.
   
        # :return: the generated IdentityKeyPair.
        return KeyPairCurve25519.generate()
        # raise Exception(pair)
        # publicKey = IdentityKey(keyPair.getPublicKey());
        # return dentityKeyPair(publicKey, keyPair.getPrivateKey());
  