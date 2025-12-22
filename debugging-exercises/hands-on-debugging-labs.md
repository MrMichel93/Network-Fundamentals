# Hands-On Debugging Labs

Practical debugging scenarios to sharpen your network troubleshooting skills. Each lab presents a realistic problem you might encounter when working with APIs.

---

## Lab 1: The Missing Data

### Scenario
You're building a weather app that calls a public weather API, but you're getting empty responses even though the API is working fine for other developers.

### Setup
```bash
# Test the API
curl http://api.weatherapi.com/v1/current.json?q=London
```

### What You'll See
```json
{
  "error": {
    "code": 1002,
    "message": "API key not provided."
  }
}
```

### Your Task
Use DevTools, Postman, or curl to:
1. Identify what's wrong with the request
2. Fix the request to get actual weather data
3. Verify the response includes temperature and conditions

### Learning Objectives
- Understanding API key authentication
- Reading error responses
- Adding headers/query parameters

### Hints

<details>
<summary>Hint 1</summary>
Check the API documentation - what does error code 1002 mean?
</details>

<details>
<summary>Hint 2</summary>
Look at the API documentation for required query parameters
</details>

<details>
<summary>Hint 3</summary>
Most weather APIs require an API key for authentication
</details>

<details>
<summary>Solution</summary>

The API requires an API key in the query parameters:

**Using curl:**
```bash
curl "http://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=London"
```

**Using Postman:**
1. Add query parameter `key` with your API key
2. Add query parameter `q` with city name
3. Send GET request

**Using DevTools:**
```javascript
fetch('http://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=London')
  .then(response => response.json())
  .then(data => console.log(data));
```

**What we learned:**
- Always check API documentation for required parameters
- Error codes often give specific clues
- API keys can be in headers OR query parameters
</details>

---

## Lab 2: The Slow Response

### Scenario
Your API endpoint works correctly but takes 10+ seconds to respond. Users are complaining about the slow performance. You need to identify the bottleneck.

### Setup
```bash
# Simulate slow endpoint
curl -w "\nTime Total: %{time_total}s\n" http://httpbin.org/delay/10
```

### Your Task
1. Measure how long the request takes
2. Identify which phase takes the most time (DNS, connect, transfer, etc.)
3. Determine if the slowness is network or server-side

### Learning Objectives
- Performance debugging
- Understanding request timing breakdown
- Using timing flags in curl

### Hints

<details>
<summary>Hint 1</summary>
Use curl's `-w` flag with timing variables
</details>

<details>
<summary>Hint 2</summary>
Browser DevTools shows timing breakdown in Network tab
</details>

<details>
<summary>Hint 3</summary>
Compare DNS lookup time vs server processing time
</details>

<details>
<summary>Solution</summary>

**Using curl with timing:**
```bash
curl -w "DNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n" \
  -o /dev/null -s http://httpbin.org/delay/10
```

**Output explanation:**
- `DNS lookup`: Time to resolve domain name
- `Connect`: Time to establish TCP connection
- `TTFB` (Time to First Byte): Time until server starts sending data
- `Total`: Complete request time

**Using Browser DevTools:**
1. Open Network tab
2. Make the request
3. Click on request
4. View Timing tab
5. Look at "Waiting (TTFB)" - this is server processing

**What we learned:**
- Most time spent in "waiting" means server is slow
- High DNS time means DNS issues
- High connect time means network latency
- Total time = sum of all phases
</details>

---

## Lab 3: The CORS Conundrum

### Scenario
You're building a frontend that calls your API, but requests are being blocked with CORS errors. The same API works fine in Postman.

### Setup
```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<body>
<script>
fetch('http://api.example.com/users')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
</script>
</body>
</html>
```

### What You'll See (in Console)
```
Access to fetch at 'http://api.example.com/users' from origin 
'http://localhost:3000' has been blocked by CORS policy: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

### Your Task
1. Understand why Postman works but browser doesn't
2. Identify what headers are missing
3. Determine how to fix it (server-side)

### Learning Objectives
- Understanding CORS
- Difference between browser and non-browser requests
- Required CORS headers

### Hints

<details>
<summary>Hint 1</summary>
CORS is a browser security feature - it doesn't affect curl or Postman
</details>

<details>
<summary>Hint 2</summary>
Check the Response headers - is Access-Control-Allow-Origin present?
</details>

<details>
<summary>Hint 3</summary>
CORS issues must be fixed on the server, not the client
</details>

<details>
<summary>Solution</summary>

**Why Postman works:**
- Postman is not a browser
- CORS only affects browser requests
- curl/Postman bypass CORS checks

**Server needs to add headers:**
```python
# Python Flask example
@app.route('/users')
def get_users():
    response = jsonify(users)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
```

```javascript
// Node.js Express example
app.get('/users', (req, res) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.json(users);
});
```

**Verify fix in DevTools:**
1. Network tab
2. Click on request
3. Headers tab
4. Look for "Access-Control-Allow-Origin" in Response Headers

**What we learned:**
- CORS is browser-specific security
- Server must explicitly allow origins
- Can't fix CORS from client-side
- '*' allows all origins (dev only)
</details>

---

## Lab 4: The Mysterious 401

### Scenario
You're testing a protected API endpoint. You have a valid JWT token, but you keep getting 401 Unauthorized errors.

### Setup
```bash
# Your request
curl -H "Authorization: token123abc" http://api.example.com/protected
```

### Response
```json
{
  "error": "Unauthorized",
  "message": "Invalid authorization header format"
}
```

### Your Task
1. Identify what's wrong with the Authorization header
2. Fix the header format
3. Successfully authenticate

### Learning Objectives
- Understanding Bearer token format
- Correct Authorization header syntax
- Debugging authentication issues

### Hints

<details>
<summary>Hint 1</summary>
Check the API documentation - what's the expected format?
</details>

<details>
<summary>Hint 2</summary>
JWT tokens usually require "Bearer" prefix
</details>

<details>
<summary>Hint 3</summary>
Header format: "Authorization: Bearer YOUR_TOKEN"
</details>

<details>
<summary>Solution</summary>

**The Problem:**
Missing "Bearer" prefix in Authorization header

**Correct format:**
```bash
curl -H "Authorization: Bearer token123abc" http://api.example.com/protected
```

**In Postman:**
1. Authorization tab
2. Type: Bearer Token
3. Token: token123abc

**In JavaScript:**
```javascript
fetch('http://api.example.com/protected', {
  headers: {
    'Authorization': 'Bearer token123abc'
  }
});
```

**Common Authorization formats:**
- `Bearer token123` - JWT tokens (most common)
- `Basic base64credentials` - Basic auth
- `Token token123` - Some APIs (GitHub, etc.)
- `API-Key key123` - API key auth

**What we learned:**
- Authorization header has specific format
- "Bearer" is most common for JWTs
- Always check API docs for exact format
- Case-sensitive!
</details>

---

## Lab 5: The Vanishing POST Data

### Scenario
You're sending JSON data to create a new user, but the server says it's not receiving any data.

### Setup
```bash
curl -X POST http://api.example.com/users \
  -d '{"name": "John", "email": "john@example.com"}'
```

### Response
```json
{
  "error": "Bad Request",
  "message": "Request body is empty"
}
```

### Your Task
1. Figure out why the server doesn't see the data
2. Fix the request
3. Successfully create the user

### Learning Objectives
- Understanding Content-Type header
- JSON requests require specific headers
- Request body formats

### Hints

<details>
<summary>Hint 1</summary>
What Content-Type header does the server expect?
</details>

<details>
<summary>Hint 2</summary>
JSON requests need Content-Type: application/json
</details>

<details>
<summary>Hint 3</summary>
Use -H to add headers in curl
</details>

<details>
<summary>Solution</summary>

**The Problem:**
Missing Content-Type header. Server doesn't know the body is JSON.

**Fixed request:**
```bash
curl -X POST http://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com"}'
```

**In Postman:**
1. Method: POST
2. Body tab → raw
3. Select JSON from dropdown (automatically sets Content-Type)
4. Enter JSON data

**In JavaScript:**
```javascript
fetch('http://api.example.com/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'John',
    email: 'john@example.com'
  })
});
```

**What we learned:**
- Content-Type tells server how to parse body
- JSON requires "application/json"
- Form data uses "application/x-www-form-urlencoded"
- Must match actual data format
</details>

---

## Lab 6: The Encoding Error

### Scenario
You're searching an API with a query that includes spaces and special characters, but you're getting unexpected results or errors.

### Setup
```bash
# Your query
curl "http://api.example.com/search?q=hello world&category=tech stuff"
```

### What Might Happen
- Only searches for "hello"
- Treats "world&category=tech" as separate parameter
- Server error or incorrect results

### Your Task
1. Identify why spaces and special characters cause issues
2. Learn proper URL encoding
3. Successfully search with complex queries

### Learning Objectives
- URL encoding rules
- When to encode
- How to encode in different tools

### Hints

<details>
<summary>Hint 1</summary>
Spaces and special characters need to be URL-encoded
</details>

<details>
<summary>Hint 2</summary>
Space becomes %20 or +
</details>

<details>
<summary>Hint 3</summary>
Use --data-urlencode in curl or let tools handle it
</details>

<details>
<summary>Solution</summary>

**The Problem:**
URLs can't contain spaces or certain special characters. Shell also interprets & as "run in background".

**Solutions:**

**Method 1: Quote the URL**
```bash
curl "http://api.example.com/search?q=hello%20world&category=tech%20stuff"
```

**Method 2: Use --data-urlencode (GET)**
```bash
curl -G http://api.example.com/search \
  --data-urlencode "q=hello world" \
  --data-urlencode "category=tech stuff"
```

**Method 3: Use --data-urlencode (POST)**
```bash
curl -X POST http://api.example.com/search \
  --data-urlencode "q=hello world" \
  --data-urlencode "category=tech stuff"
```

**In JavaScript:**
```javascript
const params = new URLSearchParams({
  q: 'hello world',
  category: 'tech stuff'
});
fetch(`http://api.example.com/search?${params}`);
```

**Common encodings:**
- Space: `%20` or `+`
- &: `%26`
- =: `%3D`
- ?: `%3F`
- #: `%23`

**What we learned:**
- URLs must be encoded
- Quote URLs in shell to prevent interpretation
- Modern tools often handle encoding
- Use libraries/functions for encoding
</details>

---

## Lab 7: The Cookie Confusion

### Scenario
You successfully log in to an API and get a session cookie, but when you make the next request, you're told you're not authenticated.

### Setup
```bash
# Login request
curl -X POST http://api.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'

# Response includes: Set-Cookie: session=abc123

# Next request (fails)
curl http://api.example.com/profile
```

### Response
```json
{
  "error": "Unauthorized",
  "message": "No session found"
}
```

### Your Task
1. Understand why the session isn't maintained
2. Learn how to save and send cookies with curl
3. Successfully maintain session across requests

### Learning Objectives
- Cookie-based authentication
- Saving and sending cookies
- Session management

### Hints

<details>
<summary>Hint 1</summary>
curl doesn't automatically save or send cookies
</details>

<details>
<summary>Hint 2</summary>
Use -c to save cookies, -b to send them
</details>

<details>
<summary>Hint 3</summary>
Cookies are stored in a text file
</details>

<details>
<summary>Solution</summary>

**The Problem:**
curl doesn't maintain cookies between requests by default.

**Solution - Save and load cookies:**

```bash
# Step 1: Login and save cookies
curl -X POST http://api.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}' \
  -c cookies.txt

# Step 2: Use saved cookies for next request
curl http://api.example.com/profile \
  -b cookies.txt

# Can also do both at once
curl http://api.example.com/profile \
  -b cookies.txt \
  -c cookies.txt
```

**Manual cookie:**
```bash
curl -H "Cookie: session=abc123" http://api.example.com/profile
```

**In Postman:**
Postman automatically handles cookies within the same session.

**In Browser:**
Browsers automatically save and send cookies.

**View saved cookies:**
```bash
cat cookies.txt
```

**What we learned:**
- Cookies maintain state between requests
- curl requires explicit cookie handling
- -c saves cookies to file
- -b loads cookies from file
- Browsers and Postman handle automatically
</details>

---

## Lab 8: The Redirect Runaround

### Scenario
You're accessing an API endpoint but getting an unexpected HTML response instead of JSON. The status code is 301 Moved Permanently.

### Setup
```bash
curl http://api.example.com/users
```

### Response
```html
<html>
<head><title>301 Moved Permanently</title></head>
<body>
<h1>Moved Permanently</h1>
<p>The document has moved <a href="https://api.example.com/users">here</a>.</p>
</body>
</html>
```

### Your Task
1. Understand what a 301 redirect means
2. Get curl to follow the redirect
3. Successfully retrieve the JSON data

### Learning Objectives
- HTTP redirects (301, 302, 307, 308)
- Following redirects in different tools
- HTTP vs HTTPS redirects

### Hints

<details>
<summary>Hint 1</summary>
curl doesn't follow redirects by default
</details>

<details>
<summary>Hint 2</summary>
Use the -L or --location flag
</details>

<details>
<summary>Hint 3</summary>
Notice the redirect is from http to https
</details>

<details>
<summary>Solution</summary>

**The Problem:**
Server redirects HTTP to HTTPS, but curl doesn't follow by default.

**Solution:**
```bash
# Follow redirects
curl -L http://api.example.com/users

# Or use HTTPS directly
curl https://api.example.com/users
```

**See redirect chain:**
```bash
curl -L -v http://api.example.com/users 2>&1 | grep "< Location:"
```

**In Postman:**
Postman follows redirects automatically (can disable in Settings)

**Redirect types:**
- **301**: Moved Permanently (use new URL from now on)
- **302**: Found (temporary redirect)
- **307**: Temporary Redirect (keep method)
- **308**: Permanent Redirect (keep method)

**View headers without following:**
```bash
curl -I http://api.example.com/users
```

**What we learned:**
- Redirects are common (http→https)
- curl needs -L to follow
- Browsers follow automatically
- Check Location header for new URL
</details>

---

## Lab 9: The Timeout Trouble

### Scenario
You're making a request to a slow API endpoint, but curl keeps timing out before the response arrives.

### Setup
```bash
curl http://api.example.com/heavy-computation
# Request times out after default timeout
```

### Response
```
curl: (28) Operation timed out after 10000 milliseconds
```

### Your Task
1. Understand the difference between connection timeout and response timeout
2. Increase timeouts appropriately
3. Successfully get the response from the slow endpoint

### Learning Objectives
- Connection vs operation timeouts
- Setting timeouts in curl
- When to increase timeouts

### Hints

<details>
<summary>Hint 1</summary>
Default timeout might be too short for slow operations
</details>

<details>
<summary>Hint 2</summary>
Use --max-time to set overall timeout
</details>

<details>
<summary>Hint 3</summary>
Use --connect-timeout for connection phase only
</details>

<details>
<summary>Solution</summary>

**Understanding timeouts:**
- **Connect timeout**: Time to establish connection
- **Max time**: Total time for entire operation

**Solution:**
```bash
# Increase total timeout to 60 seconds
curl --max-time 60 http://api.example.com/heavy-computation

# Set both connect and max time
curl --connect-timeout 10 --max-time 60 http://api.example.com/heavy-computation

# No timeout (wait forever - not recommended)
curl --max-time 0 http://api.example.com/heavy-computation
```

**In Postman:**
Settings → General → Request timeout in ms

**Best practices:**
- Set connect-timeout low (5-10s) - connection should be fast
- Set max-time based on expected operation time
- Don't disable timeouts completely
- Consider server-side timeout limits

**Debugging slow requests:**
```bash
# See timing breakdown
curl -w "\nDNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n" \
  --max-time 60 \
  http://api.example.com/heavy-computation
```

**What we learned:**
- Different timeout types serve different purposes
- Connection timeout should be short
- Operation timeout depends on task
- Always set reasonable timeouts
</details>

---

## Lab 10: The Header Mix-up

### Scenario
You're sending a request with custom headers, but the API isn't recognizing them. You suspect they're not being sent correctly.

### Setup
```bash
curl -X GET http://api.example.com/data \
  -H "X-API-Key: abc123" \
  -H "Accept: application/json"
```

### Response
```json
{
  "error": "Missing required header: x-api-key"
}
```

### Your Task
1. Verify headers are actually being sent
2. Check if headers are case-sensitive
3. Debug and fix header issues

### Learning Objectives
- Headers are case-insensitive per HTTP spec
- How to verify sent headers
- Common header issues

### Hints

<details>
<summary>Hint 1</summary>
Use -v flag to see exactly what's being sent
</details>

<details>
<summary>Hint 2</summary>
Check for typos in header names
</details>

<details>
<summary>Hint 3</summary>
Some servers might be case-sensitive despite spec
</details>

<details>
<summary>Solution</summary>

**Debug - See what's being sent:**
```bash
curl -v -X GET http://api.example.com/data \
  -H "X-API-Key: abc123" \
  -H "Accept: application/json"
```

**Look for these lines in output:**
```
> GET /data HTTP/1.1
> Host: api.example.com
> X-API-Key: abc123
> Accept: application/json
```

**Common header issues:**

**Issue 1: Typo in header name**
```bash
# Wrong: X-Api-Key (should match API docs exactly)
# Correct: X-API-Key
```

**Issue 2: Missing quotes**
```bash
# Can cause issues if value has spaces
curl -H "X-API-Key: my key 123"  # Correct
curl -H X-API-Key: my key 123    # Wrong
```

**Issue 3: Overriding default headers**
```bash
# curl adds some headers by default
# Override them explicitly if needed
curl -H "User-Agent: MyApp/1.0" http://api.example.com
```

**Issue 4: Header order (rare)**
```bash
# Some badly designed APIs care about order
curl -H "Header1: value1" -H "Header2: value2" http://api.example.com
```

**In Postman:**
Headers tab shows what's being sent (including auto-added headers)

**Verify server receives headers:**
Use httpbin.org to test:
```bash
curl -H "X-Custom-Header: test" http://httpbin.org/headers
```

**What we learned:**
- Always verify headers with -v
- Headers should be case-insensitive (but aren't always)
- Quote header values with spaces
- Check API docs for exact header names
- Use httpbin.org for testing
</details>

---

## Practice Tips

### For Each Lab:
1. **Try it yourself first** - Don't jump to hints immediately
2. **Use multiple tools** - Try the same fix in curl, Postman, and DevTools
3. **Read error messages carefully** - They often tell you exactly what's wrong
4. **Check documentation** - Real APIs have docs explaining requirements
5. **Experiment** - Try variations to understand why the fix works

### Common Debugging Steps:
1. Read the error message
2. Check API documentation
3. Verify basics (URL, method, server running)
4. Look at request details (headers, body)
5. Look at response details (status, headers, body)
6. Compare working vs non-working requests
7. Simplify - remove everything non-essential
8. Search for error message online

### Tools Comparison:

| Tool | Best For This Lab |
|------|-------------------|
| curl | Labs 2, 6, 7, 8, 9 (CLI, scripting, timing) |
| Postman | Labs 1, 4, 5, 10 (GUI, saving requests) |
| DevTools | Lab 3 (CORS is browser-specific) |
| All tools | Practice each lab with all tools! |

---

## Next Steps

After completing these labs:

1. **Review [Common Errors](./common-errors-by-tool.md)** - Reference guide for more errors
2. **Practice with real APIs** - Apply these skills to actual APIs
3. **Build something** - Create a project using APIs
4. **Help others** - Debug issues for friends or on forums

---

[← Back to Debugging Exercises](./README.md)
