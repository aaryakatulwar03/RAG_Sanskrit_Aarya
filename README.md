# Sanskrit RAG System

## Project Overview
This project is a CPU-only Retrieval-Augmented Generation (RAG) system built for Sanskrit documents.  
The system loads Sanskrit text files, preprocesses them, splits them into smaller chunks, creates embeddings, stores them in a FAISS vector index, retrieves relevant chunks for a user query, and returns an answer based on the retrieved context.

The project is designed to be simple, modular, and easy to explain.

---

## Objective
The objective of this project is to build an end-to-end Sanskrit document question-answering system that:

- works on CPU only
- ingests Sanskrit text documents
- retrieves relevant document chunks for a given query
- provides an answer based on the retrieved context

---

## Features
- Loads Sanskrit `.txt` documents from the `data/` folder
- Cleans and preprocesses the text
- Splits documents into smaller chunks
- Creates multilingual embeddings using Sentence Transformers
- Stores embeddings in a FAISS vector database
- Retrieves top relevant chunks for a query
- Uses a lightweight answer generation / extractive fallback pipeline
- Runs fully on CPU

---

## Project Structure

```text
RAG_Sanskrit_Aarya/
│
├── code/
│   ├── config.py
│   ├── preprocess.py
│   ├── build_index.py
│   ├── query_system.py
│   ├── generator.py
│   ├── utils.py
│   └── app.py
│
├── data/
│   ├── story1.txt
│   ├── story2.txt
│   ├── story3.txt
│   ├── story4.txt
│   └── story5.txt
│
├── outputs/
│   └── faiss_index/
│       ├── index.faiss
│       └── index.pkl
│
├── reports/
├── screenshots/
├── notebooks/
├── models/
├── README.md
├── requirements.txt
└── .gitignore


---


## Technologies Used

Python

LangChain

FAISS

Sentence Transformers

Hugging Face Transformers

mT5-small

VS Code

Models Used
Embedding Model

sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

Reason:

multilingual support

lightweight

suitable for CPU-based retrieval

Generator Model

google/mt5-small

Reason:

multilingual sequence-to-sequence model

better suited than English-only lightweight models for Sanskrit-related text

Answer Fallback

If the generator output is weak or unusable, the system uses a simple extractive fallback approach to return the most relevant sentence from the retrieved context.

How the System Works
Step 1: Document Loading

The system reads Sanskrit .txt files from the data/ folder.

Step 2: Preprocessing

The text is cleaned by:

removing extra spaces

removing repeated blank lines

preserving Sanskrit content safely

Step 3: Chunking

Documents are split into smaller chunks using RecursiveCharacterTextSplitter.

Current settings:

Chunk size: 500

Chunk overlap: 80

Step 4: Embedding Creation

Each chunk is converted into a vector embedding using the embedding model.

Step 5: FAISS Indexing

All chunk embeddings are stored in a FAISS vector store for efficient similarity search.

Step 6: Retrieval

For a user query, the system retrieves the top relevant chunks from FAISS.

Step 7: Answer Generation

The system tries to generate an answer using the generator model.
If the generated answer is weak, it uses extractive fallback from the retrieved context.

Installation and Setup
1. Clone or download the project

Place the project folder on your system.

2. Create a virtual environment

python -m venv venv
3. Activate the virtual environment
On Windows PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
venv\Scripts\Activate.ps1
On Command Prompt
venv\Scripts\activate.bat
4. Install dependencies
pip install -r requirements.txt

If required, also install:

pip install sentencepiece protobuf
How to Run the Project
Step 1: Build the FAISS index

Run:

python code/build_index.py

This will:

load all documents

preprocess them

split them into chunks

create embeddings

save the FAISS index in outputs/faiss_index/

Step 2: Run the full application

Run:

python code/app.py

Then enter your question when prompted.

Example Queries

You can test with queries like:

शर्करा कुत्र अस्ति ?

घण्टां के वादयन्ति ?

देवः कथं साहाय्यम् करोति ?

Example Behavior
Query

शर्करा कुत्र अस्ति ?

Retrieved Context

The system retrieves chunks from the story about Shankhanada and the sugar.

Output

The answer is generated from the retrieved context or extracted from it.

Important Files
config.py

Stores settings such as:

folder paths

chunk size

chunk overlap

model names

top-k retrieval count

preprocess.py

Handles:

text cleaning

document loading

chunk creation

build_index.py

Handles:

loading documents

splitting into chunks

generating embeddings

building and saving FAISS index

query_system.py

Handles:

loading the FAISS index

retrieval of top relevant chunks

generator.py

Handles:

generator model loading

answer generation

extractive fallback

app.py

Main end-to-end script that:

loads retriever

loads generator

accepts user query

retrieves chunks

returns final answer

Current Limitations

The generator model is lightweight and CPU-friendly, so answer quality is not always perfect

Sanskrit generation quality is limited compared to larger GPU-based models

Some answers are based on extractive fallback rather than fully natural generation

Retrieval is good, but top retrieved chunks may sometimes include less relevant results after the first result

Transliteration support is not separately implemented as a dedicated module

Future Improvements

use a stronger Sanskrit-aware or multilingual QA model

improve transliteration support

add reranking of retrieved chunks

improve answer extraction logic

add a web interface using Streamlit

support more Sanskrit documents and larger corpora

Conclusion

This project successfully implements a CPU-only Sanskrit RAG pipeline using document retrieval, FAISS indexing, multilingual embeddings, and lightweight answer generation with extractive fallback.
The system is modular, functional, and suitable as a beginner-friendly implementation of a Sanskrit document QA system.

Author

Aarya Katulwar
