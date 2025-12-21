# 🔄 WebSockets: Real-Time Communication

Learn how to build real-time, bidirectional communication applications!

## 🎯 Learning Objectives

By the end of this module, you will:
- Understand what WebSockets are and when to use them
- Learn the WebSocket protocol and handshake process
- Compare WebSockets to HTTP polling and Server-Sent Events
- Build real-time applications with WebSockets
- Understand use cases for real-time communication
- Implement a simple chat application

## What Are WebSockets?

**WebSockets** provide full-duplex (two-way) communication over a single TCP connection. Unlike HTTP, where the client always initiates requests, WebSockets allow both client and server to send messages at any time.

### Real-World Analogy: Phone Call vs Mail 📞✉️

**HTTP (Request/Response):**
- Like sending letters back and forth
- You send a letter (request), wait for reply (response)
- Each exchange starts fresh

**WebSockets:**
- Like a phone call
- Once connected, both sides can talk anytime
- Connection stays open
- Real-time, instant communication

## Why WebSockets?

Traditional HTTP isn't great for real-time features:

### HTTP Polling (The Old Way ❌)
```javascript
// Client keeps asking "any updates?" every second
setInterval(() => {
    fetch('/api/messages')
        .then(res => res.json())
        .then(data => updateUI(data));
}, 1000);
```

**Problems:**
- Wasteful (most requests return "no updates")
- High latency (up to 1 second delay)
- Server load (constant requests)
- Not truly real-time

### WebSockets (The Better Way ✅)
```javascript
// Server pushes updates when they happen
const socket = new WebSocket('ws://localhost:8000');

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    updateUI(data);  // Instant update!
};
```

**Benefits:**
- Truly real-time (no polling delay)
- Efficient (messages only when needed)
- Low latency (instant updates)
- Bidirectional (both sides can send anytime)

## WebSocket Protocol

### Connection Upgrade (HTTP → WebSocket)

WebSockets start as an HTTP request that "upgrades" to WebSocket:

**1. Client sends HTTP request:**
```http
GET /chat HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

**2. Server responds with upgrade:**
```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

**3. Now it's a WebSocket connection!** Both can send messages anytime.

### WebSocket URLs

- `ws://` - WebSocket (like HTTP)
- `wss://` - WebSocket Secure (like HTTPS)

Always use `wss://` in production for encryption!

## WebSocket Message Types

### Text Messages
```javascript
// Send text
socket.send('Hello, server!');

// Send JSON
socket.send(JSON.stringify({
    type: 'chat',
    message: 'Hello!',
    user: 'Alice'
}));
```

### Binary Messages
```javascript
// Send binary data
const buffer = new Uint8Array([1, 2, 3, 4]);
socket.send(buffer);
```

## WebSocket Client (JavaScript)

### Basic Client Example

```javascript
// Create connection
const socket = new WebSocket('ws://localhost:8000');

// Connection opened
socket.addEventListener('open', (event) => {
    console.log('Connected to server');
    socket.send('Hello Server!');
});

// Listen for messages
socket.addEventListener('message', (event) => {
    console.log('Message from server:', event.data);
});

// Connection closed
socket.addEventListener('close', (event) => {
    console.log('Disconnected from server');
});

// Error handling
socket.addEventListener('error', (error) => {
    console.error('WebSocket error:', error);
});
```

### Sending Structured Data

```javascript
function sendMessage(message) {
    const data = {
        type: 'message',
        content: message,
        timestamp: new Date().toISOString(),
        user: getCurrentUser()
    };
    
    socket.send(JSON.stringify(data));
}

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    switch(data.type) {
        case 'message':
            displayMessage(data);
            break;
        case 'user_joined':
            showNotification(`${data.user} joined`);
            break;
        case 'user_left':
            showNotification(`${data.user} left`);
            break;
    }
};
```

## WebSocket Server (Python)

### Simple Server Example

```python
import asyncio
import websockets

async def handler(websocket):
    """Handle a WebSocket connection."""
    print(f"Client connected: {websocket.remote_address}")
    
    try:
        async for message in websocket:
            print(f"Received: {message}")
            
            # Echo message back
            await websocket.send(f"Echo: {message}")
    
    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected")

async def main():
    async with websockets.serve(handler, "localhost", 8000):
        print("WebSocket server started on ws://localhost:8000")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
```

## Use Cases for WebSockets

### Perfect For: ✅

1. **Chat Applications** 💬
   - Instant messaging
   - Group chats
   - Real-time typing indicators

2. **Live Dashboards** 📊
   - Stock prices
   - Analytics dashboards
   - System monitoring

3. **Collaborative Tools** 🤝
   - Google Docs-style editing
   - Shared whiteboards
   - Real-time code editors

4. **Gaming** 🎮
   - Multiplayer games
   - Real-time position updates
   - Game state synchronization

5. **Live Updates** 🔔
   - Notifications
   - News feeds
   - Sports scores

6. **IoT Devices** 🌡️
   - Sensor data streams
   - Device control
   - Real-time monitoring

### Not Great For: ❌

1. **Simple Forms** - Use regular HTTP POST
2. **File Uploads** - Use HTTP with progress events
3. **Static Content** - Use HTTP with caching
4. **RESTful APIs** - Use HTTP for CRUD operations

**Rule of Thumb**: Use WebSockets when you need real-time, bidirectional communication. Use HTTP for everything else.

## Comparison: WebSockets vs Alternatives

### HTTP Polling
```
Client:  Request → Request → Request → Request
Server:  Response  Response  Response  Response
         (no data)  (no data)  (DATA!)   (no data)
```
- Simple to implement
- Wasteful and high latency

### Long Polling
```
Client:  Request ──────────────────→
Server:  ←────────────── Response (when data available)
```
- Better than polling
- Still requires new request each time

### Server-Sent Events (SSE)
```
Client:  Request ──────────────────────────────→
Server:  ←─ Event ←─ Event ←─ Event ←─ Event
```
- One-way (server → client only)
- Simpler than WebSockets
- Good for live feeds, notifications

### WebSockets
```
Client:  ←─ Message ─→ Message ←─ Message ─→
Server:  ←─ Message ─→ Message ←─ Message ─→
```
- Full bidirectional
- Most efficient for real-time
- More complex

## Connection Management

### Heartbeat / Keep-Alive

Prevent connections from timing out:

```javascript
// Client-side heartbeat
const socket = new WebSocket('ws://localhost:8000');

setInterval(() => {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: 'ping' }));
    }
}, 30000);  // Every 30 seconds
```

```python
# Server-side heartbeat
async def heartbeat(websocket):
    while True:
        try:
            await websocket.send(json.dumps({'type': 'ping'}))
            await asyncio.sleep(30)
        except:
            break
```

### Reconnection Logic

```javascript
class ReconnectingWebSocket {
    constructor(url) {
        this.url = url;
        this.reconnectDelay = 1000;
        this.maxReconnectDelay = 30000;
        this.connect();
    }
    
    connect() {
        this.socket = new WebSocket(this.url);
        
        this.socket.onopen = () => {
            console.log('Connected');
            this.reconnectDelay = 1000;  // Reset delay
        };
        
        this.socket.onclose = () => {
            console.log('Disconnected, reconnecting...');
            setTimeout(() => this.connect(), this.reconnectDelay);
            
            // Exponential backoff
            this.reconnectDelay = Math.min(
                this.reconnectDelay * 2,
                this.maxReconnectDelay
            );
        };
    }
    
    send(data) {
        if (this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(data);
        }
    }
}
```

## Common Pitfalls

### ❌ Not Handling Disconnections
```javascript
// Bad: Assumes connection stays open
socket.send(data);  // Might fail if disconnected!
```

```javascript
// Good: Check connection state
if (socket.readyState === WebSocket.OPEN) {
    socket.send(data);
} else {
    console.log('Not connected');
}
```

### ❌ Not Parsing JSON Properly
```javascript
// Bad: Assumes all messages are JSON
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);  // Might fail!
};
```

```javascript
// Good: Handle errors
socket.onmessage = (event) => {
    try {
        const data = JSON.parse(event.data);
        handleData(data);
    } catch (error) {
        console.error('Invalid JSON:', event.data);
    }
};
```

### ❌ Not Implementing Reconnection
- Connections can drop unexpectedly
- Always implement automatic reconnection with exponential backoff

## Security Considerations

1. **Always use WSS (WebSocket Secure)** in production
2. **Authenticate connections** - verify user identity
3. **Validate all messages** - don't trust client data
4. **Rate limit** - prevent abuse
5. **Use origin checking** - prevent unauthorized connections

```python
# Server-side authentication example
async def handler(websocket, path):
    # Get token from query or headers
    token = parse_token(websocket)
    
    if not verify_token(token):
        await websocket.close(1008, "Unauthorized")
        return
    
    # Proceed with authenticated connection
    async for message in websocket:
        # Process message
        pass
```

## Code Examples

Check the `examples/` folder for:
- `websocket_server.py` - Python WebSocket server
- `websocket_client.html` - Browser-based client
- `chat_app/` - Complete chat application

## Summary and Key Takeaways

✅ **WebSockets** enable real-time, bidirectional communication  
✅ **Start as HTTP** then upgrade to WebSocket protocol  
✅ **Perfect for** chat, live updates, collaborative tools, gaming  
✅ **Not needed for** simple forms, file uploads, static content  
✅ **Always implement** reconnection logic and error handling  
✅ **Use WSS** (secure WebSockets) in production  
✅ **Better than polling** for real-time features

## What's Next?

Learn about other network protocols: [Other Protocols](../05-Other-Protocols/)

---

[← Back: REST APIs](../03-REST-APIs/) | [Next: Other Protocols →](../05-Other-Protocols/)

## Practice

Complete the [exercises](./exercises.md) to build real-time applications!
