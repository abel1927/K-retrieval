from abc import ABC, abstractmethod

class Index(ABC):

    @abstractmethod
    def add_source(self, new_path:str)-> None:
        """ Indexa los documentos presentes en new_path"""

    @abstractmethod
    def get_rank(self, query:str) -> list:
        """ Devuelve los resultados relevantes para la consulta"""

    @abstractmethod
    def get_indexed_terms_count(self) -> int:
        """ Devuelve la cantidad de términos indexados"""

    @abstractmethod
    def get_indexed_docs_count(self) -> int:
        """ Devuelve la cantidad de documentos indexados"""

    @abstractmethod
    def get_indexed_terms(self) -> list[str]:
        """ Devuelve la lista de términos indexados"""

    @abstractmethod
    def get_indexed_docs(self) -> list[str]:
        """ Devuelve la lista de documentos indexados"""

    @abstractmethod
    def clean(self) -> list[str]:
        """ Vacía la colección"""