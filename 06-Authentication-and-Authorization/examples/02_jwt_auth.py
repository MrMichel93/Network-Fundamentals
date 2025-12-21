#!/usr/bin/env python3
"""
JWT (JSON Web Token) Authentication Example

This example demonstrates token-based authentication using JWT.
Tokens are stateless and contain all user information.

Features:
- User registration with password hashing
- Login returns JWT access token
- Refresh token support
- Protected routes with JWT verification
- Token expiration handling

Run: python 02_jwt_auth.py
Test: See exercises.md for testing instructions
"""

from flask import Flask, request, jsonify
import jwt
import bcrypt
import secrets
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

# Secret keys (in production, use environment variables!)
SECRET_KEY = secrets.token_hex(32)
REFRESH_SECRET_KEY = secrets.token_hex(32)

# Token expiration times
ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
REFRESH_TOKEN_EXPIRES = timedelta(days=7)

# In-memory user database
users_db = {}

# In-memory refresh token storage (use Redis in production!)
refresh_tokens = set()


def token_required(f):
    """
    Decorator to protect routes that require authentication
    Extracts and verifies JWT from Authorization header
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Missing Authorization header'}), 401
        
        try:
            # Extract token from "Bearer <token>" format
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({'error': 'Invalid Authorization header format'}), 401
        
        try:
            # Verify and decode token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.current_user = payload['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated


def create_access_token(username):
    """Create a JWT access token"""
    payload = {
        'username': username,
        'exp': datetime.utcnow() + ACCESS_TOKEN_EXPIRES,
        'iat': datetime.utcnow(),
        'type': 'access'
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def create_refresh_token(username):
    """Create a JWT refresh token"""
    payload = {
        'username': username,
        'exp': datetime.utcnow() + REFRESH_TOKEN_EXPIRES,
        'iat': datetime.utcnow(),
        'type': 'refresh',
        'jti': secrets.token_hex(16)  # Unique token ID
    }
    token = jwt.encode(payload, REFRESH_SECRET_KEY, algorithm='HS256')
    
    # Store refresh token (in production, use Redis with expiration)
    refresh_tokens.add(payload['jti'])
    
    return token


@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request body:
    {
        "username": "john",
        "password": "securepassword123",
        "email": "john@example.com"
    }
    """
    data = request.json
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    username = data['username']
    password = data['password']
    email = data.get('email', '')
    
    if username in users_db:
        return jsonify({'error': 'Username already exists'}), 400
    
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
    
    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Store user
    users_db[username] = {
        'password_hash': password_hash,
        'email': email,
        'created_at': datetime.utcnow().isoformat()
    }
    
    return jsonify({
        'message': 'User registered successfully',
        'username': username
    }), 201


@app.route('/login', methods=['POST'])
def login():
    """
    Login and receive JWT tokens
    
    Request body:
    {
        "username": "john",
        "password": "securepassword123"
    }
    
    Returns access token and refresh token
    """
    data = request.json
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    username = data['username']
    password = data['password']
    
    if username not in users_db:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Verify password
    stored_hash = users_db[username]['password_hash']
    if not bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Create tokens
    access_token = create_access_token(username)
    refresh_token = create_refresh_token(username)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'expires_in': int(ACCESS_TOKEN_EXPIRES.total_seconds())
    }), 200


@app.route('/refresh', methods=['POST'])
def refresh():
    """
    Refresh access token using refresh token
    
    Request body:
    {
        "refresh_token": "eyJ..."
    }
    """
    data = request.json
    
    if not data or not data.get('refresh_token'):
        return jsonify({'error': 'Missing refresh token'}), 400
    
    refresh_token = data['refresh_token']
    
    try:
        # Verify refresh token
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=['HS256'])
        
        # Check if token type is refresh
        if payload.get('type') != 'refresh':
            return jsonify({'error': 'Invalid token type'}), 401
        
        # Check if refresh token is in valid tokens set
        if payload.get('jti') not in refresh_tokens:
            return jsonify({'error': 'Invalid or revoked refresh token'}), 401
        
        username = payload['username']
        
        # Create new access token
        new_access_token = create_access_token(username)
        
        return jsonify({
            'access_token': new_access_token,
            'token_type': 'Bearer',
            'expires_in': int(ACCESS_TOKEN_EXPIRES.total_seconds())
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Refresh token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid refresh token'}), 401


@app.route('/profile')
@token_required
def profile():
    """
    Get current user's profile
    Requires valid JWT in Authorization header
    
    Header:
    Authorization: Bearer <access_token>
    """
    username = request.current_user
    
    if username not in users_db:
        return jsonify({'error': 'User not found'}), 404
    
    user_data = users_db[username]
    
    return jsonify({
        'username': username,
        'email': user_data['email'],
        'created_at': user_data['created_at']
    }), 200


@app.route('/update-profile', methods=['PUT'])
@token_required
def update_profile():
    """
    Update user profile
    Requires authentication
    
    Header:
    Authorization: Bearer <access_token>
    
    Request body:
    {
        "email": "newemail@example.com"
    }
    """
    username = request.current_user
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update allowed fields
    if 'email' in data:
        users_db[username]['email'] = data['email']
    
    return jsonify({
        'message': 'Profile updated successfully',
        'username': username
    }), 200


@app.route('/logout', methods=['POST'])
@token_required
def logout():
    """
    Logout - revoke refresh token
    
    Request body:
    {
        "refresh_token": "eyJ..."
    }
    """
    data = request.json
    
    if data and data.get('refresh_token'):
        try:
            payload = jwt.decode(
                data['refresh_token'], 
                REFRESH_SECRET_KEY, 
                algorithms=['HS256']
            )
            # Remove refresh token from valid tokens
            refresh_tokens.discard(payload.get('jti'))
        except:
            pass  # Invalid token, already invalid
    
    return jsonify({
        'message': 'Logged out successfully'
    }), 200


@app.route('/verify-token', methods=['POST'])
def verify_token():
    """
    Verify if a token is valid
    
    Request body:
    {
        "token": "eyJ..."
    }
    """
    data = request.json
    
    if not data or not data.get('token'):
        return jsonify({'error': 'Missing token'}), 400
    
    token = data['token']
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        return jsonify({
            'valid': True,
            'username': payload['username'],
            'expires_at': payload['exp'],
            'issued_at': payload['iat']
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({
            'valid': False,
            'error': 'Token has expired'
        }), 401
    except jwt.InvalidTokenError:
        return jsonify({
            'valid': False,
            'error': 'Invalid token'
        }), 401


@app.route('/')
def home():
    """
    API information endpoint
    """
    return jsonify({
        'service': 'JWT Authentication API',
        'version': '1.0',
        'endpoints': {
            'POST /register': 'Register a new user',
            'POST /login': 'Login and receive JWT tokens',
            'POST /refresh': 'Refresh access token',
            'GET /profile': 'Get user profile (requires auth)',
            'PUT /update-profile': 'Update profile (requires auth)',
            'POST /logout': 'Logout and revoke refresh token',
            'POST /verify-token': 'Verify if token is valid'
        },
        'authentication': 'JWT Bearer token',
        'token_info': {
            'access_token_expires': f'{ACCESS_TOKEN_EXPIRES.total_seconds()} seconds',
            'refresh_token_expires': f'{REFRESH_TOKEN_EXPIRES.total_seconds()} seconds'
        },
        'documentation': 'See exercises.md for usage examples'
    }), 200


if __name__ == '__main__':
    print("=" * 60)
    print("JWT Authentication Server")
    print("=" * 60)
    print(f"\nAccess token expires in: {ACCESS_TOKEN_EXPIRES}")
    print(f"Refresh token expires in: {REFRESH_TOKEN_EXPIRES}")
    print("\nStarting server on http://localhost:5001")
    print("\nAvailable endpoints:")
    print("  POST   /register       - Register new user")
    print("  POST   /login          - Login (get tokens)")
    print("  POST   /refresh        - Refresh access token")
    print("  GET    /profile        - Get profile (auth required)")
    print("  PUT    /update-profile - Update profile (auth required)")
    print("  POST   /logout         - Logout")
    print("  POST   /verify-token   - Verify token")
    print("\nSee exercises.md for usage examples")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
