from .request import Request
from socket import socket
from typing import List, Tuple, TypeVar, Union
from ..route import Route
from ..enums import Statuses
from .send import Send
from ..response_scheme import ResponseScheme
import warnings
from ..prompts import ResponsePrompt, ExceptionPrompt, ExceptionTypes
from ..cors import Cors
import sys
from ..render import Render

AUTHORIZATION_REQUEST_PARAM = "authorization_key"

App = TypeVar("App")

class Response(Request, Send):
    def __init__(self, app: App, client_socket: socket, addr: Tuple[str, int], cors: Cors):
        self.client_socket = client_socket
        self.origin = addr[0]
        self.app = app
        self.cors = cors

        super().__init__(client_socket)
        if not self.details:
            return
        self.handle_http_request()


    def handle_http_request(self):
        """Validate the HTTP request and handle it accordingly."""
        if self.details["method"].value == "OPTIONS":
            response = ResponseScheme()
            self.handle_cors(response)
            self.send(client_socket = self.client_socket, msg = response.data, status = response.status.value, cookies = response.cookies, cors = self.cors)
            return
        
        route : List[Route] = list(filter(lambda route: route.path == self.details["path"] and route.method == self.details["method"], self.app.routes.keys()))

        if route  == []:
            response = ResponseScheme()
            response.status = Statuses.NOT_FOUND

            self.send_prompt(response)
            return 
        
        route = route[0]
        if route.authorization:
            key = [val for key, val in self.details["data"].items() if key.lower() == AUTHORIZATION_REQUEST_PARAM]

            if not key:
                print(ExceptionPrompt("Route with authorization must have an authorization key in the params", ExceptionTypes.RUNTIME))
                sys.exit()

            key = key[0]

            response = route.authorization.check_authorization(key)
            if response:
                self.send_prompt(response)
                return 


        self.call_route(route)       
    
    def handle_cors(self, response: ResponseScheme) -> None:
        if response.cors: 
            self.cors = response.cors

    def send_prompt(self, response: Union[ResponseScheme, Render]) -> None:
        if isinstance(response, Render):
            response = ResponseScheme(data=response.render())

        self.handle_cors(response)
        self.send(client_socket = self.client_socket, msg = response.data, status = response.status.value, cookies = response.cookies, cors = self.cors)
        print(ResponsePrompt( response.status, self.details["method"], self.origin, self.details["path"]))
        

    def call_route(self, route):
        try: 
            route = self.app.routes.get(route)
            response = route(*(self.details["query_params"] + [value for key, value in self.details["data"].items() if key.lower() != AUTHORIZATION_REQUEST_PARAM]))
            self.send_prompt(response)
        except Exception as e:
            print(e) 
            warnings.warn(f"{route.__name__} should return a ResponseScheme type", RuntimeWarning)

            response = ResponseScheme()
            self.send_prompt(response)
