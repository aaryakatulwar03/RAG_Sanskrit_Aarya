import re
from config import DATA_FOLDER, CHUNK_SIZE, CHUNK_OVERLAP
from utils import print_separator
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(text):
    """
    Clean the text safely without damaging Sanskrit content.
    """
    text = text.strip()
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def load_text_files(folder_path):
    """
    Load all .txt files from the given folder.
    Returns a list of dictionaries.
    """
    text_files = sorted(folder_path.glob("*.txt"))
    documents = []

    for file_path in text_files:
        with open(file_path, "r", encoding="utf-8") as file:
            raw_text = file.read()

        cleaned_text = clean_text(raw_text)

        documents.append({
            "filename": file_path.name,
            "content": cleaned_text
        })

    return documents


def split_documents_into_chunks(documents, chunk_size, chunk_overlap):
    """
    Split each document into smaller chunks.
    Ignore chunks that are too small to be useful.
    Returns a list of chunk dictionaries.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "।", " ", ""]
    )

    all_chunks = []

    for doc in documents:
        chunks = text_splitter.split_text(doc["content"])

        chunk_number = 1
        for chunk in chunks:
            chunk = chunk.strip()

            if len(chunk) < 80:
                continue

            all_chunks.append({
                "source_file": doc["filename"],
                "chunk_id": chunk_number,
                "text": chunk
            })
            chunk_number += 1

    return all_chunks


if __name__ == "__main__":
    print(f"Data folder path from config: {DATA_FOLDER}")
    print(f"Chunk size from config: {CHUNK_SIZE}")
    print(f"Chunk overlap from config: {CHUNK_OVERLAP}\n")

    documents = load_text_files(DATA_FOLDER)
    print(f"Found {len(documents)} text files.\n")

    chunks = split_documents_into_chunks(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"Total useful chunks created: {len(chunks)}\n")

    for chunk in chunks[:10]:
        print(f"Source file: {chunk['source_file']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print("Chunk preview:\n")
        print(chunk["text"][:200])
        print_separator()