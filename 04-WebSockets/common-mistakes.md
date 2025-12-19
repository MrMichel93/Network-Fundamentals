# ⚠️ Common Mistakes - WebSockets

Learn from these common pitfalls when working with WebSocket connections.

## Connection Management Mistakes

### 1. Not Handling Connection Lifecycle

**Mistake:**
```javascript
const ws = new WebSocket('ws://example.com');
// Just assume it connects and works forever
ws.send('Hello');  // Might fail if not connected!
```

**Why it's wrong:**
- Connection might not be established yet
- Connection can drop unexpectedly
- No error handling

**Correct:**
```javascript
const ws = new WebSocket('ws://example.com');

ws.onopen = () => {
    console.log('Connected');
    ws.send('Hello');  // Safe to send now
};

ws.onclose = () => {
    console.log('Disconnected');
    // Implement reconnection logic
};

ws.onerror = (error) => {
    console.error('WebSocket error:', error);
};

ws.onmessage = (event) => {
    console.log('Message received:', event.data);
};
```

**Lesson:** Always handle connection lifecycle events (open, close, error, message).

---

### 2. Not Implementing Reconnection Logic

**Mistake:**
```javascript
// Connection drops and never reconnects
ws.onclose = () => {
    console.log('Connection closed');
    // That's it!
};
```

**Why it's wrong:**
- Network issues are common
- Users lose functionality
- Poor user experience

**Correct:**
```javascript
let ws;
let reconnectInterval = 1000;
const maxReconnectInterval = 30000;

function connect() {
    ws = new WebSocket('ws://example.com');
    
    ws.onopen = () => {
        console.log('Connected');
        reconnectInterval = 1000;  // Reset interval
    };
    
    ws.onclose = () => {
        console.log('Disconnected, reconnecting...');
        setTimeout(() => {
            reconnectInterval = Math.min(reconnectInterval * 2, maxReconnectInterval);
            connect();
        }, reconnectInterval);
    };
}

connect();
```

**Lesson:** Implement automatic reconnection with exponential backoff.

---

### 3. Memory Leaks from Not Closing Connections

**Mistake:**
```javascript
// Creating new connections without closing old ones
function setupWebSocket() {
    const ws = new WebSocket('ws://example.com');
    // Never close it
}

// Called multiple times
setupWebSocket();
setupWebSocket();  // Leak!
setupWebSocket();  // More leaks!
```

**Why it's wrong:**
- Multiple open connections
- Memory leaks
- Wasted server resources

**Correct:**
```javascript
let ws = null;

function setupWebSocket() {
    // Close existing connection first
    if (ws) {
        ws.close();
    }
    
    ws = new WebSocket('ws://example.com');
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (ws) {
        ws.close();
    }
});
```

**Lesson:** Always close WebSocket connections when done.

---

## Message Handling Mistakes

### 4. Sending Too Many Messages

**Mistake:**
```javascript
// Sending message on every mouse move
document.addEventListener('mousemove', (e) => {
    ws.send(JSON.stringify({x: e.clientX, y: e.clientY}));
    // Sends hundreds of messages per second!
});
```

**Why it's wrong:**
- Overwhelms the server
- Network congestion
- Poor performance

**Correct:**
```javascript
// Throttle messages
let lastSent = 0;
const throttleMs = 100;  // Send at most every 100ms

document.addEventListener('mousemove', (e) => {
    const now = Date.now();
    if (now - lastSent > throttleMs) {
        ws.send(JSON.stringify({x: e.clientX, y: e.clientY}));
        lastSent = now;
    }
});
```

**Lesson:** Throttle or debounce high-frequency events.

---

### 5. Not Validating Messages

**Mistake:**
```javascript
// Client
ws.send(JSON.stringify({type: 'delete_all'}));  // Dangerous!

// Server
ws.on('message', (data) => {
    const msg = JSON.parse(data);
    if (msg.type === 'delete_all') {
        deleteAllData();  // No validation!
    }
});
```

**Why it's wrong:**
- Security vulnerability
- No access control
- Potential data loss

**Correct:**
```javascript
// Server
ws.on('message', (data) => {
    try {
        const msg = JSON.parse(data);
        
        // Validate message structure
        if (!msg.type || !allowedTypes.includes(msg.type)) {
            ws.send(JSON.stringify({error: 'Invalid message type'}));
            return;
        }
        
        // Check permissions
        if (msg.type === 'delete_all' && !user.isAdmin) {
            ws.send(JSON.stringify({error: 'Unauthorized'}));
            return;
        }
        
        // Process message
        handleMessage(msg);
    } catch (error) {
        ws.send(JSON.stringify({error: 'Invalid JSON'}));
    }
});
```

**Lesson:** Always validate and authorize WebSocket messages.

---

## Security Mistakes

### 6. Using ws:// Instead of wss://

**Mistake:**
```javascript
const ws = new WebSocket('ws://example.com');  // Unencrypted!
```

**Why it's wrong:**
- Data transmitted in plain text
- Vulnerable to man-in-the-middle attacks
- Sensitive data exposed

**Correct:**
```javascript
const ws = new WebSocket('wss://example.com');  // Encrypted
```

**Lesson:** Always use wss:// (WebSocket Secure) in production.

---

### 7. Not Implementing Authentication

**Mistake:**
```javascript
// Server accepts all connections
wss.on('connection', (ws) => {
    // Anyone can connect!
});
```

**Why it's wrong:**
- No access control
- Anyone can connect
- Security breach

**Correct:**
```javascript
// Client: Send auth token
const ws = new WebSocket('wss://example.com');
ws.onopen = () => {
    ws.send(JSON.stringify({
        type: 'auth',
        token: localStorage.getItem('auth_token')
    }));
};

// Server: Verify auth
wss.on('connection', (ws) => {
    let authenticated = false;
    
    ws.on('message', (data) => {
        const msg = JSON.parse(data);
        
        if (!authenticated) {
            if (msg.type === 'auth' && verifyToken(msg.token)) {
                authenticated = true;
                ws.send(JSON.stringify({type: 'auth_success'}));
            } else {
                ws.close(4001, 'Unauthorized');
            }
            return;
        }
        
        // Process authenticated messages
        handleMessage(msg);
    });
});
```

**Lesson:** Always implement authentication for WebSocket connections.

---

## Performance Mistakes

### 8. Sending Large Messages

**Mistake:**
```javascript
// Sending huge images through WebSocket
const image = loadHugeImage();  // 5MB
ws.send(image);  // Blocks everything!
```

**Why it's wrong:**
- Blocks the connection
- Poor performance
- May exceed message size limits

**Correct:**
```javascript
// Send small messages, use HTTP for large files
// Option 1: Upload via HTTP, send URL via WebSocket
const uploadedUrl = await uploadImage(image);
ws.send(JSON.stringify({type: 'image', url: uploadedUrl}));

// Option 2: Send in chunks (if must use WebSocket)
const chunkSize = 64 * 1024;  // 64KB chunks
for (let i = 0; i < image.length; i += chunkSize) {
    const chunk = image.slice(i, i + chunkSize);
    ws.send(chunk);
}
```

**Lesson:** Use WebSockets for small, frequent messages. Use HTTP for large data.

---

### 9. Not Implementing Heartbeat/Ping

**Mistake:**
```javascript
// No way to detect dead connections
// Connection might be dead but still "open"
```

**Why it's wrong:**
- Dead connections accumulate
- Server resources wasted
- Can't detect network issues

**Correct:**
```javascript
// Client: Send ping
setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({type: 'ping'}));
    }
}, 30000);  // Every 30 seconds

// Server: Handle ping and send pong
ws.on('message', (data) => {
    const msg = JSON.parse(data);
    if (msg.type === 'ping') {
        ws.send(JSON.stringify({type: 'pong'}));
    }
});

// Or use built-in ping/pong (ws library)
ws.on('pong', () => {
    ws.isAlive = true;
});

setInterval(() => {
    wss.clients.forEach((ws) => {
        if (ws.isAlive === false) {
            return ws.terminate();
        }
        ws.isAlive = false;
        ws.ping();
    });
}, 30000);
```

**Lesson:** Implement heartbeat to detect and clean up dead connections.

---

## Architecture Mistakes

### 10. Using WebSockets When Not Needed

**Mistake:**
```javascript
// Using WebSocket for a simple API call
ws.send(JSON.stringify({type: 'get_user', id: 123}));
ws.onmessage = (event) => {
    const user = JSON.parse(event.data);
    // Display user
};
```

**Why it's wrong:**
- WebSockets are complex
- Overkill for request-response
- HTTP is simpler and better

**Correct:**
```javascript
// Use HTTP for simple request-response
fetch('https://api.example.com/users/123')
    .then(response => response.json())
    .then(user => {
        // Display user
    });

// Use WebSockets only for:
// - Real-time updates
// - Bidirectional communication
// - Server-initiated messages
```

**Lesson:** Use WebSockets only when you need real-time, bidirectional communication.

---

## Best Practices

### ✅ Do's
1. **Handle all connection events** (open, close, error, message)
2. **Implement reconnection logic** with exponential backoff
3. **Close connections** when done
4. **Use wss://** for security
5. **Implement authentication**
6. **Validate all messages**
7. **Throttle high-frequency events**
8. **Implement heartbeat/ping**

### ❌ Don'ts
1. **Don't assume connection is always open**
2. **Don't use ws:// in production**
3. **Don't skip authentication**
4. **Don't send too many messages**
5. **Don't send large files via WebSocket**
6. **Don't trust client messages**
7. **Don't use WebSockets when HTTP is sufficient**
8. **Don't forget to close connections**

---

## Quick Reference

| Mistake | Impact | Solution |
|---------|--------|----------|
| No reconnection | Lost connection | Implement reconnect logic |
| ws:// not wss:// | Security risk | Use wss:// in production |
| No authentication | Security breach | Validate connections |
| Too many messages | Performance issues | Throttle/debounce |
| Not closing | Memory leaks | Always close connections |
| No heartbeat | Dead connections | Implement ping/pong |

**Next:** Review [WebSockets README](./README.md) and complete [exercises](./exercises.md).
