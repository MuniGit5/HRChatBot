"""Build the vector store from handbook documents. Run once before first use."""

import os
from dotenv import load_dotenv

load_dotenv()

from rag import build_vector_store, load_documents

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set. Add it to .env file.")
        exit(1)
    texts, sources = load_documents()
    print(f"Loaded {len(texts)} chunks from {len(set(sources))} documents")
    print("Building vector store (this may take a minute)...")
    build_vector_store()
    print("Done! You can now run: streamlit run app.py")
