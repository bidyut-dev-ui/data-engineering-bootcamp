from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

def create_sample_documents():
    """Create sample documents for RAG demo"""
    docs = [
        Document(
            page_content="""
            Data Engineering Best Practices:
            1. Always validate data quality at ingestion
            2. Use idempotent operations in ETL pipelines
            3. Implement proper error handling and logging
            4. Version control your data schemas
            5. Monitor pipeline performance metrics
            """,
            metadata={"source": "best_practices.md", "category": "engineering"}
        ),
        Document(
            page_content="""
            SQL Optimization Tips:
            - Use indexes on frequently queried columns
            - Avoid SELECT * in production queries
            - Use EXPLAIN to analyze query plans
            - Partition large tables by date or region
            - Use CTEs for complex queries
            """,
            metadata={"source": "sql_tips.md", "category": "database"}
        ),
        Document(
            page_content="""
            Machine Learning Workflow:
            1. Data Collection and Exploration
            2. Feature Engineering
            3. Model Selection and Training
            4. Hyperparameter Tuning
            5. Model Evaluation
            6. Deployment and Monitoring
            """,
            metadata={"source": "ml_workflow.md", "category": "ml"}
        )
    ]
    return docs

def demo_text_splitting():
    """Demonstrate text splitting for RAG"""
    print("=== Text Splitting for RAG ===\n")
    
    docs = create_sample_documents()
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        length_function=len
    )
    
    split_docs = text_splitter.split_documents(docs)
    
    print(f"Original documents: {len(docs)}")
    print(f"Split into chunks: {len(split_docs)}\n")
    
    for i, doc in enumerate(split_docs[:5]):
        print(f"Chunk {i+1}:")
        print(f"Content: {doc.page_content[:80]}...")
        print(f"Metadata: {doc.metadata}")
        print()

def demo_simple_retrieval():
    """Demonstrate simple keyword-based retrieval"""
    print("\n=== Simple Retrieval (Keyword-Based) ===\n")
    
    docs = create_sample_documents()
    
    def search(query, documents):
        """Simple keyword search"""
        results = []
        query_lower = query.lower()
        for doc in documents:
            if query_lower in doc.page_content.lower():
                results.append(doc)
        return results
    
    query = "SQL optimization"
    results = search(query, docs)
    
    print(f"Query: '{query}'")
    print(f"Found {len(results)} relevant documents:\n")
    
    for doc in results:
        print(f"Source: {doc.metadata['source']}")
        print(f"Content: {doc.page_content[:150]}...")
        print()

def main():
    print("=== RAG Basics (No Vector DB Required) ===\n")
    
    demo_text_splitting()
    demo_simple_retrieval()
    
    print("\n✓ Tutorial complete!")
    print("\nNote: For production RAG, you would:")
    print("1. Use embeddings: from langchain.embeddings import OpenAIEmbeddings")
    print("2. Use vector store: from langchain.vectorstores import FAISS")
    print("3. Create retriever: retriever = vectorstore.as_retriever()")
    print("4. Build QA chain: RetrievalQA.from_chain_type()")

if __name__ == "__main__":
    main()
