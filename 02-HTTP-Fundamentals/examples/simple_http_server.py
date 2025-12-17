#!/usr/bin/env python3
"""
Simple HTTP Server Example

This script demonstrates how to create a basic HTTP server using Python's
built-in http.server module. It responds to GET requests with a simple HTML page.

Usage:
    python simple_http_server.py
    
Then visit: http://localhost:8000
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Custom request handler that responds to different HTTP methods and paths.
    """
    
    def do_GET(self):
        """
        Handle GET requests.
        Demonstrates:
        - Sending response headers
        - Returning HTML content
        - Different responses based on URL path
        """
        # Parse the URL path
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Route 1: Home page
        if path == '/' or path == '/index.html':
            self.send_response(200)  # OK
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Simple HTTP Server</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    h1 { color: #333; }
                    .endpoint { background: #f4f4f4; padding: 10px; margin: 10px 0; }
                </style>
            </head>
            <body>
                <h1>🌐 Welcome to Simple HTTP Server!</h1>
                <p>This server demonstrates basic HTTP concepts.</p>
                
                <h2>Available Endpoints:</h2>
                <div class="endpoint">
                    <strong>GET /</strong> - This page
                </div>
                <div class="endpoint">
                    <strong>GET /api/data</strong> - Returns JSON data
                </div>
                <div class="endpoint">
                    <strong>GET /api/user?name=YourName</strong> - Returns personalized JSON
                </div>
                <div class="endpoint">
                    <strong>GET /status</strong> - Server status
                </div>
                
                <h2>Try these commands in your terminal:</h2>
                <code>curl http://localhost:8000/api/data</code><br>
                <code>curl http://localhost:8000/api/user?name=Alice</code><br>
                <code>curl -i http://localhost:8000/status</code>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        
        # Route 2: JSON API endpoint
        elif path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # CORS header
            self.end_headers()
            
            data = {
                'message': 'Hello from the server!',
                'timestamp': '2024-01-01T12:00:00Z',
                'items': ['apple', 'banana', 'cherry']
            }
            self.wfile.write(json.dumps(data, indent=2).encode())
        
        # Route 3: Parameterized endpoint
        elif path.startswith('/api/user'):
            # Parse query parameters
            query_params = parse_qs(parsed_path.query)
            name = query_params.get('name', ['Guest'])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'greeting': f'Hello, {name}!',
                'message': 'Welcome to our API'
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        
        # Route 4: Status endpoint
        elif path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            status = {
                'status': 'running',
                'version': '1.0.0',
                'endpoints': 4
            }
            self.wfile.write(json.dumps(status, indent=2).encode())
        
        # Route 5: 404 - Not Found
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            error = {
                'error': 'Not Found',
                'message': f'The path {path} does not exist',
                'status_code': 404
            }
            self.wfile.write(json.dumps(error, indent=2).encode())
    
    def do_POST(self):
        """
        Handle POST requests.
        Demonstrates:
        - Reading request body
        - Parsing JSON data
        - Sending appropriate response
        """
        # Read the request body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # Try to parse as JSON
            data = json.loads(post_data.decode())
            
            # Send success response
            self.send_response(201)  # Created
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'message': 'Data received successfully',
                'received_data': data,
                'status': 'created'
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except json.JSONDecodeError:
            # Send error response for invalid JSON
            self.send_response(400)  # Bad Request
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            error = {
                'error': 'Invalid JSON',
                'message': 'The request body must be valid JSON',
                'status_code': 400
            }
            self.wfile.write(json.dumps(error, indent=2).encode())
    
    def log_message(self, format, *args):
        """
        Custom log format to show what's happening.
        """
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server(port=8000):
    """
    Start the HTTP server.
    
    Args:
        port (int): Port number to listen on (default: 8000)
    """
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    
    print(f"""
    ╔════════════════════════════════════════════╗
    ║   🌐 Simple HTTP Server Started!          ║
    ╠════════════════════════════════════════════╣
    ║   Listening on: http://localhost:{port}    ║
    ║   Press Ctrl+C to stop                     ║
    ╚════════════════════════════════════════════╝
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped. Goodbye!")
        httpd.shutdown()


if __name__ == '__main__':
    # Start the server on port 8000
    run_server(8000)
