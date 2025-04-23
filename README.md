
# 📄 PDF Document Chatbot using LangChain & OpenAI

This project implements a document-based chatbot using **LangChain**, **OpenAI's text-davinci-003**, and **FAISS**. The chatbot processes PDF documents and allows users to ask natural language questions, returning contextually accurate answers based on the document content.

---

## 🧠 Features

- Reads multiple PDF documents from a specified folder.
- Extracts and preprocesses text using `PyPDF2`.
- Splits long documents into manageable chunks.
- Converts text into embeddings using OpenAI.
- Stores and searches text chunks using FAISS for fast retrieval.
- Handles user questions using LangChain’s `ConversationalRetrievalChain`.
- Displays results in a Streamlit interface with chat history support.

---

## 🛠️ Technologies Used

- Python
- LangChain
- OpenAI API (`text-davinci-003`)
- FAISS (Facebook AI Similarity Search)
- PyPDF2
- Streamlit
- python-dotenv

---

## 📂 Folder Structure

```
.
├── pdf_bot.py               # Main chatbot script
├── .env                     # Contains OpenAI API key
├── pdf_data/                # Folder for storing input PDF files
```

---

## ⚙️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/pdf-chatbot.git
cd pdf-chatbot
```

### 2. Install the required packages
```bash
pip install -r requirements.txt
```

### 3. Add your OpenAI API Key
Create a `.env` file and add:
```
OPENAI_API_KEY=your_openai_key
```

### 4. Add PDF files
Put your PDF files inside the `pdf_data/` directory.

### 5. Run the Streamlit app
```bash
streamlit run pdf_bot.py
```

---

## 💬 Sample Questions to Ask

- What is a sensor fusion?
- What is BMS?
- What are the types of BMS?
- What are the Sensor fusion use cases?

---

### 🙌 Thank You
Thank you for exploring this project!
