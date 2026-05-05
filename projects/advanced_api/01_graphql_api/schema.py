#!/usr/bin/env python3
"""
GraphQL Schema Definition

This module defines the GraphQL schema for a sample blog application.
It demonstrates GraphQL type definitions, queries, mutations, and subscriptions.

Key Concepts:
- Type definitions with Strawberry
- Query resolvers for data fetching
- Mutation resolvers for data modification
- Subscription resolvers for real-time updates
- Input types for mutation arguments
"""

import strawberry
from typing import List, Optional, AsyncGenerator
from datetime import datetime
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================================
# TYPE DEFINITIONS
# ============================================================================

@strawberry.type
class Author:
    """Author type representing a blog post author."""
    id: strawberry.ID
    name: str
    email: str
    bio: Optional[str] = None
    created_at: datetime


@strawberry.type
class Post:
    """Post type representing a blog post."""
    id: strawberry.ID
    title: str
    content: str
    published: bool
    author: "Author"
    tags: List[str]
    created_at: datetime
    updated_at: Optional[datetime] = None


@strawberry.type
class Comment:
    """Comment type representing a comment on a blog post."""
    id: strawberry.ID
    content: str
    author_name: str
    post_id: strawberry.ID
    created_at: datetime


@strawberry.input
class AuthorInput:
    """Input type for creating/updating authors."""
    name: str
    email: str
    bio: Optional[str] = None


@strawberry.input
class PostInput:
    """Input type for creating/updating posts."""
    title: str
    content: str
    author_id: strawberry.ID
    tags: Optional[List[str]] = None
    published: Optional[bool] = False


@strawberry.input
class CommentInput:
    """Input type for creating comments."""
    content: str
    author_name: str
    post_id: strawberry.ID


# ============================================================================
# IN-MEMORY DATABASE (FOR DEMONSTRATION)
# ============================================================================

class Database:
    """In-memory database for demonstration purposes."""
    
    def __init__(self):
        self.authors = {}
        self.posts = {}
        self.comments = {}
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample data for demonstration."""
        # Create sample authors
        author1_id = str(uuid.uuid4())
        author2_id = str(uuid.uuid4())
        
        self.authors[author1_id] = Author(
            id=author1_id,
            name="Alice Johnson",
            email="alice@example.com",
            bio="Python developer and blogger",
            created_at=datetime.now()
        )
        
        self.authors[author2_id] = Author(
            id=author2_id,
            name="Bob Smith",
            email="bob@example.com",
            bio="Data scientist and writer",
            created_at=datetime.now()
        )
        
        # Create sample posts
        post1_id = str(uuid.uuid4())
        post2_id = str(uuid.uuid4())
        
        self.posts[post1_id] = Post(
            id=post1_id,
            title="Getting Started with GraphQL",
            content="GraphQL is a query language for APIs...",
            published=True,
            author=self.authors[author1_id],
            tags=["graphql", "api", "tutorial"],
            created_at=datetime.now()
        )
        
        self.posts[post2_id] = Post(
            id=post2_id,
            title="Advanced Python Patterns",
            content="Python offers many advanced patterns...",
            published=True,
            author=self.authors[author2_id],
            tags=["python", "patterns", "advanced"],
            created_at=datetime.now()
        )
        
        # Create sample comments
        comment1_id = str(uuid.uuid4())
        self.comments[comment1_id] = Comment(
            id=comment1_id,
            content="Great article! Very helpful.",
            author_name="Charlie",
            post_id=post1_id,
            created_at=datetime.now()
        )
    
    def get_author(self, author_id: str) -> Optional[Author]:
        """Get author by ID."""
        return self.authors.get(author_id)
    
    def get_all_authors(self) -> List[Author]:
        """Get all authors."""
        return list(self.authors.values())
    
    def create_author(self, author_input: AuthorInput) -> Author:
        """Create a new author."""
        author_id = str(uuid.uuid4())
        author = Author(
            id=author_id,
            name=author_input.name,
            email=author_input.email,
            bio=author_input.bio,
            created_at=datetime.now()
        )
        self.authors[author_id] = author
        logger.info(f"Created author: {author.name} ({author_id})")
        return author
    
    def update_author(self, author_id: str, author_input: AuthorInput) -> Optional[Author]:
        """Update an existing author."""
        if author_id not in self.authors:
            return None
        
        author = self.authors[author_id]
        # Update fields
        author.name = author_input.name
        author.email = author_input.email
        author.bio = author_input.bio
        
        logger.info(f"Updated author: {author.name} ({author_id})")
        return author
    
    def delete_author(self, author_id: str) -> bool:
        """Delete an author."""
        if author_id in self.authors:
            author_name = self.authors[author_id].name
            del self.authors[author_id]
            logger.info(f"Deleted author: {author_name} ({author_id})")
            return True
        return False
    
    def get_post(self, post_id: str) -> Optional[Post]:
        """Get post by ID."""
        return self.posts.get(post_id)
    
    def get_all_posts(self, published_only: bool = False) -> List[Post]:
        """Get all posts, optionally filtered by published status."""
        posts = list(self.posts.values())
        if published_only:
            posts = [post for post in posts if post.published]
        return posts
    
    def get_posts_by_author(self, author_id: str) -> List[Post]:
        """Get all posts by a specific author."""
        return [post for post in self.posts.values() if post.author.id == author_id]
    
    def create_post(self, post_input: PostInput) -> Optional[Post]:
        """Create a new post."""
        # Check if author exists
        author = self.get_author(post_input.author_id)
        if not author:
            return None
        
        post_id = str(uuid.uuid4())
        post = Post(
            id=post_id,
            title=post_input.title,
            content=post_input.content,
            published=post_input.published or False,
            author=author,
            tags=post_input.tags or [],
            created_at=datetime.now()
        )
        self.posts[post_id] = post
        logger.info(f"Created post: {post.title} ({post_id})")
        return post
    
    def get_comments_for_post(self, post_id: str) -> List[Comment]:
        """Get all comments for a specific post."""
        return [comment for comment in self.comments.values() if comment.post_id == post_id]
    
    def create_comment(self, comment_input: CommentInput) -> Optional[Comment]:
        """Create a new comment."""
        # Check if post exists
        post = self.get_post(comment_input.post_id)
        if not post:
            return None
        
        comment_id = str(uuid.uuid4())
        comment = Comment(
            id=comment_id,
            content=comment_input.content,
            author_name=comment_input.author_name,
            post_id=comment_input.post_id,
            created_at=datetime.now()
        )
        self.comments[comment_id] = comment
        logger.info(f"Created comment on post {comment_input.post_id} by {comment_input.author_name}")
        return comment


# Initialize database
db = Database()


# ============================================================================
# QUERY RESOLVERS
# ============================================================================

@strawberry.type
class Query:
    """GraphQL query definitions."""
    
    @strawberry.field
    def hello(self) -> str:
        """Simple hello query for testing."""
        return "Hello from GraphQL API!"
    
    @strawberry.field
    def author(self, id: strawberry.ID) -> Optional[Author]:
        """Get a single author by ID."""
        return db.get_author(str(id))
    
    @strawberry.field
    def authors(self) -> List[Author]:
        """Get all authors."""
        return db.get_all_authors()
    
    @strawberry.field
    def post(self, id: strawberry.ID) -> Optional[Post]:
        """Get a single post by ID."""
        return db.get_post(str(id))
    
    @strawberry.field
    def posts(self, published_only: Optional[bool] = False) -> List[Post]:
        """Get all posts, optionally filtered by published status."""
        return db.get_all_posts(published_only)
    
    @strawberry.field
    def posts_by_author(self, author_id: strawberry.ID) -> List[Post]:
        """Get all posts by a specific author."""
        return db.get_posts_by_author(str(author_id))
    
    @strawberry.field
    def comments(self, post_id: strawberry.ID) -> List[Comment]:
        """Get all comments for a specific post."""
        return db.get_comments_for_post(str(post_id))
    
    @strawberry.field
    def search_posts(self, query: str) -> List[Post]:
        """Search posts by title or content."""
        query_lower = query.lower()
        results = []
        
        for post in db.posts.values():
            if (query_lower in post.title.lower() or 
                query_lower in post.content.lower()):
                results.append(post)
        
        return results


# ============================================================================
# MUTATION RESOLVERS
# ============================================================================

@strawberry.type
class Mutation:
    """GraphQL mutation definitions."""
    
    @strawberry.mutation
    def create_author(self, author_input: AuthorInput) -> Author:
        """Create a new author."""
        return db.create_author(author_input)
    
    @strawberry.mutation
    def update_author(self, id: strawberry.ID, author_input: AuthorInput) -> Optional[Author]:
        """Update an existing author."""
        return db.update_author(str(id), author_input)
    
    @strawberry.mutation
    def delete_author(self, id: strawberry.ID) -> bool:
        """Delete an author."""
        return db.delete_author(str(id))
    
    @strawberry.mutation
    def create_post(self, post_input: PostInput) -> Optional[Post]:
        """Create a new post."""
        return db.create_post(post_input)
    
    @strawberry.mutation
    def publish_post(self, id: strawberry.ID) -> Optional[Post]:
        """Publish a post (set published=True)."""
        post = db.get_post(str(id))
        if post:
            post.published = True
            post.updated_at = datetime.now()
            logger.info(f"Published post: {post.title}")
        return post
    
    @strawberry.mutation
    def create_comment(self, comment_input: CommentInput) -> Optional[Comment]:
        """Create a new comment on a post."""
        return db.create_comment(comment_input)


# ============================================================================
# SUBSCRIPTION RESOLVERS
# ============================================================================

@strawberry.type
class Subscription:
    """GraphQL subscription definitions for real-time updates."""
    
    @strawberry.subscription
    async def comment_added(self, post_id: strawberry.ID) -> AsyncGenerator[Comment, None]:
        """Subscribe to new comments on a specific post."""
        # In a real implementation, this would use a pub/sub system
        # For demonstration, we'll simulate with async sleep
        import asyncio
        
        logger.info(f"Subscription started for comments on post {post_id}")
        
        # Simulate receiving new comments
        for i in range(3):
            await asyncio.sleep(2.0)  # Wait 2 seconds between "new comments"
            
            # Create a simulated comment
            comment = Comment(
                id=str(uuid.uuid4()),
                content=f"Simulated comment #{i+1} via subscription",
                author_name="Subscriber",
                post_id=str(post_id),
                created_at=datetime.now()
            )
            
            logger.info(f"Emitting comment via subscription: {comment.content}")
            yield comment
    
    @strawberry.subscription
    async def post_published(self) -> AsyncGenerator[Post, None]:
        """Subscribe to newly published posts."""
        import asyncio
        
        logger.info("Subscription started for published posts")
        
        # Simulate new posts being published
        sample_titles = [
            "New GraphQL Features",
            "Python Async Patterns",
            "Microservices Best Practices",
            "API Design Principles"
        ]
        
        for i, title in enumerate(sample_titles):
            await asyncio.sleep(3.0)  # Wait 3 seconds between "new posts"
            
            # Create a simulated post
            authors = list(db.authors.values())
            if authors:
                author = authors[i % len(authors)]
                
                post = Post(
                    id=str(uuid.uuid4()),
                    title=title,
                    content=f"Content for {title}...",
                    published=True,
                    author=author,
                    tags=["graphql", "python", "api"][:i % 3 + 1],
                    created_at=datetime.now()
                )
                
                logger.info(f"Emitting post via subscription: {post.title}")
                yield post


# ============================================================================
# SCHEMA DEFINITION
# ============================================================================

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def print_schema() -> None:
    """Print the GraphQL schema for inspection."""
    print("=" * 60)
    print("GRAPHQL SCHEMA")
    print("=" * 60)
    print(schema)
    print("=" * 60)


if __name__ == "__main__":
    # Print the schema when run directly
    print_schema()
    print("\nSchema types defined:")
    print(f"- Query fields: {[field.name for field in Query.__strawberry_field__]}")
    print(f"- Mutation fields: {[field.name for field in Mutation.__strawberry_field__]}")
    print(f"- Subscription fields: {[field.name for field in Subscription.__strawberry_field__]}")