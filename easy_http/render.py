
class Render:
    def __init__(self, path: str, **kwargs) -> None:
        self.path = path
        self.kwargs = kwargs
    

    def render(self) -> str:
        with open(self.path, "r") as f:
            content = f.read()
            for key, value in self.kwargs.items():
                content = content.replace(f"{{{{{key}}}}}", str(value))
            return content
