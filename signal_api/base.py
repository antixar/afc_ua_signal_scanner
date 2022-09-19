from .http_client import HttpClient
from .store import Store
from .utils import Logger


class Base(Logger):
    client = HttpClient
    store = Store()