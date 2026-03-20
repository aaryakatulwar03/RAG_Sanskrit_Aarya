from pathlib import Path

# Base folders
DATA_FOLDER = Path("data")
OUTPUT_FOLDER = Path("outputs")
FAISS_INDEX_FOLDER = OUTPUT_FOLDER / "faiss_index"

# Chunking settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 80

# Retrieval settings
TOP_K = 3

# Model names
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
GENERATOR_MODEL_NAME = "google/mt5-small"