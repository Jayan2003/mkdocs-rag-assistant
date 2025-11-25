
# 📘 MkDocs RAG Assistant

A **Retrieval-Augmented Generation (RAG)** system designed to answer questions from the official **MkDocs documentation**, using semantic search + LLMs.

This project automatically ingests MkDocs docs, chunks them, embeds text + images, stores embeddings in ChromaDB, and serves a Streamlit UI to answer questions with accurate grounded context.

---

# 🧩 System Overview

### 🔹 Data Source

Official MkDocs Repository
→ `docs/` folder from
[https://github.com/mkdocs/mkdocs/tree/master](https://github.com/mkdocs/mkdocs/tree/master)

### 🔹 Key Features

✔ Processes MkDocs documentation
✔ Semantic chunking by headings
✔ Cleans and normalizes content
✔ Embeds text + images
✔ Chroma vector database
✔ Gemini LLM answer generation
✔ Streamlit user interface
✔ Retrieved context is shown

---

# 🧠 Architecture

| Component                 | Purpose                                                          |
| ------------------------- | ---------------------------------------------------------------- |
| `ingest/ingest_mkdocs.py` | Reads MD files, chunks, cleans text, embeds, inserts into Chroma |
| ChromaDB                  | Vector store                                                     |
| MiniLM Embedding          | Text vectorization                                               |
| CLIP Embedding            | Image vectorization                                              |
| Gemini LLM                | Answer generation                                                |
| Streamlit                 | UI Layer                                                         |
| Retrieval k=4             | empirically optimal                                              |

---

# ✂️ Chunking Strategy

### **Method**

* **Heading-based splitting**
* Then **recursive sliding window** for long text
  (`1000 char max + 200 overlap`)

### **Why this method?**

MkDocs documentation is highly structured →
headings reliably group semantic topics.

The overlap prevents context loss.

---

# 🧼 Cleaning Method

Applied to every chunk:

✔ strip markdown headings
✔ collapse whitespace
✔ strip leading/trailing whitespace

Result → higher quality embeddings

---

# 🧬 Embedding Models

### Text Embeddings

`sentence-transformers/all-MiniLM-L6-v2`

Reason:

* Very fast
* Lightweight
* Very good semantic alignment
* SOTA for documentation QA

### **Bonus**

#### Multi-modal images included!

Images embedded using:
`OpenAI CLIP ViT-B/32`

→ stored inside same Chroma collection

---

# 📦 Vector DB

### **ChromaDB persistent client**

Stored on disk:

```
/chroma_db/
```

Collection name:

```
mkdocs_user_guide
```

---

# 🔍 Retrieval — Choosing K

I tested:

* **k=2**
* **k=4**
* **k=6**
* **k=8**

Based on 3 queries:

1. How to deploy MkDocs on GitHub Pages?
2. How do I change the theme?
3. How do I add a new page?

### Findings

| k | Quality                               |
| - | ------------------------------------- |
| 2 | often missing needed content          |
| 4 | **best balance** accuracy + relevance |
| 6 | occasional noise                      |
| 8 | worse + slow                          |

### **Chosen value:**

```
K = 4
```

Saved in `rag_answer.py`

---

# 🧪 Sample Responses

### Q1

**How do I deploy MkDocs on GitHub Pages?**

Retrieved context contained:
`deploying-your-docs.md`

Answer correct

---

### Q2

**How do I change the theme in MkDocs?**

Retrieved context contained:
`choosing-your-theme.md`
`configuration.md`

Answer correct

---

### Q3

**How do I add a new page?**

Retrieved context contained:
`navigation.md`

Answer correct

---

# 🖥 Run locally

### 1) Create venv

```
python -m venv venv
```

### 2) Activate

Windows:

```
venv\Scripts\activate
```

### 3) Install requirements

```
pip install -r requirements.txt
```

### 4) Run ingestion

```
python ingest/ingest_mkdocs.py
```

(wait until 100%)

### 5) Launch UI

```
streamlit run app/app_ui.py
```

---

# 🚀 Usage Demo

Ask something like:

> How do I deploy MkDocs to GitHub Pages?

You will see:

✔ Answer
✔ Retrieved chunks (files + text)

---

# 📁 Repository Structure

```
app/
   app_ui.py
   rag_answer.py
   run_rag.py
   test_query.py

ingest/
   ingest_mkdocs.py

data/
    mkdocs/   ← official docs

chroma_db/   ← generated automatically
```

---

# 🏆 Bonus Features Completed

✔ Multimodal embeddings (text + images)
✔ Fully running Streamlit UI

---

# 📎 Requirements Satisfied

☑ Chunking method & justification
☑ Cleaning method
☑ Embedding model
☑ Vector DB
☑ Sample questions + context
☑ K selection testing
☑ Streamlit app
☑ Multimodal support
☑ Full repo

---

# 📬 Contact

Maintainer: **Jayan Ahmed Samer**

---


