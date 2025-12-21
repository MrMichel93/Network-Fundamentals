#!/usr/bin/env python3
"""
INTENTIONALLY VULNERABLE Authentication Application

⚠️ WARNING: This application contains INTENTIONAL security vulnerabilities! ⚠️

DO NOT use this code in production!
This is for EDUCATIONAL PURPOSES ONLY.

Purpose: Learn to identify and exploit common authentication vulnerabilities

Vulnerabilities included:
1. Plaintext password storage
2. SQL injection in login
3. Weak session management
4. No rate limiting
5. Predictable session tokens
6. No HTTPS enforcement
7. Weak password requirements
8. Information disclosure
9. Missing CSRF protection
10. Default credentials

Run: python 05_vulnerable_auth.py
Test: See exercises.md for security testing exercises
"""

from flask import Flask, request, jsonify, session
import sqlite3
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'weak-secret-123'  # Vulnerability: Weak secret key

# Create database
def init_db():
    conn = sqlite3.connect('vulnerable_auth.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            role TEXT,
            created_at TEXT
        )
    ''')
    
    # Insert default admin user - Vulnerability: Default credentials
    try:
        c.execute('''
            INSERT INTO users (username, password, email, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', 'admin123', 'admin@example.com', 'admin', datetime.utcnow().isoformat()))
    except:
        pass  # User already exists
    
    conn.commit()
    conn.close()


@app.route('/register', methods=['POST'])
def register():
    """
    Vulnerable registration endpoint
    
    Vulnerabilities:
    - Plaintext password storage
    - No password strength requirements
    - No input validation
    """
    data = request.json
    
    username = data.get('username')
    password = data.get('password')  # Vulnerability: No password requirements
    email = data.get('email', '')
    
    if not username or not password:
        return jsonify({'error': 'Missing credentials'}), 400
    
    conn = sqlite3.connect('vulnerable_auth.db')
    c = conn.cursor()
    
    try:
        # Vulnerability: Storing password in PLAINTEXT!
        c.execute('''
            INSERT INTO users (username, password, email, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, password, email, 'user', datetime.utcnow().isoformat()))
        
        conn.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'username': username
        }), 201
        
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400
    finally:
        conn.close()


@app.route('/login', methods=['POST'])
def login():
    """
    VULNERABLE LOGIN - SQL Injection
    
    Vulnerabilities:
    - SQL injection in login query
    - No rate limiting
    - Information disclosure in error messages
    """
    data = request.json
    
    username = data.get('username', '')
    password = data.get('password', '')
    
    conn = sqlite3.connect('vulnerable_auth.db')
    c = conn.cursor()
    
    # Vulnerability: SQL INJECTION!
    # Try: username = admin' OR '1'='1' --
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    
    print(f"[DEBUG] Executing query: {query}")  # Vulnerability: Information disclosure
    
    c.execute(query)
    user = c.fetchone()
    conn.close()
    
    if user:
        # Vulnerability: Predictable session ID
        session_id = hashlib.md5(username.encode()).hexdigest()
        
        session['session_id'] = session_id
        session['username'] = user[1]
        session['role'] = user[4]
        session['logged_in'] = True
        
        # Vulnerability: Disclosing sensitive information
        return jsonify({
            'message': 'Login successful',
            'username': user[1],
            'email': user[3],  # Shouldn't expose email
            'role': user[4],
            'session_id': session_id,  # Shouldn't expose session ID
            'password': user[2]  # NEVER expose password!
        }), 200
    else:
        # Vulnerability: Different error messages for username vs password
        if username:
            return jsonify({'error': 'Invalid password for user'}), 401
        return jsonify({'error': 'User not found'}), 401


@app.route('/profile')
def profile():
    """
    Profile endpoint with information disclosure
    """
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    username = session.get('username')
    
    conn = sqlite3.connect('vulnerable_auth.db')
    c = conn.cursor()
    
    # Get user data
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    user = c.fetchone()
    conn.close()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Vulnerability: Exposing ALL user data including password
    return jsonify({
        'id': user[0],
        'username': user[1],
        'password': user[2],  # NEVER expose password!
        'email': user[3],
        'role': user[4],
        'created_at': user[5],
        'session_id': session.get('session_id')
    }), 200


@app.route('/users')
def list_users():
    """
    List all users - INSECURE
    
    Vulnerabilities:
    - No authentication required
    - Exposes all user data including passwords
    """
    conn = sqlite3.connect('vulnerable_auth.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    
    # Vulnerability: Exposing ALL users and their passwords!
    users_list = [{
        'id': user[0],
        'username': user[1],
        'password': user[2],  # Plaintext passwords exposed!
        'email': user[3],
        'role': user[4]
    } for user in users]
    
    return jsonify({
        'count': len(users_list),
        'users': users_list
    }), 200


@app.route('/admin/delete-user', methods=['POST'])
def delete_user():
    """
    Delete user - INSECURE
    
    Vulnerabilities:
    - No authorization check
    - SQL injection
    """
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Vulnerability: No check if user is actually admin!
    
    data = request.json
    username = data.get('username', '')
    
    conn = sqlite3.connect('vulnerable_auth.db')
    c = conn.cursor()
    
    # Vulnerability: SQL injection
    query = f"DELETE FROM users WHERE username='{username}'"
    print(f"[DEBUG] Executing: {query}")
    
    c.execute(query)
    conn.commit()
    conn.close()
    
    return jsonify({
        'message': f'User {username} deleted'
    }), 200


@app.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Password reset - INSECURE
    
    Vulnerabilities:
    - No verification of user identity
    - No email confirmation
    """
    data = request.json
    username = data.get('username')
    new_password = data.get('new_password')
    
    if not username or not new_password:
        return jsonify({'error': 'Missing data'}), 400
    
    conn = sqlite3.connect('vulnerable_auth.db')
    c = conn.cursor()
    
    # Vulnerability: Anyone can reset anyone's password!
    c.execute('UPDATE users SET password=? WHERE username=?', (new_password, username))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'message': f'Password reset for {username}',
        'new_password': new_password  # Shouldn't return password
    }), 200


@app.route('/debug/sessions')
def debug_sessions():
    """
    Debug endpoint - INSECURE
    
    Vulnerability: Exposes all session data
    """
    return jsonify({
        'current_session': dict(session),
        'session_cookie': request.cookies.get('session')
    }), 200


@app.route('/vulnerabilities')
def vulnerabilities_info():
    """
    Information about vulnerabilities in this application
    """
    return jsonify({
        'warning': 'This application is INTENTIONALLY VULNERABLE',
        'purpose': 'Educational - Learn to find and exploit vulnerabilities',
        'vulnerabilities': {
            '1': {
                'name': 'Plaintext Password Storage',
                'location': '/register, /login',
                'description': 'Passwords stored in plaintext in database',
                'impact': 'All passwords compromised if database leaked'
            },
            '2': {
                'name': 'SQL Injection',
                'location': '/login',
                'description': 'User input directly concatenated in SQL query',
                'example': "username: admin' OR '1'='1' --",
                'impact': 'Bypass authentication, extract data, modify database'
            },
            '3': {
                'name': 'No Rate Limiting',
                'location': '/login',
                'description': 'No limit on login attempts',
                'impact': 'Brute force attacks possible'
            },
            '4': {
                'name': 'Information Disclosure',
                'location': '/login, /profile, /users',
                'description': 'Exposes sensitive data like passwords',
                'impact': 'Attackers gain sensitive information'
            },
            '5': {
                'name': 'Default Credentials',
                'location': 'Database initialization',
                'credentials': 'admin / admin123',
                'impact': 'Easy unauthorized access'
            },
            '6': {
                'name': 'Weak Session Management',
                'location': '/login',
                'description': 'Predictable session IDs',
                'impact': 'Session hijacking possible'
            },
            '7': {
                'name': 'Missing Authorization',
                'location': '/admin/delete-user',
                'description': 'No check if user has admin role',
                'impact': 'Privilege escalation'
            },
            '8': {
                'name': 'Insecure Password Reset',
                'location': '/reset-password',
                'description': 'No identity verification',
                'impact': 'Anyone can reset any password'
            },
            '9': {
                'name': 'No Input Validation',
                'location': 'Multiple endpoints',
                'description': 'Missing input validation and sanitization',
                'impact': 'Various injection attacks'
            },
            '10': {
                'name': 'Debug Endpoints Exposed',
                'location': '/debug/sessions, /users',
                'description': 'Debug information accessible in production',
                'impact': 'Information leakage'
            }
        },
        'exercises': 'See exercises.md for security testing tasks'
    }), 200


@app.route('/')
def home():
    return jsonify({
        'warning': '⚠️ INTENTIONALLY VULNERABLE APPLICATION ⚠️',
        'purpose': 'Educational - Learn authentication security',
        'endpoints': {
            'POST /register': 'Register user',
            'POST /login': 'Login (vulnerable to SQL injection)',
            'GET /profile': 'Get profile',
            'GET /users': 'List all users (insecure)',
            'POST /admin/delete-user': 'Delete user (insecure)',
            'POST /reset-password': 'Reset password (insecure)',
            'GET /debug/sessions': 'Debug sessions (insecure)',
            'GET /vulnerabilities': 'List all vulnerabilities'
        },
        'default_credentials': {
            'username': 'admin',
            'password': 'admin123'
        },
        'note': 'DO NOT use this code in production!'
    }), 200


if __name__ == '__main__':
    print("=" * 60)
    print("⚠️  VULNERABLE AUTHENTICATION APPLICATION  ⚠️")
    print("=" * 60)
    print("\nWARNING: This application is INTENTIONALLY VULNERABLE!")
    print("Purpose: Educational - Learn to identify security flaws")
    print("DO NOT use this code in production!\n")
    
    # Initialize database with default admin user
    init_db()
    
    print("Database initialized with default credentials:")
    print("  Username: admin")
    print("  Password: admin123\n")
    
    print("Starting server on http://localhost:5004")
    print("\nTry to exploit the vulnerabilities!")
    print("See exercises.md for security testing tasks")
    print("\nVisit /vulnerabilities for a list of all vulnerabilities")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5004)
