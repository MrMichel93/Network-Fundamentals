# ⚠️ Common Mistakes - HTTP Fundamentals

Learn from these common pitfalls when working with HTTP and web communication.

## HTTP Method Mistakes

### 1. Using GET for Data Modification

**Mistake:**
```python
# Using GET to delete or update data
response = requests.get('https://api.example.com/delete/user/123')
```

**Why it's wrong:**
- GET should be safe and idempotent (read-only)
- Browsers prefetch GET requests
- Can be triggered by crawlers
- Security risk (CSRF attacks)

**Correct:**
```python
# Use appropriate HTTP methods
response = requests.delete('https://api.example.com/users/123')
response = requests.put('https://api.example.com/users/123', data={'name': 'John'})
```

**Lesson:** Use POST/PUT/DELETE for modifications, GET only for retrieval.

---

### 2. Confusing POST vs PUT

**Mistake:**
Not understanding when to use POST vs PUT.

**Correct understanding:**
- **POST:** Create new resources (server assigns ID)
- **PUT:** Update existing resources (client provides ID) or create with known ID
- **POST** is not idempotent, **PUT** is idempotent

**Examples:**
```python
# POST - Create new user (server assigns ID)
POST /users
Body: {"name": "Alice"}
Response: {"id": 123, "name": "Alice"}

# PUT - Update specific user (client knows ID)
PUT /users/123
Body: {"name": "Alice Updated"}
Response: {"id": 123, "name": "Alice Updated"}
```

**Lesson:** POST creates without knowing ID, PUT updates/creates with known ID.

---

## Status Code Mistakes

### 3. Ignoring Status Codes

**Mistake:**
```python
response = requests.get('https://api.example.com/data')
data = response.json()  # Might fail!
```

**Why it's wrong:**
- Assumes request succeeded
- Doesn't handle errors
- Can cause crashes

**Correct:**
```python
response = requests.get('https://api.example.com/data')
if response.status_code == 200:
    data = response.json()
elif response.status_code == 404:
    print("Resource not found")
elif response.status_code >= 500:
    print("Server error")
else:
    print(f"Error: {response.status_code}")
```

**Lesson:** Always check status codes before processing responses.

---

### 4. Misusing Status Codes

**Mistake:**
```python
# Returning 200 OK for errors
return Response({"error": "User not found"}, status=200)
```

**Why it's wrong:**
- Status code doesn't match the actual result
- Clients can't properly handle errors
- Breaks HTTP semantics

**Correct:**
```python
# Use appropriate status codes
return Response({"error": "User not found"}, status=404)
return Response({"error": "Invalid data"}, status=400)
return Response({"error": "Not authorized"}, status=401)
```

**Common status codes:**
- 200: Success
- 201: Created
- 400: Bad request
- 401: Unauthorized
- 404: Not found
- 500: Server error

**Lesson:** Status codes should accurately reflect the response outcome.

---

## Header Mistakes

### 5. Forgetting Content-Type Header

**Mistake:**
```python
# Sending JSON without Content-Type
response = requests.post('https://api.example.com/data',
                        data='{"name": "Alice"}')
```

**Why it's wrong:**
- Server doesn't know data format
- May reject or misinterpret data

**Correct:**
```python
# Specify Content-Type
response = requests.post('https://api.example.com/data',
                        json={"name": "Alice"},  # Sets Content-Type automatically
                        headers={'Content-Type': 'application/json'})
```

**Lesson:** Always specify Content-Type when sending data.

---

### 6. Not Handling CORS

**Mistake:**
Making AJAX requests without understanding CORS.

**Problem:**
```javascript
// Browser blocks this!
fetch('https://api.otherdomain.com/data')
  .then(response => response.json())
// Error: CORS policy blocked
```

**Solution (server-side):**
```python
# Server must include CORS headers
response.headers['Access-Control-Allow-Origin'] = '*'
response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT'
```

**Lesson:** CORS is a browser security feature. Server must explicitly allow cross-origin requests.

---

## Request/Response Mistakes

### 7. Not URL Encoding Parameters

**Mistake:**
```python
# Spaces and special characters not encoded
url = 'https://api.example.com/search?q=hello world&lang=en'
```

**Why it's wrong:**
- Spaces and special characters break URLs
- Can cause parsing errors

**Correct:**
```python
# URL encode parameters
import urllib.parse
params = {'q': 'hello world', 'lang': 'en'}
url = 'https://api.example.com/search?' + urllib.parse.urlencode(params)
# Result: https://api.example.com/search?q=hello+world&lang=en

# Or use requests library
response = requests.get('https://api.example.com/search', params=params)
```

**Lesson:** Always URL-encode query parameters.

---

### 8. Exposing Sensitive Data in URLs

**Mistake:**
```python
# Password in URL!
url = 'https://api.example.com/login?password=secret123'
```

**Why it's wrong:**
- URLs are logged in browser history
- URLs appear in server logs
- Can be shared accidentally

**Correct:**
```python
# Send sensitive data in request body
response = requests.post('https://api.example.com/login',
                        json={'password': 'secret123'})
```

**Lesson:** Never put sensitive data in URLs. Use request body instead.

---

## Caching Mistakes

### 9. Not Understanding Browser Caching

**Mistake:**
Wondering why changes don't appear after updating resources.

**Problem:**
- Browser caches responses based on Cache-Control headers
- Old data served from cache

**Solution:**
```python
# Server: Control caching with headers
response.headers['Cache-Control'] = 'no-cache'  # Don't cache
response.headers['Cache-Control'] = 'max-age=3600'  # Cache for 1 hour

# Client: Force fresh request
response = requests.get(url, headers={'Cache-Control': 'no-cache'})
```

**Lesson:** Understand caching headers to control when content is cached.

---

## Security Mistakes

### 10. Using HTTP Instead of HTTPS

**Mistake:**
```python
response = requests.get('http://api.example.com/data')
```

**Why it's wrong:**
- Data transmitted in plain text
- Vulnerable to man-in-the-middle attacks
- Passwords and sensitive data exposed

**Correct:**
```python
# Always use HTTPS
response = requests.get('https://api.example.com/data')
```

**Lesson:** Always use HTTPS for any sensitive data or authentication.

---

### 11. Not Validating Input

**Mistake:**
```python
# Directly using user input
@app.route('/user/<user_id>')
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    # SQL injection risk!
```

**Why it's wrong:**
- Vulnerable to injection attacks
- Can expose or modify data

**Correct:**
```python
# Validate and sanitize input
@app.route('/user/<int:user_id>')  # Type constraint
def get_user(user_id):
    if user_id < 0:
        return "Invalid ID", 400
    # Use parameterized queries
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
```

**Lesson:** Always validate and sanitize user input.

---

## Best Practices

### ✅ Do's
1. **Use appropriate HTTP methods** (GET, POST, PUT, DELETE)
2. **Check status codes** before processing responses
3. **Set correct headers** (Content-Type, Accept, etc.)
4. **Use HTTPS** for sensitive data
5. **Encode URLs** properly
6. **Handle errors** gracefully
7. **Understand caching** behavior

### ❌ Don'ts
1. **Don't use GET for modifications**
2. **Don't ignore status codes**
3. **Don't put sensitive data in URLs**
4. **Don't forget Content-Type headers**
5. **Don't ignore CORS errors**
6. **Don't use HTTP for sensitive data**
7. **Don't trust user input**

---

## Quick Reference

| Mistake | Impact | Solution |
|---------|--------|----------|
| GET for modifications | Security risk | Use POST/PUT/DELETE |
| Ignoring status codes | Crashes | Always check codes |
| Missing Content-Type | Server errors | Set appropriate headers |
| HTTP instead of HTTPS | Data exposure | Always use HTTPS |
| Unencoded URLs | Parsing errors | URL encode parameters |
| CORS errors | Blocked requests | Configure CORS headers |

**Next:** Review [HTTP Fundamentals README](./README.md) and complete [exercises](./exercises.md).
