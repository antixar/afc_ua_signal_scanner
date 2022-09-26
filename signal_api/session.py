from typing import Optional

from .base import Base
from .http_client import DEFAULT_DEVICE_ID


class SignalProtocolAddress:
    def __init__(self, number: str, device_id: int = DEFAULT_DEVICE_ID):
        self.__number = phone_number
        self.__device_id = device_id

    def to_str(self):
        return f"{self.__number}.{self.__device_id}"


class SessionBuilder:
    pass


class Session(Base):

    def __init__(self, receiver):
        self.__receiver = receiver

    async def send(self, message: str) -> Optional[str]:
        client, err = await self.client.instance()
        if err:
            return err
        contact, err = await self.store.contact.get(self.__receiver, client)
        if err:
            return err

        client, err = await self.client.instance()
        if err:
            return err
        uri = f"/v1/profile/70d636a8-3d15-4b4b-8076-0a7f703089b0"  # {self.__receiver}"
        # raise Exception(uri)
        resp, err = await client.get(uri)
        raise Exception(f"{resp} => {err}")

        return "error"
    # final remoteAddress = SignalProtocolAddress("remote", 1);
    # final sessionBuilder = SessionBuilder(sessionStore, preKeyStore,
    #  signedPreKeyStore, identityStore, remoteAddress);

    # sessionBuilder.processPreKeyBundle(retrievedPreKey);

    # final sessionCipher = SessionCipher(sessionStore, preKeyStore,
    #   signedPreKeyStore, identityStore, remoteAddress);
    # final ciphertext = sessionCipher.encrypt(utf8.encode("Hello Mixin"));

# class SessionBuilder {
#   SessionBuilder(this._sessionStore, this._preKeyStore, this._signedPreKeyStore,
#       this._identityKeyStore, this._remoteAddress);
#
#   SessionBuilder.fromSignalStore(
#       SignalProtocolStore store, SignalProtocolAddress remoteAddress)
#       : this(store, store, store, store, remoteAddress);
#
#   static const String tag = 'SessionBuilder';
#
#   SessionStore _sessionStore;
#   PreKeyStore _preKeyStore;
#   SignedPreKeyStore _signedPreKeyStore;
#   IdentityKeyStore _identityKeyStore;
#   SignalProtocolAddress _remoteAddress;
#
#   Future<Optional<int>> process(
#       SessionRecord sessionRecord, PreKeySignalMessage message) async {
#     final theirIdentityKey = message.getIdentityKey();
#
#     if (!await _identityKeyStore.isTrustedIdentity(
#         _remoteAddress, theirIdentityKey, Direction.receiving)) {
#       throw UntrustedIdentityException(
#           _remoteAddress.getName(), theirIdentityKey);
#     }
#
#     final unsignedPreKeyId = processV3(sessionRecord, message);
#
#     await _identityKeyStore.saveIdentity(_remoteAddress, theirIdentityKey);
#
#     return unsignedPreKeyId;
#   }
#
#   Future<Optional<int>> processV3(
#       SessionRecord sessionRecord, PreKeySignalMessage message) async {
#     if (sessionRecord.hasSessionState(
#         message.getMessageVersion(), message.getBaseKey().serialize())) {
#       // ignore: avoid_print
#       print(
#           "We've already setup a session for this V3 message, letting bundled message fall through...");
#       return const Optional.empty();
#     }
#
#     final ourSignedPreKey = _signedPreKeyStore
#         .loadSignedPreKey(message.getSignedPreKeyId())
#         .then((value) => value.getKeyPair());
#
#     late final Optional<ECKeyPair> ourOneTimePreKey;
#     if (message.getPreKeyId().isPresent) {
#       ourOneTimePreKey = Optional.of(await _preKeyStore
#           .loadPreKey(message.getPreKeyId().value)
#           .then((value) => value.getKeyPair()));
#     } else {
#       ourOneTimePreKey = const Optional<ECKeyPair>.empty();
#     }
#
#     if (!sessionRecord.isFresh()) sessionRecord.archiveCurrentState();
#
#     final parameters = BobSignalProtocolParameters(
#       theirBaseKey: message.getBaseKey(),
#       theirIdentityKey: message.getIdentityKey(),
#       ourIdentityKey: await _identityKeyStore.getIdentityKeyPair(),
#       ourSignedPreKey: await ourSignedPreKey,
#       ourRatchetKey: await ourSignedPreKey,
#       ourOneTimePreKey: ourOneTimePreKey,
#     );
#
#     RatchetingSession.initializeSessionBob(
#         sessionRecord.sessionState, parameters);
#
#     sessionRecord.sessionState.localRegistrationId =
#         await _identityKeyStore.getLocalRegistrationId();
#     sessionRecord.sessionState.remoteRegistrationId =
#         message.getRegistrationId();
#     sessionRecord.sessionState.aliceBaseKey = message.getBaseKey().serialize();
#
#     if (message.getPreKeyId().isPresent) {
#       return message.getPreKeyId();
#     } else {
#       return const Optional.empty();
#     }
#   }
#
#   Future<void> processPreKeyBundle(PreKeyBundle preKey) async {
#     if (!await _identityKeyStore.isTrustedIdentity(
#         _remoteAddress, preKey.getIdentityKey(), Direction.sending)) {
#       throw UntrustedIdentityException(
#           _remoteAddress.getName(), preKey.getIdentityKey());
#     }
#
#     if (preKey.getSignedPreKey() != null &&
#         !Curve.verifySignature(
#             preKey.getIdentityKey().publicKey,
#             preKey.getSignedPreKey()!.serialize(),
#             preKey.getSignedPreKeySignature())) {
#       throw InvalidKeyException('Invalid signature on device key!');
#     }
#
#     if (preKey.getSignedPreKey() == null) {
#       throw InvalidKeyException('No signed prekey!');
#     }
#
#     final sessionRecord = await _sessionStore.loadSession(_remoteAddress);
#     final ourBaseKey = Curve.generateKeyPair();
#     final theirSignedPreKey = preKey.getSignedPreKey();
#     final theirOneTimePreKey = Optional.ofNullable(preKey.getPreKey());
#     final theirOneTimePreKeyId = theirOneTimePreKey.isPresent
#         ? Optional.ofNullable(preKey.getPreKeyId())
#         : const Optional<int>.empty();
#
#     final parameters = AliceSignalProtocolParameters(
#       ourBaseKey: ourBaseKey,
#       ourIdentityKey: await _identityKeyStore.getIdentityKeyPair(),
#       theirIdentityKey: preKey.getIdentityKey(),
#       theirSignedPreKey: theirSignedPreKey!,
#       theirRatchetKey: theirSignedPreKey,
#       theirOneTimePreKey: theirOneTimePreKey,
#     );
#
#     if (!sessionRecord.isFresh()) sessionRecord.archiveCurrentState();
#
#     RatchetingSession.initializeSessionAlice(
#         sessionRecord.sessionState, parameters);
#
#     sessionRecord.sessionState.setUnacknowledgedPreKeyMessage(
#         theirOneTimePreKeyId, preKey.getSignedPreKeyId(), ourBaseKey.publicKey);
#     sessionRecord.sessionState.localRegistrationId =
#         await _identityKeyStore.getLocalRegistrationId();
#     sessionRecord.sessionState.remoteRegistrationId =
#         preKey.getRegistrationId();
#     sessionRecord.sessionState.aliceBaseKey = ourBaseKey.publicKey.serialize();
#
#     await _identityKeyStore.saveIdentity(
#         _remoteAddress, preKey.getIdentityKey());
#     await _sessionStore.storeSession(_remoteAddress, sessionRecord);
#   }
# }

# const bobAddress = SignalProtocolAddress('bob', 1);
#   final sessionBuilder = SessionBuilder(
#       sessionStore, preKeyStore, signedPreKeyStore, identityStore, bobAddress);
#
#   // Should get remote from the server
#   final remoteRegId = generateRegistrationId(false);
#   final remoteIdentityKeyPair = generateIdentityKeyPair();
#   final remotePreKeys = generatePreKeys(0, 110);
#   final remoteSignedPreKey = generateSignedPreKey(remoteIdentityKeyPair, 0);
#
#   final retrievedPreKey = PreKeyBundle(
#       remoteRegId,
#       1,
#       remotePreKeys[0].id,
#       remotePreKeys[0].getKeyPair().publicKey,
#       remoteSignedPreKey.id,
#       remoteSignedPreKey.getKeyPair().publicKey,
#       remoteSignedPreKey.signature,
#       remoteIdentityKeyPair.getPublicKey());
#
#   await sessionBuilder.processPreKeyBundle(retrievedPreKey);
#
#   final sessionCipher = SessionCipher(
#       sessionStore, preKeyStore, signedPreKeyStore, identityStore, bobAddress);
#   final ciphertext = await sessionCipher
#       .encrypt(Uint8List.fromList(utf8.encode('Hello Mixin🤣')));
#   // ignore: avoid_print
#   print(ciphertext);
#   // ignore: avoid_print
#   print(ciphertext.serialize());
#   //deliver(ciphertext);
#
#   final signalProtocolStore =
#       InMemorySignalProtocolStore(remoteIdentityKeyPair, 1);
#   const aliceAddress = SignalProtocolAddress('alice', 1);
#   final remoteSessionCipher =
#       SessionCipher.fromStore(signalProtocolStore, aliceAddress);
#
#   for (final p in remotePreKeys) {
#     await signalProtocolStore.storePreKey(p.id, p);
#   }
#   await signalProtocolStore.storeSignedPreKey(
#       remoteSignedPreKey.id, remoteSignedPreKey);
#
#   if (ciphertext.getType() == CiphertextMessage.prekeyType) {
#     await remoteSessionCipher
#         .decryptWithCallback(ciphertext as PreKeySignalMessage, (plaintext) {
#       // ignore: avoid_print
#       print(utf8.decode(plaintext));
#     });
#   }
