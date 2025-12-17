#!/usr/bin/env python3
"""
UDP Socket Example (Server and Client)

Demonstrates UDP: connectionless, fast, unreliable delivery.
Run with --server or --client flag.

Usage:
    python udp_example.py --server    # Start server
    python udp_example.py --client    # Start client
"""

import socket
import sys
import time

def run_server():
    """UDP Server - Listen for datagrams."""
    HOST = 'localhost'
    PORT = 9001
    
    # Create UDP socket
    # AF_INET = IPv4, SOCK_DGRAM = UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind to address
    server_socket.bind((HOST, PORT))
    
    print("""
    ╔════════════════════════════════════════════╗
    ║   📨 UDP Server Started!                  ║
    ╠════════════════════════════════════════════╣
    ║   Listening on: localhost:9001            ║
    ║   Press Ctrl+C to stop                     ║
    ╚════════════════════════════════════════════╝
    """)
    
    try:
        while True:
            # Receive datagram (no connection needed!)
            data, address = server_socket.recvfrom(1024)
            
            message = data.decode('utf-8')
            print(f"📨 Received from {address}: {message}")
            
            # Send response (no connection needed!)
            response = f"Server received: {message}"
            server_socket.sendto(response.encode('utf-8'), address)
            
            print(f"📤 Sent response to {address}")
    
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped. Goodbye!")
    finally:
        server_socket.close()


def run_client():
    """UDP Client - Send datagrams."""
    HOST = 'localhost'
    PORT = 9001
    
    # Create UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Set timeout for receiving (optional)
    client_socket.settimeout(5.0)
    
    print("""
    ╔════════════════════════════════════════════╗
    ║   📤 UDP Client Started!                  ║
    ╠════════════════════════════════════════════╣
    ║   Sending to: localhost:9001              ║
    ╚════════════════════════════════════════════╝
    """)
    
    try:
        for i in range(5):
            # Create message
            message = f"Hello from UDP client! (Message #{i+1})"
            
            print(f"\n📤 Sending: {message}")
            
            # Send datagram (no connection needed!)
            client_socket.sendto(message.encode('utf-8'), (HOST, PORT))
            
            try:
                # Try to receive response
                data, server = client_socket.recvfrom(1024)
                response = data.decode('utf-8')
                print(f"📨 Received: {response}")
            
            except socket.timeout:
                print("⏱️  No response (timeout)")
                # With UDP, we don't know if packet was lost!
            
            time.sleep(1)
        
        print("\n✅ Sent all messages")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        client_socket.close()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python udp_example.py --server")
        print("  python udp_example.py --client")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == '--server':
        run_server()
    elif mode == '--client':
        run_client()
    else:
        print(f"Unknown mode: {mode}")
        print("Use --server or --client")
        sys.exit(1)


if __name__ == '__main__':
    main()
