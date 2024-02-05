import datetime
from enum import Enum
from colorama import Fore, Style, init
from .enums import HttpMethod, Statuses


"""
prompts to the user

-- response prompts: probably will take a response scheme obj
-- warning prompts
-- openning and closing server: regular prompts

"""
init(autoreset=True)

class WarningTypes(Enum):
    RUNTIME = "Run Time"
    TYPE = "Type"

class ExceptionTypes(Enum):
    TYPE = "Type"
    RUNTIME = "Run Time"


class PromptDate:
    def __init__(self) -> None:
        self.current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self) -> str:
        return f"[{self.current_time}]"

class Prompt:
    def __init__(self, content:str, include_date: bool = True) -> None:
        self.content = content
        self.inclue_date = include_date

        self.date = PromptDate()
    
    @staticmethod
    def colored_prompt(prompt_text: str, color: Fore) -> str:
        return f"{color}{prompt_text}{Style.RESET_ALL}"
    
    def __str__(self) -> str:
        if isinstance(self, (WarningPrompt, ExceptionPrompt)) or not self.inclue_date:
            return self.content
        if isinstance(self, ResponsePrompt):
            content = self.colored_prompt(prompt_text=self.content, color = Fore.CYAN) if self.status == Statuses.OK else  self.colored_prompt(prompt_text=self.content, color = Fore.RED) 
            return f"{self.date} '{content}'"

        return f"{self.date} {self.content}"


class WarningPrompt(Prompt):
    def __init__(self, content:str, type: WarningTypes) -> None:
        
        content = self.colored_prompt(f"{type.value} Warning: ", Fore.YELLOW) + content
        super().__init__(content)

class ResponsePrompt(Prompt):

    def __init__(self, status: Statuses, method: HttpMethod, ip: str, path: str, version: str = "HTTP/1.1") -> None:
        super().__init__(method.value+ " " +path + " " + version)
        self.ip = ip
        self.method = method
        self.path = path
        self.status = status

    
    def __str__(self) -> str:
        return f"{self.ip} - - {super().__str__()} {self.status.value} -"


class ExceptionPrompt(Prompt):
    def __init__(self, exception_message: str, type: ExceptionTypes) -> None:
        content = self.colored_prompt(f"{type.value} Exception: ", Fore.RED) + exception_message 
        self.type = type
        super().__init__(content)


         
