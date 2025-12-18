# 🏋️ Exercises: Network Security Basics

Practice securing your network applications!

## Exercise 1: HTTPS Setup Practice 🔐

**Objective**: Understand HTTPS and SSL/TLS certificates.

**Tasks**:
1. Generate a self-signed SSL certificate
2. Run the provided HTTPS server example
3. Access it via browser and observe the warning
4. Compare HTTP vs HTTPS traffic using browser DevTools
5. Research Let's Encrypt for production certificates

<details>
<summary>💡 Hint</summary>

```bash
# Generate self-signed certificate (development only!)
openssl req -x509 -newkey rsa:4096 -nodes \
  -out cert.pem -keyout key.pem -days 365

# Fill in the prompts (can use dummy data for testing)
# Country, State, Organization, Common Name (use localhost), etc.
```

```python
# HTTPS Server (https_server.py)
from flask import Flask
import ssl

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Secure Server! 🔒</h1>'

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(ssl_context=context, port=5000)
```

```bash
# Run the server
python https_server.py

# Access in browser
# https://localhost:5000
# You'll see a security warning (expected for self-signed certs)
```

**Browser DevTools comparison:**
1. Open DevTools (F12) → Network tab
2. Visit http://example.com (if available)
3. Visit https://example.com
4. Compare the Security tab for each

**Let's Encrypt (production):**
- Free SSL certificates
- Automatically renewable
- Trusted by all browsers
- Use `certbot` tool for easy setup
</details>

**Success Criteria**: You can set up HTTPS and understand why it's important.

---

## Exercise 2: JWT Authentication Implementation 🎫

**Objective**: Implement token-based authentication.

**Tasks**:
1. Install PyJWT: `pip install pyjwt`
2. Create a login endpoint that returns a JWT token
3. Create a protected endpoint that requires valid token
4. Test with expired tokens
5. Test with invalid tokens

<details>
<summary>💡 Hint</summary>

```python
# Install: pip install pyjwt flask
import jwt
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
SECRET_KEY = 'your-secret-key-change-in-production'

# Simple user database
users = {
    'alice': 'password123',
    'bob': 'secret456'
}

def create_token(username):
    """Create JWT token."""
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def token_required(f):
    """Decorator to protect routes."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        if token.startswith('Bearer '):
            token = token.split(' ')[1]
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.current_user = payload['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

@app.route('/login', methods=['POST'])
def login():
    """Login endpoint."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users and users[username] == password:
        token = create_token(username)
        return jsonify({'token': token}), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/protected')
@token_required
def protected():
    """Protected endpoint."""
    return jsonify({
        'message': f'Hello {request.current_user}!',
        'secret_data': 'This is confidential information'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

```bash
# Test the API
# 1. Login
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password123"}'

# Copy the token from response

# 2. Access protected endpoint with token
curl http://localhost:5000/protected \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 3. Try without token (should fail)
curl http://localhost:5000/protected

# 4. Try with invalid token (should fail)
curl http://localhost:5000/protected \
  -H "Authorization: Bearer invalid-token"
```
</details>

**Success Criteria**: You can implement and test JWT authentication.

---

## Exercise 3: SQL Injection Prevention 🛡️

**Objective**: Learn to prevent SQL injection attacks.

**Tasks**:
1. Create a vulnerable endpoint with SQL injection
2. Demonstrate the vulnerability
3. Fix it using parameterized queries
4. Test both versions
5. Document the security difference

<details>
<summary>💡 Hint</summary>

```python
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Setup database
def init_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, email TEXT)''')
    c.execute("DELETE FROM users")  # Clear for testing
    c.execute("INSERT INTO users VALUES (1, 'alice', 'alice@example.com')")
    c.execute("INSERT INTO users VALUES (2, 'bob', 'bob@example.com')")
    conn.commit()
    conn.close()

init_db()

# ❌ VULNERABLE VERSION
@app.route('/vulnerable/user')
def vulnerable_user():
    username = request.args.get('username', '')
    
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    # DANGEROUS: String interpolation in SQL
    query = f"SELECT * FROM users WHERE username = '{username}'"
    print(f"Query: {query}")
    
    try:
        c.execute(query)
        result = c.fetchall()
        conn.close()
        return jsonify({'users': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ SAFE VERSION
@app.route('/safe/user')
def safe_user():
    username = request.args.get('username', '')
    
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    # SAFE: Parameterized query
    query = "SELECT * FROM users WHERE username = ?"
    c.execute(query, (username,))
    
    result = c.fetchall()
    conn.close()
    return jsonify({'users': result})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

```bash
# Test normal usage
curl "http://localhost:5000/vulnerable/user?username=alice"
curl "http://localhost:5000/safe/user?username=alice"

# SQL Injection attack on vulnerable endpoint
curl "http://localhost:5000/vulnerable/user?username=alice'%20OR%20'1'='1"
# This returns ALL users! 🚨

# Same attack on safe endpoint (fails safely)
curl "http://localhost:5000/safe/user?username=alice'%20OR%20'1'='1"
# This returns nothing (treats the whole string as username)

# More dangerous attacks possible:
# - Delete data: username='; DROP TABLE users; --
# - Modify data: username='; UPDATE users SET password='hacked'; --
# - Steal data: username=' UNION SELECT password FROM users; --
```

**Key lesson:** Never use string formatting/concatenation for SQL queries!
</details>

**Success Criteria**: You can identify and fix SQL injection vulnerabilities.

---

## Exercise 4: XSS Prevention Practice 🎭

**Objective**: Prevent Cross-Site Scripting attacks.

**Tasks**:
1. Create a simple guestbook app
2. Demonstrate XSS vulnerability
3. Fix by escaping HTML
4. Test with malicious scripts
5. Understand Content Security Policy (CSP)

<details>
<summary>💡 Hint</summary>

```python
from flask import Flask, request, render_template_string, escape

app = Flask(__name__)

messages = []

# ❌ VULNERABLE VERSION
VULNERABLE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Guestbook</title></head>
<body>
    <h1>Guestbook (Vulnerable)</h1>
    <form method="POST">
        <input type="text" name="message" placeholder="Your message">
        <button type="submit">Post</button>
    </form>
    <h2>Messages:</h2>
    {% for msg in messages %}
        <div>{{ msg|safe }}</div>
    {% endfor %}
</body>
</html>
'''

# ✅ SAFE VERSION
SAFE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Guestbook</title></head>
<body>
    <h1>Guestbook (Safe)</h1>
    <form method="POST">
        <input type="text" name="message" placeholder="Your message">
        <button type="submit">Post</button>
    </form>
    <h2>Messages:</h2>
    {% for msg in messages %}
        <div>{{ msg }}</div>
    {% endfor %}
</body>
</html>
'''

@app.route('/vulnerable', methods=['GET', 'POST'])
def vulnerable():
    if request.method == 'POST':
        msg = request.form.get('message', '')
        messages.append(msg)  # No escaping!
    return render_template_string(VULNERABLE_TEMPLATE, messages=messages)

@app.route('/safe', methods=['GET', 'POST'])
def safe():
    if request.method == 'POST':
        msg = request.form.get('message', '')
        messages.append(msg)  # Jinja2 auto-escapes by default
    return render_template_string(SAFE_TEMPLATE, messages=messages)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

```bash
# Test with normal message
# Visit: http://localhost:5000/vulnerable
# Post: "Hello, World!"

# Test with XSS attack
# Visit: http://localhost:5000/vulnerable
# Post: <script>alert('XSS Attack!')</script>
# The script will execute! 🚨

# Test safe version
# Visit: http://localhost:5000/safe
# Post: <script>alert('XSS Attack!')</script>
# The script is displayed as text, not executed ✅
```

**Content Security Policy (CSP):**
```python
@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = \
        "default-src 'self'; script-src 'self'"
    return response
```

**Common XSS vectors to test:**
- `<script>alert('XSS')</script>`
- `<img src=x onerror="alert('XSS')">`
- `<svg onload="alert('XSS')">`
- `<body onload="alert('XSS')">`
</details>

**Success Criteria**: You can prevent XSS attacks through proper output escaping.

---

## Exercise 5: CORS Configuration 🌐

**Objective**: Properly configure Cross-Origin Resource Sharing.

**Tasks**:
1. Create an API without CORS (observe browser blocking)
2. Add CORS headers
3. Test from a different origin
4. Configure CORS for specific origins only
5. Understand preflight requests

<details>
<summary>💡 Hint</summary>

```python
# Install: pip install flask-cors
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Without CORS - browsers will block requests from different origins
@app.route('/api/no-cors')
def no_cors():
    return jsonify({'message': 'This will be blocked by browser'})

# With CORS - allows all origins (development only!)
app_with_cors = Flask(__name__)
CORS(app_with_cors)

@app_with_cors.route('/api/with-cors')
def with_cors():
    return jsonify({'message': 'This works from any origin'})

# With CORS - specific origins (production)
app_specific = Flask(__name__)
CORS(app_specific, origins=['https://myapp.com', 'https://app.example.com'])

@app_specific.route('/api/specific-cors')
def specific_cors():
    return jsonify({'message': 'Only works from allowed origins'})

# Manual CORS headers
@app.route('/api/manual-cors')
def manual_cors():
    response = jsonify({'message': 'Manual CORS'})
    response.headers['Access-Control-Allow-Origin'] = 'https://myapp.com'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

```html
<!-- Test CORS from a different origin -->
<!-- Save as test-cors.html and open in browser -->
<!DOCTYPE html>
<html>
<head><title>CORS Test</title></head>
<body>
    <h1>CORS Test</h1>
    <button onclick="testNoCors()">Test No CORS</button>
    <button onclick="testWithCors()">Test With CORS</button>
    <div id="result"></div>

    <script>
        function testNoCors() {
            fetch('http://localhost:5000/api/no-cors')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('result').innerText = 
                        'Success: ' + JSON.stringify(data);
                })
                .catch(err => {
                    document.getElementById('result').innerText = 
                        'Error: ' + err.message;
                });
        }

        function testWithCors() {
            fetch('http://localhost:5000/api/with-cors')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('result').innerText = 
                        'Success: ' + JSON.stringify(data);
                })
                .catch(err => {
                    document.getElementById('result').innerText = 
                        'Error: ' + err.message;
                });
        }
    </script>
</body>
</html>
```

**Preflight Request:**
Browsers send OPTIONS request before actual request for:
- Custom headers
- Methods other than GET/POST
- Content-Type other than application/x-www-form-urlencoded

```python
@app.route('/api/data', methods=['OPTIONS', 'POST'])
def handle_preflight():
    if request.method == 'OPTIONS':
        # Preflight request
        response = jsonify({'status': 'ok'})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    else:
        # Actual request
        return jsonify({'data': 'received'})
```
</details>

**Success Criteria**: You understand CORS and can configure it properly.

---

## Exercise 6: Password Security 🔑

**Objective**: Implement secure password handling.

**Tasks**:
1. Hash passwords using bcrypt or werkzeug
2. Create user registration endpoint
3. Create login endpoint with password verification
4. Test password strength requirements
5. Implement password reset flow (design only)

<details>
<summary>💡 Hint</summary>

```python
# Install: pip install werkzeug
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)

# Simple in-memory user store
users_db = {}

def is_strong_password(password):
    """Check password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain number"
    return True, "Password is strong"

@app.route('/register', methods=['POST'])
def register():
    """User registration."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    if username in users_db:
        return jsonify({'error': 'Username already exists'}), 400
    
    # Check password strength
    is_strong, message = is_strong_password(password)
    if not is_strong:
        return jsonify({'error': message}), 400
    
    # Hash password (NEVER store plain text!)
    password_hash = generate_password_hash(password)
    
    users_db[username] = {
        'password_hash': password_hash,
        'email': data.get('email', '')
    }
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    """User login."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    user = users_db.get(username)
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Verify password
    if not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return jsonify({'message': 'Login successful'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

```bash
# Test registration
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"Weak123"}'

# Test with strong password
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"StrongPass123!","email":"alice@example.com"}'

# Test login
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"StrongPass123!"}'

# Test wrong password
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"wrongpassword"}'
```

**Password Best Practices:**
- Minimum 8 characters (12+ is better)
- Require uppercase, lowercase, numbers, special characters
- Never store plain text passwords
- Use bcrypt, scrypt, or Argon2 for hashing
- Implement rate limiting on login attempts
- Use multi-factor authentication (MFA) when possible
</details>

**Success Criteria**: You can securely store and verify passwords.

---

## Exercise 7: Rate Limiting 🚦

**Objective**: Prevent API abuse with rate limiting.

**Tasks**:
1. Install and configure Flask-Limiter
2. Add rate limits to API endpoints
3. Test exceeding the rate limit
4. Implement different limits for different endpoints
5. Understand the response when limit is exceeded

<details>
<summary>💡 Hint</summary>

```python
# Install: pip install flask-limiter
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Initialize limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,  # Track by IP address
    default_limits=["100 per hour"]  # Default limit for all routes
)

@app.route('/api/public')
@limiter.limit("10 per minute")  # Specific limit for this route
def public_api():
    return jsonify({'message': 'Public API - 10 requests per minute'})

@app.route('/api/search')
@limiter.limit("5 per minute")
def search_api():
    return jsonify({'message': 'Search API - 5 requests per minute'})

@app.route('/api/unlimited')
@limiter.exempt  # No rate limit
def unlimited_api():
    return jsonify({'message': 'No rate limit on this endpoint'})

# Custom error handler for rate limit exceeded
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': str(e.description)
    }), 429

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

```bash
# Test rate limiting
# Run this script multiple times quickly

for i in {1..15}; do
    echo "Request $i:"
    curl http://localhost:5000/api/public
    echo ""
done

# You should see 429 errors after 10 requests

# Test different endpoint
for i in {1..10}; do
    echo "Request $i:"
    curl http://localhost:5000/api/search
    echo ""
done
```

**Advanced Rate Limiting:**
```python
# Different limits for authenticated vs anonymous users
def get_user_key():
    """Get rate limit key based on authentication."""
    token = request.headers.get('Authorization')
    if token:
        # Authenticated user - more generous limit
        return f"user:{token}"
    else:
        # Anonymous user - strict limit
        return f"anon:{get_remote_address()}"

limiter = Limiter(
    app=app,
    key_func=get_user_key,
    default_limits=["100 per hour"]
)

@app.route('/api/data')
@limiter.limit("100 per minute", key_func=lambda: "auth" if request.headers.get('Authorization') else "anon")
def data_api():
    return jsonify({'data': 'value'})
```

**Why Rate Limiting?**
- Prevent DoS attacks
- Protect against brute force
- Ensure fair resource usage
- Manage API costs
</details>

**Success Criteria**: You can implement rate limiting to protect your API.

---

## Exercise 8: Security Headers 🛡️

**Objective**: Add security headers to protect against attacks.

**Tasks**:
1. Add common security headers to responses
2. Test headers using browser DevTools
3. Understand what each header does
4. Use online security scanner (securityheaders.com)
5. Achieve an "A" security rating

<details>
<summary>💡 Hint</summary>

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Secure Application</h1>'

@app.after_request
def set_security_headers(response):
    """Add security headers to all responses."""
    
    # Prevent MIME type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'DENY'
    
    # Enable XSS protection
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Enforce HTTPS
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Content Security Policy
    response.headers['Content-Security-Policy'] = \
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
    
    # Referrer Policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Permissions Policy (formerly Feature Policy)
    response.headers['Permissions-Policy'] = \
        'geolocation=(), microphone=(), camera=()'
    
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Security Headers Explained:**

1. **X-Content-Type-Options: nosniff**
   - Prevents browsers from MIME-sniffing
   - Forces browser to respect Content-Type

2. **X-Frame-Options: DENY**
   - Prevents page from being embedded in iframe
   - Protects against clickjacking

3. **X-XSS-Protection: 1; mode=block**
   - Enables browser's XSS filter
   - Blocks page if XSS detected

4. **Strict-Transport-Security (HSTS)**
   - Forces HTTPS connections
   - Prevents SSL stripping attacks

5. **Content-Security-Policy (CSP)**
   - Controls resource loading
   - Mitigates XSS and injection attacks

6. **Referrer-Policy**
   - Controls referrer information sent
   - Protects user privacy

**Testing:**
```bash
# Check headers with curl
curl -I http://localhost:5000/

# Or use online scanner
# 1. Deploy your app publicly (or use ngrok for local testing)
# 2. Visit https://securityheaders.com
# 3. Enter your URL
# 4. Review security score and recommendations
```
</details>

**Success Criteria**: You understand and implement critical security headers.

---

## Exercise 9: Input Validation 📋

**Objective**: Properly validate and sanitize user input.

**Tasks**:
1. Create API endpoints with input validation
2. Use marshmallow or similar library
3. Validate email, URLs, numbers, dates
4. Test with invalid inputs
5. Return clear error messages

<details>
<summary>💡 Hint</summary>

```python
# Install: pip install marshmallow
from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError, validate

app = Flask(__name__)

class UserSchema(Schema):
    """User input validation schema."""
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50)
    )
    email = fields.Email(required=True)
    age = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=150)
    )
    website = fields.Url(required=False)
    role = fields.Str(
        required=False,
        validate=validate.OneOf(['user', 'admin', 'moderator'])
    )

class PostSchema(Schema):
    """Blog post validation schema."""
    title = fields.Str(
        required=True,
        validate=validate.Length(min=5, max=200)
    )
    content = fields.Str(
        required=True,
        validate=validate.Length(min=10)
    )
    tags = fields.List(
        fields.Str(),
        validate=validate.Length(max=5)
    )
    published = fields.Boolean(required=False)

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create user with validation."""
    try:
        # Validate input
        schema = UserSchema()
        data = schema.load(request.json)
        
        # Input is valid, create user
        return jsonify({
            'message': 'User created',
            'user': data
        }), 201
    
    except ValidationError as err:
        # Return validation errors
        return jsonify({
            'error': 'Validation failed',
            'details': err.messages
        }), 400

@app.route('/api/posts', methods=['POST'])
def create_post():
    """Create post with validation."""
    try:
        schema = PostSchema()
        data = schema.load(request.json)
        
        return jsonify({
            'message': 'Post created',
            'post': data
        }), 201
    
    except ValidationError as err:
        return jsonify({
            'error': 'Validation failed',
            'details': err.messages
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

```bash
# Test valid input
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "age": 25,
    "website": "https://example.com",
    "role": "user"
  }'

# Test invalid email
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "bob",
    "email": "not-an-email",
    "age": 30
  }'

# Test age out of range
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "charlie",
    "email": "charlie@example.com",
    "age": 200
  }'

# Test missing required field
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "dave"
  }'

# Test post creation
curl -X POST http://localhost:5000/api/posts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my post.",
    "tags": ["python", "flask", "api"],
    "published": true
  }'
```

**Validation Best Practices:**
- Always validate on the server (never trust client)
- Validate type, length, format, range
- Provide clear error messages
- Fail securely (reject invalid input)
- Sanitize before storage/display
</details>

**Success Criteria**: You can properly validate all user input.

---

## Exercise 10: Secure API Design Challenge 🏗️

**Objective**: Design and implement a secure API from scratch.

**Tasks**:
1. Design a secure TODO API with authentication
2. Implement JWT-based auth
3. Add input validation
4. Implement rate limiting
5. Add security headers
6. Test all security measures

<details>
<summary>💡 Hint</summary>

```python
# Secure TODO API with all security measures
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import Schema, fields, ValidationError, validate
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-in-production'

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

# In-memory storage (use database in production)
users = {}
todos = {}

# Schemas
class UserRegistrationSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=8))
    email = fields.Email(required=True)

class TodoSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(validate=validate.Length(max=1000))
    completed = fields.Boolean()

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Token required'}), 401
        
        try:
            token = token.split(' ')[1]
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.current_user = payload['username']
        except:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated

# Security headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# Routes
@app.route('/api/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    try:
        schema = UserRegistrationSchema()
        data = schema.load(request.json)
        
        if data['username'] in users:
            return jsonify({'error': 'Username exists'}), 400
        
        users[data['username']] = {
            'password_hash': generate_password_hash(data['password']),
            'email': data['email']
        }
        
        return jsonify({'message': 'User registered'}), 201
    
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

@app.route('/api/login', methods=['POST'])
@limiter.limit("10 per hour")
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = users.get(username)
    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, app.config['SECRET_KEY'])
    
    return jsonify({'token': token})

@app.route('/api/todos', methods=['GET'])
@token_required
@limiter.limit("60 per minute")
def get_todos():
    user_todos = [t for t in todos.values() if t['owner'] == request.current_user]
    return jsonify({'todos': user_todos})

@app.route('/api/todos', methods=['POST'])
@token_required
@limiter.limit("30 per minute")
def create_todo():
    try:
        schema = TodoSchema()
        data = schema.load(request.json)
        
        todo_id = len(todos) + 1
        todo = {
            'id': todo_id,
            'owner': request.current_user,
            'title': data['title'],
            'description': data.get('description', ''),
            'completed': data.get('completed', False),
            'created_at': datetime.utcnow().isoformat()
        }
        
        todos[todo_id] = todo
        return jsonify(todo), 201
    
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

@app.route('/api/todos/<int:todo_id>', methods=['GET'])
@token_required
def get_todo(todo_id):
    todo = todos.get(todo_id)
    
    if not todo:
        return jsonify({'error': 'Not found'}), 404
    
    if todo['owner'] != request.current_user:
        return jsonify({'error': 'Forbidden'}), 403
    
    return jsonify(todo)

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
@token_required
def delete_todo(todo_id):
    todo = todos.get(todo_id)
    
    if not todo:
        return jsonify({'error': 'Not found'}), 404
    
    if todo['owner'] != request.current_user:
        return jsonify({'error': 'Forbidden'}), 403
    
    del todos[todo_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Test the secure API:**
```bash
# 1. Register
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"SecurePass123","email":"alice@example.com"}'

# 2. Login
TOKEN=$(curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"SecurePass123"}' | jq -r '.token')

# 3. Create TODO
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Learn security","description":"Complete all exercises"}'

# 4. Get TODOs
curl http://localhost:5000/api/todos \
  -H "Authorization: Bearer $TOKEN"
```
</details>

**Success Criteria**: You've built a fully secured API with multiple layers of protection.

---

## Mini-Quiz ✅

1. **What does HTTPS provide?**
   - [ ] Faster loading times
   - [ ] Encryption and authentication
   - [ ] Better SEO only
   - [ ] Colorful padlock icon

2. **What is JWT?**
   - [ ] Just Web Token
   - [ ] JSON Web Token
   - [ ] Java Web Technology
   - [ ] JavaScript Web Tool

3. **How should passwords be stored?**
   - [ ] Plain text
   - [ ] Encrypted
   - [ ] Hashed
   - [ ] Base64 encoded

4. **What is SQL injection?**
   - [ ] A database backup method
   - [ ] Malicious code executed via SQL queries
   - [ ] A performance optimization
   - [ ] A type of medication

5. **What does XSS stand for?**
   - [ ] XML Security Standard
   - [ ] Cross-Site Scripting
   - [ ] Extra Secure System
   - [ ] X-tra Special Security

6. **What is CORS?**
   - [ ] Common Origin Resource Security
   - [ ] Cross-Origin Resource Sharing
   - [ ] Certified Origin Routing System
   - [ ] Core Origin Request Standard

7. **What HTTP status code indicates rate limit exceeded?**
   - [ ] 401
   - [ ] 403
   - [ ] 429
   - [ ] 503

8. **What does HSTS stand for?**
   - [ ] HTTP Secure Transfer System
   - [ ] Hyper Secure Transport Service
   - [ ] HTTP Strict Transport Security
   - [ ] High Security Transfer Standard

<details>
<summary>Show Answers</summary>

1. **B** - Encryption and authentication (HTTPS encrypts data and verifies server identity)
2. **B** - JSON Web Token (compact, URL-safe token format)
3. **C** - Hashed (using bcrypt, scrypt, or Argon2)
4. **B** - Malicious code executed via SQL queries (never concatenate user input in SQL)
5. **B** - Cross-Site Scripting (injecting malicious scripts)
6. **B** - Cross-Origin Resource Sharing (allows/blocks requests from different domains)
7. **C** - 429 Too Many Requests
8. **C** - HTTP Strict Transport Security (forces HTTPS connections)

**Scoring:**
- 8/8: Security expert! 🌟
- 6-7/8: Great knowledge! 👍
- 4-5/8: Good start, review concepts
- 0-3/8: Review the lesson and practice more
</details>

---

## Security Checklist Review ✅

Before deploying any application, verify:
- [ ] HTTPS enabled (with valid certificate)
- [ ] Passwords hashed (never plain text)
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output escaping)
- [ ] CSRF protection for state-changing operations
- [ ] CORS configured properly
- [ ] Rate limiting implemented
- [ ] Security headers set
- [ ] Authentication required for protected resources
- [ ] Authorization checked (users can only access their data)
- [ ] Secrets in environment variables (not hardcoded)
- [ ] Dependencies updated regularly
- [ ] Error messages don't leak sensitive info
- [ ] Logs don't contain passwords or tokens

---

## Solutions

Complete solutions can be found in [solutions/06-security-basics-solutions.md](../solutions/06-security-basics-solutions.md)

---

[← Back to Lesson](./README.md) | [Next: Projects →](../Projects/)
