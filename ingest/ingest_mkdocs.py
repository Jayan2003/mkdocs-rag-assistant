import os
import re
import clip
import torch
from PIL import Image
from pathlib import Path
from typing import List, Dict

import chromadb
from sentence_transformers import SentenceTransformer

# ---------- CONFIG ----------
MKDOCS_DOCS_DIR = Path("data/mkdocs/docs")
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "mkdocs_user_guide"
MAX_CHARS = 1000
OVERLAP = 200


def read_markdown_files(root: Path) -> List[Path]:
    return [p for p in root.rglob("*.md")]


def split_by_headings(text: str):
    pattern = re.compile(r"^(#{1,6})\s+(.*)", re.MULTILINE)
    matches = list(pattern.finditer(text))

    if not matches:
        return [{"heading": None, "body": text}]

    sections = []
    for i, match in enumerate(matches):
        heading = match.group(2).strip()
        start_body = match.end()

        if i + 1 < len(matches):
            end = matches[i+1].start()
        else:
            end = len(text)

        body = text[start_body:end]
        sections.append({"heading": heading, "body": body.strip()})

    return sections


def split_long_text(text: str):
    if len(text) <= MAX_CHARS:
        return [text]

    parts = []
    start = 0
    while start < len(text):
        end = start + MAX_CHARS
        parts.append(text[start:end])
        start = end - OVERLAP

    return parts


def clean(t: str):
    t = re.sub(r"^#{1,6}\s+", "", t, flags=re.MULTILINE)
    t = re.sub(r"\s+", " ", t)
    return t.strip()

def embed_images(collection, image_paths):
    device = "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)

    for img_path in image_paths:
        try:
            img = preprocess(Image.open(img_path)).unsqueeze(0).to(device)
            with torch.no_grad():
                emb = model.encode_image(img).cpu().numpy()[0]

            collection.add(
                documents=[""],
                embeddings=[emb.tolist()],
                metadatas=[{"file": img_path, "type": "image"}],
                ids=[f"img-{img_path}"]
            )
        except:
            pass

def main():
    print("Reading MD files...")
    files = read_markdown_files(MKDOCS_DOCS_DIR)

    chunks = []
    idx = 0

    for file in files:
        text = file.read_text(encoding="utf-8")
        sections = split_by_headings(text)

        for sec in sections:
            parts = split_long_text(sec["body"])

            for p in parts:
                ct = clean(p)
                chunks.append({
                    "id": f"{file}:{idx}",
                    "text": ct,
                     "metadata": {
                        "file": str(file),
                        "heading": sec["heading"] or ""
                   },

                })
                idx += 1

    print("Chunks built:", len(chunks))

    print("Loading embeddings model...")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("loading embedding model…")
    emb_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("Connecting to Chroma...")
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    try:
        client.delete_collection(COLLECTION_NAME)
    except:
        pass

    collection = client.create_collection(COLLECTION_NAME)

    print("Embedding & inserting...")

    batch = 64
    for i in range(0, len(chunks), batch):
        b = chunks[i:i+batch]
        ids = [x["id"] for x in b]
        docs = [x["text"] for x in b]
        metas = [x["metadata"] for x in b]

        embs = model.encode(docs)

        collection.add(
            ids=ids,
            documents=docs,
            metadatas=metas,
            embeddings=embs
        )

        print(f"Inserted {i+len(b)} / {len(chunks)}")

    print("DONE.")
    # ---- find images ----
    print("Searching for images...")

    image_files = []

    for root, dirs, files in os.walk(MKDOCS_DOCS_DIR):
        for f in files:
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".svg")):
                image_files.append(os.path.join(root, f))

    print("Found:", len(image_files))

    embed_images(collection, image_files)

    print("Image ingestion complete.")
    print("ALL DONE.")

if __name__ == "__main__":
    main()
