#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 13:18:10 2025

@author: harshi
"""

from langchain_openai import OpenAIEmbeddings 
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from dotenv import load_dotenv
import streamlit as st
import os
import PyPDF2
from langchain.chains import ConversationalRetrievalChain

# Load from .env file
load_dotenv(dotenv_path='/Users/harshi/Documents/project/.env')
 
api_key = os.getenv("OPENAI_API_KEY")

# Specify the folder path
pdf_folder_path = "/Users/harshi/Documents/project/pdf_data"

# Initialize a variable to store the extracted text
raw_text = ""

# Loop through all PDF files in the specified folder
for file in os.listdir(pdf_folder_path):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder_path, file)

        # Read the PDF file
        pdf_reader = PyPDF2.PdfReader(pdf_path)
        for page in pdf_reader.pages:
            raw_text += page.extract_text()
# print("Raw_Text:",raw_text)

# Split the text into smaller chunks
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)
texts = text_splitter.split_text(raw_text)

# Check the content of the texts list
st.write("Number of text chunks:", len(texts))

# Download embeddings
embeddings = OpenAIEmbeddings(openai_api_key=api_key)

# Create the document search
docsearch = FAISS.from_texts(texts, embeddings)

# Create the conversational chain


qa = ConversationalRetrievalChain.from_llm(
    llm=OpenAI(
        model_name="text-davinci-003",
        openai_api_key=api_key,
    ),
    retriever=docsearch.as_retriever(),
    return_source_documents=True,
)
# Initialize chat history list
chat_history = []

# Get the user's query
query = st.text_input("Ask a question about the documents:")

# Add a generate button
generate_button = st.button("Generate Answer")

if generate_button and query:
    with st.spinner("Generating answer..."):
        result = qa({"question": query, "chat_history": chat_history})

        answer = result["answer"]
        # source_documents = result['source_documents']

        # Combine the answer and source_documents into a single response
        response = {
            "answer": answer,
            # "source_documents": source_documents
        }
        st.write("Response:", response)
