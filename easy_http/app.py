from .server import Server
from .route import Route
from .models import Response
from socket import socket 
from typing import Tuple
from .enums import HttpMethod
from typing import Optional
from .authorization import Authorization
from .cors import Cors
from .prompts import Prompt

DEFAULTPORT = 8000
WELCOMEMESSAGE = """
Welcome to Your HTTP Server!

Your server is up and running.

You can access it by sending http requests to http://localhost:{port}/

Happy coding!
"""

class App(Server):
    def __init__(self, port: int = DEFAULTPORT, authorization: Authorization = None, cors: Cors = Cors()):
        super().__init__(port)
        self.port=  port
        self.routes = {}
        self.authorization = authorization
        self.cors = cors

    def run(self) -> None:
        # run the http server
        super().run()
        print(Prompt(WELCOMEMESSAGE.format(port=self.port), include_date = False))

    def route(self, method: HttpMethod = HttpMethod.GET, path: str = "/", authorization: Optional[Authorization] = None):
        if not authorization:
            authorization = self.authorization

        def wrapper(func):

            route = Route(func, method, path, authorization)
            self.routes[route] = route.func
        return wrapper

    def handle_single_client(self, client: socket, addr: Tuple[str, int]) -> None:
        """Handle a single client connection by creating an instance of the Http_Handler class."""
        # Create an instance of the Http_Handler class to handle HTTP requests from the client
        Response(self, client, addr, self.cors)
        self.cors = Cors()


        