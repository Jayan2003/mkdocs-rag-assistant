
# 📘 MkDocs RAG Assistant

A **Retrieval-Augmented Generation (RAG)** system that answers questions from the official **MkDocs documentation** using semantic search + LLMs.

The system ingests MkDocs docs, splits them into semantic chunks, embeds **text + images**, stores everything inside ChromaDB, and uses a Streamlit UI for interactive querying.

---

# 🧩 System Overview

### 🔹 Data Source

Official MkDocs Documentation
→ Extracted from the `docs/` folder of:
👉 [https://github.com/mkdocs/mkdocs/tree/master](https://github.com/mkdocs/mkdocs/tree/master)

### 🔹 Key Features

✔ Processes entire MkDocs repo
✔ Heading-aware semantic chunking
✔ Cleans & normalizes content
✔ Embeds both **text + images (CLIP)**
✔ Stores vectors in ChromaDB
✔ Retrieval + Gemini LLM answering
✔ Streamlit UI with visible retrieved context

---

# 🧠 Architecture

| Component                 | Purpose                                      |
| ------------------------- | -------------------------------------------- |
| `ingest/ingest_mkdocs.py` | Chunk + clean + embed + insert into ChromaDB |
| **ChromaDB**              | Vector database (persistent)                 |
| **MiniLM Text Embedding** | Fast & accurate for semantic search          |
| **CLIP Image Embedding**  | Embeds screenshots / diagrams                |
| **Gemini LLM**            | Final grounded answer generation             |
| **Streamlit UI**          | User interface                               |
| Retrieval `k=4`           | Empirically optimal after testing            |

---

# ✂️ Chunking Strategy

### **Method**

* Split by **Markdown headings** (H1–H6)
* For long sections:
  🔁 **Sliding window**
  → 1000 characters max
  → 200 characters overlap

### **Why?**

MkDocs documentation is extremely heading-structured.
This method:

* preserves semantic grouping
* respects sections
* avoids cross-topic contamination
* overlap prevents missing context

---

# 🧼 Cleaning Method

Each chunk undergoes:

✔ Remove Markdown `#` headings
✔ Collapse whitespace
✔ Strip leading/trailing spaces

Result → cleaner embeddings → better retrieval.

---

# 🧬 Embedding Models

### **Text Model**

`sentence-transformers/all-MiniLM-L6-v2`

Reasons:

* Very fast
* Lightweight
* Excellent semantic performance
* Ideal for documentation Q&A

### **Image Model (BONUS)**

`OpenAI CLIP ViT-B/32`

Used to embed:

* diagrams
* screenshots
* icons

→ Stored in the same ChromaDB collection.

---

# 📦 Vector Database

### **ChromaDB (Persistent Client)**

Stored on disk:

```
/chroma_db/
```

Collection name:

```
mkdocs_user_guide
```

---

# 🔍 Retrieval — Choosing the Best K

### I tested **five** different values:

* **k = 2**
* **k = 4**
* **k = 5**
* **k = 6**
* **k = 8**

### Test Questions

1. **How do I deploy MkDocs on GitHub Pages?**
2. **How do I change the theme in MkDocs?**
3. **How do I add a new page?**

### 🔎 Results Summary

| k     | Quality                                       |
| ----- | --------------------------------------------- |
| **2** | Too little context → misses details           |
| **4** | ✅ **Best accuracy vs noise balance**          |
| **5** | More noise introduced, some answers got worse |
| **6** | High noise, reduced relevance                 |
| **8** | Too noisy & slower                            |

### 📌 Final Choice

```
K = 4
```
# 📸 Screenshots of Results (K = 4)

### **Q1 – How do I deploy MkDocs on GitHub Pages?**

![K4 Output 1](https://github.com/user-attachments/assets/5790ac1a-094d-42d5-8020-4910c36cc3d8)
![K4 Output 2](https://github.com/user-attachments/assets/bcd54b65-f0cd-4bb7-a309-9d6486d26bc9)


### **Q2 — How do I change the theme in MkDocs?**

![K4 Output 2](https://github.com/user-attachments/assets/cb21b6fc-5d71-48e2-9705-6efa870e1b5c)


### **Q3 — How do I add a new page in MkDocs?**

![K4 Output 3](https://github.com/user-attachments/assets/aa1a0efc-6c75-42bc-9c18-937ab3f56de0)


---

# 🧪 Sample Responses

### **Q1 — Deployment**

Retrieved context:
`user-guide/deploying-your-docs.md`
→ Correct answer generated.

---

### **Q2 — Changing Theme**

Retrieved context:
`choosing-your-theme.md`
`configuration.md`
→ Correct answer.

---

### **Q3 — Adding a Page**

**Retrieved Context:**

* `data/mkdocs/docs/about/release-notes.md`
* `data/mkdocs/docs/dev-guide/README.md`
* `data/mkdocs/docs/getting-started.md`
* `data/mkdocs/docs/user-guide/README.md`

---

# 🖥 Run Locally

### 1️⃣ Create environment

```
python -m venv venv
```

### 2️⃣ Activate

Windows:

```
venv\Scripts\activate
```

### 3️⃣ Install requirements

```
pip install -r requirements.txt
```

### 4️⃣ Ingest the docs

```
python ingest/ingest_mkdocs.py
```

### 5️⃣ Launch UI

```
streamlit run app/app_ui.py
```

---

# 🚀 Usage

Example question:

> **How do I deploy MkDocs to GitHub Pages?**

You will see:

✔ Answer
✔ Retrieved chunks with filenames
✔ Context used to generate the answer

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
   mkdocs/          ← official docs

chroma_db/         ← auto-generated

README.md
requirements.txt
```

---

# 🏆 Bonus Features Implemented

✔ Multimodal embeddings (text + images)
✔ Complete Streamlit RAG application

---

# 📎 Requirements Checklist

☑ Chunking method + justification
☑ Cleaning method
☑ Embedding models
☑ Vector DB choice
☑ Sample Q&A
☑ K-selection comparison (2,4,5,6,8)
☑ Final chosen K with explanation
☑ Streamlit UI
☑ Multimodal support (CLIP)
☑ Repo submission

---

# 📬 Contact

Maintainer: **Jayan Ahmed Samer**


