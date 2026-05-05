#!/usr/bin/env python3
"""
LangChain Basics - Practice Exercises

This file contains 10 exercises covering LangChain fundamentals for building LLM applications.
Focus on prompt engineering, RAG concepts, and LangChain abstractions without requiring LLM APIs.

Note: Following user priority, solutions are deferred. These exercises are designed to test
understanding of LangChain concepts and prepare for interviews.
"""

from typing import Dict, Any, List, Optional
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.schema import HumanMessage, SystemMessage


def exercise_1_prompt_templates() -> Dict[str, Any]:
    """
    Exercise 1: Prompt Template Fundamentals
    
    Create a prompt template for generating SQL queries from natural language questions.
    The template should include:
    - Input variables: question, table_name, columns
    - Clear instructions for generating valid SQL
    - Example formatting
    
    Return a dictionary with:
    - "template": The PromptTemplate object
    - "example_prompt": A formatted prompt using sample values
    """
    # TODO: Implement this exercise
    return {
        "description": "Create a SQL generation prompt template",
        "template": None,  # Replace with PromptTemplate
        "example_prompt": None  # Replace with formatted prompt
    }


def exercise_2_few_shot_prompting() -> Dict[str, Any]:
    """
    Exercise 2: Few-Shot Prompt Design
    
    Design a few-shot prompt for sentiment analysis of business statements.
    Include 3 examples showing different sentiment categories (positive, negative, neutral).
    
    Return a dictionary with:
    - "examples": The few-shot examples as a string
    - "template": The complete prompt template with examples
    - "test_prompt": Formatted prompt for a test statement
    """
    # TODO: Implement this exercise
    return {
        "description": "Design few-shot prompt for sentiment analysis",
        "examples": None,
        "template": None,
        "test_prompt": None
    }


def exercise_3_chain_of_thought() -> Dict[str, Any]:
    """
    Exercise 3: Chain-of-Thought Prompting
    
    Create a chain-of-thought prompt for solving data engineering problems.
    The prompt should guide step-by-step reasoning for optimizing a slow SQL query.
    
    Return a dictionary with:
    - "template": The chain-of-thought prompt template
    - "formatted": The formatted prompt with a sample problem
    - "steps": List of reasoning steps the prompt should elicit
    """
    # TODO: Implement this exercise
    return {
        "description": "Create chain-of-thought prompt for query optimization",
        "template": None,
        "formatted": None,
        "steps": ["Identify slow components", "Analyze query plan", "Suggest indexes", "Rewrite query"]
    }


def exercise_4_chat_prompt_templates() -> Dict[str, Any]:
    """
    Exercise 4: Chat Prompt Templates
    
    Create a chat prompt template for a data analyst assistant.
    Include system message, conversation history, and current user query.
    
    Return a dictionary with:
    - "chat_template": The ChatPromptTemplate object
    - "messages": Formatted messages with sample conversation
    - "roles": List of message roles included
    """
    # TODO: Implement this exercise
    return {
        "description": "Create chat prompt template for data analyst assistant",
        "chat_template": None,
        "messages": None,
        "roles": ["system", "human"]
    }


def exercise_5_text_splitting_strategies() -> Dict[str, Any]:
    """
    Exercise 5: Text Splitting for RAG
    
    Implement document chunking with different strategies:
    1. Fixed-size chunks with overlap
    2. Semantic-aware splitting (by paragraphs)
    3. Code-specific splitting
    
    Return a dictionary with:
    - "splitter": RecursiveCharacterTextSplitter configuration
    - "chunks": List of Document chunks from sample text
    - "stats": Dictionary with chunk count, avg size, etc.
    """
    sample_text = """
    Data Engineering Pipeline Design:
    
    A well-designed data pipeline should be:
    1. Idempotent: Running multiple times produces the same result
    2. Fault-tolerant: Handles failures gracefully
    3. Scalable: Handles increasing data volumes
    4. Maintainable: Easy to understand and modify
    5. Observable: Provides metrics and logs for monitoring
    
    Best Practices:
    - Use version control for pipeline code
    - Implement data quality checks
    - Document data lineage
    - Test with realistic data volumes
    - Monitor performance metrics
    """
    
    # TODO: Implement this exercise
    return {
        "description": "Implement text splitting strategies for RAG",
        "splitter": None,
        "chunks": [],
        "stats": {"chunk_count": 0, "avg_chars": 0}
    }


def exercise_6_simple_retrieval_implementation() -> Dict[str, Any]:
    """
    Exercise 6: Simple Retrieval Implementation
    
    Implement a keyword-based retrieval system for documents.
    Create a function that searches documents for query terms and returns relevant chunks.
    
    Return a dictionary with:
    - "search_function": Function that takes query and returns documents
    - "sample_docs": List of sample Document objects
    - "test_results": Results for test queries
    """
    # TODO: Implement this exercise
    return {
        "description": "Implement keyword-based retrieval system",
        "search_function": None,
        "sample_docs": [],
        "test_results": {}
    }


def exercise_7_rag_pipeline_design() -> Dict[str, Any]:
    """
    Exercise 7: RAG Pipeline Design
    
    Design a complete RAG pipeline architecture (without implementation).
    Describe the components: document loading, chunking, embedding, retrieval, generation.
    
    Return a dictionary with:
    - "architecture": Description of RAG pipeline components
    - "flowchart": Text representation of data flow
    - "components": List of LangChain components needed
    """
    # TODO: Implement this exercise
    return {
        "description": "Design RAG pipeline architecture",
        "architecture": "Document -> Loader -> Splitter -> Embeddings -> Vector Store -> Retriever -> LLM -> Answer",
        "flowchart": None,
        "components": ["DocumentLoader", "TextSplitter", "Embeddings", "VectorStore", "Retriever", "LLMChain"]
    }


def exercise_8_memory_implementation() -> Dict[str, Any]:
    """
    Exercise 8: Conversation Memory Design
    
    Design a conversation memory system for a chatbot.
    Implement a simple buffer that stores last N messages.
    
    Return a dictionary with:
    - "memory_class": Simple memory implementation
    - "sample_conversation": Example conversation with memory
    - "memory_contents": What gets stored in memory
    """
    # TODO: Implement this exercise
    return {
        "description": "Design conversation memory system",
        "memory_class": None,
        "sample_conversation": [],
        "memory_contents": []
    }


def exercise_9_langchain_chains() -> Dict[str, Any]:
    """
    Exercise 9: LangChain Chain Composition
    
    Design a chain that combines multiple steps:
    1. Parse user question
    2. Retrieve relevant documents
    3. Generate SQL query
    4. Execute query (simulated)
    5. Format results
    
    Return a dictionary with:
    - "chain_design": Description of chain components and flow
    - "pseudocode": Pseudocode for chain implementation
    - "inputs_outputs": Expected inputs and outputs
    """
    # TODO: Implement this exercise
    return {
        "description": "Design multi-step LangChain",
        "chain_design": "Question -> Parser -> Retriever -> SQL Generator -> Executor -> Formatter",
        "pseudocode": None,
        "inputs_outputs": {"input": "natural language question", "output": "formatted query results"}
    }


def exercise_10_production_considerations() -> Dict[str, Any]:
    """
    Exercise 10: Production Deployment Considerations
    
    Identify key considerations for deploying LangChain applications to production.
    Focus on: scalability, cost management, monitoring, error handling.
    
    Return a dictionary with:
    - "considerations": List of production considerations
    - "solutions": Proposed solutions for each consideration
    - "monitoring_metrics": Key metrics to monitor
    """
    # TODO: Implement this exercise
    return {
        "description": "Identify production deployment considerations",
        "considerations": [
            "API rate limiting and costs",
            "Response latency requirements",
            "Error handling and fallbacks",
            "Model version management",
            "Data privacy and security"
        ],
        "solutions": [],
        "monitoring_metrics": ["token_usage", "response_time", "error_rate", "retrieval_accuracy"]
    }


def main():
    """Run all exercises and print summaries"""
    print("=== LangChain Basics Practice Exercises ===\n")
    print("This file contains 10 exercises covering LangChain fundamentals.")
    print("Following user priority: exercises without solutions, focusing on interview preparation.\n")
    
    exercises = [
        ("1. Prompt Template Fundamentals", exercise_1_prompt_templates),
        ("2. Few-Shot Prompt Design", exercise_2_few_shot_prompting),
        ("3. Chain-of-Thought Prompting", exercise_3_chain_of_thought),
        ("4. Chat Prompt Templates", exercise_4_chat_prompt_templates),
        ("5. Text Splitting for RAG", exercise_5_text_splitting_strategies),
        ("6. Simple Retrieval Implementation", exercise_6_simple_retrieval_implementation),
        ("7. RAG Pipeline Design", exercise_7_rag_pipeline_design),
        ("8. Conversation Memory Design", exercise_8_memory_implementation),
        ("9. LangChain Chain Composition", exercise_9_langchain_chains),
        ("10. Production Deployment Considerations", exercise_10_production_considerations)
    ]
    
    for title, func in exercises:
        print(f"\n{title}")
        print("-" * len(title))
        try:
            result = func()
            print(f"✓ Exercise defined: {result.get('description', 'No description')}")
            if "stats" in result:
                print(f"  Stats: {result['stats']}")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print("\n" + "="*50)
    print("Exercises completed. Remember:")
    print("1. These are practice exercises without solutions (per user priority)")
    print("2. Focus on understanding LangChain concepts and architecture")
    print("3. Prepare for interview questions about LLM application development")
    print("4. Consider 8GB RAM constraints when designing production systems")
    print("\nNext steps: Implement solutions after completing all educational frameworks.")


if __name__ == "__main__":
    main()