# 🛠️ Developer Tools Setup

Welcome to Developer Tools! This module will equip you with the essential tools for testing, debugging, and working with networked applications.

## 🎯 Learning Objectives

By the end of this module, you will:
- Master browser DevTools (especially the Network tab)
- Install and use Postman for API testing
- Learn curl basics for command-line HTTP requests
- Understand HTTPie as a user-friendly curl alternative
- Know when to use each tool

## Browser DevTools: Your Best Friend 🌐

Every modern browser includes powerful developer tools built right in. These are essential for any web developer!

### Opening DevTools

**Windows/Linux**:
- Press `F12`
- Or `Ctrl + Shift + I`
- Or right-click on page → "Inspect"

**Mac**:
- Press `Cmd + Option + I`
- Or right-click on page → "Inspect Element"

### The Network Tab - Our Focus 📊

The Network tab shows all HTTP requests your browser makes. This is incredibly valuable for:
- Debugging API calls
- Understanding page load performance
- Inspecting request/response headers
- Viewing response data
- Analyzing timing

#### Network Tab Tutorial

1. **Open DevTools** and click the "Network" tab
2. **Refresh the page** (Ctrl+R / Cmd+R) to see all requests
3. **Click any request** to see details

**What you'll see**:
- **Name**: The file or endpoint requested
- **Status**: HTTP status code (200, 404, etc.)
- **Type**: File type (document, stylesheet, script, xhr, etc.)
- **Initiator**: What triggered this request
- **Size**: How big the response was
- **Time**: How long it took

#### Viewing Request Details

Click on any request to see:

**Headers Tab**:
- Request URL
- Request Method (GET, POST, etc.)
- Status Code
- Request Headers
- Response Headers

**Response Tab**:
- The actual response body
- For JSON: nicely formatted
- For HTML: the source code

**Preview Tab**:
- Rendered preview of the response
- For JSON: interactive tree view

**Timing Tab**:
- Breakdown of request timing
- DNS lookup time
- Connection time
- Server response time

#### Common Debugging Tasks

**Finding failed requests:**
- Look for red status codes (4xx, 5xx)
- Filter by status in the Network tab
- Check error messages in Response tab

**Checking request payload:**
- For POST/PUT requests, view the "Payload" or "Request" tab
- Verify JSON formatting and data values
- Check Content-Type header matches the payload

**Verifying headers:**
- Inspect Request Headers to ensure proper authentication, content-type, etc.
- Check Response Headers for caching, CORS policies
- Look for custom headers your API requires

**Analyzing load time:**
- Sort requests by Time column to find slowest resources
- Use Timing tab to identify bottlenecks (DNS, connection, server response)
- Check for waterfall patterns showing resource dependencies

### Practical Network Tab Exercises

#### Basic Exercise: Inspect a Simple Request

1. Open Network tab
2. Visit https://example.com
3. Click on the first request (should be "example.com")
4. Look at the Headers tab
5. Find:
   - Request Method
   - Status Code
   - Content-Type header
   - User-Agent header

#### Hands-On Exercise 1

Open https://jsonplaceholder.typicode.com and:
1. Open DevTools Network tab
2. Click on the page to trigger requests
3. Find the API request
4. Examine the response
5. Note the status code
6. Check the response time

#### Hands-On Exercise 2

Visit your favorite website and:
1. Clear network log
2. Reload the page
3. How many requests were made?
4. What types of resources loaded?
5. Which request took longest?
6. Any failed requests?

#### Additional Exercise: Filter Requests

The Network tab has filters at the top:
- **All**: Show everything
- **Fetch/XHR**: API calls (very useful!)
- **JS**: JavaScript files
- **CSS**: Stylesheets
- **Img**: Images
- **Doc**: HTML documents

Try visiting a complex website and filtering by different types!

#### Additional Exercise: Throttle Network Speed

Simulate slow connections:
1. Click the dropdown that says "No throttling"
2. Select "Slow 3G"
3. Refresh the page
4. See how it affects load time

This helps you understand how users with slow connections experience your site!

## Postman: The API Swiss Army Knife 🚀

Postman is a graphical tool for testing APIs. It's much more user-friendly than command-line tools for complex requests.

### Installing Postman

1. Go to https://www.postman.com/downloads/
2. Download for your operating system
3. Install and open it
4. Create a free account (optional but recommended)

### Postman Basics

#### Making Your First Request

1. Click the `+` button to create a new request
2. Enter a URL: `https://api.github.com/users/octocat`
3. Make sure method is set to `GET`
4. Click **Send**

You'll see:
- **Status**: 200 OK
- **Time**: Response time
- **Size**: Response size
- **Body**: JSON response with user data

#### Understanding the Interface

**Request Section** (top):
- **Method dropdown**: GET, POST, PUT, DELETE, etc.
- **URL bar**: Where to send the request
- **Params**: Add query parameters
- **Headers**: Set request headers
- **Body**: Add request body (for POST/PUT)

**Response Section** (bottom):
- **Body**: The response data
- **Headers**: Response headers
- **Cookies**: Any cookies set
- **Status**: HTTP status code

#### Setting Headers

1. Go to the "Headers" tab in request section
2. Add header:
   - Key: `Accept`
   - Value: `application/json`
3. Send request

#### Sending JSON Data (POST Request)

1. Change method to `POST`
2. URL: `https://jsonplaceholder.typicode.com/posts`
3. Go to "Body" tab
4. Select "raw" and "JSON" from dropdown
5. Enter:
```json
{
  "title": "My Test Post",
  "body": "This is a test",
  "userId": 1
}
```
6. Click **Send**

#### Saving Requests

1. Click "Save" button
2. Give it a name: "Create Post"
3. Create a collection: "API Practice"
4. Now you can reuse this request anytime!

### Postman Collections

**Collections** organize related requests:
- Group by project
- Share with team
- Export/import

**Create a collection**:
1. Click "New" → "Collection"
2. Name it "Network Fundamentals Practice"
3. Add requests to it

### Hands-On Exercise 1: Public API Practice

Use JSONPlaceholder to:
1. GET a list of posts
2. GET a single post
3. POST a new post
4. PUT to update a post
5. DELETE a post

### Hands-On Exercise 2: Working with Headers

1. Add custom headers
2. Observe how they appear in response
3. Try authentication headers (preview)

## curl: Command-Line HTTP Tool 💻

curl is a powerful command-line tool for making HTTP requests. It's available on almost every system.

### Check if curl is Installed

```bash
curl --version
```

You should see version information. If not installed:
- **Mac**: Pre-installed
- **Linux**: `sudo apt-get install curl` or `sudo yum install curl`
- **Windows**: Download from https://curl.se/windows/

### Basic curl Usage

#### Simple GET Request

```bash
curl https://api.github.com/users/octocat
```

This fetches data and prints it to the terminal.

#### GET Request with Pretty JSON

```bash
curl https://api.github.com/users/octocat | python -m json.tool
```

Or use jq (if installed):
```bash
curl https://api.github.com/users/octocat | jq
```

#### Save Response to File

```bash
curl https://api.github.com/users/octocat -o user.json
```

#### Include Response Headers

```bash
curl -i https://api.github.com/users/octocat
```

#### Only Show Headers

```bash
curl -I https://api.github.com/users/octocat
```

#### POST Request with JSON

```bash
curl -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Post",
    "body": "This is a test",
    "userId": 1
  }'
```

Breakdown:
- `-X POST`: Set HTTP method to POST
- `-H`: Add header
- `-d`: Send data (request body)

#### Set Custom Headers

```bash
curl https://api.github.com/users/octocat \
  -H "Accept: application/json" \
  -H "User-Agent: MyApp/1.0"
```

#### Follow Redirects

```bash
curl -L https://github.com
```

The `-L` flag tells curl to follow redirects.

### Hands-On Exercise 1

Run these commands and observe the output:
```bash
curl https://httpbin.org/get
curl -i https://httpbin.org/status/404
curl -X POST https://httpbin.org/post -d "name=test"
```

### Hands-On Exercise 2: Debug a Website

```bash
curl -v https://www.example.com
```

Analyze:
- DNS resolution time
- TLS handshake
- Headers sent/received
- Response time

### curl Cheat Sheet

```bash
# GET request
curl https://example.com

# POST with data
curl -X POST https://example.com/api -d "key=value"

# POST with JSON
curl -X POST https://example.com/api \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}'

# Custom headers
curl https://example.com -H "Authorization: Bearer token123"

# Show headers
curl -i https://example.com

# Save to file
curl https://example.com -o output.html

# Follow redirects
curl -L https://example.com

# Verbose output (debugging)
curl -v https://example.com
```

## HTTPie: curl for Humans 🎨

HTTPie is a modern, user-friendly alternative to curl with syntax highlighting and intuitive commands.

### Installing HTTPie

**Mac**:
```bash
brew install httpie
```

**Linux**:
```bash
sudo apt-get install httpie
```

**Windows**:
```bash
pip install httpie
```

**Verify installation**:
```bash
http --version
```

### HTTPie Basics

#### Simple GET Request

```bash
http https://api.github.com/users/octocat
```

Much simpler than curl! Output is automatically colored and formatted.

#### POST with JSON (Super Easy!)

```bash
http POST https://jsonplaceholder.typicode.com/posts \
  title="Test Post" \
  body="This is a test" \
  userId:=1
```

Note:
- `title="value"` → JSON string
- `userId:=1` → JSON number (`:=` for non-string)

#### Custom Headers

```bash
http https://api.github.com/users/octocat \
  Accept:application/json \
  User-Agent:MyApp/1.0
```

#### Download File

```bash
http --download https://example.com/file.zip
```

#### Show Only Headers

```bash
http --headers https://api.github.com/users/octocat
```

### Comparison with curl

| Task | curl | HTTPie |
|------|------|--------|
| GET | `curl url` | `http GET url` |
| POST JSON | `curl -X POST url -H "Content-Type: application/json" -d '{"key":"value"}'` | `http POST url key=value` |
| Custom header | `curl -H "X-Custom: value" url` | `http GET url X-Custom:value` |

### Practice Exercise

Do the same requests in both curl and HTTPie, compare ease of use.

### HTTPie vs curl

| Feature | curl | HTTPie |
|---------|------|--------|
| Syntax | More complex | Simpler, cleaner |
| JSON | Manual formatting | Automatic |
| Colors | No | Yes |
| Readability | Good | Better |
| Availability | Everywhere | Needs install |
| Power user features | More | Fewer |

**When to use**:
- **curl**: When you need maximum power or it's the only option available
- **HTTPie**: For interactive use and quick testing

## Tool Comparison Summary 🎯

| Tool | Best For | Pros | Cons |
|------|----------|------|------|
| **Browser DevTools** | Inspecting web pages, debugging frontend | Built-in, visual, powerful | Only for browser requests |
| **Postman** | API development, testing, documentation | User-friendly GUI, save requests, collections | Requires installation, GUI app |
| **curl** | Automation, scripts, quick tests | Everywhere, powerful, scriptable | Command-line syntax can be complex |
| **HTTPie** | Interactive API testing, learning | Beautiful output, simple syntax | Requires installation |

### Recommended Workflow

1. **Learning/Exploring**: Start with browser DevTools and HTTPie
2. **API Testing**: Use Postman for complex requests
3. **Automation**: Use curl in scripts
4. **Quick Tests**: HTTPie for JSON APIs, curl for everything else

## Hands-On Practice

### Exercise Set 1: Try Each Tool

Make the same request with all four tools:

**Request**: Get user data from GitHub API
- URL: `https://api.github.com/users/octocat`
- Method: GET

Try it with:
1. Browser DevTools (visit URL in browser)
2. Postman
3. curl
4. HTTPie

**Compare**: Which was easiest? Which gave you the most information?

### Exercise Set 2: POST Request

Create a new post:
- URL: `https://jsonplaceholder.typicode.com/posts`
- Method: POST
- Body:
```json
{
  "title": "Learning Tools",
  "body": "I'm testing different HTTP tools",
  "userId": 1
}
```

Try with:
1. Postman
2. curl
3. HTTPie

### Exercise Set 3: Headers

Make a request with custom headers:
- URL: `https://httpbin.org/headers`
- Headers:
  - `User-Agent: MyTestApp/1.0`
  - `Accept: application/json`

Try with all tools and verify the headers appear in the response.

## Summary and Key Takeaways

✅ **Browser DevTools** are essential for web development - master the Network tab!  
✅ **Postman** provides a GUI for testing and documenting APIs  
✅ **curl** is the universal command-line HTTP tool  
✅ **HTTPie** offers a more user-friendly command-line experience  
✅ Choose the right tool for the job - they complement each other!

## What's Next?

Now that you have your tools set up, you're ready to dive deep into **HTTP Fundamentals** and start making real requests!

---

[← Back: How The Web Works](../02-How-The-Web-Works/) | [Next: HTTP Fundamentals →](../04-HTTP-Fundamentals/)

## Practice

Complete the exercises in [exercises.md](./exercises.md) to become proficient with these tools!
