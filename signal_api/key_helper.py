import os
import random
import secrets
import sys
from dataclasses import dataclass
from loguru import logger
from typing import Any, Optional, List
from x3dh.implementations import KeyPairCurve25519
import time


class KeyPair(KeyPairCurve25519):
    pass
    

class PreKeyRecord:
    def __init__(self, key_id: int, key_pair: KeyPair):
        self.id = key_id
        self.pair = key_pair
        # raise Exception(self.pair.serialize())
        
class SignedPreKeyRecord(PreKeyRecord):
    def __init__(self, key_id, key_pair, timestamp, signature):
        super().__init__(key_id, key_pair)
        self.timestamp = timestamp
        self.signature = signature
    
        

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
    def generate_key_pair() -> KeyPair:
        # Generate a key pair.
   
        # :return: the generated IdentityKeyPair.
        return KeyPairCurve25519.generate()

    @staticmethod
    def generate_pre_keys(start: int, count: int) -> List[PreKeyRecord]:
        for i in range(start, start + count):
            yield PreKeyRecord(i, KeyHelper.generate_key_pair()) 


    @staticmethod
    def generate_signed_pre_key(identity_key_pair: KeyPair, key_id: int) -> SignedPreKeyRecord:
        key_pair = KeyHelper.generate_key_pair()
        
        signature = KeyHelper.calculate_signature(
                identity_key_pair,
                key_pair.pub
        )
        return SignedPreKeyRecord(key_id, key_pair, time.time(), signature)
     
        
    @staticmethod
    def calculate_signature(key_pair: KeyPair, message: bytes) -> bytes:
        return key_pair.encrypt(message, key_pair)

  
  # IdentityKeyPair    identityKey        = KeyHelper.generateIdentityKeyPair();
# List<PreKeyRecord> oneTimePreKeys     = KeyHelper.generatePreKeys(0, 100);
# PreKeyRecord       lastResortKey      = KeyHelper.generateLastResortPreKey();
# SignedPreKeyRecord signedPreKeyRecord = KeyHelper.generateSignedPreKey(identityKey, signedPreKeyId);



# static Uint8List calculateSignature(
#      ECPrivateKey? signingKey, Uint8List? message) {
#    if (signingKey == null || message == null) {
#      throw Exception('Values must not be null');
#    }#
#
#    if (signingKey.getType() == djbType) {
#      final privateKey = signingKey.serialize();
#      final random = generateRandomBytes();

#      return sign(privateKey, message, random);
#    } else {
#      throw Exception('Unknown Signing Key type${signingKey.getType()}');
#    }
#   }