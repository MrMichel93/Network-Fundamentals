#!/usr/bin/env python3
"""
Simple WebSocket Server Example

This server demonstrates basic WebSocket functionality:
- Accept connections
- Receive messages
- Broadcast to all connected clients

Requirements:
    pip install websockets

Usage:
    python websocket_server.py
    
Then open websocket_client.html in your browser.
"""

import asyncio
import websockets
import json
from datetime import datetime

# Store all connected clients
connected_clients = set()


async def handler(websocket):
    """
    Handle a WebSocket connection.
    
    Args:
        websocket: The WebSocket connection
    """
    # Register client
    connected_clients.add(websocket)
    client_id = id(websocket)
    print(f"✅ Client {client_id} connected. Total clients: {len(connected_clients)}")
    
    # Send welcome message
    welcome_message = {
        'type': 'system',
        'message': 'Welcome to the WebSocket server!',
        'timestamp': datetime.now().isoformat()
    }
    await websocket.send(json.dumps(welcome_message))
    
    # Notify all clients about new connection
    join_message = {
        'type': 'user_joined',
        'message': f'Client {client_id} joined',
        'client_count': len(connected_clients),
        'timestamp': datetime.now().isoformat()
    }
    await broadcast(json.dumps(join_message))
    
    try:
        # Listen for messages
        async for message in websocket:
            print(f"📨 Received from {client_id}: {message}")
            
            # Try to parse as JSON
            try:
                data = json.loads(message)
                
                # Handle different message types
                if data.get('type') == 'ping':
                    # Respond to ping with pong
                    pong = {'type': 'pong', 'timestamp': datetime.now().isoformat()}
                    await websocket.send(json.dumps(pong))
                
                elif data.get('type') == 'message':
                    # Broadcast message to all clients
                    broadcast_data = {
                        'type': 'message',
                        'from': client_id,
                        'content': data.get('content'),
                        'timestamp': datetime.now().isoformat()
                    }
                    await broadcast(json.dumps(broadcast_data))
                
                else:
                    # Echo back unknown messages
                    echo = {
                        'type': 'echo',
                        'original': message,
                        'timestamp': datetime.now().isoformat()
                    }
                    await websocket.send(json.dumps(echo))
            
            except json.JSONDecodeError:
                # Not JSON, echo back as text
                await websocket.send(f"Echo: {message}")
    
    except websockets.exceptions.ConnectionClosed:
        print(f"🔌 Client {client_id} disconnected normally")
    
    except Exception as e:
        print(f"❌ Error with client {client_id}: {e}")
    
    finally:
        # Unregister client
        connected_clients.remove(websocket)
        print(f"👋 Client {client_id} removed. Remaining clients: {len(connected_clients)}")
        
        # Notify all clients about disconnection
        leave_message = {
            'type': 'user_left',
            'message': f'Client {client_id} left',
            'client_count': len(connected_clients),
            'timestamp': datetime.now().isoformat()
        }
        await broadcast(json.dumps(leave_message))


async def broadcast(message):
    """
    Broadcast a message to all connected clients.
    
    Args:
        message: The message to broadcast (string)
    """
    if connected_clients:
        # Send to all clients concurrently
        await asyncio.gather(
            *[client.send(message) for client in connected_clients],
            return_exceptions=True
        )


async def main():
    """Start the WebSocket server."""
    host = "localhost"
    port = 8000
    
    print("""
    ╔════════════════════════════════════════════╗
    ║   🔄 WebSocket Server Started!            ║
    ╠════════════════════════════════════════════╣
    ║   Listening on: ws://localhost:8000       ║
    ║   Press Ctrl+C to stop                     ║
    ╚════════════════════════════════════════════╝
    
    Open websocket_client.html in your browser to connect!
    
    Or test with websocat (if installed):
        websocat ws://localhost:8000
    """)
    
    async with websockets.serve(handler, host, port):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped. Goodbye!")
