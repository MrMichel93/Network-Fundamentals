# 🌐 HTTP Fundamentals

Now that you understand how the internet works, let's dive into **HTTP** - the protocol that powers the World Wide Web!

## 🎯 Learning Objectives

By the end of this module, you will:
- Understand what HTTP is and why it exists
- Learn the HTTP request/response cycle
- Master HTTP methods (GET, POST, PUT, DELETE, etc.)
- Understand HTTP status codes and what they mean
- Learn about HTTP headers and their purposes
- Build simple HTTP servers and clients
- Use tools like curl to make HTTP requests

## What is HTTP?

**HTTP (HyperText Transfer Protocol)** is the foundation of data communication on the web. It's a set of rules that defines how messages are formatted and transmitted between web browsers and servers.

### Real-World Analogy: Restaurant Ordering 🍽️

Think of HTTP like ordering at a restaurant:

1. **You (Client)** look at the menu and make a request: "I'd like a burger, please"
2. **Waiter (HTTP)** carries your request to the kitchen
3. **Kitchen (Server)** prepares your burger
4. **Waiter (HTTP)** brings back the response: Your burger!

The waiter doesn't make the food - they just carry messages back and forth. That's what HTTP does!

## The HTTP Request/Response Cycle

Every time you visit a website, this happens:

```
┌─────────────┐                                    ┌─────────────┐
│   Browser   │                                    │   Server    │
│  (Client)   │                                    │             │
└──────┬──────┘                                    └──────┬──────┘
       │                                                  │
       │  1. HTTP Request                                 │
       │  "GET /index.html HTTP/1.1"                      │
       │─────────────────────────────────────────────────>│
       │                                                  │
       │                                                  │ 2. Process
       │                                                  │    Request
       │                                                  │
       │  3. HTTP Response                                │
       │  "200 OK + HTML content"                         │
       │<─────────────────────────────────────────────────│
       │                                                  │
       │ 4. Render page                                   │
       │                                                  │
```

**Key Points**:
- Client initiates the request
- Server processes and sends a response
- Each request/response is independent (stateless)
- Multiple requests may be needed for one page (HTML, CSS, images, etc.)

## HTTP Methods (Verbs)

HTTP methods tell the server what action you want to perform. Think of them as verbs in a sentence.

### GET - Retrieve Data 📖

**Purpose**: Request data from a server (like reading a book from a library)

**Example**:
```
GET /users/123 HTTP/1.1
Host: api.example.com
```

**Characteristics**:
- Read-only operation
- Data in URL (query parameters)
- Can be cached
- Can be bookmarked
- Should not modify server data

**Real-world examples**:
- Loading a web page
- Searching Google
- Viewing your profile

### POST - Create New Data ✍️

**Purpose**: Send data to create a new resource

**Example**:
```
POST /users HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "name": "Alice",
  "email": "alice@example.com"
}
```

**Characteristics**:
- Can modify server data
- Data in request body
- Not cached
- Not bookmarkable
- Creates new resources

**Real-world examples**:
- Submitting a form
- Creating an account
- Posting a comment

### PUT - Update/Replace Data 🔄

**Purpose**: Update an existing resource (or create if it doesn't exist)

**Example**:
```
PUT /users/123 HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "name": "Alice Smith",
  "email": "alice.smith@example.com"
}
```

**Characteristics**:
- Replaces entire resource
- Idempotent (same result if repeated)
- Data in request body

### PATCH - Partial Update 🩹

**Purpose**: Partially update a resource (only change specific fields)

**Example**:
```
PATCH /users/123 HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "email": "newemail@example.com"
}
```

### DELETE - Remove Data 🗑️

**Purpose**: Delete a resource

**Example**:
```
DELETE /users/123 HTTP/1.1
Host: api.example.com
```

**Characteristics**:
- Removes resources
- Idempotent
- May return success even if resource doesn't exist

### Other Methods

- **HEAD**: Like GET but only returns headers (no body)
- **OPTIONS**: Ask what methods are supported
- **CONNECT**: Establish a tunnel (used for HTTPS proxies)
- **TRACE**: Echo back the request (debugging)

### Method Summary Table

| Method | Purpose        | Has Body | Idempotent | Safe |
|--------|----------------|----------|------------|------|
| GET    | Read          | No       | Yes        | Yes  |
| POST   | Create        | Yes      | No         | No   |
| PUT    | Update/Create | Yes      | Yes        | No   |
| PATCH  | Partial Update| Yes      | No         | No   |
| DELETE | Delete        | No       | Yes        | No   |

**Idempotent** = Same result if repeated  
**Safe** = Doesn't modify server data

### 🔍 Using DevTools to See HTTP Methods

**Let's see different HTTP methods in action!**

1. **Observe GET requests**:
   - Open DevTools (F12) → Network tab
   - Visit any website
   - Click on requests - most will be GET (fetching resources)
   - Look for the "Method" column showing "GET"

2. **Observe POST requests**:
   - Go to any website with a form (e.g., GitHub login)
   - Fill out the form but DON'T submit yet
   - Make sure Network tab is open and cleared (🚫 button)
   - Submit the form
   - Look for a request with Method: "POST"
   - Click on it → "Payload" tab to see the data sent

3. **What you'll see**:
   ```
   Request URL: https://example.com/login
   Request Method: POST
   Status Code: 200 OK
   ```
   
   Under "Payload" or "Request" tab:
   ```
   username: alice
   password: ••••••
   ```

4. **Try this**:
   - Visit https://httpbin.org/forms/post
   - Open DevTools Network tab, clear it
   - Fill the form and submit
   - Find the POST request
   - Examine: Method, Status Code, and Payload

5. **Other methods**:
   - **PUT/PATCH/DELETE**: Usually seen in single-page applications (SPAs) when interacting with APIs
   - Try inspecting popular web apps (Twitter, Gmail) to see API calls with different methods

## HTTP Status Codes

Status codes tell you the result of your request. They're grouped by category:

### 1xx - Informational 💬
"Hold on, I'm processing..."

- **100 Continue**: Server received request headers, send body
- **101 Switching Protocols**: Changing to WebSocket

### 2xx - Success ✅
"All good! Here's your data."

- **200 OK**: Request succeeded
- **201 Created**: New resource created (POST)
- **204 No Content**: Success but no data to return (DELETE)

### 3xx - Redirection 🔄
"What you want is somewhere else."

- **301 Moved Permanently**: Resource permanently moved to new URL
- **302 Found**: Temporary redirect
- **304 Not Modified**: Cached version is still valid

### 4xx - Client Errors ❌
"You made a mistake in your request."

- **400 Bad Request**: Malformed request syntax
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: You don't have permission
- **404 Not Found**: Resource doesn't exist
- **405 Method Not Allowed**: Wrong HTTP method
- **429 Too Many Requests**: Rate limit exceeded

### 5xx - Server Errors 💥
"Something went wrong on our end."

- **500 Internal Server Error**: Generic server error
- **502 Bad Gateway**: Invalid response from upstream server
- **503 Service Unavailable**: Server temporarily down
- **504 Gateway Timeout**: Upstream server timeout

### Common Status Code Analogies 🎭

- **200**: "Here's what you asked for!" ✅
- **201**: "Created! Here's your receipt" 🧾
- **400**: "I don't understand what you're asking" 🤔
- **401**: "Who are you? Show me your ID" 🪪
- **403**: "I know who you are, but you can't do that" 🚫
- **404**: "That doesn't exist here" 🤷
- **500**: "Oops, something broke on my end" 🔧

### 🔍 Using DevTools to See Status Codes

**Let's verify status codes in your browser!**

1. **Open DevTools**:
   - Press F12 (or Cmd+Opt+I on Mac)
   - Click the "Network" tab
   
2. **Visit a website**:
   - Go to any website (e.g., https://github.com)
   - Watch the Network tab populate with requests
   
3. **Find status codes**:
   - Look at the "Status" column - you'll see status codes like 200, 304, etc.
   - Click on any request to see detailed information
   
4. **Try triggering different status codes**:
   - **200 OK**: Visit any normal page
   - **304 Not Modified**: Refresh a page (browser uses cache)
   - **404 Not Found**: Visit https://github.com/this-page-does-not-exist-12345
   - **301 Redirect**: Visit http://github.com (redirects to https)

**What to look for**:
- Green/gray numbers (200s, 300s) = Success or redirect
- Red numbers (400s, 500s) = Errors
- Click on a request → "Headers" tab → See "Status Code" at the top

## HTTP Headers

Headers provide additional information about the request or response. Think of them as metadata or instructions.

### HTTP Request and Response Structure Diagrams

Understanding the structure of HTTP messages is crucial. Here are detailed diagrams:

#### HTTP Request Structure:

```
GET /api/users/123 HTTP/1.1
└┬┘ └──────┬───────┘ └───┬───┘
 │         │             │
Method    Path        Version

Host: api.example.com
Content-Type: application/json
Authorization: Bearer token123
└────────┬────────────────────┘
       Headers

{"filters": {"active": true}}
└──────────┬──────────────────┘
         Body (optional)
```

**Request Components:**
- **Method**: What action to perform (GET, POST, PUT, DELETE, etc.)
- **Path**: The resource you're requesting (e.g., /api/users/123)
- **Version**: HTTP protocol version (usually HTTP/1.1 or HTTP/2)
- **Headers**: Metadata about the request (host, content type, authentication)
- **Body**: Data being sent (only for POST, PUT, PATCH requests)

#### HTTP Response Structure:

```
HTTP/1.1 200 OK
└───┬───┘ └─┬┘
  Version Status

Content-Type: application/json
Content-Length: 1234
└────────┬────────────────────┘
       Headers

{"id": 123, "name": "John"}
└──────────┬────────────────┘
         Body
```

**Response Components:**
- **Version**: HTTP protocol version
- **Status**: Status code and message (200 OK, 404 Not Found, etc.)
- **Headers**: Metadata about the response (content type, length, caching)
- **Body**: The actual data being returned (HTML, JSON, images, etc.)

### Common Request Headers

```http
GET /api/users HTTP/1.1
Host: api.example.com              ← Which server to contact
User-Agent: Mozilla/5.0            ← What browser/client
Accept: application/json           ← What format I want back
Authorization: Bearer xyz123       ← Authentication token
Content-Type: application/json     ← Format of data I'm sending
```

### Common Response Headers

```http
HTTP/1.1 200 OK
Content-Type: application/json     ← Format of data being sent
Content-Length: 1234               ← Size in bytes
Cache-Control: max-age=3600        ← How long to cache
Set-Cookie: session=abc123         ← Store this cookie
Access-Control-Allow-Origin: *     ← CORS policy
```

### Important Headers Explained

**Content-Type**: Tells what format the data is in
- `text/html` - HTML page
- `application/json` - JSON data
- `image/png` - PNG image
- `application/pdf` - PDF file

**Authorization**: Provides credentials
- `Bearer token123` - Token-based auth
- `Basic dXNlcjpwYXNz` - Username/password (base64)

**Cache-Control**: How long to store the response
- `no-cache` - Always check with server
- `max-age=3600` - Cache for 1 hour
- `public` - Can be cached by anyone

**CORS Headers** (Cross-Origin Resource Sharing):
- `Access-Control-Allow-Origin` - Which domains can access
- `Access-Control-Allow-Methods` - Which HTTP methods allowed
- `Access-Control-Allow-Headers` - Which headers allowed

### 🔍 Using DevTools to See Headers

**Let's inspect HTTP headers in your browser!**

1. **Open DevTools Network tab**:
   - Press F12 → Click "Network" tab
   - Visit any website or refresh the current page
   
2. **Select a request**:
   - Click on any request in the list (usually the first one is the HTML document)
   - You'll see detailed information appear
   
3. **View headers**:
   - Click the "Headers" tab (should be selected by default)
   - Scroll down to see two sections:
     - **Request Headers**: Headers your browser sent
     - **Response Headers**: Headers the server sent back

4. **What to look for**:
   
   **Request Headers you'll see**:
   ```
   Accept: text/html,application/json
   User-Agent: Mozilla/5.0 (your browser info)
   Accept-Language: en-US,en
   Accept-Encoding: gzip, deflate, br
   ```
   
   **Response Headers you'll see**:
   ```
   Content-Type: text/html; charset=utf-8
   Content-Length: 12345
   Cache-Control: max-age=3600
   Server: nginx/1.18.0
   Set-Cookie: session=abc123
   ```

5. **Try this exercise**:
   - Visit https://api.github.com/users/octocat
   - In DevTools, find the request
   - Look for these headers:
     - Response: `Content-Type` (should be `application/json`)
     - Response: `X-RateLimit-Limit` (GitHub's rate limit)
     - Request: `Accept` (what your browser asked for)

## HTTPS vs HTTP 🔒

**HTTP**: Unencrypted (like sending a postcard - anyone can read it)  
**HTTPS**: Encrypted with TLS/SSL (like a sealed envelope)

```
HTTP:  Browser ←──→ Server  (visible to anyone)
HTTPS: Browser ←🔒→ Server  (encrypted)
```

**Always use HTTPS** for:
- Login pages
- Payment information
- Personal data
- Any production website

## Hands-On: Making HTTP Requests with curl

**curl** is a command-line tool for making HTTP requests.

### Basic GET Request

```bash
curl https://api.github.com/users/octocat
```

### GET with Headers

```bash
curl -H "Accept: application/json" https://api.example.com/data
```

### POST Request

```bash
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}'
```

### See Full Response (Headers + Body)

```bash
curl -i https://api.github.com/users/octocat
```

### Verbose Output (Debug)

```bash
curl -v https://api.github.com/users/octocat
```

### Follow Redirects

```bash
curl -L https://github.com
```

## Using Browser Developer Tools 🛠️

Your browser has built-in tools for inspecting HTTP traffic!

**Opening DevTools**:
- Chrome/Edge: F12 or Ctrl+Shift+I (Cmd+Opt+I on Mac)
- Firefox: F12 or Ctrl+Shift+I (Cmd+Opt+I on Mac)

**Network Tab**:
1. Open DevTools
2. Click "Network" tab
3. Refresh the page
4. Click on any request to see details

**What you can see**:
- All HTTP requests made by the page
- Request/response headers
- Response body
- Timing information
- Status codes

**Try this**: Visit any website and watch the Network tab!

## Code Examples

Check the `examples/` folder for:
- `simple_http_server.py` - Basic HTTP server
- `http_client.py` - Making HTTP requests in Python
- `curl_examples.sh` - curl command examples

## Common Pitfalls and Debugging Tips

### "CORS Error"
**Problem**: Browser blocks request to different domain  
**Why**: Security feature to protect users  
**Solution**: Server must send proper CORS headers

### "404 Not Found"
**Problem**: URL doesn't exist  
**Solution**: Check spelling, verify the endpoint exists

### "401 Unauthorized"
**Problem**: Missing or invalid authentication  
**Solution**: Include proper Authorization header

### "500 Internal Server Error"
**Problem**: Server crashed or encountered an error  
**Solution**: Check server logs, not your fault as client

### Data Not Showing Up
**Problem**: Using GET when you should use POST, or vice versa  
**Solution**: Check API documentation for correct method

## 🛠️ Debugging HTTP with Tools

When things go wrong with HTTP requests, you need to know how to debug them. Here are common scenarios and how to solve them using different tools.

> **📝 Note**: Examples in this section use placeholder URLs like `api.example.com` to show the pattern. When you see these, replace them with your actual API endpoints. For hands-on practice with working URLs, see the [exercises](./exercises.md) which use real endpoints like httpbin.org and api.github.com.

### Scenario 1: Request Not Working (404 Error)

**Symptoms**: 
- Getting "404 Not Found" error
- Page or resource doesn't load
- API endpoint returns 404

**Debug with Browser DevTools:**
1. Open DevTools (F12) → Network tab
2. Reproduce the issue (refresh page or retry request)
3. Find the failed request (usually shown in red)
4. Click on it and check:
   - **Request URL**: Is the URL spelled correctly?
   - **Status**: Confirms it's 404
   - **Response**: Server might provide helpful error message
5. Compare with working URLs in your app

**Debug with curl:**
```bash
# Make the request and see the status
curl -i https://api.example.com/users/999999

# You'll see:
# HTTP/1.1 404 Not Found
# {"error": "User not found"}
```

**Debug with Postman:**
1. Create a new request
2. Enter the URL
3. Click "Send"
4. Check the status code (bottom right)
5. Verify the URL in the address bar
6. Check if the endpoint exists in API documentation

**Common Fixes**:
- ✅ Check URL spelling (typos are common!)
- ✅ Verify the endpoint exists in API docs
- ✅ Check if you need authentication
- ✅ Ensure you're using the right base URL

---

### Scenario 2: CORS Error

**Symptoms**:
- Console error: "Access to fetch at '...' from origin '...' has been blocked by CORS policy"
- Request works in Postman but not in browser
- Request works with curl but fails in JavaScript

**Debug with Browser DevTools:**
1. Open Console tab (see the CORS error)
2. Go to Network tab
3. Find the failed request
4. Check Response Headers for:
   - `Access-Control-Allow-Origin`: Should match your domain or be `*`
   - If header is missing, server needs to add it

**Understanding CORS**:
```
Your Website          API Server
(localhost:3000)      (api.example.com)
     │
     ├──► Request from JavaScript
     │
     │    ❌ Blocked! Different origin
     │
     │    Server needs to send:
     │    Access-Control-Allow-Origin: localhost:3000
```

**Debug with curl:**
```bash
# CORS doesn't affect curl (it's browser-specific)
# This will work even when browser fails:
curl https://api.example.com/data

# Check if server sends CORS headers:
curl -i -H "Origin: http://localhost:3000" \
  https://api.example.com/data | grep -i "access-control"
```

**Common Fixes**:
- ✅ Server must add CORS headers (backend change required)
- ✅ Use a proxy in development
- ✅ For testing, use Postman or curl (no CORS restrictions)
- ❌ Don't disable CORS in browser (security risk!)

---

### Scenario 3: Authentication Failure (401 Unauthorized)

**Symptoms**:
- Getting "401 Unauthorized" or "403 Forbidden"
- API returns "Authentication required"
- "Invalid token" messages

**Debug with Browser DevTools:**
1. Network tab → Find the request
2. Check Request Headers:
   - Look for `Authorization` header
   - Is it present? Is it correctly formatted?
   - Should be like: `Bearer eyJhbGc...`
3. Check Response:
   - Server might explain what's wrong
   - "Token expired", "Invalid token", etc.

**Debug with curl:**
```bash
# Request WITHOUT auth (will fail)
curl -i https://api.example.com/protected
# Returns: 401 Unauthorized

# Request WITH auth
curl -i -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.example.com/protected
# Should return: 200 OK

# Test with verbose output to see full exchange
curl -v -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.example.com/protected
```

**Debug with Postman:**
1. Open your request
2. Go to "Authorization" tab
3. Select type (Bearer Token, Basic Auth, etc.)
4. Enter credentials
5. Send request
6. Check if 401 changes to 200

**Common Fixes**:
- ✅ Check if token is expired (generate new one)
- ✅ Verify token format: `Bearer <token>` not just `<token>`
- ✅ Check token is being sent in headers, not body
- ✅ Ensure you're using the correct authentication method

---

### Scenario 4: Server Error (500/502/503)

**Symptoms**:
- "500 Internal Server Error"
- "502 Bad Gateway"
- "503 Service Unavailable"
- Request worked before but suddenly stopped

**Debug with Browser DevTools:**
1. Network tab → Find the failing request
2. Check Status Code:
   - 500: Server code crashed
   - 502: Gateway/proxy issue
   - 503: Server overloaded or down
3. Check Response:
   - May contain error details (if server configured to show them)
   - Production servers often hide details for security

**Debug with curl:**
```bash
# Check the status and response
curl -i https://api.example.com/endpoint

# If server is down, you might get connection errors:
# curl: (7) Failed to connect to api.example.com port 443: Connection refused

# Check with verbose mode
curl -v https://api.example.com/endpoint
```

**What to do**:
- ✅ **500**: Report to backend team (server-side issue)
- ✅ **502/503**: Check if server is down (try again later)
- ✅ Check status page if available (status.example.com)
- ✅ Implement retry logic with exponential backoff
- ❌ Don't keep hammering a failing server!

---

### Scenario 5: Request Timeout

**Symptoms**:
- Request takes forever and eventually fails
- "Request timeout" error
- No response from server

**Debug with Browser DevTools:**
1. Network tab → Find the request
2. Look at "Time" column (very high number)
3. Click request → "Timing" tab
4. See where time is spent:
   - Waiting (TTFB): Server processing time
   - Download: Data transfer time

**Debug with curl:**
```bash
# Set a timeout (e.g., 10 seconds)
curl --max-time 10 https://slow-api.example.com/endpoint

# See timing breakdown for any URL
# Usage: curl -w "@-" -o /dev/null -s YOUR_URL <<'EOF' ... EOF
# Example with httpbin's delay endpoint (simulates a slow server):
curl -w "@-" -o /dev/null -s https://httpbin.org/delay/2 <<'EOF'
    time_namelookup:  %{time_namelookup}\n
       time_connect:  %{time_connect}\n
    time_appconnect:  %{time_appconnect}\n
      time_redirect:  %{time_redirect}\n
   time_pretransfer:  %{time_pretransfer}\n
 time_starttransfer:  %{time_starttransfer}\n
                    ----------\n
         time_total:  %{time_total}\n
EOF
# Replace the URL with your endpoint to debug timing issues
```

**Common Fixes**:
- ✅ Increase timeout limit in your code
- ✅ Check server performance/load
- ✅ Optimize slow database queries (backend)
- ✅ Use caching to reduce server load
- ✅ Check network connectivity

---

### Scenario 6: Wrong HTTP Method (405 Method Not Allowed)

**Symptoms**:
- "405 Method Not Allowed"
- Using POST but endpoint expects GET
- Using GET but endpoint expects POST

**Debug with Browser DevTools:**
1. Network tab → Find the request
2. Check the "Method" column
3. Click request → Headers → Check "Request Method"
4. Compare with API documentation

**Debug with curl:**
```bash
# Wrong method (GET when should be POST)
curl -i https://api.example.com/create-user
# Returns: 405 Method Not Allowed

# Correct method
curl -i -X POST https://api.example.com/create-user \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice"}'
# Returns: 201 Created
```

**Debug with Postman:**
1. Check the method dropdown (GET, POST, PUT, etc.)
2. Verify against API documentation
3. Try different methods to see which works

**Common Fixes**:
- ✅ Read API documentation for correct method
- ✅ GET for fetching, POST for creating, PUT/PATCH for updating, DELETE for removing
- ✅ Check if endpoint has multiple methods for different actions

---

### Scenario 7: Malformed Request (400 Bad Request)

**Symptoms**:
- "400 Bad Request"
- "Invalid JSON"
- "Missing required field"

**Debug with Browser DevTools:**
1. Network tab → Find the request
2. Click request → "Payload" or "Request" tab
3. Check the data being sent:
   - Is JSON valid?
   - Are all required fields present?
   - Are data types correct (string vs number)?

**Debug with curl:**
```bash
# Bad JSON (missing closing quote)
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice}'
# Returns: 400 Bad Request (Invalid JSON)

# Good JSON
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}'
# Returns: 201 Created

# Pretty-print JSON to validate
echo '{"name":"Alice"}' | python -m json.tool
```

**Debug with Postman:**
1. Go to "Body" tab
2. Select "raw" and "JSON"
3. Postman will highlight JSON errors
4. Check "Pre-request Script" for any data manipulation

**Common Fixes**:
- ✅ Validate JSON syntax (use JSON validator)
- ✅ Check required fields from API docs
- ✅ Ensure correct data types (numbers not in quotes, etc.)
- ✅ Verify Content-Type header is set correctly

---

### Scenario 8: Rate Limiting (429 Too Many Requests)

**Symptoms**:
- "429 Too Many Requests"
- "Rate limit exceeded"
- Requests work then suddenly stop

**Debug with Browser DevTools:**
1. Network tab → Find the 429 request
2. Check Response Headers:
   - `X-RateLimit-Limit`: Max requests allowed
   - `X-RateLimit-Remaining`: Requests left
   - `X-RateLimit-Reset`: When limit resets (Unix timestamp)
   - `Retry-After`: Seconds to wait before retrying

**Debug with curl:**
```bash
# See rate limit headers
curl -i https://api.github.com/users/octocat | grep -i ratelimit

# You'll see:
# X-RateLimit-Limit: 60
# X-RateLimit-Remaining: 59
# X-RateLimit-Reset: 1640000000

# Convert reset timestamp to human-readable
date -d @1640000000
```

**Common Fixes**:
- ✅ Implement exponential backoff
- ✅ Cache responses to reduce requests
- ✅ Use authenticated requests (higher limits)
- ✅ Respect `Retry-After` header
- ✅ Implement request queuing

---

### Scenario 9: Redirect Issues (301/302)

**Symptoms**:
- Too many redirects
- Redirect loop
- Unexpected redirects

**Debug with Browser DevTools:**
1. Network tab
2. You'll see multiple requests to same URL
3. Each shows 301 or 302 status
4. Check Response Headers for `Location` (where it redirects)

**Debug with curl:**
```bash
# See redirect without following
curl -i http://github.com
# Returns: 301 Moved Permanently
# Location: https://github.com/

# Follow redirects automatically
curl -L http://github.com

# See redirect chain verbosely
curl -Lv http://example.com
```

**Common Fixes**:
- ✅ Use final URL directly (skip redirects)
- ✅ Check for redirect loops (A → B → A)
- ✅ Ensure HTTP → HTTPS redirects work correctly
- ✅ Set max redirects limit to prevent infinite loops

---

### Scenario 10: Content-Type Mismatch

**Symptoms**:
- Server returns data but in wrong format
- Expected JSON but got HTML
- "Unexpected token < in JSON" error

**Debug with Browser DevTools:**
1. Network tab → Find the request
2. Check Response Headers:
   - Look for `Content-Type`
   - Is it what you expected?
3. Preview tab shows how browser interprets it
4. Response tab shows raw data

**Debug with curl:**
```bash
# Check Content-Type
curl -i https://api.example.com/data | grep -i content-type

# You might see:
# Content-Type: text/html (but you expected application/json!)

# Request specific format with Accept header
curl -H "Accept: application/json" https://api.example.com/data
```

**Common Fixes**:
- ✅ Check endpoint URL (might be hitting error page)
- ✅ Add `Accept` header to request desired format
- ✅ Verify API endpoint returns JSON (check docs)
- ✅ Ensure server sets correct Content-Type header

---

### Quick Reference: Tool Comparison

| Scenario | DevTools | curl | Postman |
|----------|----------|------|---------|
| See request details | ✅ Great UI | ✅ Verbose output | ✅ Best for exploration |
| Test endpoints | ⚠️ Need webpage | ✅ Quick & scriptable | ✅ Easy to use |
| Share requests | ❌ Hard | ⚠️ Copy command | ✅ Collections |
| Automation | ❌ Manual only | ✅ Scripts | ✅ Newman CLI |
| Debug browser issues | ✅ Best tool | ❌ Can't replicate | ❌ Can't replicate |
| Check server response | ✅ Visual | ✅ Raw output | ✅ Pretty formatted |

**Pro Tip**: Use all three tools together!
1. **DevTools** - Debug in browser
2. **curl** - Quick tests and scripts  
3. **Postman** - API exploration and documentation



## Summary and Key Takeaways

✅ **HTTP** is a protocol for client-server communication on the web  
✅ **Request/Response Cycle**: Client asks, server answers  
✅ **Methods** define actions: GET (read), POST (create), PUT (update), DELETE (remove)  
✅ **Status Codes** indicate success (2xx), redirects (3xx), client errors (4xx), server errors (5xx)  
✅ **Headers** provide metadata about requests and responses  
✅ **HTTPS** encrypts HTTP for security  
✅ **Tools** like curl and browser DevTools help debug HTTP traffic

## What's Next?

Now that you understand HTTP, you're ready to learn about **REST APIs** - a structured way to build web services using HTTP!

---

[← Back: Developer Tools Setup](../03-Developer-Tools-Setup/) | [Next: Working With APIs →](../05-Working-With-APIs/)

## Practice

Don't forget to complete the [exercises](./exercises.md) to solidify your understanding!
