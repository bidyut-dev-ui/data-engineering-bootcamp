# Week 19: Introduction to LangChain

**Goal**: Learn LangChain fundamentals for building LLM applications: prompt engineering, chains, and RAG (Retrieval-Augmented Generation) concepts.

## Scenario
You want to build AI-powered applications but don't want to manage complex LLM infrastructure. LangChain provides abstractions for common patterns like prompt templates, chains, and document retrieval.

## Concepts Covered
1. **Prompt Templates**: Reusable prompt structures
2. **Few-Shot Learning**: Teaching with examples
3. **Chain-of-Thought**: Step-by-step reasoning
4. **Text Splitting**: Chunking documents for processing
5. **RAG Basics**: Retrieval-Augmented Generation
6. **Document Loaders**: Ingesting various formats
7. **Memory**: Maintaining conversation context

## Structure
- `01_prompts.py`: Prompt engineering patterns (no LLM required)
- `02_rag_basics.py`: RAG concepts with simple retrieval (no vector DB)
- `requirements.txt`: Minimal dependencies

## Instructions

### 1. Setup
```bash
cd projects/15_langchain_basics
source ../00_setup_and_refresher/venv/bin/activate
pip install langchain
```

**Note**: We're NOT installing LLM providers (OpenAI, Anthropic) to keep this CPU-only and free.

### 2. Run Prompt Engineering Tutorial
```bash
python 01_prompts.py
```

**Expected Output**:
- Formatted prompt templates
- Few-shot examples
- Chain-of-thought prompts

**What You'll Learn**:
- How to structure prompts for consistency
- Few-shot vs zero-shot prompting
- Breaking down complex tasks

### 3. Run RAG Basics Tutorial
```bash
python 02_rag_basics.py
```

**Expected Output**:
- Documents split into chunks
- Simple keyword-based retrieval
- Retrieved documents for a query

**What You'll Learn**:
- Why documents need chunking
- Basic retrieval mechanics
- How RAG improves LLM responses

## Homework / Challenge

### Challenge 1: Build a Prompt Library
Create `03_challenge.py`:
1. Create 5 prompt templates for common data tasks:
   - Data quality check
   - SQL query generation
   - Error message explanation
   - Code review
   - Documentation generation
2. Save them to a JSON file
3. Load and use them dynamically

### Challenge 2: Document QA System
Create `04_doc_qa.py`:
1. Load text files from a directory
2. Split them into chunks
3. Implement TF-IDF based retrieval (use sklearn)
4. Given a question, return top 3 relevant chunks

### Challenge 3: Conversation Memory
Create `05_memory.py`:
1. Implement a simple conversation buffer
2. Store last 5 messages
3. Include conversation history in prompts
4. Demonstrate with a mock conversation

## Expected Learning Outcomes
- ✅ Understand prompt engineering principles
- ✅ Know when to use few-shot vs zero-shot
- ✅ Understand RAG architecture
- ✅ Prepare documents for LLM processing
- ✅ Build LLM applications without API costs (for learning)

## Production Considerations
When moving to production with actual LLMs:
1. **Choose Provider**: OpenAI, Anthropic, local models (Ollama)
2. **Embeddings**: Use proper vector embeddings (not keyword search)
3. **Vector Store**: FAISS, Pinecone, or Weaviate
4. **Cost Management**: Cache responses, use smaller models when possible
5. **Monitoring**: Track token usage and response quality
