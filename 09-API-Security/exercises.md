# 🏋️ Exercises: 09 API Security

Practice securing APIs by completing these hands-on exercises.

## Exercise 1: Input Validation 📝

Create a Flask endpoint that validates user registration data.

**Requirements:**
- Username: 3-20 characters, alphanumeric only
- Email: Valid email format
- Age: Integer between 13 and 120
- Password: Minimum 8 characters, must include uppercase, lowercase, and number

**Starter Code:**

```python
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    
    # TODO: Implement validation
    # 1. Check all required fields are present
    # 2. Validate username format and length
    # 3. Validate email format
    # 4. Validate age range
    # 5. Validate password strength
    
    return jsonify({'message': 'User registered successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
```

**Test Cases:**

```bash
# Valid request
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john123", "email": "john@example.com", "age": 25, "password": "SecurePass123"}'

# Invalid username (too short)
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "ab", "email": "john@example.com", "age": 25, "password": "SecurePass123"}'

# Invalid email
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john123", "email": "invalid-email", "age": 25, "password": "SecurePass123"}'
```

**Bonus:** Use Pydantic or Marshmallow for validation.

---

## Exercise 2: SQL Injection Prevention 💉

Fix the vulnerable code to prevent SQL injection attacks.

**Vulnerable Code:**

```python
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/products/<int:category_id>')
def get_products(category_id):
    search = request.args.get('search', '')
    
    conn = sqlite3.connect('shop.db')
    # VULNERABLE!
    query = f"SELECT * FROM products WHERE category_id = {category_id} AND name LIKE '%{search}%'"
    products = conn.execute(query).fetchall()
    conn.close()
    
    return jsonify({'products': products})
```

**Your Tasks:**

1. Fix the SQL injection vulnerability using parameterized queries
2. Test with malicious inputs to verify the fix
3. Add proper error handling

**Test Cases:**

```bash
# Normal query
curl "http://localhost:5000/products/1?search=phone"

# SQL injection attempt (should be blocked)
curl "http://localhost:5000/products/1?search=' OR '1'='1"

# Another injection attempt
curl "http://localhost:5000/products/1?search='; DROP TABLE products--"
```

---

## Exercise 3: XSS Prevention 🚫

Create a comment system that prevents XSS attacks.

**Requirements:**

1. Create a POST endpoint to submit comments
2. Create a GET endpoint to retrieve comments
3. Sanitize all user input
4. Escape output properly
5. Implement Content Security Policy

**Starter Code:**

```python
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/comments', methods=['POST'])
def post_comment():
    data = request.json
    comment = data.get('comment', '')
    author = data.get('author', '')
    
    # TODO: Sanitize input before storing
    # Save to database
    
    return jsonify({'message': 'Comment posted'})

@app.route('/comments', methods=['GET'])
def get_comments():
    # TODO: Retrieve and safely return comments
    # Make sure to escape HTML
    
    return jsonify({'comments': []})

# TODO: Add CSP headers

if __name__ == '__main__':
    app.run(debug=True)
```

**Test Cases:**

```bash
# Normal comment
curl -X POST http://localhost:5000/comments \
  -H "Content-Type: application/json" \
  -d '{"comment": "Great article!", "author": "John"}'

# XSS attempt (should be sanitized)
curl -X POST http://localhost:5000/comments \
  -H "Content-Type: application/json" \
  -d '{"comment": "<script>alert(\"XSS\")</script>", "author": "Hacker"}'

# IMG tag XSS
curl -X POST http://localhost:5000/comments \
  -H "Content-Type: application/json" \
  -d '{"comment": "<img src=x onerror=alert(1)>", "author": "Hacker"}'
```

---

## Exercise 4: Rate Limiting 🚦

Implement rate limiting on an API endpoint.

**Requirements:**

1. Limit requests to 10 per minute per IP address
2. Return 429 status code when exceeded
3. Include rate limit headers in response
4. Implement different limits for different endpoints

**Starter Code:**

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# TODO: Implement rate limiting
# Consider using Flask-Limiter or manual implementation

@app.route('/api/data')
def get_data():
    # TODO: Add rate limiting
    return jsonify({'data': 'some data'})

@app.route('/api/login', methods=['POST'])
def login():
    # TODO: Add stricter rate limiting (e.g., 5 per minute)
    return jsonify({'token': 'abc123'})

if __name__ == '__main__':
    app.run(debug=True)
```

**Test Cases:**

```bash
# Test normal usage
for i in {1..5}; do
  curl http://localhost:5000/api/data
  sleep 1
done

# Test rate limiting (should get 429)
for i in {1..15}; do
  curl -i http://localhost:5000/api/data
done
```

---

## Exercise 5: CORS Configuration 🌐

Configure CORS properly for a multi-domain application.

**Scenario:**

You have an API at `api.example.com` that should:
- Allow requests from `app.example.com` and `mobile.example.com`
- Block requests from all other origins
- Allow credentials (cookies)
- Support OPTIONS preflight requests

**Starter Code:**

```python
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# TODO: Configure CORS properly

@app.route('/api/user', methods=['GET', 'OPTIONS'])
def get_user():
    if request.method == 'OPTIONS':
        # TODO: Handle preflight request
        pass
    
    # TODO: Add CORS headers to response
    return jsonify({'user': 'John Doe'})

if __name__ == '__main__':
    app.run(debug=True)
```

**Test Cases:**

Test with different Origin headers:

```bash
# Allowed origin
curl -H "Origin: https://app.example.com" \
  http://localhost:5000/api/user

# Disallowed origin (should be blocked)
curl -H "Origin: https://evil.com" \
  http://localhost:5000/api/user

# Preflight request
curl -X OPTIONS \
  -H "Origin: https://app.example.com" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: Authorization" \
  http://localhost:5000/api/user
```

---

## Exercise 6: Security Headers 🛡️

Add comprehensive security headers to your API.

**Requirements:**

Add these headers to all responses:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `Content-Security-Policy: default-src 'self'`

**Starter Code:**

```python
from flask import Flask, jsonify

app = Flask(__name__)

# TODO: Add security headers to all responses

@app.route('/api/data')
def get_data():
    return jsonify({'data': 'some data'})

if __name__ == '__main__':
    app.run(debug=True)
```

**Verification:**

```bash
curl -I http://localhost:5000/api/data
# Check that all security headers are present
```

---

## Exercise 7: Secure Authentication 🔐

Implement JWT-based authentication with proper security.

**Requirements:**

1. Create a login endpoint that returns JWT token
2. Create a protected endpoint that requires valid JWT
3. Hash passwords using bcrypt
4. Set secure token expiration
5. Implement token refresh mechanism

**Starter Code:**

```python
from flask import Flask, request, jsonify
import jwt
import bcrypt
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Use environment variable in production!

# Fake user database
users = {
    'john': bcrypt.hashpw('password123'.encode(), bcrypt.gensalt())
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # TODO: Implement login logic
    # 1. Validate credentials
    # 2. Generate JWT token
    # 3. Return token with expiration
    
    pass

@app.route('/protected', methods=['GET'])
def protected():
    # TODO: Verify JWT token
    # 1. Extract token from Authorization header
    # 2. Verify token signature
    # 3. Check expiration
    # 4. Return protected data
    
    pass

if __name__ == '__main__':
    app.run(debug=True)
```

**Test Cases:**

```bash
# Login
TOKEN=$(curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "password123"}' | jq -r '.token')

# Access protected endpoint
curl http://localhost:5000/protected \
  -H "Authorization: Bearer $TOKEN"

# Try without token (should fail)
curl http://localhost:5000/protected
```

---

## Exercise 8: Vulnerable API Lab 🔬

Complete the security lab in the `security-labs` directory.

**Tasks:**

1. Run the vulnerable API: `python security-labs/vulnerable_api.py`
2. Find all security vulnerabilities
3. Exploit each vulnerability safely
4. Create a fixed version of the API
5. Test that all vulnerabilities are patched

**Vulnerabilities to Find:**
- SQL Injection
- XSS (Stored and Reflected)
- Missing Authentication
- Missing Authorization
- No Rate Limiting
- CORS Misconfiguration
- Information Disclosure

See [security-labs/README.md](../security-labs/README.md) for detailed instructions.

---

## Exercise 9: Security Testing 🧪

Create an automated security testing suite.

**Requirements:**

Write tests that check for:
1. SQL injection vulnerabilities
2. XSS vulnerabilities
3. Authentication bypass attempts
4. Authorization issues
5. Rate limiting enforcement
6. Security headers presence

**Starter Code:**

```python
import requests
import pytest

BASE_URL = 'http://localhost:5000'

def test_sql_injection_prevention():
    """Test that SQL injection is prevented"""
    # TODO: Try various SQL injection payloads
    # Verify they don't succeed
    pass

def test_xss_prevention():
    """Test that XSS is prevented"""
    # TODO: Try various XSS payloads
    # Verify they are escaped/sanitized
    pass

def test_authentication_required():
    """Test that protected endpoints require auth"""
    # TODO: Try accessing protected endpoints without token
    # Verify 401 response
    pass

def test_rate_limiting():
    """Test that rate limiting works"""
    # TODO: Send many requests quickly
    # Verify 429 response
    pass

def test_security_headers():
    """Test that security headers are present"""
    # TODO: Check for all required security headers
    pass
```

Run with: `pytest test_security.py -v`

---

## Exercise 10: Security Audit 📋

Perform a complete security audit of an existing API.

**Use OWASP ZAP or Burp Suite to:**

1. Scan for common vulnerabilities
2. Test for SQL injection
3. Test for XSS
4. Check authentication/authorization
5. Verify security headers
6. Test rate limiting
7. Check CORS configuration

**Create a Report Including:**
- Executive summary
- List of findings (critical, high, medium, low)
- Proof of concept for each vulnerability
- Remediation recommendations
- Retesting results after fixes

---

## Bonus Challenges 🌟

### Challenge 1: Password Security
Implement a password policy that:
- Requires minimum complexity
- Prevents common passwords
- Implements password history
- Enforces password expiration
- Detects and prevents credential stuffing

### Challenge 2: API Key Management
Create a system for:
- Generating secure API keys
- Rotating API keys
- Revoking compromised keys
- Rate limiting per API key
- Logging API key usage

### Challenge 3: Secure File Upload
Implement secure file upload that:
- Validates file types
- Scans for malware
- Limits file size
- Generates safe filenames
- Stores files securely

---

## Solutions

Solutions to selected exercises are available in the `solutions/` directory (if you're stuck).

Remember: Try to solve exercises yourself first before looking at solutions!

---

[← Back to Lesson](./README.md)
