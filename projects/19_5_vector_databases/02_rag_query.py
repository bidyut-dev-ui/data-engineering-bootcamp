import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.pgvector import PGVector

# 1. Connection string pointing back to our local pgvector Docker container
CONNECTION_STRING = "postgresql+psycopg2://admin:secretpassword@localhost:5432/vectordb"
COLLECTION_NAME = "bootcamp_documents"

# 2. We must load the EXACT same embedding model used during ingestion!
print("Loading HuggingFace Embeddings Model...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def search_documents():
    """Simulates a user asking a question to a RAG system and querying the vector DB."""
    
    # 3. Connect to the existing PGVector store
    print("Connecting to PGVector database...")
    db = PGVector(
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING,
        embedding_function=embeddings,
    )
    
    # 4. The User's "Prompt"
    query = "What skills do I need for the Generative AI engineering role?"
    print(f"\nUser Query: '{query}'")
    
    # 5. Perform the vector similarity search (cosine distance)
    # This turns the query into a vector, and asks postgres to find the closest matches.
    docs_with_score = db.similarity_search_with_score(query, k=2) # Top 2 results
    
    print("\n--- Search Results ---")
    for doc, score in docs_with_score:
        print(f"Distance Score (Lower is tighter): {score:.4f}")
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}\n")
        
    print("Notice how it correctly matched the GenAI document based on semantic meaning, not exact keywords!")

if __name__ == "__main__":
    search_documents()
