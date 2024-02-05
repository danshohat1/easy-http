import json
import jwt
import datetime

class Send:
    
    @staticmethod
    def add_headers(func):
        def wrapper(**kwargs):

            response = f"HTTP/1.1 {kwargs['status']}\r\n"
            response += kwargs['cors'].generate_response()
            
            response += func(**kwargs)

            kwargs["client_socket"].sendall(response.encode())

            return response
        return wrapper

    @staticmethod
    @add_headers
    def send(**kwargs):
        """Send the HTTP response to the client."""
        result = kwargs.get("msg", "No data provided")

        # Check if cookies are provided in the response
        cookies = kwargs.get("cookies", [])

        print(result)
        # Include the result in the JSON response
        if cookies:
            response_body = {
                "data": result,
                "cookies": cookies
            }
        else:
            response_body = result 
        json_response = json.dumps(response_body)
        

        if isinstance(response_body, str):
            response = "Content-Type: text/html\r\n"
            response += f"Content-Length: {len(response_body)}\r\n\r\n"
            response += response_body
            return response
        
        response = "Content-Type: application/json\r\n"
        response += f"Content-Length: {len(json_response)}\r\n\r\n"  
        response += json.dumps(response_body)

        return response

    @staticmethod
    @add_headers
    def send_options(**kwargs):
        """Handle an OPTIONS request by responding with CORS headers."""
        return "options response"
