# URL Shortener - Solutions

This document provides three different implementations of the URL Shortener API, each demonstrating different levels of complexity and best practices.

## Approach 1: Beginner (Basic but Working)

A simple, straightforward implementation focusing on core functionality.

### Features
- Create short URLs
- Redirect to original URLs
- Basic validation
- SQLite database
- Simple error handling

### Code (Python/Flask)

```python
#!/usr/bin/env python3
"""
URL Shortener - Beginner Approach
Simple Flask API with basic functionality.
"""

from flask import Flask, request, jsonify, redirect
import sqlite3
import string
import random
import re

app = Flask(__name__)
DB_NAME = 'shortener.db'

def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def init_db():
    """Initialize database with schema."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            clicks INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create index for faster lookups
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_short_code 
        ON urls(short_code)
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def generate_short_code(length=6):
    """Generate random alphanumeric short code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def is_valid_url(url):
    """Validate URL format."""
    # Simple regex for URL validation
    # Note: This allows localhost and private IPs - in production,
    # you should block these for security (see Approach 2)
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost (consider blocking in production)
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP (consider blocking private IPs)
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url and pattern.search(url) is not None

@app.route('/', methods=['GET'])
def home():
    """API documentation."""
    return jsonify({
        'name': 'URL Shortener API',
        'version': '1.0',
        'endpoints': {
            'POST /api/urls': 'Create short URL',
            'GET /api/urls': 'List all URLs',
            'GET /api/urls/:code': 'Get URL details',
            'DELETE /api/urls/:code': 'Delete URL',
            'GET /:code': 'Redirect to original URL'
        }
    })

@app.route('/api/urls', methods=['POST'])
def create_url():
    """Create a new short URL."""
    # Get JSON data
    data = request.get_json()
    
    # Validate request
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    original_url = data['url']
    
    # Validate URL format
    if not is_valid_url(original_url):
        return jsonify({'error': 'Invalid URL format'}), 400
    
    # Get or generate short code
    custom_code = data.get('custom_code')
    
    if custom_code:
        # Validate custom code (alphanumeric, dash, underscore only)
        if not re.match(r'^[a-zA-Z0-9_-]+$', custom_code):
            return jsonify({'error': 'Invalid custom code format'}), 400
        short_code = custom_code
    else:
        # Generate random code and check uniqueness
        short_code = generate_short_code()
        conn = get_db()
        cursor = conn.cursor()
        
        # Keep generating until we find a unique code
        while True:
            cursor.execute('SELECT 1 FROM urls WHERE short_code = ?', (short_code,))
            if not cursor.fetchone():
                break
            short_code = generate_short_code()
        
        conn.close()
    
    # Insert into database
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO urls (short_code, original_url)
            VALUES (?, ?)
        ''', (short_code, original_url))
        
        conn.commit()
        
        # Get the created record
        cursor.execute('''
            SELECT short_code, original_url, clicks, created_at
            FROM urls WHERE short_code = ?
        ''', (short_code,))
        
        row = cursor.fetchone()
        conn.close()
        
        # Return response
        return jsonify({
            'short_code': row['short_code'],
            'original_url': row['original_url'],
            'short_url': f"{request.host_url}{row['short_code']}",
            'clicks': row['clicks'],
            'created_at': row['created_at']
        }), 201
        
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Short code already exists'}), 409

@app.route('/api/urls', methods=['GET'])
def list_urls():
    """List all shortened URLs."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT short_code, original_url, clicks, created_at
        FROM urls
        ORDER BY created_at DESC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    # Format results
    urls = []
    for row in rows:
        urls.append({
            'short_code': row['short_code'],
            'original_url': row['original_url'],
            'short_url': f"{request.host_url}{row['short_code']}",
            'clicks': row['clicks'],
            'created_at': row['created_at']
        })
    
    return jsonify({
        'count': len(urls),
        'urls': urls
    })

@app.route('/api/urls/<short_code>', methods=['GET'])
def get_url(short_code):
    """Get details of a specific short URL."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT short_code, original_url, clicks, created_at
        FROM urls WHERE short_code = ?
    ''', (short_code,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return jsonify({'error': 'Short code not found'}), 404
    
    return jsonify({
        'short_code': row['short_code'],
        'original_url': row['original_url'],
        'short_url': f"{request.host_url}{row['short_code']}",
        'clicks': row['clicks'],
        'created_at': row['created_at']
    })

@app.route('/api/urls/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    """Delete a short URL."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM urls WHERE short_code = ?', (short_code,))
    deleted = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    
    if deleted:
        return '', 204
    else:
        return jsonify({'error': 'Short code not found'}), 404

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    """Redirect to the original URL."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get URL
    cursor.execute('''
        SELECT original_url FROM urls WHERE short_code = ?
    ''', (short_code,))
    
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return jsonify({'error': 'Short code not found'}), 404
    
    original_url = row['original_url']
    
    # Increment click counter
    cursor.execute('''
        UPDATE urls SET clicks = clicks + 1
        WHERE short_code = ?
    ''', (short_code,))
    
    conn.commit()
    conn.close()
    
    # Redirect (301 = permanent redirect)
    return redirect(original_url, code=301)

if __name__ == '__main__':
    print("="*50)
    print("URL Shortener API")
    print("="*50)
    
    # Initialize database
    init_db()
    
    # Run server
    print("Server running on http://localhost:5000")
    app.run(debug=True, port=5000)
```

### Testing with curl

```bash
# Create short URL
curl -X POST http://localhost:5000/api/urls \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.github.com"}'

# Create with custom code
curl -X POST http://localhost:5000/api/urls \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.github.com","custom_code":"gh"}'

# List all URLs
curl http://localhost:5000/api/urls

# Get specific URL
curl http://localhost:5000/api/urls/gh

# Test redirect (in browser or with -L flag)
curl -L http://localhost:5000/gh

# Delete URL
curl -X DELETE http://localhost:5000/api/urls/gh
```

### Pros
✅ Simple and easy to understand  
✅ All basic functionality works  
✅ Good for learning API development  
✅ Single file, easy to run  

### Cons
❌ No advanced validation (e.g., blocking localhost)  
❌ No rate limiting  
❌ No testing  
❌ No logging  
❌ Potential SQL injection (though parametrized queries help)  

---

## Approach 2: Intermediate (Better Practices)

This approach improves on Approach 1 with better organization, validation, and error handling.

### Features
- Organized with classes and modules
- Enhanced URL validation (blocks private IPs)
- Better error handling
- Logging
- Configuration management
- Input sanitization

### Project Structure

```
url-shortener/
├── app.py              # Flask application
├── database.py         # Database operations
├── validators.py       # URL validation
├── config.py          # Configuration
├── shortener.db       # SQLite database
└── requirements.txt   # Dependencies
```

### config.py

```python
"""Configuration for URL shortener."""

import os

class Config:
    """Application configuration."""
    
    # Database
    DATABASE = os.getenv('DATABASE', 'shortener.db')
    
    # Short code settings
    SHORT_CODE_LENGTH = int(os.getenv('SHORT_CODE_LENGTH', 6))
    CUSTOM_CODE_MAX_LENGTH = 50
    
    # URL settings
    MAX_URL_LENGTH = 2048
    
    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Security
    BLOCK_PRIVATE_IPS = True
```

### validators.py

```python
"""URL validation and sanitization."""

import re
from urllib.parse import urlparse
import ipaddress

def is_valid_url(url, block_private=True):
    """
    Validate URL format and check if it's safe.
    
    Args:
        url: URL to validate
        block_private: Whether to block private/internal IPs
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not url:
        return False, "URL cannot be empty"
    
    if len(url) > 2048:
        return False, "URL too long (max 2048 characters)"
    
    # Must start with http:// or https://
    if not url.startswith(('http://', 'https://')):
        return False, "URL must start with http:// or https://"
    
    # Parse URL
    try:
        parsed = urlparse(url)
    except Exception:
        return False, "Invalid URL format"
    
    if not parsed.netloc:
        return False, "URL must have a valid domain"
    
    # Extract hostname (remove port if present)
    hostname = parsed.netloc.split(':')[0]
    
    # Block file:// and other dangerous protocols
    if parsed.scheme not in ('http', 'https'):
        return False, "Only HTTP and HTTPS URLs allowed"
    
    if block_private:
        # Block localhost
        if hostname.lower() in ('localhost', '127.0.0.1', '::1'):
            return False, "Cannot shorten localhost URLs"
        
        # Block private IP ranges
        try:
            ip = ipaddress.ip_address(hostname)
            if ip.is_private or ip.is_loopback or ip.is_link_local:
                return False, "Cannot shorten private IP addresses"
        except ValueError:
            # Not an IP address, that's fine
            pass
        
        # Block common internal domains
        internal_domains = ['.local', '.internal', '.corp']
        if any(hostname.endswith(domain) for domain in internal_domains):
            return False, "Cannot shorten internal domains"
    
    return True, None

def is_valid_short_code(code, max_length=50):
    """
    Validate custom short code.
    
    Args:
        code: Short code to validate
        max_length: Maximum allowed length
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not code:
        return False, "Short code cannot be empty"
    
    if len(code) > max_length:
        return False, f"Short code too long (max {max_length} characters)"
    
    # Only alphanumeric, dash, and underscore
    if not re.match(r'^[a-zA-Z0-9_-]+$', code):
        return False, "Short code can only contain letters, numbers, dashes, and underscores"
    
    # Reserved words that shouldn't be used as short codes
    reserved = ['api', 'admin', 'static', 'health', 'docs']
    if code.lower() in reserved:
        return False, f"'{code}' is a reserved word"
    
    return True, None
```

### database.py

```python
"""Database operations for URL shortener."""

import sqlite3
import logging
from contextlib import contextmanager
from config import Config

logger = logging.getLogger(__name__)

@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_database():
    """Initialize database schema."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Create urls table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                clicks INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index for fast lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_short_code 
            ON urls(short_code)
        ''')
        
        logger.info("Database initialized successfully")

def create_short_url(short_code, original_url):
    """
    Create a new short URL.
    
    Args:
        short_code: Short code to use
        original_url: Original long URL
        
    Returns:
        dict: Created URL record or None if code exists
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO urls (short_code, original_url)
                VALUES (?, ?)
            ''', (short_code, original_url))
            
            cursor.execute('''
                SELECT short_code, original_url, clicks, created_at
                FROM urls WHERE short_code = ?
            ''', (short_code,))
            
            row = cursor.fetchone()
            return dict(row) if row else None
            
    except sqlite3.IntegrityError:
        logger.warning(f"Short code already exists: {short_code}")
        return None

def get_url_by_code(short_code):
    """
    Get URL by short code.
    
    Args:
        short_code: Short code to lookup
        
    Returns:
        dict: URL record or None
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT short_code, original_url, clicks, created_at
            FROM urls WHERE short_code = ?
        ''', (short_code,))
        
        row = cursor.fetchone()
        return dict(row) if row else None

def get_all_urls(limit=100, offset=0):
    """
    Get all URLs with pagination.
    
    Args:
        limit: Maximum number of results
        offset: Number of results to skip
        
    Returns:
        list: List of URL records
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT short_code, original_url, clicks, created_at
            FROM urls
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        return [dict(row) for row in cursor.fetchall()]

def increment_clicks(short_code):
    """
    Increment click counter for a URL.
    
    Args:
        short_code: Short code to increment
        
    Returns:
        bool: True if successful
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE urls 
            SET clicks = clicks + 1, updated_at = CURRENT_TIMESTAMP
            WHERE short_code = ?
        ''', (short_code,))
        
        return cursor.rowcount > 0

def delete_url(short_code):
    """
    Delete a URL.
    
    Args:
        short_code: Short code to delete
        
    Returns:
        bool: True if deleted, False if not found
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM urls WHERE short_code = ?', (short_code,))
        deleted = cursor.rowcount > 0
        
        if deleted:
            logger.info(f"Deleted short code: {short_code}")
        
        return deleted

def code_exists(short_code):
    """
    Check if short code exists.
    
    Args:
        short_code: Code to check
        
    Returns:
        bool: True if exists
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM urls WHERE short_code = ? LIMIT 1', (short_code,))
        return cursor.fetchone() is not None
```

### app.py

```python
"""URL Shortener API - Intermediate Approach."""

from flask import Flask, request, jsonify, redirect
import string
import random
import logging

from config import Config
from database import (
    init_database, create_short_url, get_url_by_code,
    get_all_urls, increment_clicks, delete_url, code_exists
)
from validators import is_valid_url, is_valid_short_code

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def generate_short_code(length=None):
    """Generate random short code."""
    if length is None:
        length = Config.SHORT_CODE_LENGTH
    
    chars = string.ascii_letters + string.digits
    
    # Generate until we find a unique code
    max_attempts = 100
    for _ in range(max_attempts):
        code = ''.join(random.choice(chars) for _ in range(length))
        if not code_exists(code):
            return code
    
    # If we can't find a unique code, use longer code
    return generate_short_code(length + 1)

@app.route('/', methods=['GET'])
def home():
    """API documentation."""
    return jsonify({
        'name': 'URL Shortener API',
        'version': '2.0',
        'endpoints': {
            'POST /api/urls': 'Create short URL',
            'GET /api/urls': 'List all URLs (supports ?limit=N&offset=N)',
            'GET /api/urls/:code': 'Get URL details',
            'DELETE /api/urls/:code': 'Delete URL',
            'GET /:code': 'Redirect to original URL'
        }
    })

@app.route('/api/urls', methods=['POST'])
def create_url():
    """Create new short URL."""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    original_url = data['url'].strip()
    
    # Validate URL
    valid, error = is_valid_url(original_url, Config.BLOCK_PRIVATE_IPS)
    if not valid:
        return jsonify({'error': error}), 400
    
    # Handle custom code
    custom_code = data.get('custom_code')
    
    if custom_code:
        custom_code = custom_code.strip()
        valid, error = is_valid_short_code(custom_code, Config.CUSTOM_CODE_MAX_LENGTH)
        if not valid:
            return jsonify({'error': error}), 400
        short_code = custom_code
    else:
        short_code = generate_short_code()
    
    # Create in database
    result = create_short_url(short_code, original_url)
    
    if not result:
        return jsonify({'error': 'Short code already exists'}), 409
    
    logger.info(f"Created short URL: {short_code} -> {original_url}")
    
    # Format response
    result['short_url'] = f"{request.host_url}{result['short_code']}"
    return jsonify(result), 201

@app.route('/api/urls', methods=['GET'])
def list_urls_route():
    """List all URLs with pagination."""
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    # Validate pagination parameters
    if limit < 1 or limit > 1000:
        return jsonify({'error': 'Limit must be between 1 and 1000'}), 400
    if offset < 0:
        return jsonify({'error': 'Offset must be non-negative'}), 400
    
    urls = get_all_urls(limit, offset)
    
    # Add short_url field
    for url in urls:
        url['short_url'] = f"{request.host_url}{url['short_code']}"
    
    return jsonify({
        'count': len(urls),
        'limit': limit,
        'offset': offset,
        'urls': urls
    })

@app.route('/api/urls/<short_code>', methods=['GET'])
def get_url_route(short_code):
    """Get URL details."""
    url = get_url_by_code(short_code)
    
    if not url:
        return jsonify({'error': 'Short code not found'}), 404
    
    url['short_url'] = f"{request.host_url}{url['short_code']}"
    return jsonify(url)

@app.route('/api/urls/<short_code>', methods=['DELETE'])
def delete_url_route(short_code):
    """Delete URL."""
    if delete_url(short_code):
        return '', 204
    else:
        return jsonify({'error': 'Short code not found'}), 404

@app.route('/<short_code>', methods=['GET'])
def redirect_route(short_code):
    """Redirect to original URL."""
    url = get_url_by_code(short_code)
    
    if not url:
        return jsonify({'error': 'Short code not found'}), 404
    
    # Increment counter
    increment_clicks(short_code)
    
    logger.info(f"Redirecting {short_code} -> {url['original_url']}")
    
    return redirect(url['original_url'], code=301)

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    logger.error(f"Internal error: {e}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting URL Shortener API v2.0")
    
    # Initialize database
    init_database()
    
    # Run server
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
```

### Pros
✅ Well-organized modular code  
✅ Comprehensive validation  
✅ Security features (blocks private IPs)  
✅ Logging for debugging  
✅ Pagination support  
✅ Configuration management  

### Cons
❌ No rate limiting  
❌ No unit tests  
❌ No caching  

---

## Approach 3: Advanced (Production-Ready)

This approach adds comprehensive testing, rate limiting, caching, and follows enterprise-level practices.

### Additional Features
- Unit and integration tests
- Rate limiting (prevents abuse)
- Redis caching for fast lookups
- API authentication with API keys
- Comprehensive logging
- Docker support
- CI/CD ready

### Key Additional Files

#### tests/test_api.py

```python
"""API tests for URL shortener."""

import pytest
import json
from app import app
from database import init_database

@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    init_database()
    
    with app.test_client() as client:
        yield client

def test_create_url(client):
    """Test creating short URL."""
    response = client.post('/api/urls',
        data=json.dumps({'url': 'https://www.example.com'}),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'short_code' in data
    assert data['original_url'] == 'https://www.example.com'

def test_create_url_invalid(client):
    """Test creating URL with invalid format."""
    response = client.post('/api/urls',
        data=json.dumps({'url': 'not-a-url'}),
        content_type='application/json'
    )
    
    assert response.status_code == 400

def test_redirect(client):
    """Test URL redirection."""
    # Create URL first
    response = client.post('/api/urls',
        data=json.dumps({'url': 'https://www.example.com', 'custom_code': 'test123'}),
        content_type='application/json'
    )
    
    # Test redirect
    response = client.get('/test123')
    assert response.status_code == 301
    assert response.location == 'https://www.example.com'

def test_delete_url(client):
    """Test deleting URL."""
    # Create URL
    client.post('/api/urls',
        data=json.dumps({'url': 'https://www.example.com', 'custom_code': 'del123'}),
        content_type='application/json'
    )
    
    # Delete it
    response = client.delete('/api/urls/del123')
    assert response.status_code == 204
    
    # Verify it's gone
    response = client.get('/api/urls/del123')
    assert response.status_code == 404
```

### Pros
✅ Production-ready  
✅ Comprehensive testing  
✅ Rate limiting  
✅ Caching for performance  
✅ API authentication  
✅ Docker support  
✅ Well-documented  

### Cons
❌ More complex setup  
❌ Requires Redis  
❌ Steeper learning curve  

---

## Comparison

| Aspect | Approach 1 | Approach 2 | Approach 3 |
|--------|-----------|------------|------------|
| **Lines of Code** | ~300 | ~600 | ~1000+ |
| **Files** | 1 | 4-5 | 10+ |
| **Validation** | Basic | Comprehensive | Enterprise-level |
| **Testing** | Manual | Manual | Automated (pytest) |
| **Security** | Basic | Good (blocks private IPs) | Excellent (+ rate limiting) |
| **Performance** | Direct DB queries | Optimized queries | Redis caching |
| **Error Handling** | Simple | Detailed | Comprehensive |
| **Logging** | Print statements | Structured logging | Advanced logging + metrics |
| **Deployment** | Local only | Production-ready | Docker + CI/CD |
| **Suitable For** | Learning | Small projects | Production systems |

## When to Use Each Approach

### Use Approach 1 when:
- Learning REST APIs for the first time
- Building a quick prototype
- Need something simple and working

### Use Approach 2 when:
- Building a real application
- Need good code organization
- Security is important
- Want maintainable code

### Use Approach 3 when:
- Deploying to production
- Need high performance
- Expect high traffic
- Require monitoring and analytics
- Working in a team

---

[Back to Requirements](./02-url-shortener-requirements.md) | [Back to Projects](./README.md)
