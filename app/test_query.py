from sentence_transformers import SentenceTransformer
import chromadb

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "mkdocs_user_guide"

def main():

    question = input("Enter question: ")

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(COLLECTION_NAME)

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    embedding = model.encode([question])[0]

    results = collection.query(
        query_embeddings=[embedding],
        n_results=5
    )

    print("\n===== TOP MATCHES =====\n")

    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print("FILE:", meta.get("file"))
        print("HEADING:", meta.get("heading"))
        print(doc[:300], "...")
        print("-------------------------\n")


if __name__ == "__main__":
    main()
