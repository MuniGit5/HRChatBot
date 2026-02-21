# James Shield HR Assistant – Project Documentation

## Codebase Location & Access

**Where is the code stored?**
- **GitHub**: https://github.com/MuniGit5/HRChatBot
- **Live app**: https://hrchatbot-nw8tafwepqhnswzccneyzk.streamlit.app/

**How do I get access to the full codebase?**
```bash
git clone https://github.com/MuniGit5/HRChatBot.git
cd HRChatBot
```

**Related assets included in the repo:**
- `data/hr_docs/` – Employee handbook and policy documents (.docx)
- `data/hr_extra/` – Additional policy documents
- `assets/logo.png` – Company logo
- `.streamlit/config.toml` – Streamlit theme and config
- `requirements.txt` – Python dependencies
- `backup_and_restore.md` – Backup/restore instructions

**Not in the repo** (create locally):
- `.env` – API keys (see Configuration)
- `chroma_db/` – Vector store (rebuilt with `python build_db.py`)
- `.venv/` – Virtual environment (recreate with `pip install -r requirements.txt`)

---

## Languages & Frameworks

**Programming language:** Python 3.11

**Frameworks & libraries:**
- **Streamlit** – Web UI
- **OpenAI** – Embeddings and GPT for summarization
- **ChromaDB** – Vector database for RAG
- **python-docx** – Read .docx policy documents
- **python-dotenv** – Load environment variables

---

## How to Run the Application

### Step-by-step (local)

1. **Clone the repo**
   ```bash
   git clone https://github.com/MuniGit5/HRChatBot.git
   cd HRChatBot
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file** (in project root)
   ```
   OPENAI_API_KEY=your-openai-api-key-here
   ```

5. **Build the vector store** (run once)
   ```bash
   python build_db.py
   ```

6. **Run the app**
   ```bash
   streamlit run app.py
   ```

7. Open http://localhost:8501 in your browser.

### Commands summary

| Command | Purpose |
|---------|---------|
| `python build_db.py` | Build vector index from handbook documents |
| `streamlit run app.py` | Start the web app |

---

## Dependencies

**Where are dependencies listed?**  
`requirements.txt`

**Contents:**
```
openai>=1.0.0
python-docx>=1.0.0
chromadb>=0.4.0
streamlit>=1.28.0
python-dotenv>=1.0.0
```

**System requirements:**
- Python 3.9+ (tested with 3.11)
- No global/system dependencies beyond Python

---

## Configuration

**Configuration files:**
- `.env` – Environment variables (create manually)
- `.streamlit/config.toml` – Streamlit theme (in repo)

**What needs to be set for the app to run?**

Create a `.env` file in the project root:
```
OPENAI_API_KEY=sk-proj-your-openai-api-key-here
```

**Secrets / API keys:**
- **OpenAI API key** – Required. Stored in `.env` locally; in Streamlit Cloud Secrets when deployed.
- **No hardcoded credentials** – All secrets are loaded from environment/Secrets.

---

## Database & Storage

**Does the app use a database?**  
No traditional database. It uses **ChromaDB** (vector store) for semantic search.

**Storage:**
- **ChromaDB** – Stores document embeddings in `chroma_db/` (created by `build_db.py`)
- **Source documents** – `.docx` files in `data/hr_docs/` and `data/hr_extra/`
- **No migrations** – Vector store is rebuilt from documents when needed

**Sample data:**  
The `data/` folder contains the James Shield Employee Handbook and policy documents (Vacation, Holidays, Benefits, FMLA, etc.).

---

## Frontend/Backend Structure

**Type:** Full-stack (single application)

**Structure:** Monolithic – frontend and backend in the same repo.

| File | Role |
|------|------|
| `app.py` | Streamlit UI (frontend) + app logic |
| `rag.py` | RAG backend (document loading, embeddings, retrieval, OpenAI) |
| `build_db.py` | Script to build ChromaDB vector store |

---

## Build & Deployment

**Build for production:**  
No separate build step. Run `python build_db.py` once, then `streamlit run app.py`.

**Deployment:**
- **Platform:** Streamlit Community Cloud (share.streamlit.io)
- **Process:** Connect GitHub repo → Streamlit auto-deploys on push
- **Secrets:** Add `OPENAI_API_KEY` in Streamlit app Settings → Secrets
- **URL:** https://hrchatbot-nw8tafwepqhnswzccneyzk.streamlit.app/

**Docker:** Not used.

---

## Testing

**Are there any tests?**  
No automated tests in the current codebase.

**Testing framework:** None.

---

## Documentation

**Documentation in the repo:**
- `README.md` – Setup and features
- `PROJECT_DOCUMENTATION.md` – This file
- `backup_and_restore.md` – Backup/restore instructions
- Inline comments in `app.py` and `rag.py`

---

## High-Level Walkthrough

### Project structure

```
HRChatBot/
├── app.py              # Main Streamlit app (UI, topics, chat, sidebar)
├── rag.py              # RAG logic (load docs, ChromaDB, OpenAI)
├── build_db.py         # Build vector store from data/
├── requirements.txt    # Python dependencies
├── .env                # API key (create locally, not in repo)
├── .streamlit/
│   └── config.toml     # Theme (green, professional)
├── data/
│   ├── hr_docs/        # Handbook and policy .docx files
│   └── hr_extra/       # Additional policy documents
├── assets/
│   └── logo.png        # Company logo
├── chroma_db/          # Vector store (created by build_db.py)
└── README.md
```

### Main files

| File | Purpose |
|------|---------|
| **app.py** | Streamlit UI: topics, questions, chat input, sidebar (History, FAQs, Help, HR contact). Calls `get_answer()` from rag.py. |
| **rag.py** | Loads .docx from `data/`, chunks text, stores in ChromaDB, retrieves by similarity, sends to OpenAI for 2-sentence summary. |
| **build_db.py** | One-time script to build ChromaDB index from all documents in `data/`. |

### Flow

1. User selects a topic or asks a question.
2. `get_answer(question)` in `rag.py` runs.
3. Question is embedded; ChromaDB returns top similar chunks.
4. Chunks are sent to OpenAI with a strict “only use context” prompt.
5. Response is summarized to 2 sentences and shown in the UI.
