from typing import Union, List, Any
from .prompts import ExceptionPrompt, ExceptionTypes, WarningTypes, WarningPrompt
from .enums import HttpMethod
from urllib.parse import urlparse
import sys

class Cors:
    def __init__(
        self,
        trusted_urls: Union[List[str], str] = "*",
        allow_credentials: bool = True,
        allowed_methods: List[HttpMethod] = [member for member in HttpMethod],
        allowed_headers: List[str] = ["Content-Type", "Authorization"],
        max_age: int = 86400
    ) -> None:  
              
        self.check_param_type("trusted_urls", trusted_urls, (list, str), "must be a list of URLs or a string")
        self.check_param_type("allowed_methods", allowed_methods, list, "must be a list of HttpMethod values")
        self.check_param_type("allow_header", allowed_headers, list, "must be a list of strings")
        self.check_param_type("max_age", max_age, int, "must be an integer")
        self.check_param_type("allow_credentials", allow_credentials, bool, "must be a boolean (True or False)")
        
        if isinstance(trusted_urls, str):
            self.trusted_urls = [trusted_urls]
        elif "*" in trusted_urls and len(trusted_urls) > 1:
            print(WarningPrompt("'trusted urls' contains '*' and other urls, considering '*'", WarningTypes.TYPE))
            self.trusted_urls = ["*"]
        else:
            self.trusted_urls = trusted_urls

        self.allow_credentials = allow_credentials
        self.allowed_headers = allowed_headers
        self.max_age = max_age
        self.allowed_methods = allowed_methods

        self.check_urls()

    @classmethod
    def check_param_type(cls, param_name: str, param_value, expected_type, error_message: str):
        if not isinstance(param_value, expected_type):
            print(ExceptionPrompt(f"'{param_name}' {error_message}"))
            sys.exit()
    
    def is_valid_url(self, url):
        if url == "*":
            return True
        
        parsed_url = urlparse(url)
        return parsed_url.scheme in ("http", "https")

    def check_urls(self):
        if not all(self.is_valid_url(url) for url in self.trusted_urls):
            error_message = "Some URLs in 'trusted_urls' are not valid."
            print(ExceptionPrompt(error_message, ExceptionTypes.TYPE))
            sys.exit()

    @classmethod
    def join_header(cls, header: List[Any]):
        return ", ".join(header)
    
    def generate_response(self):

        if self.allow_credentials:
            response = "Access-Control-Allow-Credentials: true\r\n"
        else:
            response = "Access-Control-Allow-Credentials: false\r\n"
        
        response += f"Access-Control-Allow-Methods: {self.join_header([method.value for method in self.allowed_methods])}\r\n"
        response += f"Access-Control-Allow-Headers: {self.join_header(self.allowed_headers)}\r\n"
        response += f"Access-Control-Allow-Origin: {self.join_header(self.trusted_urls)}\r\n"
        response += f"Access-Control-Max-Age: {self.max_age}\r\n"

        return response