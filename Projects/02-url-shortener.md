# 🔗 Project 2: URL Shortener

**Difficulty**: Intermediate  
**Time**: 4-6 hours  
**Concepts**: REST APIs, CRUD operations, databases, Flask

## Project Description

Build a URL shortening service similar to bit.ly or tinyurl. Users can submit long URLs and receive short codes that redirect to the original URL.

## Learning Objectives

- Design and implement a RESTful API
- Perform CRUD operations
- Work with databases (SQLite)
- Implement redirects
- Handle URL validation
- Track click statistics

## Requirements

### Functional Requirements

1. **Shorten URLs**: Convert long URLs to short codes
2. **Redirect**: Short codes redirect to original URLs
3. **List URLs**: View all shortened URLs
4. **Delete URLs**: Remove shortened URLs
5. **Track clicks**: Count how many times each link is used
6. **Custom codes**: Allow users to specify custom short codes

### Technical Requirements

- RESTful API design
- Persistent storage (SQLite database)
- URL validation
- Collision handling (duplicate short codes)
- Error handling

## API Design

### Endpoints

```
POST   /api/urls        # Create short URL
GET    /api/urls        # List all URLs
GET    /api/urls/:code  # Get URL details
DELETE /api/urls/:code  # Delete URL
GET    /:code           # Redirect to original URL
```

### Request/Response Examples

**Create short URL:**
```http
POST /api/urls
Content-Type: application/json

{
  "url": "https://www.example.com/very/long/url",
  "custom_code": "ex123"  // optional
}

Response: 201 Created
{
  "short_code": "ex123",
  "original_url": "https://www.example.com/very/long/url",
  "short_url": "http://localhost:5000/ex123",
  "created_at": "2024-01-01T12:00:00Z"
}
```

**Get URL details:**
```http
GET /api/urls/ex123

Response: 200 OK
{
  "short_code": "ex123",
  "original_url": "https://www.example.com/very/long/url",
  "clicks": 42,
  "created_at": "2024-01-01T12:00:00Z"
}
```

## Implementation Guide

### Step 1: Project Structure

```
url-shortener/
├── app.py              # Main Flask application
├── database.py         # Database operations
├── models.py           # Data models
├── requirements.txt    # Dependencies
├── shortener.db        # SQLite database (generated)
└── README.md          # Documentation
```

### Step 2: Install Dependencies

```bash
pip install flask
```

### Step 3: Database Schema

```python
# database.py
import sqlite3
from datetime import datetime

def init_db():
    """Initialize database with schema."""
    conn = sqlite3.connect('shortener.db')
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
    
    conn.commit()
    conn.close()

def create_url(short_code, original_url):
    """Store a new shortened URL."""
    conn = sqlite3.connect('shortener.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO urls (short_code, original_url)
            VALUES (?, ?)
        ''', (short_code, original_url))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Short code already exists
    finally:
        conn.close()

def get_url(short_code):
    """Get URL by short code."""
    conn = sqlite3.connect('shortener.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT short_code, original_url, clicks, created_at
        FROM urls WHERE short_code = ?
    ''', (short_code,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'short_code': result[0],
            'original_url': result[1],
            'clicks': result[2],
            'created_at': result[3]
        }
    return None

def increment_clicks(short_code):
    """Increment click counter."""
    conn = sqlite3.connect('shortener.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE urls SET clicks = clicks + 1
        WHERE short_code = ?
    ''', (short_code,))
    
    conn.commit()
    conn.close()

def get_all_urls():
    """Get all URLs."""
    conn = sqlite3.connect('shortener.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT short_code, original_url, clicks, created_at FROM urls')
    results = cursor.fetchall()
    conn.close()
    
    return [
        {
            'short_code': r[0],
            'original_url': r[1],
            'clicks': r[2],
            'created_at': r[3]
        }
        for r in results
    ]

def delete_url(short_code):
    """Delete a URL."""
    conn = sqlite3.connect('shortener.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM urls WHERE short_code = ?', (short_code,))
    deleted = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    
    return deleted
```

### Step 4: Flask Application

```python
# app.py
from flask import Flask, request, jsonify, redirect
import string
import random
from database import init_db, create_url, get_url, get_all_urls, delete_url, increment_clicks
import re

app = Flask(__name__)

# Initialize database
init_db()

def generate_short_code(length=6):
    """Generate random short code."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def is_valid_url(url):
    """Validate URL format."""
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)

@app.route('/api/urls', methods=['POST'])
def create_short_url():
    """Create a new short URL."""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    original_url = data['url']
    
    # Validate URL
    if not is_valid_url(original_url):
        return jsonify({'error': 'Invalid URL format'}), 400
    
    # Get or generate short code
    short_code = data.get('custom_code')
    
    if short_code:
        # Validate custom code (alphanumeric only)
        if not re.match(r'^[a-zA-Z0-9_-]+$', short_code):
            return jsonify({'error': 'Invalid short code format'}), 400
    else:
        # Generate random code
        short_code = generate_short_code()
        # Ensure uniqueness
        while get_url(short_code):
            short_code = generate_short_code()
    
    # Create in database
    if create_url(short_code, original_url):
        result = get_url(short_code)
        result['short_url'] = f"{request.host_url}{short_code}"
        return jsonify(result), 201
    else:
        return jsonify({'error': 'Short code already exists'}), 409

@app.route('/api/urls', methods=['GET'])
def list_urls():
    """List all shortened URLs."""
    urls = get_all_urls()
    
    # Add full short URL
    for url in urls:
        url['short_url'] = f"{request.host_url}{url['short_code']}"
    
    return jsonify({
        'count': len(urls),
        'urls': urls
    }), 200

@app.route('/api/urls/<short_code>', methods=['GET'])
def get_url_details(short_code):
    """Get details of a shortened URL."""
    url = get_url(short_code)
    
    if not url:
        return jsonify({'error': 'Short code not found'}), 404
    
    url['short_url'] = f"{request.host_url}{short_code}"
    return jsonify(url), 200

@app.route('/api/urls/<short_code>', methods=['DELETE'])
def delete_short_url(short_code):
    """Delete a shortened URL."""
    if delete_url(short_code):
        return '', 204
    else:
        return jsonify({'error': 'Short code not found'}), 404

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    """Redirect to original URL."""
    url = get_url(short_code)
    
    if not url:
        return jsonify({'error': 'Short code not found'}), 404
    
    # Increment click counter
    increment_clicks(short_code)
    
    # Redirect
    return redirect(url['original_url'], code=301)

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
    }), 200

if __name__ == '__main__':
    print("🔗 URL Shortener API")
    print("Server running on http://localhost:5000")
    app.run(debug=True, port=5000)
```

## Features to Add (Progressive Difficulty)

### ⭐ Level 1: Basic Features
- [x] Create short URLs
- [x] Redirect to original URLs
- [x] Basic validation
- [x] Track click counts

### ⭐⭐ Level 2: Intermediate Features
- [ ] Expiration dates for URLs
- [ ] Password-protected URLs
- [ ] QR code generation
- [ ] Analytics dashboard
- [ ] Rate limiting

### ⭐⭐⭐ Level 3: Advanced Features
- [ ] User accounts and authentication
- [ ] API key management
- [ ] Custom domains
- [ ] URL preview before redirect
- [ ] Bulk URL shortening
- [ ] Export statistics

## Testing

```bash
# Create short URL
curl -X POST http://localhost:5000/api/urls \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.github.com"}'

# List all URLs
curl http://localhost:5000/api/urls

# Get URL details
curl http://localhost:5000/api/urls/abc123

# Visit short URL in browser
# http://localhost:5000/abc123

# Delete URL
curl -X DELETE http://localhost:5000/api/urls/abc123
```

## Success Criteria

- ✅ Creates short URLs for long URLs
- ✅ Redirects work correctly
- ✅ Tracks click statistics
- ✅ Handles custom short codes
- ✅ Validates URLs properly
- ✅ Prevents duplicate short codes
- ✅ RESTful API design
- ✅ Persistent storage with database

## Next Steps

Ready for the final project? Try [Project 3: Real-Time Dashboard](./03-realtime-dashboard.md)!

---

[Back to Projects](./README.md)
