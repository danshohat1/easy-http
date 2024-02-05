from .enums import HttpMethod
from typing import Optional
from .authorization import Authorization

class Route:
    # Class to define routes and associate them with corresponding functions

    def __init__(self,func, method: HttpMethod = HttpMethod.GET, path: str = "/", authorization: Optional[Authorization] = None) -> None:
        """
        Initialize a new Route insatance.

        Parameters:
        - method (HttpMethod): The HTTP method associated with the route (default is GET).
        - path (str): The path associated with the route (default is "/").
        """
        self.method = method
        self.path = path
        self.authorization = authorization
        self.func = func

        if self.authorization and self.method != HttpMethod.POST:
            raise Exception("Authorization must be in POST method")
