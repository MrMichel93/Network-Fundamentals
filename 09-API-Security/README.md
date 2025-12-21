# 🛡️ API Security

Learn how to protect your APIs from common security threats and vulnerabilities.

## 🎯 Learning Objectives

By the end of this module, you will:
- Understand common API security threats
- Implement input validation
- Set up rate limiting
- Configure CORS properly
- Prevent SQL injection attacks
- Prevent XSS (Cross-Site Scripting) attacks
- Follow security best practices

## Common API Security Threats 🚨

### 1. Injection Attacks
Malicious code inserted into queries

### 2. Broken Authentication
Weak login systems allowing unauthorized access

### 3. Sensitive Data Exposure
Leaking passwords, tokens, or personal information

### 4. Broken Access Control
Users accessing resources they shouldn't

### 5. Security Misconfiguration
Default passwords, unnecessary services enabled

### 6. Cross-Site Scripting (XSS)
Injecting malicious scripts into web pages

### 7. Lack of Rate Limiting
Allowing unlimited requests (DDoS attacks)

### 8. CORS Misconfiguration
Allowing untrusted origins to access your API

## Input Validation 📝

**Rule**: Never trust user input!

### Validate All Inputs

```python
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    
    # Validate username
    username = data.get('username', '').strip()
    if not username:
        return jsonify({'error': 'Username required'}), 400
    if len(username) < 3 or len(username) > 20:
        return jsonify({'error': 'Username must be 3-20 characters'}), 400
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return jsonify({'error': 'Username can only contain letters, numbers, and underscores'}), 400
    
    # Validate email
    email = data.get('email', '').strip()
    if not email:
        return jsonify({'error': 'Email required'}), 400
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Validate age
    age = data.get('age')
    if age is not None:
        if not isinstance(age, int) or age < 0 or age > 150:
            return jsonify({'error': 'Invalid age'}), 400
    
    # Data is validated, proceed with creation
    # ...
    return jsonify({'message': 'User created'}), 201
```

### Use Type Checking

```python
from flask import Flask, request, jsonify
from typing import Dict, Any

def validate_user_data(data: Dict[str, Any]) -> tuple[bool, str]:
    """
    Returns (is_valid, error_message)
    """
    if not isinstance(data, dict):
        return False, "Data must be an object"
    
    if 'username' not in data:
        return False, "Username is required"
    
    if not isinstance(data['username'], str):
        return False, "Username must be a string"
    
    if 'age' in data and not isinstance(data['age'], int):
        return False, "Age must be a number"
    
    return True, ""

@app.route('/users', methods=['POST'])
def create_user():
    is_valid, error = validate_user_data(request.json)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    # Proceed with creation
    # ...
```

## Rate Limiting 🚦

Prevent abuse by limiting requests per user/IP.

### Using Flask-Limiter

```python
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Configure rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,  # Limit by IP address
    default_limits=["200 per day", "50 per hour"]
)

# Global rate limit applied to all routes
@app.route('/api/data')
def get_data():
    return jsonify({'data': 'some data'})

# Specific rate limit for this route
@app.route('/api/expensive')
@limiter.limit("10 per minute")
def expensive_operation():
    return jsonify({'result': 'computed'})

# More strict limit for authentication
@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Prevent brute force attacks
    # ...
    return jsonify({'token': 'xyz123'})

# Error handler
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded. Try again later.'}), 429
```

### Manual Rate Limiting

```python
from flask import Flask, request, jsonify
from collections import defaultdict
from datetime import datetime, timedelta

app = Flask(__name__)

# Track requests by IP
request_counts = defaultdict(list)

def check_rate_limit(ip_address, limit=10, window=60):
    """
    Returns True if rate limit is exceeded
    limit: max requests
    window: time window in seconds
    """
    now = datetime.now()
    cutoff = now - timedelta(seconds=window)
    
    # Remove old requests
    request_counts[ip_address] = [
        req_time for req_time in request_counts[ip_address]
        if req_time > cutoff
    ]
    
    # Check if limit exceeded
    if len(request_counts[ip_address]) >= limit:
        return True
    
    # Record this request
    request_counts[ip_address].append(now)
    return False

@app.route('/api/data')
def get_data():
    ip = request.remote_addr
    
    if check_rate_limit(ip, limit=10, window=60):
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    return jsonify({'data': 'some data'})
```

## CORS (Cross-Origin Resource Sharing) 🌐

Control which websites can access your API.

### The Same-Origin Policy Problem

```
Browser at https://example.com tries to access https://api.yoursite.com
→ Blocked by default (different origin)!
```

### Configuring CORS

```python
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Option 1: Allow all origins (NOT recommended for production!)
CORS(app)

# Option 2: Allow specific origins (RECOMMENDED)
CORS(app, origins=[
    "https://example.com",
    "https://www.example.com"
])

# Option 3: Configure per-route
from flask_cors import cross_origin

@app.route('/public-api')
@cross_origin()  # Allow any origin for this route
def public_api():
    return jsonify({'data': 'public'})

@app.route('/private-api')
@cross_origin(origins=['https://example.com'])  # Specific origin only
def private_api():
    return jsonify({'data': 'private'})
```

### Manual CORS Headers

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    # Only allow specific origin
    origin = request.headers.get('Origin')
    if origin in ['https://example.com', 'https://www.example.com']:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response
```

## SQL Injection Prevention 💉

**SQL Injection**: Malicious SQL code inserted through user input.

### Vulnerable Code (DON'T DO THIS!)

```python
import sqlite3

# VULNERABLE TO SQL INJECTION!
@app.route('/users/<username>')
def get_user(username):
    conn = sqlite3.connect('app.db')
    # Danger: Direct string interpolation
    query = f"SELECT * FROM users WHERE username = '{username}'"
    user = conn.execute(query).fetchone()
    return jsonify(user)

# Attack: /users/admin' OR '1'='1
# Resulting query: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
# Returns all users!
```

### Safe Code (Use Parameterized Queries)

```python
import sqlite3

# SAFE: Using parameterized queries
@app.route('/users/<username>')
def get_user(username):
    conn = sqlite3.connect('app.db')
    # Safe: Use placeholders (?)
    query = "SELECT * FROM users WHERE username = ?"
    user = conn.execute(query, (username,)).fetchone()
    return jsonify(user)

# Attack is harmless - treated as literal string
# Query looks for username literally containing "admin' OR '1'='1"
```

### Using ORMs (Object-Relational Mappers)

ORMs like SQLAlchemy automatically prevent SQL injection:

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

@app.route('/users/<username>')
def get_user(username):
    # Safe: SQLAlchemy uses parameterized queries
    user = User.query.filter_by(username=username).first()
    return jsonify({'username': user.username})
```

## XSS (Cross-Site Scripting) Prevention 🚫

**XSS**: Injecting malicious JavaScript into pages viewed by other users.

### Vulnerable Code

```python
from flask import Flask, request

# VULNERABLE!
@app.route('/comment', methods=['POST'])
def post_comment():
    comment = request.json['text']
    # Storing unsanitized user input
    save_to_db(comment)
    
    # Later, when displaying:
    # <div>{comment}</div>  ← JavaScript can execute!
    return jsonify({'message': 'Posted'})

# Attack: <script>alert('XSS!')</script>
```

### Safe Code

```python
from flask import Flask, request, escape
import bleach

# SAFE: Escape HTML
@app.route('/comment', methods=['POST'])
def post_comment():
    comment = request.json['text']
    
    # Option 1: Escape HTML (converts < to &lt;, etc.)
    safe_comment = escape(comment)
    
    # Option 2: Strip HTML tags entirely
    safe_comment = bleach.clean(comment, tags=[], strip=True)
    
    # Option 3: Allow only specific safe tags
    safe_comment = bleach.clean(
        comment,
        tags=['b', 'i', 'u', 'a'],
        attributes={'a': ['href']},
        strip=True
    )
    
    save_to_db(safe_comment)
    return jsonify({'message': 'Posted'})
```

### Content Security Policy

Add header to prevent inline scripts:

```python
@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'"
    return response
```

## Security Best Practices Checklist ✅

### 1. Authentication & Authorization
- [ ] Use strong password hashing (bcrypt, argon2)
- [ ] Implement proper authentication (JWT, sessions)
- [ ] Verify user permissions before actions
- [ ] Use secure session management

### 2. Data Protection
- [ ] Always use HTTPS in production
- [ ] Encrypt sensitive data at rest
- [ ] Don't log sensitive information
- [ ] Use environment variables for secrets

### 3. Input Validation
- [ ] Validate all user input
- [ ] Use parameterized queries (prevent SQL injection)
- [ ] Sanitize output (prevent XSS)
- [ ] Set appropriate data type constraints

### 4. Rate Limiting & DoS Protection
- [ ] Implement rate limiting
- [ ] Set request size limits
- [ ] Use timeout for long operations

### 5. CORS Configuration
- [ ] Configure CORS properly
- [ ] Only allow trusted origins
- [ ] Don't use wildcard (*) in production

### 6. Error Handling
- [ ] Don't expose stack traces to users
- [ ] Log errors securely
- [ ] Return generic error messages to clients

### 7. Dependencies
- [ ] Keep dependencies updated
- [ ] Regularly scan for vulnerabilities
- [ ] Use minimal necessary dependencies

### 8. HTTP Headers
- [ ] Set security headers (CSP, X-Frame-Options, etc.)
- [ ] Remove server version headers
- [ ] Implement HSTS for HTTPS

## Security Headers Example

```python
from flask import Flask

app = Flask(__name__)

@app.after_request
def set_security_headers(response):
    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'DENY'
    
    # Prevent MIME sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Enable XSS protection
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Content Security Policy
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    
    # Force HTTPS
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    return response
```

## Summary and Key Takeaways

✅ **Never trust user input** - always validate and sanitize  
✅ **Use parameterized queries** to prevent SQL injection  
✅ **Escape output** to prevent XSS attacks  
✅ **Implement rate limiting** to prevent abuse  
✅ **Configure CORS properly** - don't allow all origins  
✅ **Use HTTPS** always in production  
✅ **Keep dependencies updated** and scan for vulnerabilities  
✅ **Set security headers** to protect against common attacks

## What's Next?

You've mastered API security basics! Continue to **WebSockets** to learn about real-time communication.

---

[← Back: Databases for APIs](../08-Databases-for-APIs/) | [Next: WebSockets →](../10-WebSockets/)

## Practice

Complete the exercises in [exercises.md](./exercises.md) to secure your APIs!
