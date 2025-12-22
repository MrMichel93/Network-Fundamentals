#!/usr/bin/env python3
"""
FIXED SQL INJECTION LAB - SECURE IMPLEMENTATION
===============================================

This is the secure version that demonstrates proper defenses
against SQL injection attacks using parameterized queries.

Security measures implemented:
1. Parameterized queries (prepared statements)
2. Input validation and sanitization
3. Proper error handling (no information disclosure)
4. Allowlist for dynamic fields (ORDER BY)
5. Least privilege principle
"""

from flask import Flask, request, jsonify
import sqlite3
import os
import re

app = Flask(__name__)
DB_FILE = 'fixed_sqli.db'

def init_db():
    """Initialize database with sample data"""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            api_key TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE secrets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            secret_data TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Insert sample users (in production, passwords would be hashed!)
    users_data = [
        ('admin', 'admin123', 'admin@example.com', 'admin', 'sk-admin-key-12345'),
        ('john', 'john456', 'john@example.com', 'user', 'sk-user-key-67890'),
        ('alice', 'alice789', 'alice@example.com', 'user', 'sk-user-key-11111'),
    ]
    
    for user in users_data:
        cursor.execute(
            "INSERT INTO users (username, password, email, role, api_key) VALUES (?, ?, ?, ?, ?)",
            user
        )
    
    cursor.execute("INSERT INTO secrets (user_id, secret_data) VALUES (1, 'Admin secret key: TOP_SECRET_123')")
    cursor.execute("INSERT INTO secrets (user_id, secret_data) VALUES (2, 'John credit card: 4532-1111-2222-3333')")
    
    conn.commit()
    conn.close()
    print("✓ Database initialized (secure version)")

init_db()


# ============================================================================
# Helper Functions
# ============================================================================

def validate_username(username):
    """Validate username format"""
    if not username or not isinstance(username, str):
        return False
    # Only allow alphanumeric and underscore, 3-20 characters
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        return False
    return True

def sanitize_input(text):
    """Basic sanitization for text input"""
    if not isinstance(text, str):
        return ""
    # Remove any null bytes and limit length
    return text.replace('\x00', '')[:100]


# ============================================================================
# FIXED: SQL Injection in Login
# ============================================================================

@app.route('/api/login', methods=['POST'])
def login():
    """
    SECURE: Uses parameterized queries
    """
    data = request.json or {}
    username = data.get('username', '')
    password = data.get('password', '')
    
    # Validate input format
    if not validate_username(username):
        return jsonify({'error': 'Invalid username format'}), 400
    
    # SECURE: Parameterized query with placeholders
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        # The database driver handles escaping automatically
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': result[0],
                    'username': result[1],
                    'email': result[3],
                    'role': result[4]
                    # SECURE: Not exposing API key in response
                }
            })
        else:
            # SECURE: Generic error message
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        # SECURE: Log error internally but don't expose details
        print(f"[ERROR] Login failed: {str(e)}")
        return jsonify({'error': 'Authentication failed'}), 500


# ============================================================================
# FIXED: SQL Injection in User Lookup
# ============================================================================

@app.route('/api/user/<username>')
def get_user(username):
    """
    SECURE: Parameterized query prevents OR-based injection
    """
    # Validate input
    if not validate_username(username):
        return jsonify({'error': 'Invalid username format'}), 400
    
    # SECURE: Parameterized query
    query = "SELECT id, username, email, role FROM users WHERE username = ?"
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            user = {
                'id': result[0],
                'username': result[1],
                'email': result[2],
                'role': result[3]
            }
            return jsonify({'user': user})
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        print(f"[ERROR] User lookup failed: {str(e)}")
        return jsonify({'error': 'Failed to retrieve user'}), 500


# ============================================================================
# FIXED: SQL Injection in Search
# ============================================================================

@app.route('/api/search')
def search_users():
    """
    SECURE: Parameterized query prevents UNION-based injection
    """
    search_term = request.args.get('q', '')
    
    # Sanitize and validate
    search_term = sanitize_input(search_term)
    if not search_term:
        return jsonify({'error': 'Search term required'}), 400
    
    # SECURE: Parameterized query with LIKE
    # The % wildcards are added safely in the parameter
    query = "SELECT id, username, email, role FROM users WHERE username LIKE ?"
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        # Add wildcards in the parameter, not in the query string
        cursor.execute(query, (f'%{search_term}%',))
        results = cursor.fetchall()
        conn.close()
        
        users = []
        for row in results:
            users.append({
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'role': row[3]
            })
        
        return jsonify({
            'results': users,
            'count': len(users)
        })
        
    except Exception as e:
        print(f"[ERROR] Search failed: {str(e)}")
        return jsonify({'error': 'Search failed'}), 500


# ============================================================================
# FIXED: SQL Injection in Order By
# ============================================================================

@app.route('/api/users')
def list_users():
    """
    SECURE: Uses allowlist for ORDER BY column names
    """
    sort_by = request.args.get('sort', 'username')
    
    # SECURE: Allowlist of valid column names
    # User input cannot modify the query structure
    ALLOWED_SORT_COLUMNS = {
        'username': 'username',
        'email': 'email',
        'role': 'role',
        'id': 'id'
    }
    
    # Validate against allowlist
    if sort_by not in ALLOWED_SORT_COLUMNS:
        sort_by = 'username'  # Default to safe value
    
    # Use the validated column name (not directly from user input)
    column = ALLOWED_SORT_COLUMNS[sort_by]
    
    # SECURE: Column name is from allowlist, not user input
    query = f"SELECT id, username, email, role FROM users ORDER BY {column}"
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        
        users = []
        for row in results:
            users.append({
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'role': row[3]
            })
        
        return jsonify({'users': users})
        
    except Exception as e:
        print(f"[ERROR] List users failed: {str(e)}")
        return jsonify({'error': 'Failed to retrieve users'}), 500


# ============================================================================
# Home page
# ============================================================================

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SQL Injection Lab - Secure Version</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; max-width: 800px; }
            h1 { color: #2e7d32; }
            .success { background: #d4edda; border-left: 4px solid #28a745; padding: 15px; margin: 20px 0; }
            code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
            ul { line-height: 1.8; }
            .check { color: #28a745; }
        </style>
    </head>
    <body>
        <h1>✅ SQL Injection Lab - Secure Implementation</h1>
        
        <div class="success">
            <strong class="check">✓ Secure:</strong> This version uses proper defenses against SQL injection!
        </div>
        
        <h2>Security Measures Implemented:</h2>
        <ul>
            <li class="check">✓ Parameterized queries (prepared statements)</li>
            <li class="check">✓ Input validation and sanitization</li>
            <li class="check">✓ Allowlist for dynamic fields (ORDER BY)</li>
            <li class="check">✓ Generic error messages (no information disclosure)</li>
            <li class="check">✓ No sensitive data in responses</li>
        </ul>
        
        <h2>Endpoints (Now Secure):</h2>
        <ul>
            <li><code>POST /api/login</code> - Login with username/password</li>
            <li><code>GET /api/user/&lt;username&gt;</code> - Get user by username</li>
            <li><code>GET /api/search?q=&lt;term&gt;</code> - Search users</li>
            <li><code>GET /api/users?sort=&lt;column&gt;</code> - List users (sorted)</li>
        </ul>
        
        <h2>Testing:</h2>
        <p>Run the same attack payloads from the vulnerable version. They should all fail gracefully!</p>
        <p>Use <code>test_security.py</code> to verify all protections are working.</p>
    </body>
    </html>
    """


if __name__ == '__main__':
    print("\n" + "="*60)
    print("✅ SQL INJECTION LAB - SECURE VERSION")
    print("="*60)
    print("✓ Parameterized queries enabled")
    print("✓ Input validation active")
    print("✓ Security measures in place")
    print("="*60 + "\n")
    print("Server: http://localhost:5002\n")
    
    app.run(debug=True, host='127.0.0.1', port=5002)
