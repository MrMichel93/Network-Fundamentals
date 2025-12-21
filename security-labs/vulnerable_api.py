#!/usr/bin/env python3
"""
VULNERABLE API FOR EDUCATIONAL PURPOSES ONLY
=============================================

This API contains intentional security vulnerabilities for learning purposes.
DO NOT use this code in production or deploy it on public servers!

Vulnerabilities included:
1. SQL Injection
2. Cross-Site Scripting (XSS)
3. Missing Authentication/Authorization
4. No Rate Limiting
5. Improper CORS Configuration
6. Information Disclosure

Your task: Find and fix all vulnerabilities!
"""

from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Initialize database
DB_FILE = 'vulnerable.db'

def init_db():
    """Initialize the database with sample data"""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user'
        )
    ''')
    
    # Create comments table
    cursor.execute('''
        CREATE TABLE comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample users
    cursor.execute("INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                   ('admin', 'admin123', 'admin@example.com', 'admin'))
    cursor.execute("INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                   ('user1', 'password1', 'user1@example.com', 'user'))
    cursor.execute("INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                   ('user2', 'password2', 'user2@example.com', 'user'))
    
    # Insert sample comments
    cursor.execute("INSERT INTO comments (user_id, text) VALUES (?, ?)",
                   (1, 'This is a safe comment'))
    cursor.execute("INSERT INTO comments (user_id, text) VALUES (?, ?)",
                   (2, 'Another normal comment'))
    
    conn.commit()
    conn.close()
    print("✓ Database initialized with sample data")

# Initialize on startup
init_db()


# ============================================================================
# VULNERABILITY 1: SQL INJECTION
# ============================================================================

@app.route('/api/login', methods=['POST'])
def login():
    """
    VULNERABLE: SQL Injection in login endpoint
    
    Try this attack:
    {
        "username": "admin' --",
        "password": "anything"
    }
    """
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')
    
    conn = sqlite3.connect(DB_FILE)
    # DANGER: String concatenation with user input!
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    print(f"[DEBUG] Executing query: {query}")  # Information disclosure!
    
    try:
        cursor = conn.cursor()
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
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    except Exception as e:
        # DANGER: Exposing error details!
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<username>')
def get_user(username):
    """
    VULNERABLE: SQL Injection in user lookup
    
    Try: /api/users/admin' OR '1'='1
    """
    conn = sqlite3.connect(DB_FILE)
    # DANGER: f-string with user input!
    query = f"SELECT id, username, email, role FROM users WHERE username = '{username}'"
    
    print(f"[DEBUG] Query: {query}")
    
    try:
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
        return jsonify({'error': str(e), 'query': query}), 500  # Information disclosure!


# ============================================================================
# VULNERABILITY 2: CROSS-SITE SCRIPTING (XSS)
# ============================================================================

@app.route('/api/comments', methods=['POST'])
def add_comment():
    """
    VULNERABLE: Stores unsanitized user input
    
    Try posting: {"text": "<script>alert('XSS')</script>"}
    """
    data = request.json
    comment_text = data.get('text', '')
    user_id = data.get('user_id', 1)
    
    # DANGER: No input validation or sanitization!
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (user_id, text) VALUES (?, ?)",
                   (user_id, comment_text))
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'message': 'Comment posted',
        'comment': comment_text  # Reflecting unsanitized input!
    })


@app.route('/comments')
def view_comments():
    """
    VULNERABLE: Renders unsanitized HTML
    
    This will execute any scripts stored in comments!
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT text, created_at FROM comments ORDER BY created_at DESC")
    comments = cursor.fetchall()
    conn.close()
    
    # DANGER: Rendering unsanitized user input as HTML!
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Comments</title></head>
    <body>
        <h1>Comments</h1>
        <div>
    """
    
    for comment in comments:
        # DANGER: Directly inserting user content into HTML!
        html += f"<p>{comment[0]}</p><small>{comment[1]}</small><hr>"
    
    html += """
        </div>
        <a href="/">Back to Home</a>
    </body>
    </html>
    """
    
    return html


@app.route('/api/search')
def search():
    """
    VULNERABLE: Reflected XSS
    
    Try: /api/search?q=<script>alert('XSS')</script>
    """
    query = request.args.get('q', '')
    
    # DANGER: Reflecting user input without escaping!
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Search Results</title></head>
    <body>
        <h1>Search Results for: {query}</h1>
        <p>No results found.</p>
    </body>
    </html>
    """
    
    return html


# ============================================================================
# VULNERABILITY 3: MISSING AUTHENTICATION/AUTHORIZATION
# ============================================================================

@app.route('/api/admin/users')
def get_all_users():
    """
    VULNERABLE: No authentication required!
    
    Anyone can access this admin endpoint!
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, email, role FROM users")
    users = cursor.fetchall()
    conn.close()
    
    # DANGER: Exposing passwords!
    result = []
    for user in users:
        result.append({
            'id': user[0],
            'username': user[1],
            'password': user[2],  # NEVER expose passwords!
            'email': user[3],
            'role': user[4]
        })
    
    return jsonify({'users': result})


@app.route('/api/admin/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    VULNERABLE: No authorization check!
    
    Anyone can delete any user!
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': f'User {user_id} deleted'})


# ============================================================================
# VULNERABILITY 4: NO RATE LIMITING
# ============================================================================

@app.route('/api/expensive-operation')
def expensive_operation():
    """
    VULNERABLE: No rate limiting!
    
    This endpoint can be abused to cause DoS!
    """
    # Simulate expensive operation
    import time
    time.sleep(2)
    
    return jsonify({'result': 'Operation completed'})


# ============================================================================
# VULNERABILITY 5: IMPROPER CORS CONFIGURATION
# ============================================================================

@app.after_request
def add_cors_headers(response):
    """
    VULNERABLE: Allows all origins!
    
    This allows any website to access the API!
    """
    response.headers['Access-Control-Allow-Origin'] = '*'  # DANGER!
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response


# ============================================================================
# VULNERABILITY 6: INFORMATION DISCLOSURE
# ============================================================================

@app.route('/')
def home():
    """Home page with API documentation"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Vulnerable API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
            .warning { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <h1>🔓 Vulnerable API - Educational Lab</h1>
        
        <div class="warning">
            <strong>⚠️ Warning:</strong> This API is intentionally vulnerable!
            Do NOT deploy this on a public server. For educational purposes only!
        </div>
        
        <h2>Available Endpoints:</h2>
        
        <h3>1. SQL Injection Vulnerabilities</h3>
        <ul>
            <li><code>POST /api/login</code> - Login with username/password</li>
            <li><code>GET /api/users/&lt;username&gt;</code> - Get user by username</li>
        </ul>
        
        <h3>2. XSS Vulnerabilities</h3>
        <ul>
            <li><code>POST /api/comments</code> - Post a comment (stored XSS)</li>
            <li><code>GET /comments</code> - View comments (XSS executes here)</li>
            <li><code>GET /api/search?q=...</code> - Search (reflected XSS)</li>
        </ul>
        
        <h3>3. Missing Authentication/Authorization</h3>
        <ul>
            <li><code>GET /api/admin/users</code> - Get all users (no auth!)</li>
            <li><code>DELETE /api/admin/delete-user/&lt;id&gt;</code> - Delete user (no auth!)</li>
        </ul>
        
        <h3>4. No Rate Limiting</h3>
        <ul>
            <li><code>GET /api/expensive-operation</code> - Slow operation (no rate limit)</li>
        </ul>
        
        <h2>Your Tasks:</h2>
        <ol>
            <li>Test each vulnerability using curl, Postman, or browser</li>
            <li>Understand how each attack works</li>
            <li>Create a fixed version with proper security measures</li>
            <li>Test that your fixes prevent the attacks</li>
        </ol>
        
        <h2>Sample Attacks:</h2>
        
        <h3>SQL Injection:</h3>
        <pre>curl -X POST http://localhost:5000/api/login \\
  -H "Content-Type: application/json" \\
  -d '{"username": "admin'\'' --", "password": "anything"}'</pre>
        
        <h3>XSS:</h3>
        <pre>curl -X POST http://localhost:5000/api/comments \\
  -H "Content-Type: application/json" \\
  -d '{"text": "&lt;script&gt;alert('XSS')&lt;/script&gt;"}'</pre>
        
        <h3>No Authentication:</h3>
        <pre>curl http://localhost:5000/api/admin/users</pre>
        
    </body>
    </html>
    """


# Enable debug mode (DANGER: Never do this in production!)
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔓 VULNERABLE API SERVER")
    print("="*60)
    print("⚠️  This server is intentionally vulnerable!")
    print("⚠️  For educational purposes only!")
    print("⚠️  Do NOT expose this to the internet!")
    print("="*60 + "\n")
    print("Server running on http://localhost:5000")
    print("Open http://localhost:5000 in your browser to get started\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
