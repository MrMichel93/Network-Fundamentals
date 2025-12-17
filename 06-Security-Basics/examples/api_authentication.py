#!/usr/bin/env python3
"""
API Authentication Examples

Demonstrates different authentication methods:
1. API Key
2. Bearer Token (JWT)
3. Basic Auth

Requirements:
    pip install flask pyjwt

Usage:
    python api_authentication.py
"""

from flask import Flask, request, jsonify
import jwt
import base64
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

# Secret key for JWT (in production, use environment variable!)
SECRET_KEY = 'your-secret-key-keep-it-safe'

# Mock data
API_KEYS = {
    'demo-api-key-123': 'user1',
    'demo-api-key-456': 'user2'
}

USERS = {
    'alice': 'password123',
    'bob': 'secret456'
}


# ============================================
# Authentication Decorators
# ============================================

def require_api_key(f):
    """Decorator to require API key."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'error': 'API key required'}), 401
        
        if api_key not in API_KEYS:
            return jsonify({'error': 'Invalid API key'}), 401
        
        # Add user to request context
        request.current_user = API_KEYS[api_key]
        return f(*args, **kwargs)
    
    return decorated_function


def require_jwt(f):
    """Decorator to require JWT token."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Authorization header required'}), 401
        
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Invalid authorization format'}), 401
        
        token = auth_header.split(' ')[1]
        
        try:
            # Verify and decode token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.current_user = payload['user_id']
            return f(*args, **kwargs)
        
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
    
    return decorated_function


def require_basic_auth(f):
    """Decorator to require Basic authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Authorization required'}), 401
        
        if not auth_header.startswith('Basic '):
            return jsonify({'error': 'Invalid authorization format'}), 401
        
        try:
            # Decode base64 credentials
            encoded_credentials = auth_header.split(' ')[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            username, password = decoded_credentials.split(':', 1)
            
            # Verify credentials
            if username not in USERS or USERS[username] != password:
                return jsonify({'error': 'Invalid credentials'}), 401
            
            request.current_user = username
            return f(*args, **kwargs)
        
        except Exception as e:
            return jsonify({'error': 'Invalid authorization'}), 401
    
    return decorated_function


# ============================================
# Endpoints
# ============================================

@app.route('/')
def home():
    """API documentation."""
    return jsonify({
        'name': 'Authentication Demo API',
        'version': '1.0',
        'endpoints': {
            'POST /login': 'Get JWT token (username/password)',
            'GET /api-key/data': 'API Key authentication',
            'GET /jwt/data': 'JWT authentication',
            'GET /basic/data': 'Basic authentication'
        },
        'examples': {
            'api_key': 'curl -H "X-API-Key: demo-api-key-123" http://localhost:5000/api-key/data',
            'jwt': 'curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:5000/jwt/data',
            'basic': 'curl -u alice:password123 http://localhost:5000/basic/data'
        }
    })


@app.route('/login', methods=['POST'])
def login():
    """
    Login endpoint - returns JWT token.
    
    Body: {"username": "alice", "password": "password123"}
    """
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
    
    username = data['username']
    password = data['password']
    
    # Verify credentials
    if username not in USERS or USERS[username] != password:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Create JWT token
    payload = {
        'user_id': username,
        'exp': datetime.utcnow() + timedelta(hours=24)  # 24-hour expiration
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user_id': username,
        'expires_in': '24 hours'
    }), 200


@app.route('/api-key/data', methods=['GET'])
@require_api_key
def api_key_data():
    """Protected endpoint using API Key."""
    return jsonify({
        'message': f'Hello, {request.current_user}!',
        'data': 'This is protected data (API Key auth)',
        'auth_method': 'API Key'
    })


@app.route('/jwt/data', methods=['GET'])
@require_jwt
def jwt_data():
    """Protected endpoint using JWT."""
    return jsonify({
        'message': f'Hello, {request.current_user}!',
        'data': 'This is protected data (JWT auth)',
        'auth_method': 'JWT Bearer Token'
    })


@app.route('/basic/data', methods=['GET'])
@require_basic_auth
def basic_data():
    """Protected endpoint using Basic Auth."""
    return jsonify({
        'message': f'Hello, {request.current_user}!',
        'data': 'This is protected data (Basic auth)',
        'auth_method': 'HTTP Basic Authentication'
    })


if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════╗
    ║   🔒 Authentication Demo API              ║
    ╠════════════════════════════════════════════╣
    ║   Listening on: http://localhost:5000     ║
    ╚════════════════════════════════════════════╝
    
    Test credentials:
    - Username: alice, Password: password123
    - Username: bob, Password: secret456
    
    API Keys:
    - demo-api-key-123 (user1)
    - demo-api-key-456 (user2)
    
    Examples:
    
    # 1. API Key Authentication
    curl -H "X-API-Key: demo-api-key-123" \\
      http://localhost:5000/api-key/data
    
    # 2. Get JWT Token
    curl -X POST http://localhost:5000/login \\
      -H "Content-Type: application/json" \\
      -d '{"username":"alice","password":"password123"}'
    
    # 3. Use JWT Token
    curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \\
      http://localhost:5000/jwt/data
    
    # 4. Basic Authentication
    curl -u alice:password123 \\
      http://localhost:5000/basic/data
    """)
    
    app.run(debug=True, port=5000)
