# 🏋️ Exercises: HTTP Fundamentals

Practice your HTTP skills with these hands-on exercises!

## Exercise 1: Explore HTTP with Browser DevTools 🔍

**Objective**: Learn to inspect HTTP traffic in your browser.

**Tasks**:
1. Open your browser's DevTools (F12)
2. Go to the Network tab
3. Visit https://github.com
4. Find the main HTML document request
5. Answer these questions:
   - What HTTP method was used?
   - What status code was returned?
   - What's the Content-Type?
   - How many total requests were made?
   - What headers were sent?

**Additional Interactive Tasks**:
6. **Trigger a 404 Error**:
   - In the same Network tab, visit https://github.com/this-page-definitely-does-not-exist-12345
   - Find the request that returned 404
   - Look at the Response tab - what does GitHub show you?
   
7. **See a Redirect**:
   - Visit http://github.com (http, not https)
   - Watch for the 301 redirect to https
   - Check the Location header to see where it redirected

8. **Inspect Headers**:
   - Pick any request from the list
   - Click on it and go to Headers tab
   - Find these specific headers:
     - `User-Agent` (Request Headers)
     - `Content-Type` (Response Headers)
     - `Cache-Control` (Response Headers)

<details>
<summary>💡 Hint</summary>

- The first request is usually the HTML document
- Click on a request to see detailed headers
- Look at the "Response Headers" and "Request Headers" sections
- Count all items in the Network list (refresh the page first)
- Red entries are failed requests (404, 500, etc.)
- 301/302 entries show redirects
</details>

**Success Criteria**: You can identify HTTP methods, status codes, and headers in real web traffic.

---

## Exercise 2: curl Practice 🎯

**Objective**: Make HTTP requests using curl.

**Tasks**:
1. Make a GET request to `https://api.github.com/users/octocat`
2. Save the response to a file named `octocat.json`
3. Make a request that shows response headers (`-i` flag)
4. Make a POST request to `https://httpbin.org/post` with JSON data
5. Check the status code without downloading the body

<details>
<summary>💡 Hint</summary>

```bash
# Task 1
curl https://api.github.com/users/octocat

# Task 2
curl -o octocat.json https://api.github.com/users/octocat

# Task 3
curl -i https://api.github.com/users/octocat

# Task 4
curl -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"name":"YourName"}'

# Task 5
curl -I https://api.github.com/users/octocat
# or
curl -o /dev/null -s -w "%{http_code}\n" https://api.github.com/users/octocat
```
</details>

**Success Criteria**: You're comfortable using curl for different HTTP methods.

---

## Exercise 2.5: Postman API Testing 📮

**Objective**: Use Postman to make HTTP requests interactively.

**Setup**:
1. If you don't have Postman, download it from https://www.postman.com/downloads/ or use the web version
2. Create a free account (optional but recommended for saving work)

**Tasks**:

**Part 1: GET Requests**
1. Open Postman and create a new request
2. Set method to GET
3. Enter URL: `https://api.github.com/users/octocat`
4. Click "Send"
5. Observe:
   - Status code (bottom right): Should be 200 OK
   - Response time
   - Response body (JSON data about the user)
   - Headers tab (see response headers)

**Part 2: Testing Different Endpoints**
6. Try these GET requests and note the status codes:
   - `https://api.github.com/users/octocat/repos` (200 - success)
   - `https://api.github.com/users/this-user-does-not-exist-12345` (404 - not found)
   - `https://httpbin.org/status/500` (500 - server error)
   - `https://httpbin.org/delay/3` (200 - but slow, watch the time!)

**Part 3: POST Requests**
7. Create a new request
8. Set method to POST
9. Enter URL: `https://httpbin.org/post`
10. Go to "Body" tab
11. Select "raw" and "JSON" from dropdown
12. Enter JSON:
    ```json
    {
      "name": "Your Name",
      "email": "your.email@example.com",
      "message": "Learning HTTP!"
    }
    ```
13. Click "Send"
14. Check response - httpbin echoes back what you sent

**Part 4: Headers Practice**
15. Create a new GET request to `https://httpbin.org/headers`
16. Go to "Headers" tab
17. Add custom headers:
    - Key: `User-Agent`, Value: `MyApp/1.0`
    - Key: `X-Custom-Header`, Value: `Hello`
18. Send and see your headers echoed back

**Part 5: Authentication**
19. Create request to: `https://httpbin.org/bearer`
20. Go to "Authorization" tab
21. Select type: "Bearer Token"
22. Enter any token: `test-token-12345`
23. Send request - should return 200 with your token

**Part 6: Save Your Work**
24. Create a new Collection called "HTTP Practice"
25. Save all your requests to this collection
26. Try organizing them into folders

<details>
<summary>💡 Hint</summary>

- Use the "Save" button to keep requests for later
- Collections let you group related requests
- Use environments to store variables (base URLs, tokens)
- The "Code" button shows how to make the same request in various languages
- Pre-request Scripts can set up data before requests
</details>

**Success Criteria**: You can confidently use Postman to test APIs, send different types of requests, and understand the responses.

---

## Exercise 3: Build a Simple HTTP Server 🖥️

**Objective**: Create and test your own HTTP server.

**Tasks**:
1. Run the provided `simple_http_server.py`
2. Visit http://localhost:8000 in your browser
3. Test each endpoint using curl:
   - GET /
   - GET /api/data
   - GET /api/user?name=YourName
   - GET /status
4. Try a path that doesn't exist - what status code do you get?

<details>
<summary>💡 Hint</summary>

```bash
# Start the server
python simple_http_server.py

# In another terminal, test endpoints:
curl http://localhost:8000/
curl http://localhost:8000/api/data
curl http://localhost:8000/api/user?name=Alice
curl http://localhost:8000/status
curl -i http://localhost:8000/nonexistent
```

Expected: 404 Not Found for nonexistent paths
</details>

**Success Criteria**: Your server responds correctly to different requests.

---

## Exercise 4: HTTP Client Practice 📱

**Objective**: Make requests programmatically with Python.

**Tasks**:
1. Run `http_client.py` to see examples
2. Modify it to:
   - Search for a different GitHub user
   - Add a custom User-Agent header
   - Handle a 404 error gracefully
3. Write a function that checks if a URL is alive (returns 200)

<details>
<summary>💡 Hint</summary>

```python
import requests

def is_url_alive(url):
    """Check if URL returns 200 OK"""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Test it
print(is_url_alive("https://github.com"))  # Should be True
print(is_url_alive("https://github.com/nonexistent"))  # Should be False
```
</details>

**Success Criteria**: You can make HTTP requests and handle responses in Python.

---

## Exercise 5: Status Code Scavenger Hunt 🔎

**Objective**: Understand different HTTP status codes.

**Tasks**:
Find and document examples of these status codes in the wild:
1. 200 OK
2. 301 Moved Permanently
3. 404 Not Found
4. 500 Internal Server Error

Use httpbin.org to test:
- https://httpbin.org/status/200
- https://httpbin.org/status/301
- https://httpbin.org/status/404
- https://httpbin.org/status/500

<details>
<summary>💡 Hint</summary>

```bash
# Test each status code
curl -i https://httpbin.org/status/200
curl -i https://httpbin.org/status/301
curl -i https://httpbin.org/status/404
curl -i https://httpbin.org/status/500

# Real-world examples:
curl -I https://github.com  # Usually 200
curl -I http://github.com   # 301 to https
curl -I https://github.com/nonexistent  # 404
# 500 errors are server-specific and harder to find intentionally
```
</details>

**Success Criteria**: You understand different HTTP status codes.

---

## Exercise 5.5: Interactive Status Code Practice 🎯

**Objective**: Actively trigger different HTTP status codes to understand them better.

**Tasks**:

**In Your Browser (DevTools Network Tab Open):**

1. **Trigger a 200 OK**:
   - Visit: https://httpbin.org/status/200
   - Verify status in Network tab
   - Click the request → Preview tab shows "OK"

2. **Trigger a 404 Not Found**:
   - Visit: https://github.com/definitelynotarealpage12345
   - See 404 in Network tab
   - Look at GitHub's custom 404 page

3. **Trigger a 301 Redirect**:
   - Visit: http://github.com (note: HTTP not HTTPS)
   - Watch Network tab for 301 status
   - See it redirect to https://github.com
   - Check the Location header

4. **Trigger a 500 Server Error**:
   - Visit: https://httpbin.org/status/500
   - See 500 in Network tab
   - Note: This is simulated, real 500s are server bugs

**With curl:**

5. **See Status Codes in Terminal**:
```bash
# Get just the status code
curl -o /dev/null -s -w "%{http_code}\n" https://httpbin.org/status/200
# Output: 200

curl -o /dev/null -s -w "%{http_code}\n" https://httpbin.org/status/404
# Output: 404

# See full headers
curl -i https://httpbin.org/status/301
```

6. **Test Multiple Status Codes**:
```bash
for code in 200 201 204 301 302 400 401 403 404 500 502 503; do
  echo "Testing $code:"
  if curl -o /dev/null -s -w "  Status: %{http_code}\n" https://httpbin.org/status/$code; then
    echo "  ✓ Success"
  else
    echo "  ✗ Request failed (network issue)"
  fi
  sleep 0.2  # Small delay to be respectful to the server
done
```

**With Postman:**

7. **Create a Status Code Testing Collection**:
   - Create requests for each status code:
     - `https://httpbin.org/status/200`
     - `https://httpbin.org/status/201`
     - `https://httpbin.org/status/400`
     - `https://httpbin.org/status/401`
     - `https://httpbin.org/status/404`
     - `https://httpbin.org/status/500`
   - Save them in a collection
   - Run them all and observe the status codes

8. **Real-World Examples**:
   - 200: `https://api.github.com/users/octocat`
   - 404: `https://api.github.com/users/thisuserdoesnotexist12345`
   - 403: Try accessing a private repo without auth

<details>
<summary>💡 Hint</summary>

- httpbin.org is designed for HTTP testing - perfect for practice!
- Status codes in 200s = Success
- Status codes in 300s = Redirects
- Status codes in 400s = Client errors (you made a mistake)
- Status codes in 500s = Server errors (server's problem)
- Use `-i` with curl to see full response including headers
</details>

**Success Criteria**: You can confidently identify what different status codes mean and know how to trigger them for testing.

---

## Exercise 6: Headers Investigation 🔬

**Objective**: Understand the purpose of common HTTP headers.

**Tasks**:
1. Make a request to any API and identify these headers:
   - Content-Type
   - Content-Length
   - Cache-Control
   - Server
2. Send custom headers in your request:
   - User-Agent
   - Accept
   - Authorization (Bearer token)

<details>
<summary>💡 Hint</summary>

```bash
# See response headers
curl -i https://api.github.com/users/octocat | grep -i "content-type\|content-length\|cache-control\|server"

# Send custom headers
curl -H "User-Agent: MyApp/1.0" \
     -H "Accept: application/json" \
     -H "Authorization: Bearer fake-token" \
     https://httpbin.org/headers
```
</details>

**Success Criteria**: You understand the purpose of key HTTP headers.

---

## Exercise 7: POST Data Practice 📝

**Objective**: Send data to a server using POST.

**Tasks**:
1. Use curl to POST JSON data to `https://httpbin.org/post`
2. Create a Python script that POSTs form data
3. Verify the server received your data correctly

<details>
<summary>💡 Hint</summary>

```bash
# curl POST with JSON
curl -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com"}'
```

```python
# Python POST example
import requests

# POST JSON
response = requests.post(
    'https://httpbin.org/post',
    json={'username': 'alice', 'email': 'alice@example.com'}
)
print(response.json())

# POST form data
response = requests.post(
    'https://httpbin.org/post',
    data={'username': 'alice', 'email': 'alice@example.com'}
)
print(response.json())
```
</details>

**Success Criteria**: You can send data to servers using POST.

---

## Exercise 7.5: Debugging HTTP Requests 🔧

**Objective**: Practice debugging common HTTP issues using the techniques from the lesson.

**Scenario 1: The Broken API Call**

You're trying to get user data but getting errors. Debug it!

```bash
# This request fails - debug it!
curl https://api.github.com/user/octocat
```

**Your Tasks**:
1. Run the command - what error do you get?
2. Check the status code
3. Read the error message
4. Find the correct URL (hint: check GitHub API docs or compare with working examples)
5. Fix it and verify it works

<details>
<summary>💡 Solution</summary>

The URL is wrong! It should be `/users/` (plural) not `/user/`:
```bash
curl https://api.github.com/users/octocat
```
</details>

**Scenario 2: Missing Authentication**

Try to access a protected endpoint:

```bash
curl https://httpbin.org/bearer
```

**Your Tasks**:
1. What status code do you get? (Should be 401)
2. Use DevTools or curl to add a Bearer token
3. Verify it works with authentication

<details>
<summary>💡 Solution</summary>

```bash
curl -H "Authorization: Bearer my-secret-token" https://httpbin.org/bearer
```
</details>

**Scenario 3: Wrong Content-Type**

You're sending JSON but the server doesn't recognize it:

```bash
curl -X POST https://httpbin.org/post \
  -d '{"name":"Alice"}'
```

**Your Tasks**:
1. Run it - it works but check what httpbin thinks you sent
2. The server interprets it as form data, not JSON!
3. Add the correct Content-Type header
4. Verify the server now sees it as JSON

<details>
<summary>💡 Solution</summary>

```bash
curl -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice"}'
```
</details>

**Scenario 4: CORS Investigation**

Open this HTML file in your browser:

```html
<!DOCTYPE html>
<html>
<body>
  <h1>CORS Test</h1>
  <button onclick="makeRequest()">Make Request</button>
  <div id="result"></div>
  
  <script>
    async function makeRequest() {
      try {
        const response = await fetch('https://api.github.com/users/octocat');
        const data = await response.json();
        document.getElementById('result').textContent = JSON.stringify(data, null, 2);
      } catch (error) {
        document.getElementById('result').textContent = 'Error: ' + error.message;
      }
    }
  </script>
</body>
</html>
```

**Your Tasks**:
1. Save as `cors-test.html` and open in browser
2. Click the button - does it work?
3. Check DevTools Network tab
4. Look for CORS headers in Response
5. Why does it work? (GitHub API allows CORS from any origin)

**Scenario 5: Rate Limiting**

```bash
# Make requests to demonstrate rate limiting (be responsible!)
# NOTE: Using a smaller number to avoid exhausting your quota
# GitHub allows 60 requests/hour for unauthenticated users
for i in {1..35}; do
  curl -s https://api.github.com/users/octocat > /dev/null
  echo "Request $i done"
  sleep 1  # Be respectful to the API
done

# Check rate limit status
echo -e "\nChecking rate limit status:"
curl -s https://api.github.com/users/octocat | head -1
```

**Your Tasks**:
1. Run this script
2. Eventually you'll hit rate limit (60 requests/hour for unauthenticated)
3. Check the headers on a failed request:
   ```bash
   curl -i https://api.github.com/users/octocat | grep -i ratelimit
   ```
4. Note the `X-RateLimit-Remaining` and `X-RateLimit-Reset` headers

<details>
<summary>💡 Hint</summary>

- Use `-i` with curl to see response headers
- DevTools Network tab shows all request/response details
- Read error messages carefully - they often tell you what's wrong
- GitHub API docs: https://docs.github.com/rest
</details>

**Success Criteria**: You can identify and fix common HTTP request problems using debugging tools.

---

## Challenge Exercise: Build an API Tester 🚀

**Objective**: Create a tool to test API endpoints.

**Requirements**:
Build a Python script that:
1. Takes a URL as input
2. Makes a GET request
3. Displays:
   - Status code
   - Response time
   - Content type
   - Response size
   - First 100 characters of response
4. Handles errors gracefully

<details>
<summary>💡 Hint</summary>

```python
#!/usr/bin/env python3
import requests
import sys

def test_api(url):
    """Test an API endpoint and display information."""
    try:
        response = requests.get(url, timeout=10)
        
        print(f"URL: {url}")
        print(f"Status: {response.status_code} {response.reason}")
        print(f"Time: {response.elapsed.total_seconds():.3f} seconds")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        print(f"Size: {len(response.content)} bytes")
        print(f"\nPreview: {response.text[:100]}...")
        
    except requests.exceptions.Timeout:
        print(f"❌ Timeout: {url} took too long to respond")
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error: Could not connect to {url}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python api_tester.py <URL>")
        sys.exit(1)
    
    test_api(sys.argv[1])
```

**Usage:**
```bash
python api_tester.py https://api.github.com/users/octocat
```
</details>

**Success Criteria**: Your tool successfully tests and reports on any URL.

---

## Mini-Quiz ✅

1. **What HTTP method should you use to retrieve data?**
   - [ ] POST
   - [ ] GET
   - [ ] DELETE
   - [ ] PUT

2. **What does a 404 status code mean?**
   - [ ] Success
   - [ ] Server Error
   - [ ] Not Found
   - [ ] Unauthorized

3. **Which header specifies the format of the data being sent?**
   - [ ] Accept
   - [ ] User-Agent
   - [ ] Content-Type
   - [ ] Authorization

4. **What's the difference between POST and PUT?**
   - [ ] POST creates, PUT updates
   - [ ] They're the same
   - [ ] POST is faster
   - [ ] PUT is more secure

5. **What does the -i flag do in curl?**
   - [ ] Ignores errors
   - [ ] Includes response headers in output
   - [ ] Makes an interactive request
   - [ ] Installs dependencies

<details>
<summary>Show Answers</summary>

1. **B** - GET (retrieves data without modification)
2. **C** - Not Found (resource doesn't exist)
3. **C** - Content-Type (specifies data format)
4. **A** - POST creates, PUT updates (generally)
5. **B** - Includes response headers in output

**Scoring:**
- 5/5: HTTP expert! 🌟
- 3-4/5: Good understanding! 👍
- 1-2/5: Review the lesson and try again
</details>

---

## Solutions

Complete solutions can be found in [solutions/02-http-solutions.md](../solutions/02-http-solutions.md)

---

[← Back to Lesson](./README.md) | [Next: Working With APIs →](../05-Working-With-APIs/)
