from config import FAISS_INDEX_FOLDER, EMBEDDING_MODEL_NAME, TOP_K
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def load_vectorstore():
    """
    Load the saved FAISS vector store from disk.
    """
    print("Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME
    )
    print(f"Embedding model loaded: {EMBEDDING_MODEL_NAME}\n")

    print("Loading saved FAISS index...")
    vectorstore = FAISS.load_local(
        str(FAISS_INDEX_FOLDER),
        embeddings,
        allow_dangerous_deserialization=True
    )
    print("FAISS index loaded successfully.\n")

    return vectorstore


def search_query(vectorstore, query, top_k=TOP_K):
    """
    Search the FAISS vector store for the most relevant chunks.
    """
    results = vectorstore.similarity_search(query, k=top_k)
    return results


if __name__ == "__main__":
    vectorstore = load_vectorstore()

    query = input("Enter your question: ").strip()
    print(f"\nYour query: {query}\n")

    results = search_query(vectorstore, query)

    print(f"Top {TOP_K} retrieved chunks:\n")

    for i, doc in enumerate(results, start=1):
        print(f"Result {i}")
        print(f"Source file: {doc.metadata.get('source_file')}")
        print(f"Chunk ID: {doc.metadata.get('chunk_id')}")
        print("Chunk text:\n")
        print(doc.page_content[:300])
        print("\n" + "-" * 50 + "\n")