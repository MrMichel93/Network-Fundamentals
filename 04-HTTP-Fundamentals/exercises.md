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

<details>
<summary>💡 Hint</summary>

- The first request is usually the HTML document
- Click on a request to see detailed headers
- Look at the "Response Headers" and "Request Headers" sections
- Count all items in the Network list (refresh the page first)
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

**Success Criteria**: You can recognize and explain common status codes.

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
