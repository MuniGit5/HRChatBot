# James Shield HR Assistant

A simple RAG-based HR assistant that answers questions using **only** the company handbook documents. Uses OpenAI to summarize retrieved content into 2 sentences.

## Setup

1. Ensure `.env` has your OpenAI API key:
   ```
   OPENAI_API_KEY=your-key-here
   ```

2. Create/activate virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Build the vector store (run once):
   ```bash
   source .venv/bin/activate && python build_db.py
   ```
   Or: `.venv/bin/python build_db.py`

4. Run the app:
   ```bash
   source .venv/bin/activate && streamlit run app.py
   ```

## Features

- **5 Topics**: PTO & Vacation, Holidays, Benefits, Conduct & Ethics, Timekeeping
- **Pre-loaded questions**: Click a topic, then click the question to get the answer
- **Custom questions**: Ask any HR-related question
- **Handbook-only answers**: Answers are sourced only from documents in `data/` folder
- **Fallback**: If no relevant info found, directs users to contact HR directly

## Data

Documents are loaded from:
- `data/hr_docs/` - Main handbook
- `data/hr_extra/` - Policy documents (Vacation, Holidays, Benefits, Timekeeping, etc.)
