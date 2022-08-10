from typing import TypeVar, Type, Iterator
import websockets, ssl, pathlib, socket, time
import asyncio, string
from websockets.exceptions import InvalidHandshake
import logging
from websockets.legacy.client import WebSocketClientProtocol
from .protos import  WebSocketResources_pb2 as ws_resources
from random import randint
import base64, random, json

T = TypeVar('T', bound='Listener')
LOGGER = logging.getLogger(__name__)
PING_TIMEOUT = 5.0


def generateRegistrationID():
	return randint(1, 2^32) & 0x3fff

def generatePassword():
    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
    return base64.b64encode(bytes(password, 'utf-8'))







class Listener:
    def __init__(self):
        self.__ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        pem_file = pathlib.Path(__file__).with_name("cert.pem")
        self.__ssl_context.load_verify_locations(pem_file)
        
        self.__in_queue = asyncio.Queue()
        self.__out_queue = asyncio.Queue()
        
        

    async def __ping_pong(self, ws: WebSocketClientProtocol):
        
        while True:
            t0 = time.perf_counter()
            
            pong_waiter = await ws.ping()
            await pong_waiter
            await asyncio.sleep(PING_TIMEOUT)
            t1 = time.perf_counter()
            LOGGER.warning("aaaa Connection latency: %.3f seconds" % (t1 - t0))
    
    async def start(self):
        queue = asyncio.Queue()
    
    async def __listen(self, ws: WebSocketClientProtocol):
        LOGGER.warning("start to listen...")
        async for msg in ws:
             LOGGER.warning(msg)

    
    async def listen(self, ws_link: str, **kwargs: dict) -> Iterator:
        headers = {
            "User-Agent": "Signal-Desktop/1.2.3",
        }
        
        req_test = {
            "message": {
                "number": "+3806311111111",
                "password": "TTNHRE5WUzUyNkQwRERISw==",
                # "captcha": "test",
                "use_voice": False,
            },
            "type": 100
        }
        
        req2 = {
            "request": req_test,
            "type": 10,
            
        }
        raise Exception(json.dumps(req2))
        # ws_link += "?login=test&password=test"
        try:
            async with websockets.connect(ws_link, ssl=self.__ssl_context) as ws:
                asyncio.ensure_future(self.__ping_pong(ws))
                asyncio.ensure_future(self.__listen(ws))
                await asyncio.sleep(1)
                test = ws_resources.WebSocketMessage()
                test.type = ws_resources.WebSocketMessage.Type.REQUEST
                
                

#	registerMessage := &CrayfishWebSocketRequest_REGISTER_MESSAGE{
#		Number:   phoneNumber,
#		Password: registrationInfo.Password,
#		Captcha:  captcha,
#		UseVoice: false+,
#	}
#	messageType := CrayfishWebSocketMessage_REQUEST
#	requestType := CrayfishWebSocketRequestMessageTyp_START_REGISTRATION
#	request := &CrayfishWebSocketRequestMessage{
#		Type:    &requestType,
#		Message: registerMessage,
#	}
#	registerRequestMessage := &CrayfishWebSocketMessage{
#		Type:    &messageType,
#		Request: request,
#	}
#	m, err := json.Marshal(registerRequestMessage)
#	if err != nil {
#		return err
#	}
#	log.Debugf("[textsecure-crayfish-ws] Registering via crayfish send")
#	c.wsconn.send <- m
#	return nil

                
                
                
                req = ws_resources.WebSocketRequestMessage(
                    # optional string verb    = 1;
                    # optional string path    = 2;
                    # optional bytes  body    = 3;
                    # repeated string headers = 5;
                    # optional uint64 id      = 6;

                 )
                # test.request.id = 12345 
                test.request.path = "/v1/keepalive"
                # test.request.body=b'aaaaaa'
                # raise Exception(test.SerializeToString())
                # await ws.send(test.SerializeToString())
                await ws.send(json.dumps(req2))
                LOGGER.warning("AAAAA")
                #await ws.send(b'aaaaaa')
                await asyncio.sleep(30)
                # async for msg in ws:
                #    LOGGER.warning(f"AAAAAAA {msg}")
                yield "test"
                # 
                
                
                    
                
                
        except (socket.gaierror, InvalidHandshake) as exc:
            print(ws_link, str(exc))
            raise
            
    async def send(self, msg):
        await self.__in_queue.put(msg)
