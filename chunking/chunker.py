from abc import ABC, abstractmethod

class Chunker(ABC):
    """
    Interface for product types
    """

    @abstractmethod
    def chunk_text(self,text)-> list:
        pass