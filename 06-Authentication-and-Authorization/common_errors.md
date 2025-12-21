# Common Authentication Errors and Solutions

This guide helps you troubleshoot common authentication issues.

## Table of Contents
- [Session-Based Authentication](#session-based-authentication)
- [JWT Authentication](#jwt-authentication)
- [API Key Authentication](#api-key-authentication)
- [OAuth 2.0](#oauth-20)
- [General Issues](#general-issues)

---

## Session-Based Authentication

### Error: "Session cookie not set"

**Symptom**: Login succeeds but session cookie not saved

**Causes**:
1. Missing `app.secret_key` in Flask
2. Browser blocking cookies
3. SameSite attribute issues

**Solutions**:
```python
# Ensure secret key is set
app.secret_key = 'your-secret-key-here'  # Use secure random key

# Configure session cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set True in production with HTTPS
```

**Testing**:
```bash
# Check if cookie is set
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}' \
  -v 2>&1 | grep Set-Cookie
```

---

### Error: "Session expired" or "Not authenticated"

**Symptom**: User logged in but can't access protected routes

**Causes**:
1. Session not persisted correctly
2. Cookie not sent with request
3. Session timeout

**Solutions**:
```python
# Check session data
@app.route('/debug-session')
def debug_session():
    return jsonify(dict(session))

# Extend session lifetime
from datetime import timedelta
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

@app.route('/login', methods=['POST'])
def login():
    # ... verify credentials ...
    session.permanent = True  # Use PERMANENT_SESSION_LIFETIME
    session['username'] = username
```

**Testing**:
```bash
# Save cookie and reuse
curl -X POST http://localhost:5000/login \
  -d '{"username":"user","password":"pass"}' \
  -c cookies.txt

curl http://localhost:5000/profile -b cookies.txt
```

---

### Error: "CSRF token missing"

**Symptom**: Forms fail with CSRF error

**Cause**: CSRF protection enabled but token not included

**Solution**:
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# Exempt specific endpoints (API endpoints)
@app.route('/api/login', methods=['POST'])
@csrf.exempt
def api_login():
    # API login without CSRF check
```

---

## JWT Authentication

### Error: "Token has expired"

**Symptom**: `jwt.ExpiredSignatureError`

**Cause**: Access token lifetime exceeded

**Solutions**:

**Option 1: Use refresh token**
```python
# Client-side
try:
    response = requests.get('/profile', 
                          headers={'Authorization': f'Bearer {access_token}'})
except:
    # Token expired, refresh it
    refresh_response = requests.post('/refresh',
                                    json={'refresh_token': refresh_token})
    new_token = refresh_response.json()['access_token']
    # Retry with new token
```

**Option 2: Increase token lifetime** (development only)
```python
# Increase for testing
ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Instead of minutes=15
```

---

### Error: "Invalid token" or "Token could not be decoded"

**Symptoms**: 
- `jwt.InvalidTokenError`
- `jwt.DecodeError`

**Causes**:
1. Wrong secret key
2. Token corrupted/modified
3. Wrong algorithm
4. Token format incorrect

**Solutions**:

**Check token format**:
```bash
# Token should have 3 parts separated by dots
echo "eyJhbGc...header.payload.signature"
```

**Verify secret key matches**:
```python
# Same secret for encode and decode
SECRET_KEY = 'your-secret-key'

# Encoding
token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# Decoding
payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
```

**Check algorithm**:
```python
# Always specify algorithms in decode
jwt.decode(token, SECRET_KEY, algorithms=['HS256'])  # Correct
jwt.decode(token, SECRET_KEY)  # May fail
```

---

### Error: "Missing Authorization header"

**Symptom**: 401 error when accessing protected endpoints

**Cause**: Token not included in request

**Solution**:
```python
# Correct format
headers = {'Authorization': 'Bearer <your-token-here>'}

# NOT just the token
headers = {'Authorization': '<your-token-here>'}  # Wrong!

# Example
import requests

token = "eyJhbGc..."
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:5001/profile', headers=headers)
```

**curl**:
```bash
curl http://localhost:5001/profile \
  -H "Authorization: Bearer eyJhbGc..."
```

---

### Error: "Token not valid yet" or "iat in future"

**Symptom**: Token rejected even though just created

**Cause**: Clock skew between servers

**Solution**:
```python
# Add clock skew tolerance
import jwt

try:
    payload = jwt.decode(
        token, 
        SECRET_KEY, 
        algorithms=['HS256'],
        leeway=timedelta(seconds=10)  # Allow 10 second skew
    )
except jwt.InvalidTokenError as e:
    print(f"Token error: {e}")
```

---

## API Key Authentication

### Error: "Missing API key"

**Symptom**: 401 Unauthorized when making requests

**Cause**: API key not included in headers

**Solutions**:

**Check header name**:
```python
# Server expects
api_key = request.headers.get('X-API-Key')

# Client must send
headers = {'X-API-Key': 'your-api-key-here'}
```

**Common variations**:
- `X-API-Key`
- `X-Api-Key`
- `Api-Key`
- `Authorization: ApiKey <key>`

**Testing**:
```bash
# With header
curl http://localhost:5002/api/data \
  -H "X-API-Key: your-key-here"

# Check what server receives
curl http://localhost:5002/api/data \
  -H "X-API-Key: test" -v
```

---

### Error: "Rate limit exceeded" (429 Too Many Requests)

**Symptom**: Requests blocked after several attempts

**Cause**: Too many requests in time window

**Solutions**:

**Wait for reset**:
```python
response = requests.get(url, headers=headers)

if response.status_code == 429:
    retry_after = int(response.headers.get('Retry-After', 60))
    print(f"Rate limited. Retry after {retry_after} seconds")
    time.sleep(retry_after)
    # Retry request
```

**Implement exponential backoff**:
```python
import time

def api_call_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)
        
        if response.status_code != 429:
            return response
        
        wait_time = 2 ** attempt  # 1, 2, 4, 8 seconds
        print(f"Retry in {wait_time} seconds...")
        time.sleep(wait_time)
    
    raise Exception("Max retries exceeded")
```

**Check rate limit status**:
```bash
curl http://localhost:5002/api/keys/info \
  -H "X-API-Key: your-key" | jq '.rate_limit'
```

---

### Error: "API key has been revoked"

**Symptom**: Previously working key now returns 401

**Cause**: Key was revoked or deleted

**Solution**:
```bash
# Create new API key
curl -X POST http://localhost:5002/api/keys/create \
  -H "Content-Type: application/json" \
  -d '{"owner":"you@example.com","description":"New key"}'
```

---

## OAuth 2.0

### Error: "Invalid redirect_uri"

**Symptom**: OAuth flow fails with redirect error

**Cause**: Redirect URI doesn't match registered URI

**Solution**:
1. Check registered callback URL in OAuth provider settings
2. Ensure exact match (including protocol and trailing slash)

```python
# Must match exactly
REGISTERED:  http://localhost:5003/callback
YOUR CODE:   http://localhost:5003/callback  ✓

# These won't match
REGISTERED:  http://localhost:5003/callback
YOUR CODE:   http://localhost:5003/callback/  ✗ (trailing slash)
YOUR CODE:   https://localhost:5003/callback  ✗ (https vs http)
```

---

### Error: "Invalid state parameter" or CSRF error

**Symptom**: OAuth callback fails with state mismatch

**Cause**: State parameter doesn't match

**Solution**:
```python
# Store state before redirect
@app.route('/login')
def login():
    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state  # Store in session
    
    auth_url = f"{OAUTH_URL}?state={state}&..."
    return redirect(auth_url)

# Verify state in callback
@app.route('/callback')
def callback():
    received_state = request.args.get('state')
    stored_state = session.get('oauth_state')
    
    if received_state != stored_state:
        return "CSRF attack detected", 400
    
    # Continue OAuth flow...
```

---

### Error: "access_token not found" or "Failed to obtain access token"

**Symptom**: Cannot exchange authorization code for token

**Causes**:
1. Invalid client credentials
2. Expired authorization code
3. Wrong token endpoint
4. Code already used

**Solutions**:

**Check client credentials**:
```python
# Verify CLIENT_ID and CLIENT_SECRET
print(f"Client ID: {GITHUB_CLIENT_ID}")
print(f"Client Secret: {GITHUB_CLIENT_SECRET[:5]}...")  # Don't print full secret
```

**Check authorization code**:
```python
@app.route('/callback')
def callback():
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        return f"OAuth error: {error}", 400
    
    if not code:
        return "No authorization code received", 400
    
    # Exchange code for token...
```

**Debug token request**:
```python
token_response = requests.post(
    GITHUB_TOKEN_URL,
    data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code
    },
    headers={'Accept': 'application/json'}
)

print(f"Token response status: {token_response.status_code}")
print(f"Token response body: {token_response.text}")
```

---

### Error: "Invalid client_id" or "Client authentication failed"

**Symptom**: OAuth app not recognized

**Solution**:
1. Verify client ID is correct
2. Check OAuth app is registered
3. Ensure environment variables are set

```bash
# Check environment variables
echo $GITHUB_CLIENT_ID
echo $GITHUB_CLIENT_SECRET

# Set if missing
export GITHUB_CLIENT_ID='your-client-id'
export GITHUB_CLIENT_SECRET='your-client-secret'
```

---

## General Issues

### Error: "Connection refused" (ECONNREFUSED)

**Symptom**: Cannot connect to server

**Cause**: Server not running or wrong port

**Solution**:
```bash
# Check if server is running
lsof -i :5000  # Replace 5000 with your port

# Start server
python examples/01_session_auth.py

# Check correct port in code
app.run(port=5000)  # Server runs on 5000
curl http://localhost:5000  # Client connects to 5000
```

---

### Error: "ModuleNotFoundError: No module named 'bcrypt'"

**Symptom**: Import errors when running examples

**Cause**: Missing dependencies

**Solution**:
```bash
# Install dependencies
cd examples
pip install -r requirements.txt

# Or install individually
pip install flask bcrypt pyjwt requests
```

---

### Error: "CORS error" in browser

**Symptom**: Browser blocks API requests from web app

**Cause**: Cross-Origin Resource Sharing not configured

**Solution**:
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Or specific origins
CORS(app, origins=['http://localhost:3000'])
```

---

### Error: "Passwords not matching" or hash verification fails

**Symptom**: Valid password rejected

**Causes**:
1. Password not encoded as bytes
2. Different bcrypt versions
3. Corrupted hash

**Solution**:
```python
import bcrypt

# Always encode to bytes
password = "mypassword"

# Hash
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Verify - must encode password again
is_valid = bcrypt.checkpw(password.encode('utf-8'), hashed)

# NOT this
is_valid = bcrypt.checkpw(password, hashed)  # Will fail
```

---

### Error: "SQLite database is locked"

**Symptom**: Database operations fail with lock error

**Cause**: Multiple connections or threads accessing database

**Solution**:
```python
# Close connections properly
conn = sqlite3.connect('auth.db')
try:
    # Database operations
    cursor.execute(...)
    conn.commit()
finally:
    conn.close()

# Or use context manager
with sqlite3.connect('auth.db') as conn:
    cursor = conn.cursor()
    cursor.execute(...)
```

---

### Error: "ValueError: Invalid salt"

**Symptom**: bcrypt fails to verify password

**Cause**: Hash stored as string instead of bytes

**Solution**:
```python
# Store hash as bytes in database
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# If storing in SQLite, use BLOB type
cursor.execute(
    "CREATE TABLE users (username TEXT, password_hash BLOB)"
)

# When verifying
stored_hash = cursor.fetchone()[1]  # Already bytes from BLOB
is_valid = bcrypt.checkpw(password.encode('utf-8'), stored_hash)
```

---

## Debugging Tips

### Enable Debug Mode

```python
# Flask debug mode (development only!)
app.run(debug=True)

# More detailed error messages
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Log Requests

```python
@app.before_request
def log_request():
    print(f"{request.method} {request.path}")
    print(f"Headers: {dict(request.headers)}")
    if request.json:
        print(f"Body: {request.json}")
```

### Test Authentication State

```python
@app.route('/debug/auth')
def debug_auth():
    return jsonify({
        'session': dict(session),
        'headers': dict(request.headers),
        'cookies': dict(request.cookies)
    })
```

### Use HTTP Client Tools

```bash
# curl with verbose output
curl -v http://localhost:5000/login

# httpie (prettier output)
http POST localhost:5000/login username=test password=test

# Python requests with debugging
import requests
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

response = requests.post('http://localhost:5000/login', 
                        json={'username': 'test', 'password': 'test'})
```

---

## Getting Help

If you're still stuck:

1. **Check server logs** for error messages
2. **Read the error message** carefully - it often tells you exactly what's wrong
3. **Compare with working examples** in the `examples/` directory
4. **Test with curl first** before using libraries
5. **Search for specific error messages** online
6. **Check the security_testing.md guide** for common vulnerabilities

## Quick Reference

### Common HTTP Status Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Not authorized
- `404 Not Found` - Resource doesn't exist
- `429 Too Many Requests` - Rate limited
- `500 Internal Server Error` - Server error

### Authentication Header Formats

```bash
# Session (cookie)
Cookie: session=abc123

# JWT
Authorization: Bearer eyJhbGc...

# API Key
X-API-Key: your-api-key-here

# Basic Auth (legacy)
Authorization: Basic base64(username:password)
```

---

**Remember**: Most authentication errors are due to:
1. Missing or incorrect credentials
2. Expired tokens
3. Missing headers
4. Server not running
5. Incorrect secret keys

Start with the basics and work your way up! 🚀
