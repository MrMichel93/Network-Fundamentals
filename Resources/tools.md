# 🛠️ Networking Tools Guide

Essential tools for learning, testing, and debugging networked applications.

## Command-Line Tools

### curl - Make HTTP Requests

**What it does:** Make HTTP requests from the command line

**Installation:**
- Mac/Linux: Usually pre-installed
- Windows: Download from [curl.se](https://curl.se/windows/)

**Basic Usage:**
```bash
# GET request
curl https://api.github.com

# POST request
curl -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}'

# Include response headers
curl -i https://api.github.com

# Save response to file
curl -o output.json https://api.github.com

# Verbose output (debugging)
curl -v https://api.github.com
```

**Learn more:** `curl --help` or `man curl`

---

### ping - Test Network Connectivity

**What it does:** Test if a host is reachable

**Usage:**
```bash
# Basic ping
ping google.com

# Specific number of requests
ping -c 4 google.com   # Mac/Linux
ping -n 4 google.com   # Windows

# Continuous ping (stop with Ctrl+C)
ping google.com
```

**What to check:**
- Response time (lower is better, <50ms is good)
- Packet loss (0% is ideal)
- If host is reachable

---

### traceroute / tracert - Trace Network Path

**What it does:** Show the path data takes to reach a host

**Usage:**
```bash
# Mac/Linux
traceroute google.com

# Windows
tracert google.com
```

**Interpret results:**
- Each line is a "hop" (router)
- Time shows latency to that hop
- `* * *` means router didn't respond (normal)

---

### nslookup - DNS Lookup

**What it does:** Query DNS servers for domain information

**Usage:**
```bash
# Look up domain
nslookup github.com

# Specify DNS server
nslookup github.com 8.8.8.8

# Reverse lookup (IP to domain)
nslookup 8.8.8.8
```

---

### netstat - Network Statistics

**What it does:** Show network connections and statistics

**Usage:**
```bash
# Show all connections
netstat -a

# Show listening ports
netstat -l    # Linux
netstat -an   # Windows

# Show which program is using which port
netstat -tulpn   # Linux
netstat -ano     # Windows
```

---

### dig - DNS Information

**What it does:** Advanced DNS lookups

**Installation:**
```bash
# Mac/Linux (usually pre-installed)
brew install bind   # Mac if needed
sudo apt install dnsutils   # Ubuntu/Debian

# Windows: included in BIND download
```

**Usage:**
```bash
# Basic lookup
dig github.com

# Specific record type
dig github.com MX  # Mail servers
dig github.com A   # IPv4 addresses
dig github.com AAAA  # IPv6 addresses

# Trace DNS resolution
dig +trace github.com

# Short output
dig +short github.com
```

---

## GUI Tools

### Postman - API Testing

**What it does:** Test APIs with a graphical interface

**Download:** [postman.com](https://www.postman.com/downloads/)

**Features:**
- Send HTTP requests (GET, POST, PUT, DELETE, etc.)
- Save requests in collections
- Environment variables
- Automated testing
- Mock servers

**Basic Usage:**
1. Create new request
2. Select HTTP method (GET, POST, etc.)
3. Enter URL
4. Add headers if needed
5. Add body (for POST/PUT)
6. Click "Send"

**Alternatives:**
- **Insomnia** - Similar to Postman
- **Hoppscotch** - Web-based, open source
- **Thunder Client** - VS Code extension

---

### Browser Developer Tools

**What it does:** Inspect network traffic in your browser

**Open DevTools:**
- Chrome/Edge: F12 or Ctrl+Shift+I (Cmd+Opt+I on Mac)
- Firefox: F12 or Ctrl+Shift+I (Cmd+Opt+I on Mac)

**Network Tab:**
- See all HTTP requests
- View request/response headers
- Check status codes
- Measure timing
- Filter by type (XHR, JS, CSS, images)

**Tips:**
- Click "Preserve log" to keep requests when navigating
- Right-click requests to "Copy as cURL"
- Filter by domain or file type
- Use "Disable cache" when testing

---

### Wireshark - Packet Analyzer

**What it does:** Capture and analyze network packets

**Download:** [wireshark.org](https://www.wireshark.org/download.html)

**⚠️ Warning:** Advanced tool, can be overwhelming for beginners

**Basic Usage:**
1. Select network interface
2. Click "Start capturing"
3. Filter traffic (e.g., `http`, `tcp.port == 80`)
4. Click on packets to inspect details
5. Stop capturing

**Common Filters:**
- `http` - HTTP traffic
- `tcp.port == 80` - Port 80 traffic
- `ip.addr == 192.168.1.1` - Specific IP
- `dns` - DNS queries

**When to use:**
- Deep packet inspection
- Network troubleshooting
- Understanding protocols at low level
- Security analysis

---

## Python Libraries

### requests - HTTP for Humans

**Installation:**
```bash
pip install requests
```

**Usage:**
```python
import requests

# GET request
response = requests.get('https://api.github.com')
data = response.json()

# POST request
response = requests.post(
    'https://httpbin.org/post',
    json={'key': 'value'}
)

# Custom headers
headers = {'Authorization': 'Bearer token'}
response = requests.get('https://api.github.com', headers=headers)
```

---

### websockets - WebSocket Client/Server

**Installation:**
```bash
pip install websockets
```

**Usage:**
```python
import asyncio
import websockets

async def client():
    async with websockets.connect('ws://localhost:8000') as ws:
        await ws.send('Hello')
        response = await ws.recv()
        print(response)

asyncio.run(client())
```

---

### Flask - Web Framework

**Installation:**
```bash
pip install flask
```

**Usage:**
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/hello')
def hello():
    return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Online Tools

### JSONPlaceholder - Fake REST API

**URL:** [jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com/)

**What it does:** Free fake API for testing and prototyping

**Endpoints:**
- `/posts` - Blog posts
- `/comments` - Comments
- `/users` - Users
- `/todos` - Todo items

**Example:**
```bash
# GET request
curl https://jsonplaceholder.typicode.com/posts/1

# POST request
curl -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"foo","body":"bar","userId":1}'
```

---

### httpbin - HTTP Testing Service

**URL:** [httpbin.org](https://httpbin.org/)

**What it does:** Test HTTP requests and responses

**Useful endpoints:**
- `/get` - Returns GET data
- `/post` - Returns POST data
- `/status/:code` - Returns specified status code
- `/delay/:seconds` - Delayed response
- `/headers` - Returns request headers
- `/ip` - Returns your IP

---

### WebSocket.org Echo Test

**URL:** [websocket.org/echo.html](https://www.websocket.org/echo.html)

**What it does:** Test WebSocket connections

---

### SSL Labs - Test HTTPS

**URL:** [ssllabs.com/ssltest/](https://www.ssllabs.com/ssltest/)

**What it does:** Analyze SSL/TLS configuration

---

## Browser Extensions

### JSONView

**What it does:** Format JSON in browser

**Install:**
- [Chrome](https://chrome.google.com/webstore/detail/jsonview)
- [Firefox](https://addons.mozilla.org/en-US/firefox/addon/jsonview/)

---

### REST Client (VS Code Extension)

**What it does:** Make HTTP requests directly in VS Code

**Installation:**
1. Open VS Code
2. Extensions (Ctrl+Shift+X)
3. Search "REST Client"
4. Install

**Usage:**
Create `.http` file:
```http
### GET request
GET https://api.github.com/users/octocat

### POST request
POST https://httpbin.org/post
Content-Type: application/json

{
  "name": "Alice",
  "email": "alice@example.com"
}
```

Click "Send Request" above each request.

---

## Debugging Tips

### Check if Service is Running

```bash
# Check specific port
# Mac/Linux
lsof -i :5000

# Windows
netstat -ano | findstr :5000
```

### Test Connectivity

```bash
# Can you reach the host?
ping example.com

# Can you connect to specific port?
telnet example.com 80

# Or use nc (netcat)
nc -zv example.com 80
```

### Monitor Network Traffic

```bash
# Mac
sudo tcpdump -i any port 80

# Linux
sudo tcpdump -i any port 80

# Windows: Use Wireshark
```

### Test DNS

```bash
# Which DNS server am I using?
# Mac/Linux
cat /etc/resolv.conf

# Windows
ipconfig /all

# Test different DNS server
nslookup github.com 8.8.8.8
```

---

## Tool Recommendations by Use Case

### Learning HTTP
- ✅ curl
- ✅ Browser DevTools
- ✅ Postman

### Testing APIs
- ✅ Postman / Insomnia
- ✅ curl
- ✅ Python requests library

### Debugging Network Issues
- ✅ ping
- ✅ traceroute
- ✅ nslookup / dig
- ✅ Browser DevTools

### Real-Time Applications
- ✅ Browser DevTools (WebSocket frames)
- ✅ websocat (WebSocket client)
- ✅ Wireshark (advanced)

### Security Testing
- ✅ SSL Labs
- ✅ OWASP ZAP
- ✅ Burp Suite

---

## Next Steps

1. **Install the essential tools**: curl, Postman, Browser DevTools
2. **Practice with examples** in each module
3. **Experiment** with online testing services
4. **Use DevTools** every time you browse

---

[Back to Resources](./README.md)
