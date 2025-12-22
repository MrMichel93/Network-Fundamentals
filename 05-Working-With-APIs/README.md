# 🌐 Working With APIs

Now that you understand HTTP fundamentals, let's put that knowledge into practice by consuming real APIs!

## 🎯 Learning Objectives

By the end of this module, you will:
- Know how to make requests with different tools (curl, HTTPie, Postman, Python)
- Be able to read and understand API documentation
- Handle JSON responses effectively
- Understand error handling and debugging
- Work with query parameters and request bodies
- Practice with real-world public APIs

## What is API Consumption?

**API Consumption** means using an existing API to get data or perform actions. You're the **client** making requests to someone else's **server**.

### Common Use Cases

- Fetching weather data for your app
- Getting user information from social media
- Processing payments with Stripe
- Sending emails via SendGrid
- Searching with Google Maps API

## Reading API Documentation 📚

Good API documentation tells you:
1. **Base URL**: Where the API lives
2. **Endpoints**: What resources are available
3. **Methods**: What HTTP methods to use
4. **Parameters**: What data to send
5. **Authentication**: How to prove who you are
6. **Response format**: What you'll get back
7. **Rate limits**: How many requests you can make
8. **Examples**: Sample requests and responses

### Example: Reading GitHub API Docs

Let's look at the GitHub API for getting a user:

**Endpoint**: `GET /users/:username`  
**Base URL**: `https://api.github.com`  
**Authentication**: Optional (higher rate limits when authenticated)  
**Response**: JSON with user data

**Full URL**: `https://api.github.com/users/octocat`

This tells us everything we need to make the request!

### API Interaction Flow Diagram

Here's a visual representation of the complete API consumption process:

```
API Consumption Flow:

Developer                    Client App                    API Server
    |                            |                             |
    |─── Read API Docs           |                             |
    |                            |                             |
    |─── Write Code              |                             |
    |    (requests.get(...))     |                             |
    |                            |                             |
    |─── Run Program ───────────>|                             |
    |                            |                             |
    |                            |──── HTTP Request ──────────>|
    |                            |     GET /users/123          |
    |                            |     Headers: Auth, Accept   |
    |                            |                             |
    |                            |                             |─── Validate
    |                            |                             |─── Query DB
    |                            |                             |─── Process
    |                            |                             |
    |                            |<─── HTTP Response ──────────|
    |                            |     200 OK                  |
    |                            |     {"id": 123, "name": ...}|
    |                            |                             |
    |                            |─── Parse JSON               |
    |                            |─── Handle Data              |
    |                            |                             |
    |<─── Display Result ────────|                             |
    |    "User: John Doe"        |                             |
```

**Step-by-Step Process:**

1. **Read API Documentation**
   - Understand endpoints, parameters, authentication
   - Note response format and error codes

2. **Write Client Code**
   - Import HTTP library (requests, axios, fetch)
   - Configure request (URL, headers, body)
   - Add authentication if needed

3. **Make HTTP Request**
   - Client sends request to API server
   - Includes method, headers, and data
   - Waits for response

4. **Server Processing**
   - Validates request (auth, params)
   - Queries database if needed
   - Processes business logic
   - Prepares response

5. **Receive Response**
   - Client gets HTTP response
   - Parse JSON/XML data
   - Handle errors (4xx, 5xx)
   - Display or use data

## Making Requests with Python 🐍

Python's `requests` library makes API calls easy.

### Installing requests

```bash
pip install requests
```

### Simple GET Request

```python
import requests

response = requests.get('https://api.github.com/users/octocat')
print(response.status_code)  # 200
print(response.json())        # Dictionary of user data
```

### Checking the Response

```python
import requests

response = requests.get('https://api.github.com/users/octocat')

# Check if successful
if response.status_code == 200:
    data = response.json()
    print(f"User: {data['login']}")
    print(f"Name: {data['name']}")
    print(f"Public repos: {data['public_repos']}")
else:
    print(f"Error: {response.status_code}")
```

### Handling Query Parameters

```python
import requests

# Search for Python repositories
params = {
    'q': 'language:python',
    'sort': 'stars',
    'order': 'desc'
}

response = requests.get(
    'https://api.github.com/search/repositories',
    params=params
)

data = response.json()
print(f"Total results: {data['total_count']}")
```

### POST Request with JSON

```python
import requests

# Create a new post (example API)
data = {
    'title': 'My Post',
    'body': 'This is a test post',
    'userId': 1
}

response = requests.post(
    'https://jsonplaceholder.typicode.com/posts',
    json=data  # Automatically sets Content-Type header
)

print(response.status_code)  # 201 Created
print(response.json())        # Created post with ID
```

### Setting Headers

```python
import requests

headers = {
    'Accept': 'application/json',
    'User-Agent': 'MyApp/1.0'
}

response = requests.get(
    'https://api.github.com/users/octocat',
    headers=headers
)
```

## Handling Responses 📥

### JSON Responses

Most modern APIs return JSON:

```python
import requests

response = requests.get('https://api.github.com/users/octocat')
data = response.json()  # Parse JSON to Python dict

# Access data
print(data['login'])     # Direct access
print(data.get('bio'))   # Safe access (won't error if missing)
```

### Checking Response Status

```python
import requests

response = requests.get('https://api.github.com/users/fakeuser123')

if response.status_code == 200:
    print("Success!")
elif response.status_code == 404:
    print("User not found")
elif response.status_code == 403:
    print("Access forbidden")
else:
    print(f"Error: {response.status_code}")
```

### Using response.ok

```python
import requests

response = requests.get('https://api.github.com/users/octocat')

if response.ok:  # True if status is 200-299
    data = response.json()
    print(data)
else:
    print(f"Request failed: {response.status_code}")
```

## Error Handling 🚨

APIs can fail for many reasons. Always handle errors!

### Common HTTP Errors

- **400 Bad Request**: Your request is malformed
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: You don't have permission
- **404 Not Found**: Resource doesn't exist
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server problem
- **503 Service Unavailable**: Server is down

### Proper Error Handling

```python
import requests

try:
    response = requests.get(
        'https://api.github.com/users/octocat',
        timeout=5  # 5 second timeout
    )
    response.raise_for_status()  # Raises exception for 4xx/5xx
    
    data = response.json()
    print(data['login'])
    
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.ConnectionError:
    print("Failed to connect")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

### Parsing Error Messages

```python
import requests

response = requests.get('https://api.github.com/users/thisdoesntexist123')

if not response.ok:
    try:
        error_data = response.json()
        print(f"Error: {error_data.get('message', 'Unknown error')}")
    except:
        print(f"Error: {response.status_code} - {response.text}")
```

## Working with Public APIs 🌍

### Popular Free APIs for Practice

1. **JSONPlaceholder** - Fake data for testing
   - Base URL: `https://jsonplaceholder.typicode.com`
   - No auth required

2. **OpenWeather** - Weather data
   - Base URL: `https://api.openweathermap.org/data/2.5`
   - Requires free API key

3. **GitHub API** - Repository and user data
   - Base URL: `https://api.github.com`
   - Higher limits with auth

4. **Dog CEO** - Random dog images
   - Base URL: `https://dog.ceo/api`
   - No auth required

5. **REST Countries** - Country information
   - Base URL: `https://restcountries.com/v3.1`
   - No auth required

### Example: Weather API

```python
import requests

# Get your free API key from openweathermap.org
API_KEY = 'your_api_key_here'
city = 'London'

url = f'https://api.openweathermap.org/data/2.5/weather'
params = {
    'q': city,
    'appid': API_KEY,
    'units': 'metric'  # Celsius
}

response = requests.get(url, params=params)

if response.ok:
    data = response.json()
    temp = data['main']['temp']
    description = data['weather'][0]['description']
    print(f"Weather in {city}: {temp}°C, {description}")
else:
    print(f"Error: {response.status_code}")
```

## Best Practices 🎯

### 1. Always Check Status Codes

```python
if response.status_code == 200:
    # Process data
elif response.status_code == 404:
    # Handle not found
```

### 2. Use Timeouts

```python
response = requests.get(url, timeout=10)
```

### 3. Handle Exceptions

```python
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

### 4. Respect Rate Limits

```python
import time

for item in items:
    response = requests.get(f'api/endpoint/{item}')
    time.sleep(1)  # Wait 1 second between requests
```

### 5. Use Sessions for Multiple Requests

```python
import requests

with requests.Session() as session:
    session.headers.update({'User-Agent': 'MyApp/1.0'})
    
    # Headers persist across requests
    response1 = session.get('https://api.github.com/users/user1')
    response2 = session.get('https://api.github.com/users/user2')
```

## Debugging API Requests 🔧

### Print Request Details

```python
import requests

response = requests.get('https://api.github.com/users/octocat')

print(f"URL: {response.url}")
print(f"Status: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"Response time: {response.elapsed.total_seconds()}s")
```

### Use Verbose Mode with curl

```bash
curl -v https://api.github.com/users/octocat
```

Shows full request/response including headers.

### Use HTTPie for Pretty Output

```bash
http https://api.github.com/users/octocat
```

Colored, formatted JSON output.

## Summary and Key Takeaways

✅ **Read documentation** carefully before making requests  
✅ **Use Python requests library** for easy API consumption  
✅ **Always handle errors** - networks fail, APIs change  
✅ **Check status codes** to understand what happened  
✅ **Respect rate limits** to avoid being blocked  
✅ **Use proper timeouts** to avoid hanging forever  
✅ **Parse JSON carefully** - not all fields may exist

## What's Next?

Now that you can work with APIs, you need to understand **Authentication and Authorization** to access protected resources!

---

[← Back: HTTP Fundamentals](../04-HTTP-Fundamentals/) | [Next: Authentication and Authorization →](../06-Authentication-and-Authorization/)

## Practice

Complete the exercises in [exercises.md](./exercises.md) to master API consumption!
