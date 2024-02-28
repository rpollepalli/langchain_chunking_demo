from langchain.embeddings import HuggingFaceEmbeddings
import time


class CustomHuggingFaceEmbeddings():
        
    def embed_documents(chunks)->any:
        start_time = time.perf_counter
        print(f"\t\t\tStarted the embed_documents the chunks ")
        embeddings = HuggingFaceEmbeddings()
        vectors=embeddings.embed_documents(chunks)
        end_time = time.perf_counter 
        #total_time= end_time-start_time
        print(f"\t\t\tEnded the embed_documents the chunks ")
        return vectors