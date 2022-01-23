from abc import ABC, abstractmethod
from typing import Dict

class Index(ABC):

    @abstractmethod
    def add_source(self, new_path:str)-> int:
        """ Indexa los documentos presentes en source_path"""

    @abstractmethod
    def get_rank(self, query:str) -> list:
        """ Devuelve los resultados relevantes para la consulta"""

    @abstractmethod
    def get_sources(self) -> list[str]:
        """ Devuelve las rutas presentes en la colección"""

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
    def clean(self):
        """ Vacía la colección"""

    @abstractmethod
    def get_stats(self) -> Dict:
        """ Devuelve estadisticas de la colección """