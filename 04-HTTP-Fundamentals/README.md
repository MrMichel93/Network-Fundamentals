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

## HTTP Headers

Headers provide additional information about the request or response. Think of them as metadata or instructions.

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

[← Back: How The Internet Works](../01-How-The-Internet-Works/) | [Next: REST APIs →](../03-REST-APIs/)

## Practice

Don't forget to complete the [exercises](./exercises.md) to solidify your understanding!
