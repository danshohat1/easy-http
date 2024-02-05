from datetime import datetime, timedelta
import jwt

class JWTKey:

    def __init__(self, secret_key: str,  **kwargs):
        self.secret_key = secret_key
        for key, value in kwargs.items():
            setattr(self, key, value)   
        

    def __str__(self) -> str:

    
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=10)
        }

        for key, value in self.__dict__.items():
            if key != 'secret_key':
                payload[key] = value

        return jwt.encode(payload, self.secret_key, algorithm="HS256")

