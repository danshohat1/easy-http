from .enums import Statuses
from typing import Any, List, Dict,TypeVar, Optional
from .cors import Cors
from dataclasses import dataclass, field

Authorization = TypeVar("Authorization")

@dataclass()
class ResponseScheme:

    data: Any = None
    status: Statuses = Statuses.OK
    cookies: List[Dict[str, Any]] = field(default_factory=list)
    cors: Optional[Cors]= None
    
    
    def set_cookie(self, cookie: Dict[str, Any]) -> None:
        self.cookies.append(cookie)
    

    



    