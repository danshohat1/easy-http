from enum import Enum

class Statuses(Enum):
    # Enumeration for HTTP status codes
    OK = "200 OK"
    NOT_FOUND = "404 Not Found"
    UNAUTHORIZED = "403 Unauthorized"

class HttpMethod(Enum):
    # Enumeration for HTTP methods

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"

    @staticmethod
    def get_method(method: str) -> "HttpMethod":
        """
        Get the corresponding HttpMethod enum from a string representation of an HTTP method.

        Parameters:
        - method (str): String representation of an HTTP method.

        Returns:
        - HttpMethod: Corresponding HttpMethod enum.
        """
        try: 
            return next(_method for _method in HttpMethod if _method.value == method.upper())
        except StopIteration:
            return None