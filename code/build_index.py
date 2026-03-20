from config import (
    DATA_FOLDER,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL_NAME,
    FAISS_INDEX_FOLDER
)
from preprocess import load_text_files, split_documents_into_chunks
from utils import ensure_folder_exists

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def main():
    print("Loading documents...")
    documents = load_text_files(DATA_FOLDER)
    print(f"Loaded {len(documents)} documents.\n")

    print("Splitting documents into chunks...")
    chunks = split_documents_into_chunks(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"Created {len(chunks)} useful chunks.\n")

    chunk_texts = [chunk["text"] for chunk in chunks]
    chunk_metadatas = [
        {
            "source_file": chunk["source_file"],
            "chunk_id": chunk["chunk_id"]
        }
        for chunk in chunks
    ]

    print("Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME
    )
    print(f"Embedding model loaded: {EMBEDDING_MODEL_NAME}\n")

    print("Creating FAISS vector store...")
    vectorstore = FAISS.from_texts(
        texts=chunk_texts,
        embedding=embeddings,
        metadatas=chunk_metadatas
    )
    print("FAISS vector store created.\n")

    print("Saving FAISS index...")
    ensure_folder_exists(FAISS_INDEX_FOLDER)
    vectorstore.save_local(str(FAISS_INDEX_FOLDER))
    print(f"FAISS index saved successfully at: {FAISS_INDEX_FOLDER}")


if __name__ == "__main__":
    main()