# LangChain & LLM Applications Interview Questions

This document contains comprehensive interview questions for LangChain and LLM application development, organized by difficulty and topic area.

## 📚 Core Concepts

### 1. **What is LangChain and what problems does it solve?**
LangChain is a framework for developing applications powered by language models. It provides:
- **Abstractions** for common patterns (prompts, chains, agents)
- **Integration** with various LLM providers (OpenAI, Anthropic, Hugging Face, etc.)
- **Tools** for document loading, text splitting, vector stores, and retrieval
- **Orchestration** for complex multi-step LLM workflows

It solves problems like:
- Managing prompt templates and variables
- Chaining multiple LLM calls
- Integrating external data sources (RAG)
- Handling conversation memory and state
- Building agents that use tools

### 2. **Explain the difference between zero-shot, few-shot, and chain-of-thought prompting**
- **Zero-shot**: Provide only the task description, no examples
  ```python
  template = "Translate this to French: {text}"
  ```
- **Few-shot**: Provide examples to demonstrate the desired format
  ```python
  template = """
  Example 1: "Hello" -> "Bonjour"
  Example 2: "Goodbye" -> "Au revoir"
  Now translate: {text} -> 
  """
  ```
- **Chain-of-thought**: Encourage step-by-step reasoning
  ```python
  template = """
  Let's solve this step by step:
  Question: {question}
  Reasoning:
  1. First, I need to...
  2. Then I should...
  3. Therefore, the answer is...
  """
  ```

### 3. **What is Retrieval-Augmented Generation (RAG) and why is it important?**
RAG combines retrieval of relevant documents with generation using LLMs:
1. **Retrieval**: Find relevant documents/chunks from a knowledge base
2. **Augmentation**: Inject retrieved context into the prompt
3. **Generation**: LLM generates answer using the context

**Importance**:
- Reduces hallucination by grounding in factual information
- Allows LLMs to access up-to-date or proprietary information
- More efficient than fine-tuning for domain-specific knowledge
- Enables citation of sources for verifiability

### 4. **Describe the key components of a LangChain application**
1. **LLMs/Models**: The language model (OpenAI, Anthropic, local, etc.)
2. **Prompts**: Templates with variables and instructions
3. **Chains**: Sequences of calls to LLMs or other utilities
4. **Memory**: Persistence of conversation state
5. **Indexes**: Document loaders, text splitters, vector stores
6. **Retrievers**: Fetch relevant documents for RAG
7. **Agents**: LLMs that use tools to accomplish tasks
8. **Callbacks**: Hooks for monitoring and logging

### 5. **How does LangChain handle conversation memory?**
LangChain provides several memory types:
- **ConversationBufferMemory**: Stores entire conversation
- **ConversationBufferWindowMemory**: Stores last N messages
- **ConversationSummaryMemory**: Stores summarized conversation
- **ConversationKnowledgeGraphMemory**: Stores entities and relationships
- **VectorStore-backed Memory**: Stores memories in a vector database

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
memory.save_context({"input": "Hi"}, {"output": "Hello!"})
```

## 🛠️ Technical Implementation

### 6. **How would you implement a prompt template for SQL generation?**
```python
from langchain.prompts import PromptTemplate

sql_template = PromptTemplate(
    input_variables=["question", "table_schema", "examples"],
    template="""
You are a SQL expert. Given the following table schema:
{table_schema}

Examples of similar questions and their SQL:
{examples}

Generate a SQL query for: {question}

SQL Query:
"""
)
```

### 7. **Explain different text splitting strategies and when to use each**
- **CharacterTextSplitter**: Simple character-based splitting
  ```python
  splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
  ```
- **RecursiveCharacterTextSplitter**: Tries to keep paragraphs/sentences together
  ```python
  splitter = RecursiveCharacterTextSplitter(
      chunk_size=1000,
      chunk_overlap=200,
      separators=["\n\n", "\n", " ", ""]
  )
  ```
- **TokenTextSplitter**: Splits by tokens (more accurate for LLM context)
- **SemanticChunker**: Splits at semantic boundaries using embeddings

**When to use**:
- **RecursiveCharacterTextSplitter**: General purpose, preserves structure
- **TokenTextSplitter**: When exact token counts matter for LLM limits
- **SemanticChunker**: For documents where semantic coherence is critical

### 8. **How would you implement a simple RAG system without a vector database?**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimpleRAG:
    def __init__(self, documents):
        self.documents = documents
        self.vectorizer = TfidfVectorizer()
        self.vectors = self.vectorizer.fit_transform(documents)
    
    def retrieve(self, query, top_k=3):
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.vectors).flatten()
        top_indices = similarities.argsort()[-top_k:][::-1]
        return [self.documents[i] for i in top_indices]
    
    def generate_prompt(self, query, retrieved_docs):
        context = "\n\n".join(retrieved_docs)
        return f"""Context:\n{context}\n\nQuestion: {query}\nAnswer:"""
```

### 9. **What are LangChain agents and how do they work?**
Agents are LLMs that use tools to accomplish tasks:
```python
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

tools = [
    Tool(
        name="Search",
        func=search_function,
        description="Search for information"
    ),
    Tool(
        name="Calculator",
        func=calculator_function,
        description="Perform calculations"
    )
]

agent = initialize_agent(
    tools=tools,
    llm=OpenAI(temperature=0),
    agent="zero-shot-react-description"
)

result = agent.run("What's the population of Tokyo divided by 2?")
```

**How they work**:
1. LLM decides which tool to use based on the query
2. Executes the tool with appropriate parameters
3. Receives tool output
4. Decides next action (use another tool or provide final answer)

### 10. **How would you handle rate limiting and errors in production LLM applications?**
```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import RateLimitError, APIError

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type((RateLimitError, APIError))
)
def safe_llm_call(llm, prompt, fallback_response="Service unavailable"):
    try:
        response = llm.invoke(prompt)
        return response.content
    except RateLimitError:
        print("Rate limited, waiting before retry...")
        time.sleep(30)  # Wait longer for rate limits
        raise
    except APIError as e:
        if "timeout" in str(e).lower():
            print("Timeout error, retrying...")
            raise
        else:
            return fallback_response
```

## 🔍 RAG & Retrieval

### 11. **Compare different vector databases for RAG applications**
| Database | Pros | Cons | Best For |
|----------|------|------|----------|
| **FAISS** | Fast, memory-efficient, Facebook research | No persistence, single-node | Research, prototyping |
| **Pinecone** | Managed, scalable, easy API | Cost, vendor lock-in | Production, scale |
| **Weaviate** | Hybrid search, GraphQL, open source | Learning curve | Complex queries |
| **Chroma** | Simple, Python-native, lightweight | Less mature | Small projects |
| **Qdrant** | Performance, filtering, cloud-native | Smaller community | Filter-heavy apps |
| **Milvus** | High performance, distributed | Complex setup | Large-scale production |

### 12. **How would you optimize retrieval quality in a RAG system?**
1. **Chunking Strategy**:
   - Experiment with chunk sizes (256, 512, 1024 tokens)
   - Use overlap (10-20%) to maintain context
   - Consider semantic chunking

2. **Embedding Models**:
   - Use domain-specific embeddings if available
   - Consider multilingual models for diverse content
   - Evaluate different models on your data

3. **Retrieval Methods**:
   - **Hybrid Search**: Combine semantic + keyword search
   - **Re-ranking**: Use cross-encoder to re-rank results
   - **Metadata Filtering**: Filter by date, source, etc.

4. **Query Expansion**:
   ```python
   def expand_query(query):
       # Generate similar queries
       similar = [
           query,
           f"what is {query}",
           f"explain {query}",
           f"details about {query}"
       ]
       return similar
   ```

### 13. **What is query expansion and why is it useful?**
Query expansion generates multiple variations of a query to improve retrieval:
```python
def expand_query_with_llm(query, llm):
    prompt = f"""Generate 3 different ways to ask this question:
    Original: {query}
    
    Variations:
    1. """
    
    response = llm.invoke(prompt)
    variations = parse_variations(response)
    return [query] + variations
```

**Benefits**:
- Increases recall by matching different phrasings
- Handles synonyms and related concepts
- Improves results for ambiguous queries
- Can be done with LLMs or rule-based approaches

### 14. **How would you implement hybrid search (semantic + keyword)?**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class HybridRetriever:
    def __init__(self, documents, embeddings):
        self.documents = documents
        self.embeddings = embeddings  # Pre-computed embeddings
        self.tfidf = TfidfVectorizer().fit(documents)
        self.tfidf_vectors = self.tfidf.transform(documents)
    
    def search(self, query, query_embedding, alpha=0.5, top_k=5):
        # Semantic similarity
        semantic_scores = np.dot(self.embeddings, query_embedding)
        
        # Keyword similarity
        query_tfidf = self.tfidf.transform([query])
        keyword_scores = cosine_similarity(query_tfidf, self.tfidf_vectors).flatten()
        
        # Combine scores
        combined_scores = alpha * semantic_scores + (1 - alpha) * keyword_scores
        
        # Get top results
        top_indices = combined_scores.argsort()[-top_k:][::-1]
        return [(self.documents[i], combined_scores[i]) for i in top_indices]
```

### 15. **Explain the concept of "chunking" and its impact on RAG performance**
**Chunking** is splitting documents into smaller pieces for processing.

**Impact on performance**:
- **Too small chunks**: Lose context, poor retrieval quality
- **Too large chunks**: Exceed LLM context limits, irrelevant content
- **Optimal size**: 256-1024 tokens depending on content type

**Strategies**:
- **Fixed-size**: Simple but may break sentences
- **Sentence-aware**: Split at sentence boundaries
- **Paragraph-aware**: Split at paragraph boundaries  
- **Semantic**: Use embeddings to find natural breaks
- **Recursive**: Try larger splits first, then smaller

## ⚡ Performance & Optimization

### 16. **How would you optimize a LangChain application for 8GB RAM?**
1. **Memory Management**:
   ```python
   # Process documents in batches
   batch_size = 100  # Adjust based on memory
   for i in range(0, len(documents), batch_size):
       batch = documents[i:i+batch_size]
       process_batch(batch)
       del batch  # Explicit deletion
       import gc
       gc.collect()
   ```

2. **Model Selection**:
   - Use smaller embedding models (all-MiniLM-L6-v2 instead of larger ones)
   - Consider quantized models for inference
   - Use CPU-optimized models if GPU memory is limited

3. **Caching**:
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=1000)
   def get_embedding(text):
       return embedding_model.encode(text)
   ```

4. **Disk-based storage**:
   ```python
   # Store vectors on disk, not in memory
   import faiss
   index = faiss.read_index("vectors.index")  # Load from disk when needed
   ```

### 17. **What techniques can reduce LLM API costs?**
1. **Prompt Optimization**:
   - Use concise prompts
   - Cache common responses
   - Implement few-shot learning to reduce explanation

2. **Response Caching**:
   ```python
   import redis
   import hashlib
   
   cache = redis.Redis()
   
   def cached_llm_call(prompt, llm, ttl=3600):
       key = hashlib.md5(prompt.encode()).hexdigest()
       cached = cache.get(key)
       if cached:
           return cached.decode()
       
       response = llm.invoke(prompt)
       cache.setex(key, ttl, response.content)
       return response.content
   ```

3. **Token Management**:
   - Set max_tokens to reasonable limits
   - Use streaming for long responses
   - Implement token counting and budgeting

4. **Model Selection**:
   - Use cheaper models (gpt-3.5-turbo instead of gpt-4) when possible
   - Consider self-hosted models for high-volume use

### 18. **How would you implement streaming responses in a LangChain application?**
```python
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import OpenAI

# Method 1: Using callbacks
llm = OpenAI(
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
    temperature=0
)

# Method 2: Custom streaming
class CustomStreamHandler:
    def __init__(self):
        self.tokens = []
    
    def on_llm_new_token(self, token: str, **kwargs):
        self.tokens.append(token)
        print(token, end="", flush=True)

# Method 3: For web applications
async def stream_response(prompt, llm):
    response = ""
    async for chunk in llm.astream(prompt):
        response += chunk.content
        yield chunk.content  # Send to client
```

### 19. **What monitoring metrics would you track for a production LLM application?**
```python
class LLMMonitor:
    def __init__(self):
        self.metrics = {
            'requests_total': 0,
            'tokens_input_total': 0,
            'tokens_output_total': 0,
            'cost_total': 0.0,
            'latency_p50': 0.0,
            'latency_p95': 0.0,
            'latency_p99': 0.0,
            'error_rate': 0.0,
            'cache_hit_rate': 0.0,
            'user_satisfaction': 0.0  # From feedback
        }
    
    def record_request(self, input_tokens, output_tokens, latency, error=False):
        self.metrics['requests_total'] += 1
        self.metrics['tokens_input_total'] += input_tokens
        self.metrics['tokens_output_total'] += output_tokens
        self.metrics['cost_total'] += self.calculate_cost(input_tokens, output_tokens)
        
        # Update latency percentiles
        self.update_latency(latency)
        
        if error:
            self.metrics['error_rate'] = (
                self.metrics.get('error_count', 0) + 1
            ) / self.metrics['requests_total']
```

### 20. **How would you handle hallucinations in LLM responses?**
1. **RAG with citations**: Always provide source documents
2. **Confidence scoring**: Ask LLM to provide confidence scores
3. **Fact-checking pipeline**:
   ```python
   def verify_response(response, sources):
       # Extract claims from response
       claims = extract_claims(response)
       
       # Check each claim against sources
       for claim in claims:
           if not is_supported(claim, sources):
               return False, f"Claim not supported: {claim}"
       
       return True, "All claims supported"
   ```

4. **Prompt engineering**:
   ```python
   anti_hallucination_prompt = """
   Answer the question based ONLY on the provided context.
   If the context doesn't contain the answer, say "I cannot answer based on the provided information."
   
   Context: {context}
   
   Question: {question}
   
   Answer: 
   """
   ```

## 🔒 Security & Production

### 21. **What security considerations are important for LLM applications?**
1. **Prompt Injection**: Sanitize user inputs, use input validation
2. **Data Leakage**: Don't include sensitive data in prompts
3. **API Keys**: Rotate regularly, use environment variables
4. **Rate Limiting**: Prevent abuse and manage costs
5. **Content Filtering**: Implement output moderation
6. **Audit Logging**: Log all prompts and responses
7. **Access Control**: Restrict who can use the application

### 22. **How would you implement A/B testing for different prompt strategies?**
```python
class PromptExperiment:
    def __init__(self, variants):
        self.variants = variants  # List of (name, prompt_template)
        self.results = {name: {'success': 0, 'total': 0} for name, _ in variants}
    
    def get_variant(self, user_id):
        # Deterministic assignment based on user_id
        hash_val = hash(user_id) % 100
        if hash_val < 50:  # 50% traffic to variant A
            return self.variants[0]
        else:
            return self.variants[1]
    
    def record_result(self, variant_name, success):
        self.results[variant_name]['total'] += 1
        if success:
            self.results[variant_name]['success'] += 1
    
    def get_winner(self):
        # Calculate success rates
        rates = {}
        for name, data in self.results.items():
            if data['total'] > 0:
                rates[name] = data['success'] / data['total']
        
        return max(rates.items(), key=lambda x: x[1])
```

### 23. **Describe a deployment pipeline for a LangChain application**
1. **Development**:
   - Local testing with mock LLMs
   - Unit tests for chains and prompts
   - Integration tests with real LLMs (staging only)

2. **CI/CD**:
   ```yaml
   # .github/workflows/deploy.yml
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - Run prompt injection tests
         - Run unit tests
         - Run integration tests (staging)
     
     deploy:
       needs: test
       runs-on: ubuntu-latest
       steps:
         - Deploy to staging
         - Run smoke tests
         - Deploy to production (canary rollout)
   ```

3. **Monitoring**:
   - Log all prompts/responses (anonymized)
   - Monitor token usage and costs
   - Set up alerts for error spikes
   - Track user feedback and satisfaction

### 24. **How would you handle multilingual content in a RAG system?**
1. **Language Detection**:
   ```python
   from langdetect import detect
   
   def detect_language(text):
       try:
           return detect(text)
       except:
           return 'en'  # Default to English
   ```

2. **Multilingual Embeddings**:
   ```python
   # Use models that support multiple languages
   model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
   ```

3. **Query Translation**:
   ```python
   def translate_query(query, target_lang='en'):
       if detect_language(query) == target_lang:
           return query
       
       # Use translation service or LLM
       translated = translation_service.translate(query, target_lang)
       return translated
   ```

4. **Language-specific chunking**: Adjust chunk sizes based on language characteristics

### 25. **What strategies would you use for incremental document updates in a RAG system?**
1. **Versioned embeddings**:
   ```python
   class VersionedVectorStore:
       def __init__(self):
           self.versions = {}  # doc_id -> [(embedding, timestamp)]
       
       def update_document(self, doc_id, new_content):
           new_embedding = embed(new_content)
           self.versions[doc_id].append((new_embedding, datetime.now()))
       
       def search(self, query, version='latest'):
           # Search appropriate version
           pass
   ```

2. **Delta updates**: Only re-embed changed sections
3. **Scheduled re-embedding**: Periodic full updates
4. **Hybrid approach**: Real-time updates for critical docs, batch for others

## 🎯 Scenario-Based Questions

### 26. **You're building a customer support chatbot. How would you design the RAG system?**
**Approach**:
1. **Knowledge Base**:
   - Product documentation
   - FAQ articles
   - Previous support tickets
   - Release notes

2. **Chunking Strategy**:
   - FAQ: Keep entire Q&A pairs together
   - Documentation: Split by section headers
   - Tickets: Split by conversation turns

3. **Retrieval**:
   - Hybrid search (semantic + keyword)
   - Boost recent documents
   - Filter by product/version metadata

4. **Response Generation**:
   - Include source citations
   - Ask clarifying questions for ambiguous queries
   - Escalate to human agent when confidence is low

5. **Evaluation**:
   - A/B test different retrieval strategies
   - Collect user feedback (thumbs up/down)
   - Monitor deflection rate (questions resolved without human)

### 27. **Your LLM application is experiencing high latency. How would you diagnose and fix it?**
**Diagnosis**:
1. **Profile each component**:
   ```python
   import time
   
   def timed_operation(func, *args):
       start = time.time()
       result = func(*args)
       elapsed = time.time() - start
       print(f"{func.__name__}: {elapsed:.2f}s")
       return result
   ```

2. **Check bottlenecks**:
   - Embedding generation time
   - Vector search latency
   - LLM API response time
   - Network latency

3. **Monitor resource usage**:
   - CPU/Memory during peak
   - Network I/O
   - Disk I/O for vector stores

**Solutions**:
1. **Caching**:
   - Cache embeddings for static documents
   - Cache LLM responses for common queries
   - Use CDN for static assets

2. **Optimizations**:
   - Use smaller embedding models
   - Implement approximate nearest neighbor search
   - Batch requests when possible
   - Use streaming responses

3. **Infrastructure**:
   - Scale horizontally with load balancers
   - Use faster hardware (GPUs for embeddings)
   - Implement connection pooling

### 28. **How would you implement a fact-checking layer for an LLM-powered news summarizer?**
```python
class FactChecker:
    def __init__(self, trusted_sources):
        self.trusted_sources = trusted_sources  # List of reliable domains
        self.claim_extractor = ClaimExtractor()
        self.source_verifier = SourceVerifier()
    
    def check_summary(self, summary, original_article):
        # Extract claims from summary
        claims = self.claim_extractor.extract(summary)
        
        verified_claims = []
        unverified_claims = []
        
        for claim in claims:
            # Check if claim is in original article
            if self.in_article(claim, original_article):
                verified_claims.append(claim)
            # Check trusted sources
            elif self.source_verifier.verify(claim, self.trusted_sources):
                verified_claims.append(claim)
            else:
                unverified_claims.append(claim)
        
        return {
            'verified': verified_claims,
            'unverified': unverified_claims,
            'confidence': len(verified_claims) / max(len(claims), 1)
        }
```

### 29. **Design a system that can handle 10,000 concurrent users querying a RAG system**
**Architecture**:
1. **Load Balancer**: Distribute requests across multiple instances
2. **Application Servers** (stateless):
   - Handle prompt construction
   - Manage conversation state (in Redis)
   - Call LLM APIs

3. **Vector Database Cluster**:
   - Sharded by document category
   - Read replicas for scaling
   - Connection pooling

4. **Caching Layer**:
   - Redis for frequent queries
   - CDN for static embeddings

5. **Async Processing**:
   ```python
   async def handle_query(user_query, session):
       # Async embedding generation
       query_embedding = await embed_async(user_query)
       
       # Async vector search
       results = await vector_store.search_async(query_embedding)
       
       # Async LLM call
       response = await llm.ainvoke(construct_prompt(results, user_query))
       
       return response
   ```

6. **Rate Limiting**: Per-user and global limits
7. **Monitoring**: Real-time dashboards for all components

### 30. **How would you update a RAG system when new documents arrive continuously?**
**Real-time updates**:
```python
class StreamingRAGUpdater:
    def __init__(self, vector_store, batch_size=100, update_interval=60):
        self.vector_store = vector_store
        self.batch_size = batch_size
        self.update_interval = update_interval
        self.pending_docs = []
        self.last_update = time.time()
    
    def add_document(self, document):
        self.pending_docs.append(document)
        
        # Batch update if enough documents or time elapsed
        if (len(self.pending_docs) >= self.batch_size or 
            time.time() - self.last_update > self.update_interval):
            self.flush_batch()
    
    def flush_batch(self):
        if not self.pending_docs:
            return
        
        # Process batch
        embeddings = embed_batch(self.pending_docs)
        self.vector_store.add_vectors(embeddings, self.pending_docs)
        
        # Clear and update timestamp
        self.pending_docs = []
        self.last_update = time.time()
```

**Strategies**:
1. **Micro-batching**: Update every N documents or T seconds
2. **Priority queue**: Important documents processed first
3. **Incremental indexing**: Only update changed sections
4. **Versioning**: Maintain multiple indices for zero-downtime updates

## 💻 Coding Exercises

### 31. **Implement a prompt template for data analysis questions**
```python
def create_data_analysis_prompt():
    # TODO: Implement a prompt template that:
    # 1. Takes a dataset description and question
    # 2. Includes examples of good analysis
    # 3. Guides the LLM through step-by-step reasoning
    # 4. Requests output in a structured format (JSON)
    pass
```

### 32. **Create a simple RAG system with TF-IDF retrieval**
```python
class SimpleRAGSystem:
    def __init__(self, documents):
        # TODO: Initialize TF-IDF vectorizer
        # TODO: Fit on documents
        pass
    
    def retrieve(self, query, top_k=3):
        # TODO: Convert query to TF-IDF vector
        # TODO: Calculate cosine similarity with all documents
        # TODO: Return top_k most similar documents
        pass
    
    def answer(self, query):
        # TODO: Retrieve relevant documents
        # TODO: Construct prompt with context
        # TODO: Generate answer using LLM
        # TODO: Return answer with sources
        pass
```

### 33. **Implement conversation memory with summary**
```python
class SummarizingMemory:
    def __init__(self, max_messages=10):
        # TODO: Store recent messages
        # TODO: Maintain conversation summary
        # TODO: Implement message addition with automatic summarization
        pass
    
    def add_message(self, role, content):
        # TODO: Add message to history
        # TODO: Update summary if needed
        pass
    
    def get_summary(self):
        # TODO: Return current conversation summary
        pass
    
    def get_recent_messages(self, n=5):
        # TODO: Return last n messages
        pass
```

### 34. **Build a cost-aware LLM wrapper with caching**
```python
class CostAwareLLM:
    def __init__(self, llm, max_cost_per_day=10.0):
        # TODO: Initialize LLM and cost tracking
        # TODO: Set up cache (Redis or in-memory)
        pass
    
    def invoke(self, prompt, use_cache=True):
        # TODO: Check cache first if use_cache=True
        # TODO: Calculate token count and estimated cost
        # TODO: Check if within daily budget
        # TODO: Call LLM if not cached and within budget
        # TODO: Cache result
        # TODO: Update cost tracking
        # TODO: Return response
        pass
    
    def get_daily_cost(self):
        # TODO: Return cost so far today
        pass
```

### 35. **Create a hybrid search retriever**
```python
class HybridRetriever:
    def __init__(self, documents):
        # TODO: Initialize both semantic and keyword retrievers
        # TODO: Pre-compute embeddings for semantic search
        # TODO: Build TF-IDF index for keyword search
        pass
    
    def search(self, query, alpha=0.5, top_k=5):
        # TODO: Get semantic similarity scores
        # TODO: Get keyword similarity scores
        # TODO: Combine scores using alpha parameter
        # TODO: Return top_k documents with combined scores
        pass
    
    def tune_alpha(self, queries, relevant_docs):
        # TODO: Find optimal alpha using validation data
        # TODO: Return best alpha value
        pass
```

## 📚 Recommended Resources

### Books & Courses:
- **"Prompt Engineering for Developers"** - DeepLearning.AI
- **"Building LLM Applications with LangChain"** - Official documentation
- **"Designing Machine Learning Systems"** - Chip Huyen

### Documentation:
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI Cookbook](https://cookbook.openai.com/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)

### Tools & Libraries:
- **LlamaIndex**: Alternative to LangChain for RAG
- **Haystack**: NLP framework with RAG capabilities
- **Weaviate**: Vector database with hybrid search
- **Chroma**: Lightweight vector database

### Practice Platforms:
- **Hugging Face Spaces**: Deploy LLM apps
- **LangChain Templates**: Pre-built solutions
- **OpenAI Playground**: Experiment with prompts

## 🎯 Interview Preparation Tips

### 1. **Understand the fundamentals**:
   - Prompt engineering techniques
   - RAG architecture and components
   - LLM limitations and capabilities

### 2. **Practice explaining trade-offs**:
   - Accuracy vs. latency vs. cost
   - Different embedding models and vector stores
   - Prompt design choices

### 3. **Be ready for coding exercises**:
   - Implement basic RAG systems
   - Design prompt templates
   - Optimize for performance and cost

### 4. **Prepare questions for the interviewer**:
   - What are the main use cases for LLMs in your organization?
   - What scale are you operating at (QPS, data volume)?
   - What are your biggest challenges with LLM applications?

### 5. **Showcase your experience**:
   - Discuss projects where you used LangChain/LLMs
   - Explain design decisions and trade-offs
   - Share lessons learned from production deployments

## 🔗 Related Resources in This Repository
- `01_prompts.py` - Prompt engineering examples
- `02_rag_basics.py` - RAG implementation basics
- `practice_exercises.py` - Hands-on coding challenges
- `GOTCHAS_BEST_PRACTICES.md` - Common pitfalls and solutions