# Authentication Examples

This directory contains working code examples demonstrating various authentication methods.

## 📁 Files

### 1. Session-Based Authentication (`01_session_auth.py`)
Traditional session-based authentication using Flask sessions and cookies.

**Features:**
- User registration with bcrypt password hashing
- Login/logout functionality
- Session management
- Protected routes

**Run:**
```bash
python 01_session_auth.py
```

**Test:**
```bash
# Register a user
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"password123","email":"john@example.com"}'

# Login
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"password123"}' \
  -c cookies.txt

# Access protected route
curl http://localhost:5000/profile -b cookies.txt
```

### 2. JWT Authentication (`02_jwt_auth.py`)
Token-based authentication using JSON Web Tokens (JWT).

**Features:**
- JWT access tokens
- Refresh tokens
- Token expiration
- Stateless authentication

**Run:**
```bash
python 02_jwt_auth.py
```

**Test:**
```bash
# Register a user
curl -X POST http://localhost:5001/register \
  -H "Content-Type: application/json" \
  -d '{"username":"jane","password":"securepass123","email":"jane@example.com"}'

# Login and get tokens
curl -X POST http://localhost:5001/login \
  -H "Content-Type: application/json" \
  -d '{"username":"jane","password":"securepass123"}'

# Save the access_token from response, then:
TOKEN="<your-access-token>"

# Access protected route
curl http://localhost:5001/profile \
  -H "Authorization: Bearer $TOKEN"
```

### 3. API Key Authentication (`03_api_key_auth.py`)
API key-based authentication with rate limiting.

**Features:**
- API key generation
- Rate limiting (10 requests per minute)
- Usage tracking
- Key revocation

**Run:**
```bash
python 03_api_key_auth.py
```

**Test:**
```bash
# Create API key
curl -X POST http://localhost:5002/api/keys/create \
  -H "Content-Type: application/json" \
  -d '{"owner":"you@example.com","description":"Test key"}'

# Save the api_key from response, then:
API_KEY="<your-api-key>"

# Access protected endpoint
curl http://localhost:5002/api/data \
  -H "X-API-Key: $API_KEY"

# Check rate limit status
curl http://localhost:5002/api/keys/info \
  -H "X-API-Key: $API_KEY"
```

### 4. OAuth 2.0 Example (`04_oauth_example.py`)
GitHub OAuth integration demonstrating OAuth 2.0 flow.

**Features:**
- GitHub OAuth integration
- Authorization code flow
- Access token handling
- API calls with OAuth token

**Setup:**
1. Register OAuth app at https://github.com/settings/developers
2. Set callback URL to `http://localhost:5003/callback`
3. Set environment variables:
```bash
export GITHUB_CLIENT_ID='your-client-id'
export GITHUB_CLIENT_SECRET='your-client-secret'
```

**Run:**
```bash
python 04_oauth_example.py
```

**Test:**
Open browser to http://localhost:5003 and follow OAuth flow.

### 5. Vulnerable Auth App (`05_vulnerable_auth.py`)

⚠️ **WARNING: INTENTIONALLY VULNERABLE** ⚠️

This application contains deliberate security vulnerabilities for educational purposes.

**Vulnerabilities included:**
- Plaintext password storage
- SQL injection
- No rate limiting
- Weak session management
- Information disclosure
- Default credentials (admin/admin123)
- Missing authorization checks
- And more...

**Run:**
```bash
python 05_vulnerable_auth.py
```

**Purpose:** Learn to identify and exploit common authentication vulnerabilities. See exercises.md for security testing tasks.

## 🛠️ Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install flask bcrypt pyjwt requests
```

## 🔒 Security Notes

- **Examples 1-4:** Demonstrate best practices but are simplified for learning
- **Example 5:** INTENTIONALLY VULNERABLE - DO NOT use in production
- Always use HTTPS in production
- Store secrets in environment variables
- Use proper database (not in-memory) in production
- Implement proper error handling
- Add logging and monitoring

## 📚 Additional Resources

- See `../README.md` for detailed authentication concepts
- See `../exercises.md` for hands-on practice
- See `../postman/` for Postman collections
- See `../security_testing.md` for security testing guide

## 💡 Tips

1. **Run on different ports:** Each example uses a different port (5000-5004)
2. **Test in order:** Start with session auth, then JWT, then API keys
3. **Use Postman:** Import collections from `../postman/` directory
4. **Read the code:** Each file is heavily commented for learning
5. **Experiment safely:** All examples can be run locally without risk

## 🐛 Troubleshooting

**Port already in use:**
```bash
# Change the port in the script or kill existing process
lsof -ti:5000 | xargs kill
```

**Module not found:**
```bash
pip install -r requirements.txt
```

**OAuth not working:**
- Make sure you've registered GitHub OAuth app
- Check environment variables are set correctly
- Verify callback URL matches exactly

## 📖 Learning Path

1. Start with `01_session_auth.py` - understand basics
2. Move to `02_jwt_auth.py` - learn modern approach
3. Try `03_api_key_auth.py` - see API authentication
4. Explore `04_oauth_example.py` - understand delegated auth
5. Test `05_vulnerable_auth.py` - learn security by breaking things

Happy learning! 🚀
