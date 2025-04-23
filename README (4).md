# 🧠 PDF Chatbot with LangChain & OpenAI

## 📘 Overview

This project demonstrates a document-based **chatbot** using **LangChain**, **OpenAI**, and **FAISS**, designed to comprehend PDF documents and answer user questions through natural language queries. The application utilizes OpenAI's language models and FAISS vector search for document retrieval, enabling accurate and contextual responses.

---

## 🚀 Features

- 📄 Reads and processes multiple PDF files.
- 🧩 Splits documents into manageable text chunks.
- 🧠 Converts text into embeddings using OpenAI.
- 🔍 Performs document similarity search with FAISS.
- 🤖 Handles question-answering with conversational memory.
- 💬 Provides real-time Q&A interface using **Streamlit**.

---

## 🧱 Project Structure

```
.
├── pdf_bot.py               # Main chatbot implementation
├── .env                     # Contains your OpenAI API Key
├── pdf_data/                # Folder with input PDF documents
```

---

## ⚙️ How It Works

1. **Document Ingestion**  
   PDF files are loaded from a specified folder using `PyPDF2`.

2. **Text Preprocessing**  
   Text is split into chunks using `CharacterTextSplitter` from LangChain.

3. **Embedding Generation**  
   Chunks are embedded into vector representations using `OpenAIEmbeddings`.

4. **Vector Store**  
   FAISS is used to store and retrieve similar document chunks efficiently.

5. **Question Answering**  
   `ConversationalRetrievalChain` handles context-aware Q&A using OpenAI's LLM.

6. **Streamlit UI**  
   Simple interface for querying the chatbot.

---

## 💡 Technologies Used

- `LangChain`
- `OpenAI (text-davinci-003)`
- `FAISS`
- `PyPDF2`
- `Streamlit`
- `dotenv`

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/pdf-chatbot.git
cd pdf-chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt` (example)**:
```text
langchain
openai
faiss-cpu
streamlit
python-dotenv
PyPDF2
```

### 3. Add API Key

Create a `.env` file in the root directory and add:

```
OPENAI_API_KEY=your_openai_api_key
```

### 4. Add PDF Files

Place your PDF documents inside the `/pdf_data/` directory.

### 5. Run the App

```bash
streamlit run pdf_bot.py
```

---

## ✅ Sample Questions

- *What is Sensor Fusion?*
- *Explain BMS and its types.*
- *What are the use cases of Sensor Fusion?*

---

## 📌 Interview/Academic Notes

- Implemented using **Conversational Retrieval Chains** with memory support.
- Used **vector similarity** over traditional keyword matching.
- Ensures contextual accuracy using **OpenAI’s powerful LLM**.
- Designed with modularity for extensibility (e.g., switch to BERT embeddings or UI enhancements).

---

## 📧 Contact

Maintained by **Harshitha**.  
For queries, feel free to reach out via [your-email@example.com].