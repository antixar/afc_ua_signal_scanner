from typing import Optional
from .base import Base
from .http_client.HttpClient import DEFAULT_DEVICE_ID

class Address:
    def __init__(self, number: str, device_id: int=DEFAULT_DEVICE_ID):
        self.__number = phone_number
        self.__device_id = device_id

class Session(Base):

    def __init__(self, receiver):
        self.__receiver = receiver
        
    async def send(self, message: str) -> Optional[str]:
    # final remoteAddress = SignalProtocolAddress("remote", 1);
    # final sessionBuilder = SessionBuilder(sessionStore, preKeyStore,
    #  signedPreKeyStore, identityStore, remoteAddress);

    # sessionBuilder.processPreKeyBundle(retrievedPreKey);

    # final sessionCipher = SessionCipher(sessionStore, preKeyStore,
    #   signedPreKeyStore, identityStore, remoteAddress);
    #final ciphertext = sessionCipher.encrypt(utf8.encode("Hello Mixin"));
