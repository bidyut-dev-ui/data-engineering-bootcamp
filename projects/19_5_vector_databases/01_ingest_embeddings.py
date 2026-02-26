import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.docstore.document import Document

# 1. Connection string for our local pgvector Docker container
CONNECTION_STRING = "postgresql+psycopg2://admin:secretpassword@localhost:5432/vectordb"
COLLECTION_NAME = "bootcamp_documents"

# 2. Setup a lightweight, local CPU-friendly Embeddings Model
# This entirely avoids OpenAI API keys or GPU requirements!
print("Loading HuggingFace Embeddings Model (CPU friendly)...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def ingest_data():
    """Simulates converting raw documents into Vector Embeddings and storing them."""
    
    # 3. Our "Raw Data" (could be PDFs, Confluence, etc.)
    docs = [
        Document(
            page_content="Data Company requires a Senior Data Engineer with AWS LocalStack experience.", 
            metadata={"source": "job_board", "role": "Data Engineer"}
        ),
        Document(
            page_content="The Generative AI/ML Engineer role at the Pune office requires LangChain and Vector Database experience.", 
            metadata={"source": "job_board", "role": "GenAI Engineer"}
        ),
        Document(
            page_content="Airflow is traditionally used for batch processing orchestrations.", 
            metadata={"source": "engineering_wiki", "category": "orchestration"}
        )
    ]
    
    print(f"Embedding {len(docs)} documents and inserting into PGVector...")
    
    # 4. Ingest! This automatically calculates embeddings and writes to Postgres
    db = PGVector.from_documents(
        embedding=embeddings,
        documents=docs,
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING,
        pre_delete_collection=True # Clean start
    )
    
    print("Ingestion complete. Documents are now mathematically searchable!")

if __name__ == "__main__":
    ingest_data()
