#!/usr/bin/env python3
"""
Session-Based Authentication Example

This example demonstrates traditional session-based authentication
with Flask. Sessions are stored server-side and identified by cookies.

Features:
- User registration with password hashing
- Login/logout functionality
- Protected routes
- Session management

Run: python 01_session_auth.py
Test: See exercises.md for testing instructions
"""

from flask import Flask, request, jsonify, session
import bcrypt
import secrets
from datetime import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Generate secure secret key

# In-memory user database (use a real database in production!)
users_db = {}

# In-memory session store (Flask handles this, but showing for clarity)
# Sessions are automatically managed by Flask with secure cookies


@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user with hashed password
    
    Request body:
    {
        "username": "john",
        "password": "securepassword123",
        "email": "john@example.com"
    }
    """
    data = request.json
    
    # Validate input
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    username = data['username']
    password = data['password']
    email = data.get('email', '')
    
    # Check if user already exists
    if username in users_db:
        return jsonify({'error': 'Username already exists'}), 400
    
    # Validate password strength
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
    
    # Hash password with bcrypt
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
    Login with username and password
    Creates a session on success
    
    Request body:
    {
        "username": "john",
        "password": "securepassword123"
    }
    """
    data = request.json
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    username = data['username']
    password = data['password']
    
    # Check if user exists
    if username not in users_db:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Verify password
    stored_hash = users_db[username]['password_hash']
    if not bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Create session
    session['username'] = username
    session['logged_in'] = True
    session['login_time'] = datetime.utcnow().isoformat()
    
    return jsonify({
        'message': 'Logged in successfully',
        'username': username
    }), 200


@app.route('/profile')
def profile():
    """
    Get current user's profile
    Requires authentication (active session)
    """
    # Check if user is logged in
    if not session.get('logged_in'):
        return jsonify({'error': 'Authentication required'}), 401
    
    username = session.get('username')
    
    if username not in users_db:
        return jsonify({'error': 'User not found'}), 404
    
    user_data = users_db[username]
    
    return jsonify({
        'username': username,
        'email': user_data['email'],
        'created_at': user_data['created_at'],
        'session_info': {
            'login_time': session.get('login_time'),
            'session_active': True
        }
    }), 200


@app.route('/update-profile', methods=['PUT'])
def update_profile():
    """
    Update user profile
    Requires authentication
    
    Request body:
    {
        "email": "newemail@example.com"
    }
    """
    if not session.get('logged_in'):
        return jsonify({'error': 'Authentication required'}), 401
    
    username = session.get('username')
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
def logout():
    """
    Logout and destroy session
    """
    if not session.get('logged_in'):
        return jsonify({'error': 'Not logged in'}), 400
    
    username = session.get('username')
    
    # Clear session
    session.clear()
    
    return jsonify({
        'message': 'Logged out successfully',
        'username': username
    }), 200


@app.route('/session-info')
def session_info():
    """
    Get information about current session
    Useful for debugging
    """
    if not session.get('logged_in'):
        return jsonify({
            'authenticated': False,
            'message': 'No active session'
        }), 200
    
    return jsonify({
        'authenticated': True,
        'username': session.get('username'),
        'login_time': session.get('login_time'),
        'session_keys': list(session.keys())
    }), 200


@app.route('/')
def home():
    """
    API information endpoint
    """
    return jsonify({
        'service': 'Session-Based Authentication API',
        'version': '1.0',
        'endpoints': {
            'POST /register': 'Register a new user',
            'POST /login': 'Login and create session',
            'GET /profile': 'Get user profile (requires auth)',
            'PUT /update-profile': 'Update profile (requires auth)',
            'POST /logout': 'Logout and destroy session',
            'GET /session-info': 'Get current session information'
        },
        'authentication': 'Session-based (cookies)',
        'documentation': 'See exercises.md for usage examples'
    }), 200


if __name__ == '__main__':
    print("=" * 60)
    print("Session-Based Authentication Server")
    print("=" * 60)
    print("\nStarting server on http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  POST   /register       - Register new user")
    print("  POST   /login          - Login")
    print("  GET    /profile        - Get profile (auth required)")
    print("  PUT    /update-profile - Update profile (auth required)")
    print("  POST   /logout         - Logout")
    print("  GET    /session-info   - Session information")
    print("\nSee exercises.md for usage examples")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
