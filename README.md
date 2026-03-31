
# PDF Q&A Bot

Upload PDFs and ask questions about them using OpenAI's GPT-4o-mini and LangChain.

## Features

- Upload PDFs and ask natural language questions
- AI-powered answers with source document references
- Chat history within sessions
- Rate limiting and file validation
- Automatic retry logic for API calls

## Tech Stack

- Python 3.9+
- LangChain + OpenAI API
- FAISS for vector search
- Streamlit for web UI

## Setup

1. Clone and navigate to the project:
```bash
cd Text-summarization
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=sk-your-key-here
```

Get your key at https://platform.openai.com/api-keys

5. Run the app:
```bash
streamlit run pdf_bot.py
```

Open `http://localhost:8501` in your browser.

## Usage

1. Upload PDFs in the sidebar
2. Ask questions about your documents
3. View answers with source references
4. Chat history persists during your session

## Limits

- 20 questions per hour
- 50MB max file size
- PDF files only

## License

MIT
