#!/usr/bin/env python3
"""
Simple Chat Application Server with WebSockets

Features:
- User nicknames
- Join/leave notifications
- Message broadcasting
- Online user list

Requirements:
    pip install websockets

Usage:
    python chat_server.py
    
Then open chat_client.html in multiple browser tabs to test!
"""

import asyncio
import websockets
import json
from datetime import datetime

# Store connected users: {websocket: username}
users = {}


async def notify_users():
    """Send updated user list to all connected clients."""
    if users:
        user_list = list(users.values())
        message = json.dumps({
            'type': 'user_list',
            'users': user_list
        })
        await asyncio.gather(
            *[user.send(message) for user in users.keys()],
            return_exceptions=True
        )


async def broadcast(message, sender=None):
    """Broadcast message to all users except sender."""
    if users:
        tasks = [
            user.send(message)
            for user in users.keys()
            if user != sender
        ]
        await asyncio.gather(*tasks, return_exceptions=True)


async def handler(websocket):
    """Handle a chat client connection."""
    user_name = None
    
    try:
        # Wait for user to set their nickname
        async for message in websocket:
            data = json.loads(message)
            
            if data['type'] == 'join' and 'username' in data:
                user_name = data['username']
                users[websocket] = user_name
                
                print(f"✅ {user_name} joined. Total users: {len(users)}")
                
                # Send welcome message
                welcome = {
                    'type': 'system',
                    'message': f'Welcome, {user_name}!',
                    'timestamp': datetime.now().isoformat()
                }
                await websocket.send(json.dumps(welcome))
                
                # Notify others
                join_msg = {
                    'type': 'system',
                    'message': f'{user_name} joined the chat',
                    'timestamp': datetime.now().isoformat()
                }
                await broadcast(json.dumps(join_msg), websocket)
                
                # Send updated user list
                await notify_users()
                break
        
        # Now handle chat messages
        async for message in websocket:
            data = json.loads(message)
            
            if data['type'] == 'message':
                # Broadcast chat message
                chat_msg = {
                    'type': 'message',
                    'username': user_name,
                    'content': data['content'],
                    'timestamp': datetime.now().isoformat()
                }
                
                # Send to all users (including sender for confirmation)
                msg_json = json.dumps(chat_msg)
                await asyncio.gather(
                    *[user.send(msg_json) for user in users.keys()],
                    return_exceptions=True
                )
                
    except websockets.exceptions.ConnectionClosed:
        print(f"🔌 {user_name or 'Unknown'} disconnected")
    
    finally:
        # Remove user and notify others
        if websocket in users:
            user_name = users[websocket]
            del users[websocket]
            
            print(f"👋 {user_name} left. Remaining users: {len(users)}")
            
            # Notify about user leaving
            leave_msg = {
                'type': 'system',
                'message': f'{user_name} left the chat',
                'timestamp': datetime.now().isoformat()
            }
            await broadcast(json.dumps(leave_msg))
            
            # Update user list
            await notify_users()


async def main():
    """Start the chat server."""
    print("""
    ╔════════════════════════════════════════════╗
    ║   💬 Chat Server Started!                 ║
    ╠════════════════════════════════════════════╣
    ║   Listening on: ws://localhost:8765       ║
    ║   Press Ctrl+C to stop                     ║
    ╚════════════════════════════════════════════╝
    
    Open chat_client.html in multiple browser tabs to test!
    """)
    
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped. Goodbye!")
