#!/usr/bin/env python3
"""
Simple TCP Socket Client

Connects to TCP server and sends/receives messages.

Usage:
    python tcp_socket_client.py
"""

import socket

def main():
    """Connect to TCP server and communicate."""
    HOST = 'localhost'
    PORT = 9000
    
    # Create TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print("🔌 Connecting to server...")
    
    try:
        # Connect to server
        client_socket.connect((HOST, PORT))
        print(f"✅ Connected to {HOST}:{PORT}")
        
        # Receive welcome message
        welcome = client_socket.recv(1024).decode('utf-8')
        print(f"📨 Server: {welcome}")
        
        # Interactive loop
        print("\nType messages (or 'quit' to exit):")
        while True:
            # Get user input
            message = input("You: ").strip()
            
            if not message:
                continue
            
            # Send message to server
            client_socket.send(message.encode('utf-8'))
            
            # Check if quitting
            if message.lower() == 'quit':
                print("Disconnecting...")
                break
            
            # Receive response
            response = client_socket.recv(1024).decode('utf-8')
            print(f"📨 {response}", end='')
    
    except ConnectionRefusedError:
        print("❌ Could not connect to server. Is it running?")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client_socket.close()
        print("👋 Disconnected")


if __name__ == '__main__':
    main()
