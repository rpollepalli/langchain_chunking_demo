from chunking.chunker import Chunker
import spacy

class SpacyChunker(Chunker):
    
    def chunk_text(self,text)-> list[str]:
       nlp = spacy.load('en_core_web_sm')
       doc = nlp(text)
       sentences = list(doc.sents)
       return sentences