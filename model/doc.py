
class Doc:

    def __init__(self, name:str, path:str, first_300:str, extension:str) -> None:
        self._name = name
        self._extension = extension
        self._path = path
        self._fist_300 = first_300

    def __str__(self) -> str:
        return self._name

    def name(self)-> str:
        return self._name
    
    def extension(self)-> str:
        return self._extension

    def path(self)-> str:
        return self._path

    def first_300(self)-> str:
        return self._fist_300