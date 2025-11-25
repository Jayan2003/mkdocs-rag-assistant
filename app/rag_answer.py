
import google.generativeai as genai
import os
import chromadb
from sentence_transformers import SentenceTransformer

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
llm = genai.GenerativeModel("gemini-pro-latest")


client = chromadb.PersistentClient(path="chroma_db")
col = client.get_collection("mkdocs_user_guide")
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
K_NEIGHBORS = 4  # chosen after small experiments: good balance of coverage vs noise

def rag_answer(q):
    # embed query
    q_vec = embedder.encode([q])[0]

    # retrieve
    results = col.query(
        query_embeddings=[q_vec],
        n_results=K_NEIGHBORS,
    )

    chunks = results["documents"][0]
    
    context = "\n\n".join(chunks)

    prompt = f"""
You are an expert MkDocs assistant.
Answer strictly from the given context.
If the answer is not inside context, say: "Not found in documentation."

CONTEXT:
{context}

QUESTION: {q}

FINAL ANSWER:
"""

    resp = llm.generate_content(prompt)

    return resp.text
