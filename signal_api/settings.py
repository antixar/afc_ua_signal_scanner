import os

TEXT_SECURE_HTTP_TIMEOUT = 10

# TEXT_SECURE_WEBSOCKET_API = os.environ.get("TEXT_SECURE_WEBSOCKET_API", "wss://textsecure-service.whispersystems.org/v1/websocket/")
TEXT_SECURE_WEBSOCKET_API = os.environ.get(
    "TEXT_SECURE_WEBSOCKET_API", "wss://chat.signal.org/v1/websocket/"
)

TEXT_SECURE_SERVER_URL = os.environ.get(
    #   "TEXT_SECURE_SERVER_URL", "https://textsecure-service.whispersystems.org/",
    "TEXT_SECURE_SERVER_URL", "https://chat.signal.org/"
)

# openssl s_client -showcerts -servername textsecure-service.whispersystems.org -connect textsecure-service.whispersystems.org:443 </dev/null
