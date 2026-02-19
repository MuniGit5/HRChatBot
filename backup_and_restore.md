# Backup & Restore Guide

## Option 1: ZIP Archive (Simplest)

### Create a backup
1. Compress the entire `hr-chatbot` folder into a ZIP file
2. **Exclude** (don't include): `.venv`, `chroma_db`, `__pycache__`, `.DS_Store`
3. Save the ZIP to: Google Drive, Dropbox, OneDrive, iCloud, or USB drive

**On Mac (Terminal):**
```bash
cd "/Users/munig/Desktop/Spring 2026/CIS 565/final project/565 Final Project"
zip -r HRChatBot-backup.zip hr-chatbot -x "hr-chatbot/.venv/*" -x "hr-chatbot/chroma_db/*" -x "hr-chatbot/__pycache__/*" -x "hr-chatbot/*/__pycache__/*" -x "*.DS_Store"
```

### Restore and run later
1. Unzip the folder wherever you want
2. Open Terminal, go to the folder:
   ```bash
   cd path/to/hr-chatbot
   ```
3. Create virtual environment and install:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Add your OpenAI API key to `.env` (create it if missing):
   ```
   OPENAI_API_KEY=your-key-here
   ```
5. Build the index and run:
   ```bash
   python build_db.py
   streamlit run app.py
   ```

---

## Option 2: Cloud Storage (Drag & Drop)

- **Google Drive**: Create folder → Upload entire `hr-chatbot` folder (you can exclude `.venv` to save space)
- **Dropbox / OneDrive / iCloud**: Same approach
- Later: Download, then follow "Restore and run" steps above

---

## Option 3: GitHub (Version control)

If you get authentication working, GitHub gives you:
- Cloud backup
- Version history
- Easy to clone on any computer

---

## What to include in backup

| Include | Exclude (can rebuild) |
|---------|------------------------|
| app.py, rag.py, build_db.py | .venv |
| data/ (all .docx files) | chroma_db |
| assets/logo.png | __pycache__ |
| .streamlit/config.toml | |
| requirements.txt | |
| .env (keep secure!) | |

**Note:** `.env` contains your API key. Store it securely. You can recreate it later with your key.
