# 🔒 Network Security Basics

Learn how to keep your networked applications secure!

## 🎯 Learning Objectives

By the end of this module, you will:
- Understand HTTPS and TLS/SSL encryption
- Learn about authentication and authorization
- Understand common web vulnerabilities
- Know how to implement basic security measures
- Learn about CORS and why it matters
- Understand API security best practices

## Why Security Matters

**Without security:**
- Passwords sent in plain text (anyone can read them)
- Data can be modified in transit
- Impersonation is easy
- Privacy is compromised

**With security:**
- Data is encrypted (unreadable by eavesdroppers)
- Integrity is verified (tampering is detected)
- Identity is confirmed (authentication)
- Access is controlled (authorization)

## HTTPS: Secure HTTP 🔐

### HTTP vs HTTPS

**HTTP (Port 80):**
```
Browser → [Plain text: "password123"] → Server
         Anyone can read this! ❌
```

**HTTPS (Port 443):**
```
Browser → [Encrypted: "x7$k2@mP..."] → Server
         Unreadable to eavesdroppers! ✅
```

### How HTTPS Works (TLS/SSL)

**1. Handshake**
```
Client: "Hello, let's talk securely"
Server: "Here's my certificate and public key"
Client: [Verifies certificate] "OK, here's a session key (encrypted)"
Server: "Got it, let's start encrypted communication"
```

**2. Encrypted Communication**
- All data encrypted with session key
- Fast symmetric encryption
- Both sides can encrypt/decrypt

**3. Certificate Verification**
- Certificate issued by trusted authority (CA)
- Verifies server identity
- Browser shows padlock icon 🔒

### Always Use HTTPS When:
- Handling passwords
- Processing payments
- Transmitting personal data
- Any production application

### Setting Up HTTPS (Python Example)

```python
from flask import Flask
import ssl

app = Flask(__name__)

# Generate certificate (development only!)
# openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(ssl_context=context, port=443)
```

**Production**: Use Let's Encrypt for free SSL certificates!

## Authentication: Who Are You? 🆔

Authentication verifies identity. Common methods:

### 1. API Keys

**Simple but limited security**

```python
# Server side
API_KEYS = {'abc123': 'user1', 'xyz789': 'user2'}

@app.route('/api/data')
def get_data():
    api_key = request.headers.get('X-API-Key')
    if api_key not in API_KEYS:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify({'data': 'secret info'})
```

```bash
# Client usage
curl -H "X-API-Key: abc123" https://api.example.com/data
```

**Pros**: Simple  
**Cons**: If leaked, anyone can use it

### 2. Bearer Tokens (JWT)

**More secure, includes expiration**

```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = 'your-secret-key'

def create_token(user_id):
    """Create a JWT token."""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
```

```python
# Protected endpoint
@app.route('/api/protected')
def protected():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized'}), 401
    
    token = auth_header.split(' ')[1]
    user_id = verify_token(token)
    
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    
    return jsonify({'message': f'Hello user {user_id}'})
```

### 3. OAuth 2.0

**Industry standard for authorization**

Used by Google, Facebook, GitHub for "Sign in with..." buttons.

**Flow:**
1. User clicks "Sign in with Google"
2. Redirected to Google login
3. User authorizes your app
4. Google returns authorization code
5. Your app exchanges code for access token
6. Use token to access user's data

## Authorization: What Can You Do? 🚦

Authorization controls access after authentication.

### Role-Based Access Control (RBAC)

```python
ROLES = {
    'alice': 'admin',
    'bob': 'user',
    'charlie': 'guest'
}

PERMISSIONS = {
    'admin': ['read', 'write', 'delete'],
    'user': ['read', 'write'],
    'guest': ['read']
}

def has_permission(user, action):
    """Check if user can perform action."""
    role = ROLES.get(user)
    if not role:
        return False
    return action in PERMISSIONS.get(role, [])

@app.route('/api/delete/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    user = get_current_user()  # From auth token
    
    if not has_permission(user, 'delete'):
        return jsonify({'error': 'Forbidden'}), 403
    
    # Proceed with deletion
    return jsonify({'message': 'Deleted'})
```

## Common Web Vulnerabilities

### 1. SQL Injection 💉

**Problem**: User input executed as SQL code

```python
# ❌ VULNERABLE
username = request.form['username']
query = f"SELECT * FROM users WHERE username = '{username}'"
# User enters: admin' OR '1'='1
# Executes: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
# Returns all users!
```

```python
# ✅ SAFE: Use parameterized queries
username = request.form['username']
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
```

### 2. Cross-Site Scripting (XSS) 🎭

**Problem**: Malicious scripts injected into web pages

```html
<!-- ❌ VULNERABLE -->
<div>Welcome, {{ username }}</div>
<!-- User sets username to: <script>alert('XSS')</script> -->
```

```html
<!-- ✅ SAFE: Escape HTML -->
<div>Welcome, {{ username|escape }}</div>
<!-- Output: Welcome, &lt;script&gt;alert('XSS')&lt;/script&gt; -->
```

### 3. Cross-Site Request Forgery (CSRF) 🎪

**Problem**: Attacker tricks user into making unwanted requests

**Protection**: Use CSRF tokens

```python
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret'
csrf = CSRFProtect(app)

# Forms now require CSRF token
# Token automatically validated
```

### 4. Insecure Direct Object References

**Problem**: Accessing other users' data

```python
# ❌ VULNERABLE
@app.route('/api/messages/<message_id>')
def get_message(message_id):
    message = db.get_message(message_id)
    return jsonify(message)
# Anyone can access any message!
```

```python
# ✅ SAFE: Verify ownership
@app.route('/api/messages/<message_id>')
def get_message(message_id):
    user = get_current_user()
    message = db.get_message(message_id)
    
    if message.owner_id != user.id:
        return jsonify({'error': 'Forbidden'}), 403
    
    return jsonify(message)
```

## CORS (Cross-Origin Resource Sharing) 🌐

### The Problem

Browsers block requests to different domains for security:

```javascript
// On https://myapp.com
fetch('https://api.otherapp.com/data')
// ❌ Blocked by browser!
```

### The Solution

Server explicitly allows specific origins:

```python
from flask_cors import CORS

app = Flask(__name__)

# Allow all origins (development only!)
CORS(app)

# Or be specific (production)
CORS(app, origins=['https://myapp.com'])
```

**Response headers:**
```http
Access-Control-Allow-Origin: https://myapp.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
```

## API Security Best Practices

### 1. Rate Limiting

Prevent abuse by limiting requests:

```python
from flask_limiter import Limiter

limiter = Limiter(app, default_limits=["100 per hour"])

@app.route('/api/data')
@limiter.limit("10 per minute")
def get_data():
    return jsonify({'data': 'value'})
```

### 2. Input Validation

Never trust user input:

```python
from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    email = fields.Email(required=True)
    age = fields.Integer(required=True, validate=lambda x: 0 < x < 150)

@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = UserSchema().load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    # Data is validated
    user = create_user_in_db(data)
    return jsonify(user), 201
```

### 3. Secure Password Storage

**Never store plain text passwords!**

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Store password
password_hash = generate_password_hash('user_password')
db.store_user(username, password_hash)

# Verify password
stored_hash = db.get_password_hash(username)
if check_password_hash(stored_hash, entered_password):
    # Password correct
    pass
```

### 4. Use Environment Variables for Secrets

```python
import os

# ❌ DON'T hardcode secrets
SECRET_KEY = 'my-secret-key-123'

# ✅ DO use environment variables
SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')
```

## Security Checklist ✅

Before deploying:
- [ ] Use HTTPS in production
- [ ] Implement authentication
- [ ] Validate all user input
- [ ] Use parameterized SQL queries
- [ ] Escape HTML output
- [ ] Implement CSRF protection
- [ ] Set up CORS properly
- [ ] Rate limit API endpoints
- [ ] Hash passwords (never store plain text)
- [ ] Use environment variables for secrets
- [ ] Implement proper error handling (don't leak info)
- [ ] Keep dependencies updated
- [ ] Use security headers

## Security Headers

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    return response
```

## Code Examples

Check the `examples/` folder for:
- `https_server.py` - HTTPS server setup
- `api_authentication.py` - JWT authentication example

## Summary and Key Takeaways

✅ **Always use HTTPS** to encrypt data in transit  
✅ **Authenticate users** with secure tokens (JWT)  
✅ **Authorize access** based on roles/permissions  
✅ **Validate all input** - never trust user data  
✅ **Escape output** to prevent XSS  
✅ **Use parameterized queries** to prevent SQL injection  
✅ **Rate limit APIs** to prevent abuse  
✅ **Hash passwords** - never store plain text  
✅ **Use CORS correctly** for cross-origin requests

## What's Next?

Put your knowledge to practice: [Projects](../Projects/)

---

[← Back: Other Protocols](../05-Other-Protocols/) | [Next: Projects →](../Projects/)

## Practice

Complete the [exercises](./exercises.md) to secure applications!
