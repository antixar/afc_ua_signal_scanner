# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: WhisperTextProtocol.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x19WhisperTextProtocol.proto\x12\ntextsecure"a\n\rSignalMessage\x12\x12\n\nratchetKey\x18\x01 \x01(\x0c\x12\x0f\n\x07\x63ounter\x18\x02 \x01(\r\x12\x17\n\x0fpreviousCounter\x18\x03 \x01(\r\x12\x12\n\nciphertext\x18\x04 \x01(\x0c"\x8e\x01\n\x13PreKeySignalMessage\x12\x16\n\x0eregistrationId\x18\x05 \x01(\r\x12\x10\n\x08preKeyId\x18\x01 \x01(\r\x12\x16\n\x0esignedPreKeyId\x18\x06 \x01(\r\x12\x0f\n\x07\x62\x61seKey\x18\x02 \x01(\x0c\x12\x13\n\x0bidentityKey\x18\x03 \x01(\x0c\x12\x0f\n\x07message\x18\x04 \x01(\x0c"t\n\x12KeyExchangeMessage\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0f\n\x07\x62\x61seKey\x18\x02 \x01(\x0c\x12\x12\n\nratchetKey\x18\x03 \x01(\x0c\x12\x13\n\x0bidentityKey\x18\x04 \x01(\x0c\x12\x18\n\x10\x62\x61seKeySignature\x18\x05 \x01(\x0c"E\n\x10SenderKeyMessage\x12\n\n\x02id\x18\x01 \x01(\r\x12\x11\n\titeration\x18\x02 \x01(\r\x12\x12\n\nciphertext\x18\x03 \x01(\x0c"c\n\x1cSenderKeyDistributionMessage\x12\n\n\x02id\x18\x01 \x01(\r\x12\x11\n\titeration\x18\x02 \x01(\r\x12\x10\n\x08\x63hainKey\x18\x03 \x01(\x0c\x12\x12\n\nsigningKey\x18\x04 \x01(\x0c"E\n\x1c\x44\x65viceConsistencyCodeMessage\x12\x12\n\ngeneration\x18\x01 \x01(\r\x12\x11\n\tsignature\x18\x02 \x01(\x0c\x42\x35\n%org.whispersystems.libsignal.protocolB\x0cSignalProtos'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "WhisperTextProtocol_pb2", globals()
)
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = (
        b"\n%org.whispersystems.libsignal.protocolB\014SignalProtos"
    )
    _SIGNALMESSAGE._serialized_start = 41
    _SIGNALMESSAGE._serialized_end = 138
    _PREKEYSIGNALMESSAGE._serialized_start = 141
    _PREKEYSIGNALMESSAGE._serialized_end = 283
    _KEYEXCHANGEMESSAGE._serialized_start = 285
    _KEYEXCHANGEMESSAGE._serialized_end = 401
    _SENDERKEYMESSAGE._serialized_start = 403
    _SENDERKEYMESSAGE._serialized_end = 472
    _SENDERKEYDISTRIBUTIONMESSAGE._serialized_start = 474
    _SENDERKEYDISTRIBUTIONMESSAGE._serialized_end = 573
    _DEVICECONSISTENCYCODEMESSAGE._serialized_start = 575
    _DEVICECONSISTENCYCODEMESSAGE._serialized_end = 644
# @@protoc_insertion_point(module_scope)
