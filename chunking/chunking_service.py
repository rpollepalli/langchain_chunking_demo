from abc import ABC, abstractmethod
from chunking.fixed_length_chunker import FixedLengthChunker
from chunking.clustering_chunker import ClusteringChunker
from chunking.kmeans_chunker import KmeansChunker
from chunking.nltk_sentence_chunker import NltkSentenceChunker
from spacy_chunker import SpacyChunker


class ChunkingService():
    
    """
    Chunking service which is extended by specific chunking method classes
    """

    def __init__(self, chunkertype,text ):
       
        self.chunkertype=chunkertype
        self.text=text
        

    @abstractmethod
    def chunk_text(self,text)->list[str]:
        pass

    def factory_method(self):
        """
        Factory method returning object of the class based on the chunker type
        """
        print(f"\t\t\tChecking the chunkerType {self.chunkertype} ")
        
        if self.chunkertype=='FixedLength':
            print("\t\t\treturning FixedLengthChunkingService ")
            return FixedLengthChunkingService(self.chunkertype, self.text)
        elif self.chunkertype=='Clustering':
            return ClusteringChunkingService(self.chunkertype, self.text)
        elif self.chunkertype=='kmeans':
            return KmeansChunkingService(self.chunkertype, self.text)
        elif self.chunkertype=='nltk':
            return NltkSentenceChunkingService(self.chunkertype, self.text)
        elif self.chunkertype=='spacy':
            return SpacyChunker(self.chunkertype, self.text)
      
        
    
    def chunking(self)-> list[str]:
        
        #print(self.chunkertype)
       
        # calling factory to fetch the right chunker
        service = self.factory_method()
        return service.chunk_text()
    
    
class FixedLengthChunkingService(ChunkingService):    
    
    def chunk_text(self)->list[str]:
        return FixedLengthChunker().chunk_text(self.text)

class ClusteringChunkingService(ChunkingService):
    
    def chunk_text(self)->list[str]:
        return ClusteringChunker().chunk_text(self.text)
    
class KmeansChunkingService(ChunkingService):
    
    def chunk_text(self)->list[str]:
        return KmeansChunker().chunk_text(self.text)
    
class NltkSentenceChunkingService(ChunkingService):
    
    def chunk_text(self)->list[str]:
        return NltkSentenceChunker().chunk_text(self.text)
    
class SpacyChunkingService(ChunkingService):
    
    def chunk_text(self)->list[str]:
        return SpacyChunker().chunk_text(self.text)
    