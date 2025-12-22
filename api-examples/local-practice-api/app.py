"""
Practice API - A Complete REST API for Learning

Features:
- JWT Authentication
- CRUD Operations
- SQLite Database
- Error Handling
- Rate Limiting
- Input Validation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import sqlite3
import jwt
import datetime
import hashlib
import os
from collections import defaultdict
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
# NOTE: For educational purposes only!
# In production, use environment variables: os.environ.get('SECRET_KEY')
SECRET_KEY = 'your-secret-key-change-in-production'
DATABASE = 'practice_api.db'
TOKEN_EXPIRY = 24  # hours
RATE_LIMIT = 100  # requests per minute per IP

# Rate limiting storage
rate_limit_storage = defaultdict(list)


def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


def init_db():
    """Initialize database with schema"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users (id)
        )
    ''')
    
    # Comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts (id),
            FOREIGN KEY (author_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()


def hash_password(password):
    """
    Hash a password using SHA-256
    
    NOTE: For educational purposes only!
    In production, use bcrypt, scrypt, or Argon2 with proper salting.
    SHA-256 alone is vulnerable to rainbow table attacks.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, password_hash):
    """Verify a password against its hash"""
    return hash_password(password) == password_hash


def generate_token(user_id, username):
    """Generate JWT token for user"""
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_EXPIRY)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def decode_token(token):
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def rate_limit_check(ip_address):
    """
    Check if IP has exceeded rate limit
    
    NOTE: This is a basic implementation for educational purposes.
    In production, use Flask-Limiter or similar libraries.
    This function is currently not enforced - you can add it as an exercise!
    """
    now = time.time()
    minute_ago = now - 60
    
    # Clean old entries
    rate_limit_storage[ip_address] = [
        t for t in rate_limit_storage[ip_address] if t > minute_ago
    ]
    
    # Check limit
    if len(rate_limit_storage[ip_address]) >= RATE_LIMIT:
        return False
    
    # Add current request
    rate_limit_storage[ip_address].append(now)
    return True


def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                'error': {
                    'code': 'UNAUTHORIZED',
                    'message': 'Authorization header missing'
                }
            }), 401
        
        try:
            token = auth_header.split(' ')[1]  # Bearer <token>
        except IndexError:
            return jsonify({
                'error': {
                    'code': 'INVALID_TOKEN',
                    'message': 'Invalid authorization header format'
                }
            }), 401
        
        payload = decode_token(token)
        if not payload:
            return jsonify({
                'error': {
                    'code': 'INVALID_TOKEN',
                    'message': 'Token is invalid or expired'
                }
            }), 401
        
        # Add user info to request
        request.user_id = payload['user_id']
        request.username = payload['username']
        
        return f(*args, **kwargs)
    
    return decorated_function


# ============================================================================
# HEALTH & TESTING ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.utcnow().isoformat()
    })


@app.route('/api/test/echo', methods=['POST'])
def echo():
    """Echo back the request data"""
    return jsonify({
        'echo': request.get_json(),
        'received_at': datetime.datetime.utcnow().isoformat()
    })


@app.route('/api/test/error/<int:code>', methods=['GET'])
def test_error(code):
    """Generate specific error codes for testing"""
    error_messages = {
        400: 'Bad Request - Invalid input',
        401: 'Unauthorized - Authentication required',
        403: 'Forbidden - Access denied',
        404: 'Not Found - Resource does not exist',
        500: 'Internal Server Error - Something went wrong'
    }
    
    message = error_messages.get(code, 'Unknown error')
    return jsonify({
        'error': {
            'code': f'TEST_ERROR_{code}',
            'message': message
        }
    }), code


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validation
    if not data or not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Missing required fields',
                'details': 'username, email, and password are required'
            }
        }), 400
    
    username = data['username']
    email = data['email']
    password = data['password']
    
    # Basic validation
    if len(password) < 6:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Password must be at least 6 characters'
            }
        }), 400
    
    if '@' not in email:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Invalid email address'
            }
        }), 400
    
    # Hash password
    password_hash = hash_password(password)
    
    # Insert user
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'message': 'User created successfully',
            'user_id': user_id
        }), 201
        
    except sqlite3.IntegrityError as e:
        if 'username' in str(e):
            return jsonify({
                'error': {
                    'code': 'CONFLICT',
                    'message': 'Username already exists'
                }
            }), 409
        else:
            return jsonify({
                'error': {
                    'code': 'CONFLICT',
                    'message': 'Email already exists'
                }
            }), 409


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login and get JWT token"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['username', 'password']):
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Username and password are required'
            }
        }), 400
    
    username = data['username']
    password = data['password']
    
    # Find user
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, username, email, password_hash FROM users WHERE username = ?',
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    
    if not user or not verify_password(password, user['password_hash']):
        return jsonify({
            'error': {
                'code': 'INVALID_CREDENTIALS',
                'message': 'Invalid username or password'
            }
        }), 401
    
    # Generate token
    token = generate_token(user['id'], user['username'])
    
    return jsonify({
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email']
        }
    })


# ============================================================================
# USER ENDPOINTS
# ============================================================================

@app.route('/api/users/me', methods=['GET'])
@require_auth
def get_current_user():
    """Get current user profile"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, username, email, created_at FROM users WHERE id = ?',
        (request.user_id,)
    )
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': 'User not found'
            }
        }), 404
    
    return jsonify(dict(user))


@app.route('/api/users/me', methods=['PATCH'])
@require_auth
def update_current_user():
    """Update current user profile"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'No data provided'
            }
        }), 400
    
    # Only allow updating email
    if 'email' not in data:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Only email can be updated'
            }
        }), 400
    
    email = data['email']
    
    if '@' not in email:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Invalid email address'
            }
        }), 400
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE users SET email = ? WHERE id = ?',
            (email, request.user_id)
        )
        conn.commit()
        
        # Get updated user
        cursor.execute(
            'SELECT id, username, email FROM users WHERE id = ?',
            (request.user_id,)
        )
        user = cursor.fetchone()
        conn.close()
        
        return jsonify(dict(user))
        
    except sqlite3.IntegrityError:
        return jsonify({
            'error': {
                'code': 'CONFLICT',
                'message': 'Email already exists'
            }
        }), 409


# ============================================================================
# POSTS ENDPOINTS
# ============================================================================

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Get all posts with optional filtering and pagination"""
    # Query parameters with validation
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except (ValueError, TypeError):
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Page and limit must be valid integers'
            }
        }), 400
    
    # Validate ranges
    if page < 1:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Page must be greater than 0'
            }
        }), 400
    
    if limit < 1 or limit > 100:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Limit must be between 1 and 100'
            }
        }), 400
    
    author = request.args.get('author')
    
    offset = (page - 1) * limit
    
    # Build query
    conn = get_db()
    cursor = conn.cursor()
    
    if author:
        # Get total count first
        cursor.execute('''
            SELECT COUNT(*) as count FROM posts p
            JOIN users u ON p.author_id = u.id
            WHERE u.username = ?
        ''', (author,))
        total = cursor.fetchone()['count']
        
        # Get posts
        cursor.execute('''
            SELECT p.id, p.title, p.content, u.username as author, p.created_at, p.updated_at
            FROM posts p
            JOIN users u ON p.author_id = u.id
            WHERE u.username = ?
            ORDER BY p.created_at DESC
            LIMIT ? OFFSET ?
        ''', (author, limit, offset))
        posts = [dict(row) for row in cursor.fetchall()]
    else:
        # Get total count first
        cursor.execute('SELECT COUNT(*) as count FROM posts')
        total = cursor.fetchone()['count']
        
        # Get posts
        cursor.execute('''
            SELECT p.id, p.title, p.content, u.username as author, p.created_at, p.updated_at
            FROM posts p
            JOIN users u ON p.author_id = u.id
            ORDER BY p.created_at DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        posts = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'data': posts,
        'meta': {
            'total': total,
            'page': page,
            'limit': limit
        }
    })


@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a specific post"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id, p.title, p.content, u.username as author, p.created_at, p.updated_at
        FROM posts p
        JOIN users u ON p.author_id = u.id
        WHERE p.id = ?
    ''', (post_id,))
    post = cursor.fetchone()
    conn.close()
    
    if not post:
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Post not found'
            }
        }), 404
    
    return jsonify(dict(post))


@app.route('/api/posts', methods=['POST'])
@require_auth
def create_post():
    """Create a new post"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['title', 'content']):
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Title and content are required'
            }
        }), 400
    
    title = data['title']
    content = data['content']
    
    if len(title) < 3:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Title must be at least 3 characters'
            }
        }), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)',
        (title, content, request.user_id)
    )
    conn.commit()
    post_id = cursor.lastrowid
    
    # Get created post
    cursor.execute('''
        SELECT p.id, p.title, p.content, u.username as author, p.created_at
        FROM posts p
        JOIN users u ON p.author_id = u.id
        WHERE p.id = ?
    ''', (post_id,))
    post = cursor.fetchone()
    conn.close()
    
    return jsonify(dict(post)), 201


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
@require_auth
def update_post(post_id):
    """Update a post"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['title', 'content']):
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Title and content are required'
            }
        }), 400
    
    # Check if post exists and belongs to user
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT author_id FROM posts WHERE id = ?', (post_id,))
    post = cursor.fetchone()
    
    if not post:
        conn.close()
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Post not found'
            }
        }), 404
    
    if post['author_id'] != request.user_id:
        conn.close()
        return jsonify({
            'error': {
                'code': 'FORBIDDEN',
                'message': 'You can only update your own posts'
            }
        }), 403
    
    # Update post
    cursor.execute(
        'UPDATE posts SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
        (data['title'], data['content'], post_id)
    )
    conn.commit()
    
    # Get updated post
    cursor.execute('''
        SELECT p.id, p.title, p.content, u.username as author, p.created_at, p.updated_at
        FROM posts p
        JOIN users u ON p.author_id = u.id
        WHERE p.id = ?
    ''', (post_id,))
    updated_post = cursor.fetchone()
    conn.close()
    
    return jsonify(dict(updated_post))


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
@require_auth
def delete_post(post_id):
    """Delete a post"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT author_id FROM posts WHERE id = ?', (post_id,))
    post = cursor.fetchone()
    
    if not post:
        conn.close()
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Post not found'
            }
        }), 404
    
    if post['author_id'] != request.user_id:
        conn.close()
        return jsonify({
            'error': {
                'code': 'FORBIDDEN',
                'message': 'You can only delete your own posts'
            }
        }), 403
    
    # Delete comments first (foreign key constraint)
    cursor.execute('DELETE FROM comments WHERE post_id = ?', (post_id,))
    cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    
    return '', 204


# ============================================================================
# COMMENTS ENDPOINTS
# ============================================================================

@app.route('/api/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    """Get all comments for a post"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if post exists
    cursor.execute('SELECT id FROM posts WHERE id = ?', (post_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Post not found'
            }
        }), 404
    
    cursor.execute('''
        SELECT c.id, c.post_id, u.username as author, c.content, c.created_at
        FROM comments c
        JOIN users u ON c.author_id = u.id
        WHERE c.post_id = ?
        ORDER BY c.created_at ASC
    ''', (post_id,))
    comments = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(comments)


@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
@require_auth
def create_comment(post_id):
    """Add a comment to a post"""
    data = request.get_json()
    
    if not data or 'content' not in data:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Content is required'
            }
        }), 400
    
    content = data['content']
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if post exists
    cursor.execute('SELECT id FROM posts WHERE id = ?', (post_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Post not found'
            }
        }), 404
    
    # Create comment
    cursor.execute(
        'INSERT INTO comments (post_id, author_id, content) VALUES (?, ?, ?)',
        (post_id, request.user_id, content)
    )
    conn.commit()
    comment_id = cursor.lastrowid
    
    # Get created comment
    cursor.execute('''
        SELECT c.id, c.post_id, u.username as author, c.content, c.created_at
        FROM comments c
        JOIN users u ON c.author_id = u.id
        WHERE c.id = ?
    ''', (comment_id,))
    comment = cursor.fetchone()
    conn.close()
    
    return jsonify(dict(comment)), 201


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': {
            'code': 'NOT_FOUND',
            'message': 'Endpoint not found'
        }
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': {
            'code': 'INTERNAL_ERROR',
            'message': 'Internal server error'
        }
    }), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Initialize database on first run
    if not os.path.exists(DATABASE):
        print('Initializing database...')
        init_db()
        print('Database initialized!')
    
    print('=' * 60)
    print('🚀 Practice API Server Starting...')
    print('=' * 60)
    print(f'📍 Server: http://localhost:5000')
    print(f'📖 Health: http://localhost:5000/api/health')
    print(f'📚 Docs: See README.md for full API documentation')
    print('=' * 60)
    print('💡 Quick Start:')
    print('   1. Register: POST /api/auth/register')
    print('   2. Login: POST /api/auth/login')
    print('   3. Create Post: POST /api/posts (with token)')
    print('=' * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
