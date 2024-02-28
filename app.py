
from rag.llm.customllm import default_llm

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain.vectorstores.pgvector import PGVector
from pgvector.psycopg2 import register_vector
import psycopg2
from configparser import ConfigParser, Error
from dotenv import load_dotenv
import os
import streamlit as st
import requests
import pandas as pd
import numpy as np


def init():
    load_dotenv()
    
def startUI():
    #st.session_state["user_input"] = st.text_input(label="Enter a question :")
    #st.header('This is a header with a divider', divider='rainbow')
   
    #st.title('_Generative AI_ :blue[Rocks] :sunglasses:')
    st.header('Welcome to clustering adjacent sentences chunking stratergy demo', divider='blue')   
    st.text(" ")
    st.text(" ")
    st.text(" ")
       
    user_input = st.text_input(label="Enter a prompt :")
    
    option = st.selectbox(
   "Select chunking stratergy : ",
   ("Clustering adjacent", "Fixed Length"),
   index=None,
   placeholder="Select chunking stratergy...",
)

    st.button("Submit", on_click=on_submit, args=(user_input,option))
    
    #question = "what is the topography of Jacksonville,FL?"
    
    

def on_submit(userinput, option):
    #question = "what is the topography of Jacksonville,FL?"
    question = userinput
    print(question)
    template = """Instructions: Use only the following context to answer the question.

    Context: {context}
    Question: {question}
    """
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    from langchain.embeddings import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings()
    
    
    col_name=os.environ["COLLECTION_NAME"]
    
    if(option ==  'Fixed Length'):
        col_name=os.environ["FXL_COLLECTION_NAME"]        
    elif(option ==  ''):
        col_name=os.environ["COLLECTION_NAME"]
    print(option)
    print(col_name)
    
    db = PGVector(
        collection_name=col_name,
        connection_string=os.environ["CONNECTION_STRING"],
        embedding_function=embeddings,
    )
    
    print("Iam here 2")
    retriever = db.as_retriever(search_kwargs={'k': 1})  # default 4

    print("Iam here 3")

    # llm = CustomLLM()
    llm = default_llm
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
  
    answer = chain.invoke(question)
    st.write(str(answer))

if __name__ == "__main__":
    init()
    startUI()