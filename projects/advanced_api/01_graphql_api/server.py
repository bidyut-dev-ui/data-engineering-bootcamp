#!/usr/bin/env python3
"""
GraphQL Server Implementation

This module implements a GraphQL server using Strawberry with FastAPI.
It demonstrates:
- GraphQL endpoint setup with FastAPI
- GraphQL playground for interactive queries
- Subscription support with WebSockets
- Error handling and logging
- Performance monitoring

Key Features:
- Full GraphQL implementation (queries, mutations, subscriptions)
- WebSocket support for real-time subscriptions
- Interactive GraphQL playground
- Request logging and error handling
"""

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import strawberry
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager
import logging
import time
from typing import Dict, Any

# Import schema from schema.py
from schema import schema, print_schema

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# MIDDLEWARE AND UTILITIES
# ============================================================================

class RequestLogger:
    """Middleware to log GraphQL requests and responses."""
    
    async def __call__(self, request: Request, call_next):
        """Log request details and response time."""
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")
        
        if request.method == "POST" and "graphql" in request.url.path:
            try:
                body = await request.json()
                operation_name = body.get("operationName", "unnamed")
                logger.info(f"GraphQL Operation: {operation_name}")
            except Exception:
                pass
        
        # Process request
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        logger.info(f"Response: {response.status_code} ({process_time:.3f}s)")
        
        return response


class ErrorHandler:
    """Middleware to handle and log errors."""
    
    async def __call__(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(f"Unhandled error: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error")


# ============================================================================
# GRAPHQL ROUTER SETUP
# ============================================================================

# Create GraphQL router with schema
graphql_app = GraphQLRouter(
    schema,
    graphiql=True,  # Enable GraphiQL playground
    subscription_protocols=["graphql-ws"]  # WebSocket protocol for subscriptions
)


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    logger.info("Starting GraphQL server...")
    print_schema()
    yield
    # Shutdown
    logger.info("Shutting down GraphQL server...")


# Create FastAPI application
app = FastAPI(
    title="Advanced GraphQL API",
    description="A sample GraphQL API demonstrating advanced features",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.middleware("http")(RequestLogger())
app.middleware("http")(ErrorHandler())

# Add GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")


# ============================================================================
# ADDITIONAL ROUTES
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API information."""
    return """
    <html>
        <head>
            <title>Advanced GraphQL API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .card { background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }
                .endpoint { background: #e8f4f8; padding: 10px; border-radius: 4px; font-family: monospace; }
                a { color: #007bff; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Advanced GraphQL API</h1>
                <p>Welcome to the Advanced GraphQL API demonstration.</p>
                
                <div class="card">
                    <h2>📚 Available Endpoints</h2>
                    
                    <h3>GraphQL Endpoints:</h3>
                    <div class="endpoint">POST /graphql</div>
                    <p>Main GraphQL endpoint for queries and mutations</p>
                    
                    <div class="endpoint">GET /graphql</div>
                    <p>GraphiQL playground for interactive queries</p>
                    
                    <div class="endpoint">WS /graphql</div>
                    <p>WebSocket endpoint for GraphQL subscriptions</p>
                    
                    <h3>REST Endpoints:</h3>
                    <div class="endpoint">GET /health</div>
                    <p>Health check endpoint</p>
                    
                    <div class="endpoint">GET /schema</div>
                    <p>View GraphQL schema in text format</p>
                </div>
                
                <div class="card">
                    <h2>🔗 Quick Links</h2>
                    <ul>
                        <li><a href="/graphql" target="_blank">GraphiQL Playground</a></li>
                        <li><a href="/schema" target="_blank">GraphQL Schema</a></li>
                        <li><a href="/health" target="_blank">Health Check</a></li>
                    </ul>
                </div>
                
                <div class="card">
                    <h2>📖 Example Queries</h2>
                    <h3>Get all posts:</h3>
                    <pre>
query {
  posts(publishedOnly: true) {
    id
    title
    author {
      name
      email
    }
    tags
  }
}
                    </pre>
                    
                    <h3>Create a new post:</h3>
                    <pre>
mutation {
  createPost(postInput: {
    title: "New Post",
    content: "Post content...",
    authorId: "author-id-here",
    tags: ["graphql", "api"]
  }) {
    id
    title
    published
  }
}
                    </pre>
                    
                    <h3>Subscribe to new comments:</h3>
                    <pre>
subscription {
  commentAdded(postId: "post-id-here") {
    id
    content
    authorName
    createdAt
  }
}
                    </pre>
                </div>
                
                <div class="card">
                    <h2>⚙️ Features</h2>
                    <ul>
                        <li>Full GraphQL implementation (Queries, Mutations, Subscriptions)</li>
                        <li>Real-time updates via WebSocket subscriptions</li>
                        <li>Interactive GraphiQL playground</li>
                        <li>Request logging and error handling</li>
                        <li>CORS support</li>
                        <li>Health monitoring</li>
                    </ul>
                </div>
            </div>
        </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "graphql-api",
        "version": "1.0.0"
    }


@app.get("/schema")
async def get_schema():
    """Return the GraphQL schema in text format."""
    return {
        "schema": str(schema),
        "types": {
            "query": [field.name for field in schema.query.__strawberry_field__],
            "mutation": [field.name for field in schema.mutation.__strawberry_field__],
            "subscription": [field.name for field in schema.subscription.__strawberry_field__]
        }
    }


# ============================================================================
# GRAPHQL QUERY EXAMPLES
# ============================================================================

@app.get("/examples")
async def graphql_examples():
    """Return example GraphQL queries."""
    return {
        "queries": [
            {
                "name": "Get all published posts",
                "query": """
                query {
                  posts(publishedOnly: true) {
                    id
                    title
                    author {
                      name
                      email
                    }
                    tags
                    createdAt
                  }
                }
                """
            },
            {
                "name": "Get author with posts",
                "query": """
                query {
                  author(id: "author-id") {
                    name
                    email
                    bio
                    posts {
                      title
                      published
                    }
                  }
                }
                """
            },
            {
                "name": "Search posts",
                "query": """
                query {
                  searchPosts(query: "GraphQL") {
                    title
                    content
                    author {
                      name
                    }
                  }
                }
                """
            }
        ],
        "mutations": [
            {
                "name": "Create new author",
                "query": """
                mutation {
                  createAuthor(authorInput: {
                    name: "New Author",
                    email: "author@example.com",
                    bio: "Software developer"
                  }) {
                    id
                    name
                    email
                  }
                }
                """
            },
            {
                "name": "Create new post",
                "query": """
                mutation {
                  createPost(postInput: {
                    title: "New Post Title",
                    content: "Post content goes here...",
                    authorId: "author-id",
                    tags: ["python", "graphql"],
                    published: true
                  }) {
                    id
                    title
                    published
                  }
                }
                """
            }
        ],
        "subscriptions": [
            {
                "name": "Subscribe to new comments",
                "query": """
                subscription {
                  commentAdded(postId: "post-id") {
                    id
                    content
                    authorName
                    createdAt
                  }
                }
                """
            },
            {
                "name": "Subscribe to published posts",
                "query": """
                subscription {
                  postPublished {
                    id
                    title
                    author {
                      name
                    }
                    createdAt
                  }
                }
                """
            }
        ]
    }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Run the server
    logger.info("Starting GraphQL server on http://localhost:8000")
    logger.info("GraphiQL playground available at http://localhost:8000/graphql")
    logger.info("WebSocket subscriptions available at ws://localhost:8000/graphql")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True  # Enable auto-reload for development
    )