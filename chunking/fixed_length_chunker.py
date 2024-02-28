from chunking.chunker import Chunker
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time


class FixedLengthChunker(Chunker):
    """
    Implimentation of the interface Chunker
    """

    def chunk_text(self,text)-> list[str]:
        start_time = time.perf_counter
        print(f"\t\t\tStarted the chunking the text ")
        # Initialize the text splitter with custom parameters
        custom_text_splitter_n = RecursiveCharacterTextSplitter(
            # Set custom chunk size
            chunk_size = 300,
            chunk_overlap  = 30,
            # Use length of the text as the size measure
            length_function = len,
            # Use only "\n\n" as the separator
            separators = ['\n']

        )       
        # Create the chunk    
        final_texts= custom_text_splitter_n.split_text(text)
        end_time = time.perf_counter
        
        print(f"\t\t\tEnded the chunking the text ")
        return final_texts