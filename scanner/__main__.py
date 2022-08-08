from protos import WhisperTextProtocol_pb2 as text_protocol

test = text_protocol.SignalMessage()
test.ratchetKey = b'aaaaa'
test.counter = 1
test.previousCounter = 2
test.ciphertext = b'bbbbb'

with open('out.bin', 'wb') as f:
    f.write(test.SerializeToString())