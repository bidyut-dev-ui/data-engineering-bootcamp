#!/usr/bin/env python3
"""
WebSocket Chat Server

This module implements a real-time chat server using WebSockets.
It demonstrates:
- WebSocket connection management
- Room-based messaging
- User authentication and session management
- Heartbeat and connection health monitoring
- Error handling and reconnection logic

Key Features:
- Multiple chat rooms support
- User presence tracking
- Message broadcasting
- Private messaging
- Connection state management
"""

import asyncio
import json
import logging
import uuid
import time
from typing import Dict, Set, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime

import websockets
from websockets.exceptions import ConnectionClosed, ConnectionClosedOK
from websockets.server import WebSocketServerProtocol

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# DATA MODELS
# ============================================================================

class MessageType(Enum):
    """Types of messages that can be sent."""
    CHAT = "chat"
    JOIN = "join"
    LEAVE = "leave"
    ERROR = "error"
    HEARTBEAT = "heartbeat"
    USER_LIST = "user_list"
    PRIVATE = "private"
    SYSTEM = "system"


@dataclass
class User:
    """Represents a connected user."""
    id: str
    username: str
    connection: WebSocketServerProtocol
    joined_at: datetime
    last_seen: datetime
    room: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "username": self.username,
            "joined_at": self.joined_at.isoformat(),
            "room": self.room
        }


@dataclass
class ChatMessage:
    """Represents a chat message."""
    id: str
    type: MessageType
    sender: str
    content: str
    timestamp: datetime
    room: Optional[str] = None
    recipient: Optional[str] = None  # For private messages
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "type": self.type.value,
            "sender": self.sender,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "room": self.room,
            "recipient": self.recipient
        }


# ============================================================================
# CHAT SERVER
# ============================================================================

class ChatServer:
    """WebSocket chat server managing connections, rooms, and messages."""
    
    def __init__(self):
        self.users: Dict[str, User] = {}  # user_id -> User
        self.rooms: Dict[str, Set[str]] = {}  # room_name -> set of user_ids
        self.message_history: Dict[str, List[ChatMessage]] = {}  # room_name -> list of messages
        self.max_history_per_room = 100
        
        # Statistics
        self.stats = {
            "connections_total": 0,
            "messages_total": 0,
            "active_connections": 0,
            "rooms_created": 0
        }
    
    async def handle_connection(self, websocket: WebSocketServerProtocol, path: str):
        """Handle a new WebSocket connection."""
        user = None
        
        try:
            # Authenticate user (in real app, this would validate tokens)
            user = await self._authenticate_user(websocket)
            if not user:
                return
            
            self.stats["connections_total"] += 1
            self.stats["active_connections"] += 1
            
            logger.info(f"User connected: {user.username} ({user.id})")
            
            # Send welcome message
            await self._send_welcome(user)
            
            # Main message handling loop
            async for message in websocket:
                await self._handle_message(user, message)
        
        except ConnectionClosedOK:
            logger.info(f"User disconnected normally: {user.username if user else 'Unknown'}")
        
        except ConnectionClosed as e:
            logger.warning(f"User disconnected with error: {e}")
        
        except Exception as e:
            logger.error(f"Error handling connection: {e}", exc_info=True)
        
        finally:
            # Clean up user connection
            if user:
                await self._handle_user_disconnect(user)
                self.stats["active_connections"] -= 1
    
    async def _authenticate_user(self, websocket: WebSocketServerProtocol) -> Optional[User]:
        """Authenticate user and create User object."""
        try:
            # Wait for authentication message
            auth_message = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            auth_data = json.loads(auth_message)
            
            if auth_data.get("type") != "auth":
                await websocket.send(json.dumps({
                    "type": "error",
                    "content": "Authentication required first"
                }))
                return None
            
            username = auth_data.get("username", f"user_{uuid.uuid4().hex[:8]}")
            user_id = str(uuid.uuid4())
            
            user = User(
                id=user_id,
                username=username,
                connection=websocket,
                joined_at=datetime.now(),
                last_seen=datetime.now()
            )
            
            self.users[user_id] = user
            
            # Send authentication success
            await websocket.send(json.dumps({
                "type": "auth_success",
                "user_id": user_id,
                "username": username,
                "timestamp": datetime.now().isoformat()
            }))
            
            return user
        
        except asyncio.TimeoutError:
            logger.warning("Authentication timeout")
            await websocket.send(json.dumps({
                "type": "error",
                "content": "Authentication timeout"
            }))
            return None
        
        except json.JSONDecodeError:
            logger.warning("Invalid JSON in authentication")
            await websocket.send(json.dumps({
                "type": "error",
                "content": "Invalid authentication data"
            }))
            return None
    
    async def _send_welcome(self, user: User):
        """Send welcome message to new user."""
        welcome_msg = ChatMessage(
            id=str(uuid.uuid4()),
            type=MessageType.SYSTEM,
            sender="System",
            content=f"Welcome to the chat server, {user.username}!",
            timestamp=datetime.now()
        )
        
        await user.connection.send(json.dumps({
            "type": "system",
            "message": welcome_msg.to_dict(),
            "server_info": {
                "users_online": len(self.users),
                "rooms_available": list(self.rooms.keys()),
                "server_time": datetime.now().isoformat()
            }
        }))
    
    async def _handle_message(self, user: User, raw_message: str):
        """Handle incoming message from user."""
        try:
            message_data = json.loads(raw_message)
            message_type = message_data.get("type")
            
            # Update last seen timestamp
            user.last_seen = datetime.now()
            
            # Handle heartbeat
            if message_type == "heartbeat":
                await self._handle_heartbeat(user)
                return
            
            # Handle different message types
            if message_type == "join":
                await self._handle_join_room(user, message_data)
            
            elif message_type == "leave":
                await self._handle_leave_room(user, message_data)
            
            elif message_type == "chat":
                await self._handle_chat_message(user, message_data)
            
            elif message_type == "private":
                await self._handle_private_message(user, message_data)
            
            elif message_type == "list_users":
                await self._handle_list_users(user, message_data)
            
            elif message_type == "list_rooms":
                await self._handle_list_rooms(user)
            
            else:
                await self._send_error(user, f"Unknown message type: {message_type}")
        
        except json.JSONDecodeError:
            await self._send_error(user, "Invalid JSON format")
        
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            await self._send_error(user, f"Internal server error: {str(e)}")
    
    async def _handle_heartbeat(self, user: User):
        """Handle heartbeat message."""
        user.last_seen = datetime.now()
        await user.connection.send(json.dumps({
            "type": "heartbeat_ack",
            "timestamp": datetime.now().isoformat()
        }))
    
    async def _handle_join_room(self, user: User, data: Dict[str, Any]):
        """Handle user joining a room."""
        room_name = data.get("room", "general")
        
        # Leave current room if any
        if user.room:
            await self._handle_leave_room(user, {"room": user.room})
        
        # Create room if it doesn't exist
        if room_name not in self.rooms:
            self.rooms[room_name] = set()
            self.message_history[room_name] = []
            self.stats["rooms_created"] += 1
            logger.info(f"Created new room: {room_name}")
        
        # Add user to room
        self.rooms[room_name].add(user.id)
        user.room = room_name
        
        # Send join notification to room
        join_msg = ChatMessage(
            id=str(uuid.uuid4()),
            type=MessageType.JOIN,
            sender=user.username,
            content=f"{user.username} joined the room",
            timestamp=datetime.now(),
            room=room_name
        )
        
        await self._broadcast_to_room(room_name, join_msg)
        
        # Send room history to user
        history = self.message_history.get(room_name, [])
        recent_history = history[-20:]  # Last 20 messages
        
        await user.connection.send(json.dumps({
            "type": "room_joined",
            "room": room_name,
            "users_in_room": [self.users[uid].username for uid in self.rooms[room_name]],
            "message_history": [msg.to_dict() for msg in recent_history]
        }))
        
        logger.info(f"User {user.username} joined room {room_name}")
    
    async def _handle_leave_room(self, user: User, data: Dict[str, Any]):
        """Handle user leaving a room."""
        room_name = data.get("room")
        
        if not room_name or room_name not in self.rooms:
            await self._send_error(user, f"Not in room: {room_name}")
            return
        
        if user.id not in self.rooms[room_name]:
            await self._send_error(user, f"Not a member of room: {room_name}")
            return
        
        # Remove user from room
        self.rooms[room_name].remove(user.id)
        user.room = None
        
        # Send leave notification to room
        leave_msg = ChatMessage(
            id=str(uuid.uuid4()),
            type=MessageType.LEAVE,
            sender=user.username,
            content=f"{user.username} left the room",
            timestamp=datetime.now(),
            room=room_name
        )
        
        await self._broadcast_to_room(room_name, leave_msg)
        
        # Clean up empty room
        if not self.rooms[room_name]:
            del self.rooms[room_name]
            if room_name in self.message_history:
                del self.message_history[room_name]
            logger.info(f"Room {room_name} deleted (empty)")
        
        logger.info(f"User {user.username} left room {room_name}")
    
    async def _handle_chat_message(self, user: User, data: Dict[str, Any]):
        """Handle chat message."""
        if not user.room:
            await self._send_error(user, "You must join a room first")
            return
        
        content = data.get("content", "").strip()
        if not content:
            await self._send_error(user, "Message content cannot be empty")
            return
        
        # Create chat message
        chat_msg = ChatMessage(
            id=str(uuid.uuid4()),
            type=MessageType.CHAT,
            sender=user.username,
            content=content,
            timestamp=datetime.now(),
            room=user.room
        )
        
        # Add to room history
        room_history = self.message_history.get(user.room, [])
        room_history.append(chat_msg)
        
        # Trim history if too long
        if len(room_history) > self.max_history_per_room:
            room_history = room_history[-self.max_history_per_room:]
        
        self.message_history[user.room] = room_history
        self.stats["messages_total"] += 1
        
        # Broadcast to room
        await self._broadcast_to_room(user.room, chat_msg)
        
        logger.info(f"Chat message from {user.username} in {user.room}: {content[:50]}...")
    
    async def _handle_private_message(self, user: User, data: Dict[str, Any]):
        """Handle private message between users."""
        recipient_username = data.get("recipient")
        content = data.get("content", "").strip()
        
        if not recipient_username or not content:
            await self._send_error(user, "Recipient and content are required")
            return
        
        # Find recipient
        recipient = None
        for u in self.users.values():
            if u.username == recipient_username:
                recipient = u
                break
        
        if not recipient:
            await self._send_error(user, f"User '{recipient_username}' not found")
            return
        
        # Create private message
        private_msg = ChatMessage(
            id=str(uuid.uuid4()),
            type=MessageType.PRIVATE,
            sender=user.username,
            content=content,
            timestamp=datetime.now(),
            recipient=recipient.username
        )
        
        # Send to recipient
        await recipient.connection.send(json.dumps({
            "type": "private_message",
            "message": private_msg.to_dict()
        }))
        
        # Send confirmation to sender
        await user.connection.send(json.dumps({
            "type": "private_sent",
            "message_id": private_msg.id,
            "recipient": recipient.username,
            "timestamp": datetime.now().isoformat()
        }))
        
        logger.info(f"Private message from {user.username} to {recipient.username}")
    
    async def _handle_list_users(self, user: User, data: Dict[str, Any]):
        """Handle request to list users."""
        room_name = data.get("room")
        
        if room_name:
            # List users in specific room
            if room_name not in self.rooms:
                await self._send_error(user, f"Room '{room_name}' not found")
                return
            
            user_ids = self.rooms[room_name]
            users_in_room = [self.users[uid].username for uid in user_ids]
            
            await user.connection.send(json.dumps({
                "type": "user_list",
                "room": room_name,
                "users": users_in_room,
                "count": len(users_in_room)
            }))
        
        else:
            # List all connected users
            all_users = [u.username for u in self.users.values()]
            
            await user.connection.send(json.dumps({
                "type": "user_list",
                "users": all_users,
                "count": len(all_users)
            }))
    
    async def _handle_list_rooms(self, user: User):
        """Handle request to list available rooms."""
        rooms_info = []
        
        for room_name, user_ids in self.rooms.items():
            rooms_info.append({
                "name": room_name,
                "user_count": len(user_ids),
                "users": [self.users[uid].username for uid in user_ids]
            })
        
        await user.connection.send(json.dumps({
            "type": "room_list",
            "rooms": rooms_info,
            "count": len(rooms_info)
        }))
    
    async def _handle_user_disconnect(self, user: User):
        """Handle user disconnection."""
        # Remove user from rooms
        if user.room and user.room in self.rooms:
            self.rooms[user.room].discard(user.id)
            
            # Send leave notification
            leave_msg = ChatMessage(
                id=str(uuid.uuid4()),
                type=MessageType.LEAVE,
                sender=user.username,
                content=f"{user.username} disconnected",
                timestamp=datetime.now(),
                room=user.room
            )
            
            await self._broadcast_to_room(user.room, leave_msg)
            
            # Clean up empty room
            if not self.rooms[user.room]:
                del self.rooms[user.room]
                if user.room in self.message_history:
                    del self.message_history[user.room]
        
        # Remove user from users dict
        if user.id in self.users:
            del self.users[user.id]
        
        logger.info(f"User cleanup completed: {user.username}")
    
    async def _broadcast_to_room(self, room_name: str, message: ChatMessage):
        """Broadcast message to all users in a room."""
        if room_name not in self.rooms:
            return
        
        message_dict = message.to_dict()
        
        for user_id in self.rooms[room_name]:
            user = self.users.get(user_id)
            if user and user.connection:
                try:
                    await user.connection.send(json.dumps({
                        "type": "message",
                        "message": message_dict
                    }))
                except (ConnectionClosed, ConnectionClosedOK):
                    # Connection closed, will be cleaned up later
                    pass
                except Exception as e:
                    logger.error(f"Error broadcasting to user {user.username}: {e}")
    
    async def _send_error(self, user: User, error_message: str):
        """Send error message to user."""
        error_msg = ChatMessage(
            id=str(uuid.uuid4()),
            type=MessageType.ERROR,
            sender="System",
            content=error_message,
            timestamp=datetime.now()
        )
        
        try:
            await user.connection.send(json.dumps({
                "type": "error",
                "message": error_msg.to_dict()
            }))
        except (ConnectionClosed, ConnectionClosedOK):
            pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get server statistics."""
        return {
            **self.stats,
            "users_online": len(self.users),
            "rooms_active": len(self.rooms),
            "timestamp": datetime.now().isoformat()
        }


# ============================================================================
# SERVER MANAGEMENT
# ============================================================================

async def health_monitor(server: ChatServer, interval: int = 30):
    """Monitor server health and clean up stale connections."""
    while True:
        await asyncio.sleep(interval)
        
        # Check for stale connections (no heartbeat for 2 minutes)
        now = datetime.now()
        stale_users = []
        
        for user in server.users.values():
            time_diff = (now - user.last_seen).total_seconds()
            if time_diff > 120:  # 2 minutes
                stale_users.append(user)
        
        # Clean up stale users
        for user in stale_users:
            logger.warning(f"Cleaning up stale connection: {user.username}")
            await server._handle_user_disconnect(user)
        
        # Log statistics
        stats = server.get_stats()
        logger.info(f"Server stats: {stats}")


async def main():
    """Main function to start the chat server."""
    server = ChatServer()
    
    # Start health monitor
    monitor_task = asyncio.create_task(health_monitor(server))
    
    # Start WebSocket server
    host = "0.0.0.0"
    port = 8765
    
    logger.info(f"Starting WebSocket chat server on ws://{host}:{port}")
    logger.info("Clients can connect and send authentication message first")
    
    try:
        async with websockets.serve(
            server.handle_connection,
            host,
            port,
            ping_interval=20,
            ping_timeout=60,
            close_timeout=10
        ):
            logger.info("Server started successfully")
            logger.info("Press Ctrl+C to stop the server")
            
            # Keep server running
            await asyncio.Future()
    
    except asyncio.CancelledError:
        logger.info("Server shutting down...")
    
    finally:
        # Cancel monitor task
        monitor_task.cancel()
        try:
            await monitor_task
        except asyncio.CancelledError:
            pass
        
        logger.info("Server shutdown complete")


# ============================================================================
# CLIENT EXAMPLE
# ============================================================================

async def example_client():
    """Example client to demonstrate WebSocket communication."""
    import asyncio
    
    async def chat_client():
        uri = "ws://localhost:8765"
        
        async with websockets.connect(uri) as websocket:
            # Authenticate
            await websocket.send(json.dumps({
                "type": "auth",
                "username": "example_user"
            }))
            
            # Receive authentication response
            response = await websocket.recv()
            print(f"Auth response: {response}")
            
            # Join a room
            await websocket.send(json.dumps({
                "type": "join",
                "room": "general"
            }))
            
            # Send a chat message
            await websocket.send(json.dumps({
                "type": "chat",
                "content": "Hello from example client!"
            }))
            
            # Listen for messages for 5 seconds
            try:
                for _ in range(5):
                    message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    print(f"Received: {message}")
            except asyncio.TimeoutError:
                print("No more messages")
            
            # Leave room
            await websocket.send(json.dumps({
                "type": "leave",
                "room": "general"
            }))
    
    # Run example client
    try:
        await chat_client()
    except Exception as e:
        print(f"Client error: {e}")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--client":
        # Run example client
        asyncio.run(example_client())
    else:
        # Run server
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}", exc_info=True)