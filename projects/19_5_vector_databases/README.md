# Week 19.5: Vector Databases & RAG

**Tag:** `#role-genai-engineer`, `#skill-ai-rag`

## Overview
To qualify for a Generative AI/ML Engineer role, you must understand how to interact with Vector Databases and implement Retrieval-Augmented Generation (RAG) pipelines. 

While enterprise tools like Pinecone or Weaviate are often used in the cloud, you can build a complete, highly-scalable RAG system locally (and for free) using Postgres enhanced with the `pgvector` extension. 

## Learning Objectives
- Understanding standard PG Database scaling applied to Vector Workloads.
- Generating Text Embeddings without Expensive APIs (Using local HuggingFace CPU models).
- Storing Vector representations of documents in `pgvector`.
- Performing Mathematical Similarity Searches (Cosine Distance) to provide precise context to an LLM.

## Project Instructions

### 1. Start the PGVector Database
We are utilizing standard PostgreSQL images bundled with the `pgvector` extension.
```bash
docker compose up -d
```
Verify the container is running with `docker ps`. It is limited strictly to 1GB of RAM to maintain our hardware constraints.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
*Note: This will download a lightweight embedding model on the first run.*

### 3. Ingest Data (Embeddings)
Run the ingestion script. It will convert raw text strings into mathematical arrays (embeddings) and store them directly inside Postgres.
```bash
python 01_ingest_embeddings.py
```

### 4. Query the Vector Database
Now, simulate a user asking a chatbot a question. The system will embed the user's question, run a vector similarity search across the Postgres tables, and retrieve the most semantically relevant text.
```bash
python 02_rag_query.py
```
Observe how the database understands *meaning* rather than simply matching keywords!
