from langchain.document_loaders.image import UnstructuredImageLoader
from langchain.document_loaders import PyPDFLoader
import os
from filetype import guess
from time import perf_counter




"""function to detect the file type in the path. uses filetype.guess to detect file type"""
def detect_document_type(document_path):
    
    guess_file = guess(document_path)
    file_type = ""
    image_types = ['jpg', 'jpeg', 'png', 'gif']
    
    if(guess_file.extension.lower() == "pdf"):
        file_type = "pdf"
        
    elif(guess_file.extension.lower() in image_types):
        file_type = "image"
        
    else:
        file_type = "unkown"
        
    return file_type

"""function to extract content from files"""
def extract_file_content(file_path):
    start_time = perf_counter
    print(f"\t\t\tstarted reading the file from {file_path}")
    file_type = detect_document_type(file_path)
    #Based on file type respevtive document loader will be used
    if(file_type == "pdf"):
        loader = PyPDFLoader(file_path)     
    elif(file_type == "image"):
        loader = UnstructuredImageLoader(file_path)
        
    documents = loader.load()
    documents_content = '\n'.join(doc.page_content for doc in documents)
    end_time = perf_counter
    #total_time = (end_time+start_time)
    print(f"\t\t\tEnded reading the file")
    return documents_content