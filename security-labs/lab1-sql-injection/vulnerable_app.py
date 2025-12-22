#!/usr/bin/env python3
"""
VULNERABLE SQL INJECTION LAB - FOR EDUCATIONAL PURPOSES ONLY
=============================================================

This application intentionally contains SQL injection vulnerabilities.
DO NOT use in production or deploy on public servers!

Vulnerabilities:
1. Authentication bypass via SQL injection
2. Data extraction through OR-based injection
3. UNION-based SQL injection
4. Error-based information disclosure
"""

from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'vulnerable_sqli.db'

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
    
    # Insert sample users
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
    
    # Insert secrets
    cursor.execute("INSERT INTO secrets (user_id, secret_data) VALUES (1, 'Admin secret key: TOP_SECRET_123')")
    cursor.execute("INSERT INTO secrets (user_id, secret_data) VALUES (2, 'John credit card: 4532-1111-2222-3333')")
    
    conn.commit()
    conn.close()
    print("✓ Database initialized")

init_db()


# ============================================================================
# VULNERABILITY 1: SQL Injection in Login
# ============================================================================

@app.route('/api/login', methods=['POST'])
def login():
    """
    VULNERABLE: SQL Injection in authentication
    
    Attack: {"username": "admin' --", "password": "anything"}
    """
    data = request.json or {}
    username = data.get('username', '')
    password = data.get('password', '')
    
    # DANGER: String concatenation with user input!
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    # DANGER: Logging the query exposes the vulnerability
    print(f"[VULNERABLE] Executing: {query}")
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query)
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
                    'role': result[4],
                    'api_key': result[5]  # DANGER: Exposing API key!
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        # DANGER: Exposing SQL error details!
        return jsonify({
            'error': str(e),
            'query': query  # DANGER: Showing the query!
        }), 500


# ============================================================================
# VULNERABILITY 2: SQL Injection in User Lookup
# ============================================================================

@app.route('/api/user/<username>')
def get_user(username):
    """
    VULNERABLE: OR-based SQL injection
    
    Attack: /api/user/admin' OR '1'='1
    """
    # DANGER: Direct string interpolation
    query = f"SELECT id, username, email, role FROM users WHERE username = '{username}'"
    
    print(f"[VULNERABLE] Query: {query}")
    
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
        
        if users:
            return jsonify({'users': users})
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        # DANGER: Information disclosure
        return jsonify({
            'error': str(e),
            'query': query,
            'hint': 'Check your SQL syntax'
        }), 500


# ============================================================================
# VULNERABILITY 3: SQL Injection in Search
# ============================================================================

@app.route('/api/search')
def search_users():
    """
    VULNERABLE: UNION-based SQL injection
    
    Attack: /api/search?q=admin' UNION SELECT id,secret_data,1,2 FROM secrets--
    """
    search_term = request.args.get('q', '')
    
    # DANGER: Unescaped user input in LIKE clause
    query = f"SELECT id, username, email, role FROM users WHERE username LIKE '%{search_term}%'"
    
    print(f"[VULNERABLE] Search query: {query}")
    
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
        
        return jsonify({
            'results': users,
            'count': len(users)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'query': query
        }), 500


# ============================================================================
# VULNERABILITY 4: SQL Injection in Order By
# ============================================================================

@app.route('/api/users')
def list_users():
    """
    VULNERABLE: SQL injection in ORDER BY clause
    
    Attack: /api/users?sort=username; DROP TABLE users--
    """
    sort_by = request.args.get('sort', 'username')
    
    # DANGER: Direct use of user input in ORDER BY
    query = f"SELECT id, username, email, role FROM users ORDER BY {sort_by}"
    
    print(f"[VULNERABLE] List query: {query}")
    
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
        return jsonify({'error': str(e), 'query': query}), 500


# ============================================================================
# Home page
# ============================================================================

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SQL Injection Lab</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; max-width: 800px; }
            h1 { color: #d32f2f; }
            .warning { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }
            code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
            ul { line-height: 1.8; }
        </style>
    </head>
    <body>
        <h1>🔓 SQL Injection Lab - Vulnerable App</h1>
        
        <div class="warning">
            <strong>⚠️ Warning:</strong> This application is intentionally vulnerable!
            For educational purposes only. Do NOT deploy on public servers!
        </div>
        
        <h2>Vulnerable Endpoints:</h2>
        <ul>
            <li><code>POST /api/login</code> - Login with username/password</li>
            <li><code>GET /api/user/&lt;username&gt;</code> - Get user by username</li>
            <li><code>GET /api/search?q=&lt;term&gt;</code> - Search users</li>
            <li><code>GET /api/users?sort=&lt;column&gt;</code> - List users (sorted)</li>
        </ul>
        
        <h2>Sample Attacks:</h2>
        <p>See <code>exploit_examples.sh</code> for detailed attack examples.</p>
        
        <h2>Your Task:</h2>
        <ol>
            <li>Test each vulnerability using the provided exploits</li>
            <li>Understand how each attack works</li>
            <li>Study the fixed version in <code>fixed_app.py</code></li>
            <li>Run tests to verify the fixes</li>
        </ol>
    </body>
    </html>
    """


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔓 SQL INJECTION LAB - VULNERABLE APPLICATION")
    print("="*60)
    print("⚠️  This app is intentionally vulnerable!")
    print("⚠️  For educational purposes only!")
    print("="*60 + "\n")
    print("Server: http://localhost:5001\n")
    
    app.run(debug=True, host='127.0.0.1', port=5001)
