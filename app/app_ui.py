import streamlit as st
from rag_answer import rag_answer
import chromadb
from sentence_transformers import SentenceTransformer

st.set_page_config(page_title="MkDocs RAG Assistant", layout="wide")

CHROMA_DIR = "chroma_db"
COLLECTION = "mkdocs_user_guide"

@st.cache_resource
def load_db():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    col = client.get_collection(COLLECTION)
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return col, model

collection, embedder = load_db()

st.title("📘 MkDocs RAG Assistant")
st.write("Ask any question related to MkDocs documentation.")

question = st.text_input("Enter your question:")

if question:

    # Call full RAG answering logic
    answer = rag_answer(question)

    st.subheader("💬 Answer")
    st.write(answer)

    # ALSO show retrieved chunks
    q_embed = embedder.encode([question])[0]

    result = collection.query(
        query_embeddings=[q_embed],
        n_results=4,
        # include=["documents", "metadatas"]
    )

    docs = result["documents"][0]
    metas = result["metadatas"][0]

    st.subheader("📄 Retrieved Context")
    for doc, meta in zip(docs, metas):
        with st.expander(meta.get("file", "")):
            st.write(doc)
