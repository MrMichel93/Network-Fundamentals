# 🛡️ Security Labs

Hands-on security exercises and penetration testing scenarios.

## Purpose

This directory contains practical security exercises where you'll:
- Identify vulnerabilities in real code
- Exploit them safely (in a controlled environment)
- Learn how to fix them properly
- Test your fixes to verify they work

## ⚠️ Important Warning

**The code in this directory contains intentional security vulnerabilities!**

- **NEVER** deploy this code to production
- **NEVER** expose it to the internet
- Only run on localhost (127.0.0.1)
- Use for educational purposes only

## Lab Setup

### Prerequisites

```bash
# Install Python 3.7 or higher
python3 --version

# Install Flask
pip install flask

# Optional: Install testing tools
pip install requests pytest
```

### Running the Vulnerable API

```bash
# Navigate to security-labs directory
cd security-labs

# Run the vulnerable API
python3 vulnerable_api.py
```

The server will start on `http://localhost:5000`

## Lab Exercises

### Lab 1: SQL Injection

**Objective:** Find and fix SQL injection vulnerabilities

**Vulnerable Endpoints:**
- `POST /api/login` - Login endpoint
- `GET /api/users/<username>` - User lookup

**Tasks:**

1. **Test the vulnerability:**
   ```bash
   # Try bypassing authentication
   curl -X POST http://localhost:5000/api/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin'\'' --", "password": "anything"}'
   
   # Try extracting all users
   curl "http://localhost:5000/api/users/admin'%20OR%20'1'='1"
   ```

2. **Understand the attack:**
   - Look at the server logs to see the malicious SQL query
   - Understand how `--` comments out the rest of the query
   - Learn about `OR '1'='1'` always-true conditions

3. **Fix the vulnerability:**
   - Replace string concatenation with parameterized queries
   - Use `?` placeholders in sqlite3
   - Never trust user input in SQL queries

4. **Test your fix:**
   - Verify the attack payloads no longer work
   - Ensure legitimate queries still work
   - Check that error messages don't leak SQL info

**Solution Example:**

```python
# BEFORE (Vulnerable):
query = f"SELECT * FROM users WHERE username = '{username}'"

# AFTER (Secure):
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

### Lab 2: Cross-Site Scripting (XSS)

**Objective:** Find and prevent XSS attacks

**Vulnerable Endpoints:**
- `POST /api/comments` - Stored XSS
- `GET /comments` - XSS execution
- `GET /api/search` - Reflected XSS

**Tasks:**

1. **Test stored XSS:**
   ```bash
   # Inject malicious script
   curl -X POST http://localhost:5000/api/comments \
     -H "Content-Type: application/json" \
     -d '{"text": "<script>alert(\"XSS\")</script>"}'
   
   # View comments to execute the script
   # Open http://localhost:5000/comments in browser
   ```

2. **Test reflected XSS:**
   ```bash
   # Open in browser:
   http://localhost:5000/api/search?q=<script>alert('XSS')</script>
   ```

3. **Fix the vulnerabilities:**
   - Escape HTML output using `markupsafe.escape()` or Jinja2 templates
   - Sanitize input using `bleach.clean()`
   - Implement Content Security Policy headers
   - Use HTTPOnly cookies

4. **Test your fix:**
   - Verify scripts are escaped (show as text, not executed)
   - Ensure legitimate HTML is handled properly
   - Check CSP headers are set

**Solution Example:**

```python
# BEFORE (Vulnerable):
html = f"<p>{comment_text}</p>"

# AFTER (Secure):
from markupsafe import escape
safe_text = escape(comment_text)
html = f"<p>{safe_text}</p>"

# Or use templates (Jinja2 auto-escapes):
return render_template('comments.html', text=comment_text)
```

### Lab 3: Broken Authentication/Authorization

**Objective:** Implement proper access controls

**Vulnerable Endpoints:**
- `GET /api/admin/users` - No authentication
- `DELETE /api/admin/delete-user/<id>` - No authorization

**Tasks:**

1. **Test the vulnerability:**
   ```bash
   # Access admin endpoint without authentication
   curl http://localhost:5000/api/admin/users
   
   # Delete a user without permission
   curl -X DELETE http://localhost:5000/api/admin/delete-user/1
   ```

2. **Understand the problem:**
   - No authentication check (who are you?)
   - No authorization check (what can you do?)
   - Sensitive data exposure (passwords visible!)

3. **Fix the vulnerabilities:**
   - Implement JWT or session-based authentication
   - Add authorization checks for admin routes
   - Never return passwords in API responses
   - Use role-based access control (RBAC)

4. **Test your fix:**
   - Verify endpoints reject unauthenticated requests (401)
   - Verify endpoints reject unauthorized requests (403)
   - Confirm passwords are not in responses

**Solution Example:**

```python
# Add authentication decorator
from functools import wraps
from flask import request, jsonify

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not validate_token(token):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

# Add authorization decorator
def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if user.role != 'admin':
            return jsonify({'error': 'Forbidden'}), 403
        return f(*args, **kwargs)
    return decorated

# Apply to endpoint
@app.route('/api/admin/users')
@require_auth
@require_admin
def get_all_users():
    # ... endpoint code
```

### Lab 4: Rate Limiting

**Objective:** Implement rate limiting to prevent abuse

**Vulnerable Endpoint:**
- `GET /api/expensive-operation` - No rate limit

**Tasks:**

1. **Test the vulnerability:**
   ```bash
   # Send many requests quickly
   for i in {1..50}; do 
     curl http://localhost:5000/api/expensive-operation &
   done
   ```

2. **Observe the problem:**
   - Server becomes slow/unresponsive
   - No limit on number of requests
   - Could lead to DoS attack

3. **Fix the vulnerability:**
   - Implement rate limiting using Flask-Limiter
   - Return 429 status code when limit exceeded
   - Add rate limit headers
   - Consider different limits for different endpoints

4. **Test your fix:**
   - Verify rate limit is enforced
   - Check for 429 response when limit exceeded
   - Verify headers include limit info

**Solution Example:**

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/expensive-operation')
@limiter.limit("10 per minute")
def expensive_operation():
    # ... endpoint code
```

### Lab 5: CORS Misconfiguration

**Objective:** Configure CORS properly

**Current Issue:**
- `Access-Control-Allow-Origin: *` allows any origin

**Tasks:**

1. **Test the vulnerability:**
   - Create a malicious webpage that calls the API
   - Observe that it works (it shouldn't!)

2. **Fix the vulnerability:**
   - Whitelist specific origins only
   - Validate Origin header before reflecting
   - Don't use `*` in production

3. **Test your fix:**
   - Verify allowed origins can access API
   - Verify unauthorized origins are blocked

**Solution Example:**

```python
ALLOWED_ORIGINS = ['https://myapp.com', 'https://www.myapp.com']

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
    return response
```

## Testing Your Fixes

### Manual Testing Checklist

After fixing all vulnerabilities, verify:

- [ ] SQL injection attacks fail gracefully
- [ ] XSS payloads are escaped or sanitized
- [ ] Protected endpoints require authentication
- [ ] Admin actions require admin role
- [ ] Rate limiting prevents abuse
- [ ] CORS only allows trusted origins
- [ ] Error messages don't leak sensitive info
- [ ] Passwords are hashed and never returned
- [ ] Security headers are set
- [ ] All user input is validated

### Automated Testing

Create a test script:

```python
# test_security.py
import requests
import json

BASE_URL = 'http://localhost:5000'

def test_sql_injection():
    """Test that SQL injection is prevented"""
    response = requests.post(
        f'{BASE_URL}/api/login',
        json={'username': "admin' --", 'password': 'anything'}
    )
    assert response.status_code == 401, "SQL injection should not bypass auth"
    print("✓ SQL injection prevented")

def test_xss():
    """Test that XSS is prevented"""
    response = requests.post(
        f'{BASE_URL}/api/comments',
        json={'text': '<script>alert("XSS")</script>'}
    )
    # Script should be escaped in response
    assert '<script>' not in response.text, "XSS should be escaped"
    print("✓ XSS prevented")

def test_authentication():
    """Test that authentication is required"""
    response = requests.get(f'{BASE_URL}/api/admin/users')
    assert response.status_code in [401, 403], "Should require authentication"
    print("✓ Authentication required")

def test_rate_limiting():
    """Test that rate limiting works"""
    for i in range(15):
        response = requests.get(f'{BASE_URL}/api/expensive-operation')
    assert response.status_code == 429, "Should be rate limited"
    print("✓ Rate limiting works")

if __name__ == '__main__':
    print("Running security tests...")
    test_sql_injection()
    test_xss()
    test_authentication()
    test_rate_limiting()
    print("\n✅ All security tests passed!")
```

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP ZAP](https://www.zaproxy.org/)
- [Burp Suite](https://portswigger.net/burp/communitydownload)
- [SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
- [XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

## Planned Labs

### Future Additions

- **Lab 6:** HTTPS and Certificate Validation
- **Lab 7:** JWT Token Security
- **Lab 8:** File Upload Vulnerabilities
- **Lab 9:** API Key Management
- **Lab 10:** Mass Assignment Protection

## Support

If you have questions or find issues with the labs:
1. Review the code and comments carefully
2. Check the main [API Security module](../09-API-Security/)
3. Search for solutions to common problems
4. Experiment and learn by doing!

## Coming Soon

Detailed security labs will be added in future updates!

---

[← Back to Main](../README.md) | [API Security Module →](../09-API-Security/)
