import jwt
from typing import Union, Dict, Callable, Optional
from datetime import datetime, timedelta
from ..response_scheme import ResponseScheme
import secrets
from .jwt_key import JWTKey
import inspect

SECRET_KEY = "hey_you_found_me"

class Authorization:
    def __init__(self, true_case: Callable = lambda arg: None, false_case: Callable = lambda: None) -> None:
  
        if len(inspect.signature(true_case).parameters) != 1:
            raise TypeError(f"The true_case function must have one parameter (dict type). got {len(inspect.signature(true_case).parameters)}")

        if len(inspect.signature(false_case).parameters) != 0:
            raise TypeError(f"The false_case function must have no parameters. got {len(inspect.signature(true_case).parameters)}")

        self.true_case = true_case
        self.false_case = false_case
        self.secret_key = secrets.token_hex(32)

    def token(self, **kwargs) -> str:
        for key in kwargs.keys():
            if key == "exp":
                raise Exception("'exp' is not a valid name for token arg.")
            
        return str(JWTKey(self.secret_key, **kwargs))
    
    def false_res(self) -> bool: 
        res =  self.false_case()
        if isinstance(res, ResponseScheme):
            return res
    
    def true_res(self, data) -> bool:
        res =  self.true_case(data)
        if isinstance(res, ResponseScheme):
            return res
    
    def check_authorization(self, key) -> Optional[ResponseScheme]: 
        try:
            decoded_token = jwt.decode(str(key), self.secret_key, algorithms=["HS256"])
            expiration_time = datetime.utcfromtimestamp(decoded_token["exp"])
        
            if datetime.utcnow() > expiration_time:
            
                return self.false_res()
            
        
            return self.true_res(dict([(key, val) for key, val in decoded_token.items() if key != "exp"]))
        
        except:
            return self.false_res()


        

