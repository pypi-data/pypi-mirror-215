__version__ = '0.9.3-1'
__user_agent__ = f"E620py/{__version__} (by mrcrabs)"
base_url = 'https://e621.net'

from .logging import main_log
from .api import E6Get, E6Post, ConnectionHandler
from . import exceptions
from . import objects
from . import downloader
class Client:
    def __init__(self, connection_handler = ConnectionHandler):
        
        self.ConnectionHandler = connection_handler
        self.Get = E6Get(self.ConnectionHandler)
        self.Post = E6Post(self.ConnectionHandler)
        
