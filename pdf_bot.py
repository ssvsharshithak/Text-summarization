#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Q&A Bot - Streamlit Application
Created on Sat Apr 19 13:18:10 2025
@author: harshi
"""

import streamlit as st
import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
import PyPDF2
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
MODEL_NAME = "gpt-4o-mini"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MAX_FILE_SIZE_MB = 50
RATE_LIMIT_QUESTIONS = 20  # per hour
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1  # seconds

# Load environment
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Page configuration
st.set_page_config(page_title="PDF Q&A Bot", layout="wide")
st.title("📄 PDF Question & Answer Bot")

# Validate API key
if not API_KEY:
    st.error("❌ API key not found! Please add OPENAI_API_KEY to .env file")
    st.stop()

# Initialize session state for rate limiting
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if "query_timestamp" not in st.session_state:
    st.session_state.query_timestamp = datetime.now()





def validate_file(_file):
    """Validate uploaded file"""
    # Check file size
    file_size_mb = _file.size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        return False, f"File too large ({file_size_mb:.1f}MB > {MAX_FILE_SIZE_MB}MB)"
    
    # Check file type
    if _file.type != "application/pdf":
        return False, "Only PDF files are supported"
    
    return True, "OK"


def check_rate_limit():
    """Check if user exceeded rate limit"""
    current_time = datetime.now()
    time_diff = current_time - st.session_state.query_timestamp
    
    # Reset counter if over an hour
    if time_diff > timedelta(hours=1):
        st.session_state.query_count = 0
        st.session_state.query_timestamp = current_time
    
    if st.session_state.query_count >= RATE_LIMIT_QUESTIONS:
        return False, f"Rate limit exceeded! Max {RATE_LIMIT_QUESTIONS} questions per hour. Please wait."
    
    return True, "OK"


def call_with_retry(func, *args, **kwargs):
    """Call function with retry logic"""
    for attempt in range(RETRY_ATTEMPTS):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt < RETRY_ATTEMPTS - 1:
                wait_time = RETRY_DELAY * (attempt + 1)
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"All {RETRY_ATTEMPTS} attempts failed: {e}")
                raise


@st.cache_resource
def load_and_process_pdfs(pdf_files=None):
    """Load and process PDFs with caching and retry logic"""
    try:
        raw_text = ""
        processed_files = []
        invalid_files = []
        
        # Process uploaded files only
        if not pdf_files:
            return None, [], 0, []
        
        for pdf_file in pdf_files:
            try:
                # Validate file
                is_valid, message = validate_file(pdf_file)
                if not is_valid:
                    invalid_files.append(f"{pdf_file.name}: {message}")
                    continue
                
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    raw_text += page.extract_text()
                processed_files.append(pdf_file.name)
            except Exception as e:
                logger.error(f"Error processing {pdf_file.name}: {e}")
                invalid_files.append(f"{pdf_file.name}: {str(e)}")
        
        if invalid_files:
            for error in invalid_files:
                st.warning(f"⚠️ {error}")
        
        if not raw_text.strip():
            st.error("❌ No text could be extracted from PDFs")
            return None, [], 0, invalid_files
        
        # Split text into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
        )
        texts = text_splitter.split_text(raw_text)
        
        # Create embeddings and vector store with retry
        def create_embeddings():
            embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)
            return FAISS.from_texts(texts, embeddings)
        
        docsearch = call_with_retry(create_embeddings)
        
        return docsearch, processed_files, len(texts), invalid_files
    except Exception as e:
        logger.error(f"Error loading PDFs: {e}")
        st.error(f"❌ Error processing PDFs: {e}")
        return None, [], 0, [str(e)]


@st.cache_resource
def create_qa_chain(_docsearch):
    """Create QA chain with caching"""
    if _docsearch is None:
        return None
    
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(
            model=MODEL_NAME,
            openai_api_key=API_KEY,
            temperature=0.1,
        ),
        retriever=_docsearch.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,
    )
    return qa


# Sidebar - File management and settings
with st.sidebar:
    st.header("📁 Document Management")
    
    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help=f"Upload one or more PDF files (max {MAX_FILE_SIZE_MB}MB each)"
    )
    
    if uploaded_files:
        st.info(f"✓ {len(uploaded_files)} file(s) uploaded")
    



# Main content
st.subheader("Document Processing")

# Load PDFs
if uploaded_files:
    docsearch, processed_files, num_chunks, invalid_files = load_and_process_pdfs(uploaded_files)
else:
    docsearch, processed_files, num_chunks, invalid_files = None, [], 0, []

if docsearch:
    st.success(f"✓ Processed {len(processed_files)} document(s) with {num_chunks} text chunks")
    
    with st.expander("📋 Processed Files"):
        for file in processed_files:
            st.write(f"• {file}")
        if invalid_files:
            st.warning("Failed to process:")
            for error in invalid_files:
                st.write(f"• {error}")
    
    # Create QA chain
    qa = create_qa_chain(docsearch)
    
    if qa:
        # Initialize chat history in session state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Chat interface
        st.subheader("💬 Ask Questions")
        
        # Rate limit check
        is_allowed, limit_msg = check_rate_limit()
        if not is_allowed:
            st.warning(f"⚠️ {limit_msg}")
        
        col1, col2 = st.columns([4, 1])
        with col1:
            query = st.text_input(
                "Ask a question about your documents:",
                key="query_input",
                placeholder="Type your question here...",
                disabled=not is_allowed
            )
        with col2:
            generate_button = st.button("🔍 Ask", key="ask_button", disabled=not is_allowed)
        
        if generate_button and query:
            if not is_allowed:
                st.error(" Rate limit exceeded!")
            else:
                with st.spinner("Generating answer..."):
                    try:
                        def get_answer():
                            return qa({
                                "question": query,
                                "chat_history": st.session_state.chat_history
                            })
                        
                        result = call_with_retry(get_answer)
                        
                        answer = result["answer"]
                        st.session_state.chat_history.append((query, answer))
                        
                        # Display answer
                        st.markdown("### Answer:")
                        st.write(answer)
                        
                        # Display source documents
                        if result.get("source_documents"):
                            with st.expander(f"📚 Source Documents ({len(result['source_documents'])})"):
                                for i, doc in enumerate(result["source_documents"][:3], 1):
                                    st.write(f"**Document {i}:**")
                                    st.write(doc.page_content[:500] + "...")
                    
                    except Exception as e:
                        logger.error(f"Error generating answer: {e}")
                        st.error(f"❌ Error: {e}")
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("---")
            st.subheader(f"📝 Chat History ({len(st.session_state.chat_history)})")
            for i, (q, a) in enumerate(st.session_state.chat_history, 1):
                with st.expander(f"Q{i}: {q[:50]}..."):
                    st.write(f"**Q:** {q}")
                    st.write(f"**A:** {a}")
else:
    st.warning("⚠️ Please upload PDF files to get started")
    st.info("👉 Upload PDFs using the file uploader in the sidebar")
