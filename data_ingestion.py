from input.extract_raw_data import extract_file_content
from data.database import checkDBConnection, connect_to_db, data_ingestion
from embeddings.embedder import CustomHuggingFaceEmbeddings
from chunking.chunking_service import ChunkingService
import time
import argparse


def ingest_data(file_path, chuking_type, table_name):
    start_time = time.perf_counter
    print(f"Started the ingest_data process ")
    documents_content = extract_file_content(file_path)    
    chunkingService = ChunkingService(chuking_type,documents_content)
    chunks = chunkingService.chunking()
    #print(chunks[0])
    vectors = CustomHuggingFaceEmbeddings.embed_documents(chunks)
    #print(vectors[0])
    data_ingestion(chunks,vectors)
    
    end_time = time.perf_counter
    #total_time = (end_time-start_time)
    print(f"Ended the ingest_data process ")

"""main function"""
if __name__ == "__main__":
    file_path = "./Jacksonville_FL.pdf"
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str)
    parser.add_argument('--chunking_type', type=str)
    parser.add_argument('--table_name', type=str)
    args = parser.parse_args() 
    ingest_data(args.file_path.strip(),args.chunking_type.strip(),args.table_name.strip())
    #checkDBConnection()
   