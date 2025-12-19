# ⚠️ Common Mistakes - Security Basics

Learn from these common security pitfalls in network applications.

## Authentication & Authorization Mistakes

### 1. Storing Passwords in Plain Text

**Mistake:**
```python
users = {
    "alice": {"password": "password123"},  # NEVER do this!
    "bob": {"password": "secret"}
}
```

**Why it's catastrophic:**
- Database breach exposes all passwords
- Users often reuse passwords
- Legal liability
- Regulatory violations (GDPR, etc.)

**Correct:**
```python
from werkzeug.security import generate_password_hash, check_password_hash

users = {
    "alice": {
        "password_hash": generate_password_hash("password123")
    }
}

# Verify password
if check_password_hash(users["alice"]["password_hash"], entered_password):
    # Allow access
```

**Lesson:** NEVER store plain text passwords. Always use proper hashing (bcrypt, Argon2).

---

### 2. Using Weak Hashing Algorithms

**Mistake:**
```python
import hashlib
# Using MD5 or SHA1 for passwords
password_hash = hashlib.md5(password.encode()).hexdigest()  # Weak!
```

**Why it's wrong:**
- MD5 and SHA1 are broken
- Fast to brute force
- Rainbow tables exist
- No salt

**Correct:**
```python
# Use bcrypt or Argon2
from werkzeug.security import generate_password_hash, check_password_hash

# Uses PBKDF2 by default (secure)
password_hash = generate_password_hash(password)

# Or use bcrypt directly
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

**Lesson:** Use proper password hashing algorithms (bcrypt, Argon2, PBKDF2), never MD5/SHA1.

---

### 3. Not Implementing Rate Limiting

**Mistake:**
```python
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    # No limit on login attempts!
    if check_credentials(username, password):
        return {"token": generate_token()}
    return {"error": "Invalid credentials"}, 401
```

**Why it's wrong:**
- Allows brute force attacks
- Can guess passwords
- Vulnerable to credential stuffing

**Correct:**
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Max 5 attempts per minute
def login():
    username = request.json['username']
    password = request.json['password']
    if check_credentials(username, password):
        return {"token": generate_token()}
    return {"error": "Invalid credentials"}, 401
```

**Lesson:** Always implement rate limiting on authentication endpoints.

---

## HTTPS/TLS Mistakes

### 4. Using HTTP Instead of HTTPS

**Mistake:**
```python
# Sending sensitive data over HTTP
response = requests.post('http://api.example.com/login',
                        json={'password': 'secret'})
```

**Why it's wrong:**
- Data transmitted in plain text
- Passwords visible on network
- Vulnerable to MITM attacks
- Browser warnings

**Correct:**
```python
# Always use HTTPS
response = requests.post('https://api.example.com/login',
                        json={'password': 'secret'})
```

**Lesson:** ALWAYS use HTTPS for any sensitive data or authentication.

---

### 5. Disabling SSL Verification

**Mistake:**
```python
# Disabling SSL verification to "fix" errors
response = requests.get('https://api.example.com',
                       verify=False)  # DANGEROUS!
```

**Why it's wrong:**
- Defeats purpose of HTTPS
- Vulnerable to MITM attacks
- No certificate validation
- False sense of security

**Correct:**
```python
# Fix the actual problem (certificate issues)
# Option 1: Use valid certificates
response = requests.get('https://api.example.com')

# Option 2: For self-signed certs in development only
response = requests.get('https://localhost:8000',
                       verify='/path/to/ca-cert.pem')
```

**Lesson:** Never disable SSL verification in production. Fix certificate issues properly.

---

## Input Validation Mistakes

### 6. SQL Injection Vulnerability

**Mistake:**
```python
# Building SQL queries with string concatenation
user_id = request.args.get('id')
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)  # Vulnerable!

# Attack: ?id=1 OR 1=1; DROP TABLE users;--
```

**Why it's catastrophic:**
- Attacker can read entire database
- Can modify or delete data
- Can execute arbitrary SQL

**Correct:**
```python
# Use parameterized queries
user_id = request.args.get('id')
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))  # Safe!

# Or use ORM
user = User.query.filter_by(id=user_id).first()
```

**Lesson:** NEVER concatenate user input into SQL. Always use parameterized queries.

---

### 7. Cross-Site Scripting (XSS)

**Mistake:**
```python
# Directly rendering user input
@app.route('/profile')
def profile():
    name = request.args.get('name')
    return f"<h1>Hello {name}</h1>"  # Vulnerable!

# Attack: ?name=<script>alert('XSS')</script>
```

**Why it's wrong:**
- Executes attacker's JavaScript
- Can steal cookies/tokens
- Can deface page
- Can redirect users

**Correct:**
```python
from flask import escape

@app.route('/profile')
def profile():
    name = request.args.get('name', '')
    return f"<h1>Hello {escape(name)}</h1>"  # Safe!

# Or use templates with auto-escaping
return render_template('profile.html', name=name)
```

**Lesson:** Always escape user input before rendering in HTML.

---

### 8. Command Injection

**Mistake:**
```python
# Executing shell commands with user input
filename = request.args.get('file')
os.system(f'cat {filename}')  # Vulnerable!

# Attack: ?file=test.txt; rm -rf /
```

**Why it's wrong:**
- Attacker can execute arbitrary commands
- Can delete files
- Can compromise entire system

**Correct:**
```python
import subprocess
from pathlib import Path

filename = request.args.get('file')

# Validate filename
if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
    return "Invalid filename", 400

# Use subprocess with list (no shell)
result = subprocess.run(['cat', filename], 
                       capture_output=True,
                       text=True)

# Or better: use Python's file operations
with open(filename, 'r') as f:
    content = f.read()
```

**Lesson:** Never pass user input to shell commands. Validate and sanitize all input.

---

## Session & Token Mistakes

### 9. Storing Tokens in LocalStorage

**Mistake:**
```javascript
// Storing JWT in localStorage
localStorage.setItem('token', jwt_token);

// Vulnerable to XSS attacks!
// Any JavaScript can access localStorage
```

**Why it's wrong:**
- Accessible by any JavaScript
- XSS attack can steal token
- No httpOnly protection

**Correct:**
```javascript
// Option 1: Use httpOnly cookies (backend)
response.set_cookie('token', jwt_token,
                   httponly=True,  // Not accessible to JavaScript
                   secure=True,     // Only over HTTPS
                   samesite='Lax')  // CSRF protection

// Option 2: If you must use localStorage, implement additional security
// - Content Security Policy
// - Token refresh with short expiry
// - XSS prevention
```

**Lesson:** Prefer httpOnly cookies for tokens. If using localStorage, implement strong XSS prevention.

---

### 10. Not Setting Token Expiration

**Mistake:**
```python
# Creating tokens that never expire
token = jwt.encode({'user_id': user.id}, SECRET_KEY)
# Token valid forever!
```

**Why it's wrong:**
- Stolen tokens work indefinitely
- No way to revoke access
- Security nightmare

**Correct:**
```python
from datetime import datetime, timedelta

# Set short expiration
expiration = datetime.utcnow() + timedelta(hours=1)
token = jwt.encode({
    'user_id': user.id,
    'exp': expiration
}, SECRET_KEY)

# Implement refresh tokens for longer sessions
refresh_token = generate_refresh_token(user.id)
```

**Lesson:** Always set token expiration. Use refresh tokens for long sessions.

---

## CORS & Security Headers Mistakes

### 11. Using Wildcard CORS

**Mistake:**
```python
# Allowing all origins
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
```

**Why it's wrong:**
- Allows any website to call your API
- Credentials exposed to any origin
- Security vulnerability

**Correct:**
```python
# Whitelist specific origins
ALLOWED_ORIGINS = ['https://trusted-site.com', 'https://another-trusted.com']

@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
```

**Lesson:** Never use wildcard CORS with credentials. Whitelist specific origins.

---

### 12. Missing Security Headers

**Mistake:**
```python
# Not setting security headers
@app.route('/')
def index():
    return render_template('index.html')
```

**Why it's wrong:**
- Vulnerable to clickjacking
- Vulnerable to XSS
- No HTTPS enforcement
- Missing security protections

**Correct:**
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

**Lesson:** Always set security headers to protect against common attacks.

---

## Best Practices

### ✅ Do's
1. **Use HTTPS everywhere**
2. **Hash passwords properly** (bcrypt, Argon2)
3. **Validate all input**
4. **Use parameterized queries**
5. **Implement rate limiting**
6. **Set token expiration**
7. **Use security headers**
8. **Escape output**
9. **Keep dependencies updated**
10. **Follow principle of least privilege**

### ❌ Don'ts
1. **Don't store plain text passwords**
2. **Don't use MD5/SHA1 for passwords**
3. **Don't concatenate SQL queries**
4. **Don't trust user input**
5. **Don't disable SSL verification**
6. **Don't use wildcard CORS with credentials**
7. **Don't store sensitive data in localStorage**
8. **Don't skip input validation**
9. **Don't expose error details to users**
10. **Don't hardcode secrets**

---

## OWASP Top 10 Quick Reference

| Vulnerability | Example | Prevention |
|--------------|---------|------------|
| Injection | SQL injection | Parameterized queries |
| Broken Auth | Weak passwords | Strong hashing, MFA |
| Sensitive Data Exposure | HTTP instead of HTTPS | Use HTTPS everywhere |
| XML External Entities | XML parsing attacks | Disable external entities |
| Broken Access Control | No authorization checks | Implement proper authz |
| Security Misconfiguration | Default passwords | Secure defaults, hardening |
| XSS | Unescaped output | Escape all output |
| Insecure Deserialization | Pickle exploits | Validate serialized data |
| Using Components with Known Vulnerabilities | Old libraries | Keep dependencies updated |
| Insufficient Logging | No audit trail | Log security events |

---

## Security Checklist

Before deploying:
- [ ] All passwords are hashed
- [ ] HTTPS is enforced
- [ ] Input validation is implemented
- [ ] SQL queries are parameterized
- [ ] Rate limiting is active
- [ ] Security headers are set
- [ ] Tokens have expiration
- [ ] Dependencies are updated
- [ ] Error messages don't expose details
- [ ] Logging is configured

**Next:** Review [Security Basics README](./README.md) and complete [exercises](./exercises.md).
