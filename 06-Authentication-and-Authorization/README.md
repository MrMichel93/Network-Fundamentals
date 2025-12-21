# 🔐 Authentication and Authorization

Learn how to securely identify users and control access to resources in networked applications.

## 🎯 Learning Objectives

By the end of this module, you will:
- Understand the difference between authentication and authorization
- Learn session-based authentication
- Master token-based authentication (JWT)
- Understand OAuth 2.0 basics
- Know how to use API keys
- Implement authentication in your applications
- Understand security best practices

## Authentication vs Authorization 🤔

These terms are often confused, but they're different!

### Authentication (AuthN) - "Who are you?"

**Definition**: Proving your identity

**Examples**:
- Logging in with username and password
- Using your fingerprint to unlock your phone
- Showing your ID at airport security

**Question it answers**: "Are you really who you claim to be?"

### Authorization (AuthZ) - "What can you do?"

**Definition**: Determining what you're allowed to access

**Examples**:
- Admin users can delete accounts; regular users cannot
- You can edit your own posts but not others' posts
- Premium subscribers can download videos; free users cannot

**Question it answers**: "Are you allowed to do this action?"

### The Sequence

```
1. Authentication: Prove who you are
2. Authorization: Check what you can do
3. Access granted or denied
```

**Real-world example**:
- You show your driver's license (authentication)
- Bouncer checks if you're 21+ (authorization)
- You're allowed in or turned away

## Session-Based Authentication 🎫

The traditional way to authenticate web users.

### How It Works

```
1. User logs in with credentials
   Client → Server: POST /login {username, password}

2. Server verifies credentials
   Server: Check username/password in database

3. Server creates a session
   Server: Create session ID, store user info

4. Server sends session ID to client
   Server → Client: Set-Cookie: session_id=abc123

5. Client includes session ID in future requests
   Client → Server: Cookie: session_id=abc123

6. Server looks up session to identify user
   Server: Find session abc123 → User is John
```

### Session Flow Diagram

```
Browser                        Server                    Database
  |                               |                          |
  |-- POST /login --------------->|                          |
  |   {user: "john", pwd: "***"}  |                          |
  |                               |-- Verify credentials --->|
  |                               |<-- User found -----------|
  |                               |                          |
  |                               |-- Store session -------->|
  |<-- Set-Cookie: session_id ----|                          |
  |                               |                          |
  |-- GET /profile -------------->|                          |
  |   Cookie: session_id          |                          |
  |                               |-- Lookup session ------->|
  |                               |<-- User data ------------|
  |<-- Profile page --------------|                          |
```

### Session Implementation (Python/Flask)

```python
from flask import Flask, session, request, jsonify
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret for signing cookies

# Fake user database
users = {
    'john': 'password123',  # Don't store plaintext in real apps!
    'jane': 'securepass456'
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Check credentials
    if username in users and users[username] == password:
        session['username'] = username
        session['logged_in'] = True
        return jsonify({'message': 'Logged in successfully'})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/profile')
def profile():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    username = session.get('username')
    return jsonify({'username': username, 'message': 'This is your profile'})

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})
```

### Pros and Cons of Sessions

**Pros**:
- ✅ Server controls everything
- ✅ Can invalidate sessions immediately
- ✅ Simpler to implement
- ✅ Works well for traditional web apps

**Cons**:
- ❌ Requires server-side storage
- ❌ Doesn't scale as easily
- ❌ Problematic for mobile apps
- ❌ CSRF vulnerability risk

## Token-Based Authentication (JWT) 🎟️

Modern approach, especially for APIs and mobile apps.

### What is JWT?

**JWT (JSON Web Token)** is a compact, self-contained token containing user information.

### JWT Structure

A JWT looks like this:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImpvaG4ifQ.Xo1KGk5QZkZ8
```

It has three parts separated by dots:
```
HEADER.PAYLOAD.SIGNATURE
```

**1. Header** (base64 encoded):
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**2. Payload** (base64 encoded):
```json
{
  "user_id": 1,
  "username": "john",
  "exp": 1735689600  // Expiration timestamp
}
```

**3. Signature**:
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret_key
)
```

### How JWT Works

```
1. User logs in
   Client → Server: POST /login {username, password}

2. Server verifies and creates JWT
   Server: Check credentials
   Server: Create JWT with user info

3. Server sends JWT to client
   Server → Client: {token: "eyJhbGc..."}

4. Client stores JWT (localStorage, memory)
   Client: Store token

5. Client includes JWT in future requests
   Client → Server: Authorization: Bearer eyJhbGc...

6. Server verifies JWT signature
   Server: Verify token signature
   Server: Extract user info from payload
```

### JWT Implementation (Python/Flask)

```python
from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
SECRET_KEY = 'your-secret-key-keep-it-safe'

users = {
    'john': 'password123',
    'jane': 'securepass456'
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Verify credentials
    if username in users and users[username] == password:
        # Create JWT
        payload = {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        
        return jsonify({'token': token})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/profile')
def profile():
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return jsonify({'error': 'No token provided'}), 401
    
    try:
        # Extract token (format: "Bearer <token>")
        token = auth_header.split(' ')[1]
        
        # Verify and decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        username = payload['username']
        
        return jsonify({'username': username, 'message': 'Authenticated!'})
        
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
```

### Using JWT in Requests

**Python client**:
```python
import requests

# Login
response = requests.post('http://localhost:5000/login', 
                        json={'username': 'john', 'password': 'password123'})
token = response.json()['token']

# Use token for authenticated requests
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:5000/profile', headers=headers)
print(response.json())
```

**curl**:
```bash
# Login
TOKEN=$(curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"password123"}' \
  | jq -r '.token')

# Use token
curl http://localhost:5000/profile \
  -H "Authorization: Bearer $TOKEN"
```

### Pros and Cons of JWT

**Pros**:
- ✅ Stateless (no server-side storage needed)
- ✅ Scales easily
- ✅ Works great for APIs and mobile apps
- ✅ Can include custom claims
- ✅ Works across domains

**Cons**:
- ❌ Can't invalidate easily
- ❌ Tokens can be large
- ❌ Replay attack risk if not over HTTPS
- ❌ Need to handle token refresh

### Refresh Tokens

**The Problem**: Access tokens should be short-lived for security, but requiring users to login frequently is bad UX.

**The Solution**: Use refresh tokens!

```
┌─────────────┐         ┌──────────┐
│   Client    │         │  Server  │
└──────┬──────┘         └────┬─────┘
       │                     │
       │ Login               │
       ├────────────────────>│
       │                     │
       │ Access + Refresh    │
       │<────────────────────┤
       │  Token              │
       │                     │
       │ Request + Access    │
       ├────────────────────>│
       │                     │
       │ Response            │
       │<────────────────────┤
       │                     │
       │ (Access expires)    │
       │                     │
       │ Refresh Request     │
       ├────────────────────>│
       │                     │
       │ New Access Token    │
       │<────────────────────┤
```

**How it works**:
1. Login returns both access token (short-lived) and refresh token (long-lived)
2. Use access token for requests
3. When access token expires, use refresh token to get new access token
4. Refresh tokens can be revoked if compromised

**Implementation**:
```python
# Two token types with different expiration
ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)   # Short-lived
REFRESH_TOKEN_EXPIRES = timedelta(days=7)      # Long-lived

@app.route('/login', methods=['POST'])
def login():
    # Verify credentials...
    
    # Create both tokens
    access_token = create_access_token(username)
    refresh_token = create_refresh_token(username)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    })

@app.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.json.get('refresh_token')
    
    # Verify refresh token
    payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=['HS256'])
    
    # Check if revoked (check database/Redis)
    if is_revoked(refresh_token):
        return jsonify({'error': 'Token revoked'}), 401
    
    # Create new access token
    new_access_token = create_access_token(payload['username'])
    
    return jsonify({'access_token': new_access_token})
```

### Storing JWTs: localStorage vs httpOnly Cookies

**localStorage** (Common but risky):
```javascript
// Store token
localStorage.setItem('token', accessToken);

// Use token
const token = localStorage.getItem('token');
fetch('/api/data', {
    headers: { 'Authorization': `Bearer ${token}` }
});
```

**Risks**:
- ❌ Vulnerable to XSS attacks
- ❌ JavaScript can access and steal token
- ❌ Any third-party script can read it

**httpOnly Cookies** (More secure):
```python
# Server sets httpOnly cookie
response.set_cookie(
    'token',
    access_token,
    httponly=True,   # Cannot be accessed by JavaScript
    secure=True,     # Only sent over HTTPS
    samesite='Strict'  # CSRF protection
)
```

**Benefits**:
- ✅ Not accessible via JavaScript
- ✅ Automatically included in requests
- ✅ Protected from XSS attacks

**Comparison Table**:

| Feature | localStorage | httpOnly Cookie |
|---------|-------------|-----------------|
| XSS Protection | ❌ Vulnerable | ✅ Protected |
| CSRF Protection | ✅ Not vulnerable | ⚠️ Needs CSRF tokens |
| Mobile Apps | ✅ Easy to use | ❌ Complicated |
| Cross-domain | ✅ Easy | ⚠️ Needs CORS setup |
| Best for | Mobile/SPAs | Traditional web apps |

**Recommendation**: Use httpOnly cookies for web apps, localStorage only if necessary (with strong XSS protection).

## API Keys 🔑

Simplest form of authentication for APIs.

### What are API Keys?

Long random strings that identify an application or user.

**Example**:
```
X-API-Key: 9a8b7c6d5e4f3g2h1i0j
```

### How API Keys Work

```
1. Developer registers for API access
2. Service generates unique API key
3. Developer includes key in requests
4. Service validates key and tracks usage
```

### Using API Keys

**In Headers**:
```python
import requests

headers = {'X-API-Key': 'your-api-key-here'}
response = requests.get('https://api.example.com/data', headers=headers)
```

**In Query Parameters** (less secure):
```python
import requests

params = {'api_key': 'your-api-key-here'}
response = requests.get('https://api.example.com/data', params=params)
```

**Example: OpenWeather API**:
```python
import requests

API_KEY = 'your-openweather-api-key'
url = 'https://api.openweathermap.org/data/2.5/weather'
params = {
    'q': 'London',
    'appid': API_KEY
}

response = requests.get(url, params=params)
print(response.json())
```

### API Key Best Practices

- ✅ Keep keys secret (don't commit to Git!)
- ✅ Use environment variables
- ✅ Rotate keys periodically
- ✅ Use different keys for dev/prod
- ✅ Always use HTTPS
- ❌ Don't hardcode in source files
- ❌ Don't expose in client-side code

**Store in environment variables**:
```python
import os

API_KEY = os.environ.get('WEATHER_API_KEY')
```

### Rate Limiting with API Keys

Rate limiting prevents abuse and ensures fair usage of your API.

**Why Rate Limit?**
- Prevent brute force attacks
- Protect against DDoS
- Ensure fair resource allocation
- Enforce pricing tiers

**Common Rate Limit Strategies**:

1. **Fixed Window**: X requests per time window
   ```
   10 requests per minute
   100 requests per hour
   ```

2. **Sliding Window**: More accurate, tracks exact time
   ```
   Track timestamp of each request
   Count requests in last 60 seconds
   ```

3. **Token Bucket**: Requests "cost" tokens that refill over time

**Implementation Example**:
```python
from flask import Flask, request, jsonify
from collections import defaultdict
import time

app = Flask(__name__)

# Store: {api_key: [timestamp1, timestamp2, ...]}
rate_limit_store = defaultdict(list)

RATE_LIMIT = 10  # requests
TIME_WINDOW = 60  # seconds

def check_rate_limit(api_key):
    current_time = time.time()
    
    # Get request timestamps for this key
    requests = rate_limit_store[api_key]
    
    # Remove timestamps older than time window
    requests[:] = [ts for ts in requests if current_time - ts < TIME_WINDOW]
    
    # Check if limit exceeded
    if len(requests) >= RATE_LIMIT:
        oldest = min(requests)
        retry_after = int(oldest + TIME_WINDOW - current_time)
        return False, retry_after
    
    # Record this request
    requests.append(current_time)
    return True, 0

@app.route('/api/data')
def get_data():
    api_key = request.headers.get('X-API-Key')
    
    if not api_key:
        return jsonify({'error': 'Missing API key'}), 401
    
    # Check rate limit
    allowed, retry_after = check_rate_limit(api_key)
    
    if not allowed:
        return jsonify({
            'error': 'Rate limit exceeded',
            'retry_after': retry_after
        }), 429
    
    # Serve the request
    return jsonify({'data': 'Your data here'})
```

**Using Flask-Limiter** (Production-ready):
```python
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")  # Strict limit for login
def login():
    # Login logic
    pass

@app.route("/api/data")
@limiter.limit("100 per hour")
def api_data():
    # Data endpoint
    pass
```

**Rate Limit Headers** (Best Practice):
```python
# Include rate limit info in response headers
response.headers['X-RateLimit-Limit'] = '100'
response.headers['X-RateLimit-Remaining'] = '87'
response.headers['X-RateLimit-Reset'] = '1735689600'  # Unix timestamp

# For rate limit errors
response.headers['Retry-After'] = '45'  # Seconds until retry
```

**Client Handling**:
```python
import requests
import time

def api_call_with_retry(url, headers):
    response = requests.get(url, headers=headers)
    
    if response.status_code == 429:
        # Rate limited
        retry_after = int(response.headers.get('Retry-After', 60))
        print(f"Rate limited. Waiting {retry_after} seconds...")
        time.sleep(retry_after)
        return api_call_with_retry(url, headers)
    
    return response
```

## OAuth 2.0 Basics 🔓

OAuth allows users to grant third-party access without sharing passwords.

### Real-World Example

**Scenario**: You want to use a cool photo printing service that needs your Facebook photos.

**Bad way** (don't do this):
- Give the service your Facebook password
- They log in as you

**Good way** (OAuth):
- Click "Connect with Facebook"
- Facebook asks: "Allow photo service to access your photos?"
- You approve
- Service gets limited access token (not your password)

### OAuth 2.0 Flow

```
1. User clicks "Login with Google/Facebook/GitHub"
   
2. Redirect to provider's authorization page
   App → Provider: "User wants to authorize this app"
   
3. User approves
   User → Provider: "Yes, I approve"
   
4. Provider redirects back with authorization code
   Provider → App: code=abc123
   
5. App exchanges code for access token
   App → Provider: POST /token {code: abc123, client_secret: ***}
   Provider → App: {access_token: "xyz789"}
   
6. App uses access token to access resources
   App → Provider API: Authorization: Bearer xyz789
```

### OAuth Terminology

- **Resource Owner**: User
- **Client**: Your app
- **Authorization Server**: Google/Facebook/GitHub login
- **Resource Server**: Google/Facebook/GitHub API
- **Access Token**: Credential to access resources
- **Scope**: What the app can access (e.g., "read:user", "write:posts")

### Simple OAuth Example (Login with GitHub)

```python
from flask import Flask, redirect, request, session
import requests

app = Flask(__name__)
app.secret_key = 'super-secret-key'

# Register your app on GitHub to get these
CLIENT_ID = 'your-github-client-id'
CLIENT_SECRET = 'your-github-client-secret'

@app.route('/login')
def login():
    # Redirect to GitHub authorization
    github_auth_url = (
        f'https://github.com/login/oauth/authorize'
        f'?client_id={CLIENT_ID}'
        f'&scope=user:email'
    )
    return redirect(github_auth_url)

@app.route('/callback')
def callback():
    # GitHub redirects here with code
    code = request.args.get('code')
    
    # Exchange code for access token
    token_response = requests.post(
        'https://github.com/login/oauth/access_token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code
        },
        headers={'Accept': 'application/json'}
    )
    
    access_token = token_response.json()['access_token']
    
    # Use access token to get user info
    user_response = requests.get(
        'https://api.github.com/user',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    user_data = user_response.json()
    session['username'] = user_data['login']
    
    return f"Logged in as {user_data['login']}"
```

## Security Best Practices 🛡️

### 1. Always Use HTTPS

- Prevents token/password interception
- Encrypts all communication

### 2. Never Store Passwords in Plain Text

```python
# BAD
users = {'john': 'password123'}

# GOOD - use bcrypt
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
```

### 3. Set Token Expiration

```python
# JWT with 1-hour expiration
payload = {
    'user_id': 123,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
}
```

### 4. Validate All Input

```python
if not username or not password:
    return jsonify({'error': 'Missing credentials'}), 400

if len(password) < 8:
    return jsonify({'error': 'Password too short'}), 400
```

### 5. Use Environment Variables for Secrets

```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY')
API_KEY = os.environ.get('API_KEY')
```

### 6. Implement Rate Limiting

Prevent brute force attacks:
```python
# Allow 5 login attempts per minute
from flask_limiter import Limiter

limiter = Limiter(app)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Login logic
```

### 7. Protect Against Common Vulnerabilities

**SQL Injection**:
```python
# BAD - Vulnerable to SQL injection
query = f"SELECT * FROM users WHERE username='{username}'"

# GOOD - Use parameterized queries
cursor.execute("SELECT * FROM users WHERE username=?", (username,))
```

**Cross-Site Scripting (XSS)**:
```python
# Sanitize user input
from markupsafe import escape

safe_username = escape(username)

# Use httpOnly cookies for tokens
response.set_cookie('token', value, httponly=True)
```

**Cross-Site Request Forgery (CSRF)**:
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# Or use SameSite cookie attribute
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = True
```

## Common Authentication Vulnerabilities ⚠️

### 1. **Broken Authentication**
- Weak passwords allowed
- No account lockout
- Session tokens predictable
- Session fixation attacks

**Prevention**:
- Enforce strong password policies
- Implement account lockout after failed attempts
- Use cryptographically secure random tokens
- Regenerate session ID after login

### 2. **Credential Stuffing**
Attackers use leaked credentials from other breaches.

**Prevention**:
- Monitor for unusual login patterns
- Implement CAPTCHA after failed attempts
- Use device fingerprinting
- Notify users of new device logins

### 3. **Session Hijacking**
Attacker steals session token and impersonates user.

**Prevention**:
- Use HTTPS only
- Set httpOnly and Secure flags on cookies
- Implement session timeouts
- Bind sessions to IP address (optional)

### 4. **JWT Vulnerabilities**

**Algorithm Confusion**:
```python
# Attacker changes algorithm to 'none'
# Always specify algorithms explicitly
jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
```

**Weak Secret Key**:
```python
# BAD
SECRET_KEY = 'secret'

# GOOD
import secrets
SECRET_KEY = secrets.token_hex(32)
```

### 5. **OAuth Attacks**

**Open Redirect**:
```python
# Validate redirect_uri
allowed_redirects = ['https://yourapp.com/callback']
if redirect_uri not in allowed_redirects:
    return error('Invalid redirect URI')
```

**CSRF in OAuth Flow**:
```python
# Use state parameter for CSRF protection
state = secrets.token_urlsafe(16)
session['oauth_state'] = state

# Verify state in callback
if request.args.get('state') != session.get('oauth_state'):
    return error('Invalid state')
```

## Hands-On Practice 💻

Ready to implement authentication yourself? Check out:

1. **Working Examples**: See `examples/` directory for complete code
   - Session-based auth (Flask)
   - JWT auth with refresh tokens
   - API key authentication
   - OAuth 2.0 integration
   - Intentionally vulnerable app (for security testing)

2. **Exercises**: Complete hands-on tasks in `exercises.md`
   - Build and test each authentication method
   - Exploit vulnerabilities in the vulnerable app
   - Create your own TODO API with auth

3. **Testing Tools**: Use Postman collections in `postman/`
   - Pre-configured API tests
   - Automated test scripts
   - Environment setup

4. **Security Testing**: Follow the guide in `security_testing.md`
   - Find common vulnerabilities
   - Learn exploitation techniques
   - Practice remediation

## Summary and Key Takeaways

✅ **Authentication** = Who you are (identity)  
✅ **Authorization** = What you can do (permissions)  
✅ **Sessions** = Server-side state, good for traditional web apps  
✅ **JWT** = Self-contained tokens, great for APIs and mobile  
✅ **API Keys** = Simple identification, good for service-to-service  
✅ **OAuth** = Delegated access without sharing passwords  
✅ **Always use HTTPS** for authentication  
✅ **Never store passwords in plain text**  
✅ **Set token expiration** to limit damage from stolen tokens

## What's Next?

Now that you understand authentication, you're ready to learn about **REST API Design** - how to build your own well-designed APIs!

---

[← Back: Working With APIs](../05-Working-With-APIs/) | [Next: REST API Design →](../07-REST-API-Design/)

## Practice

Complete the exercises in [exercises.md](./exercises.md) to implement authentication!
