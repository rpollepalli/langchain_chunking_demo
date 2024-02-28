from chunking.chunker import Chunker
import nltk


class NltkSentenceChunker(Chunker):
    def chunk_text(self,text)-> list[str]:
        sentences = nltk.sent_tokenize(text)
        return sentences