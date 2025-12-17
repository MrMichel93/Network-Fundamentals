#!/usr/bin/env python3
"""
Simple TCP Socket Server

Demonstrates TCP connection, reliable delivery, and bidirectional communication.

Usage:
    python tcp_socket_server.py
    
Then run tcp_socket_client.py in another terminal.
"""

import socket
import threading

def handle_client(client_socket, address):
    """Handle individual client connection."""
    print(f"✅ New connection from {address}")
    
    try:
        # Send welcome message
        client_socket.send(b"Welcome to TCP Server!\n")
        
        while True:
            # Receive data (up to 1024 bytes)
            data = client_socket.recv(1024)
            
            if not data:
                # Client closed connection
                break
            
            message = data.decode('utf-8').strip()
            print(f"📨 Received from {address}: {message}")
            
            # Echo message back to client
            response = f"Server echo: {message}\n"
            client_socket.send(response.encode('utf-8'))
            
            # Special command to close
            if message.lower() == 'quit':
                print(f"Client {address} requested disconnect")
                break
    
    except Exception as e:
        print(f"❌ Error handling client {address}: {e}")
    
    finally:
        print(f"👋 Connection closed: {address}")
        client_socket.close()


def main():
    """Start the TCP server."""
    HOST = 'localhost'
    PORT = 9000
    
    # Create TCP socket
    # AF_INET = IPv4, SOCK_STREAM = TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow reusing the address (useful for development)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to address and port
    server_socket.bind((HOST, PORT))
    
    # Listen for connections (max 5 queued connections)
    server_socket.listen(5)
    
    print("""
    ╔════════════════════════════════════════════╗
    ║   🔌 TCP Server Started!                  ║
    ╠════════════════════════════════════════════╣
    ║   Listening on: localhost:9000            ║
    ║   Press Ctrl+C to stop                     ║
    ╚════════════════════════════════════════════╝
    """)
    
    try:
        while True:
            # Accept incoming connection
            client_socket, address = server_socket.accept()
            
            # Handle client in a new thread (allows multiple clients)
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address)
            )
            client_thread.daemon = True
            client_thread.start()
    
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped. Goodbye!")
    
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
