# Project 3: Real-Time Dashboard - Requirements

## Learning Objectives
By completing this project, you will:
- [ ] Understand WebSocket protocol and how it differs from HTTP
- [ ] Implement WebSocket server and client
- [ ] Handle real-time bidirectional communication
- [ ] Manage multiple concurrent connections
- [ ] Process and visualize streaming data
- [ ] Implement connection management and auto-reconnection
- [ ] Work with asynchronous programming
- [ ] Build responsive front-end interfaces
- [ ] Handle connection lifecycle events
- [ ] Broadcast messages to multiple clients

## Requirements

### Functional Requirements

1. **Real-Time Data Streaming**
   - Server continuously sends data to connected clients
   - Multiple types of data streams (metrics, events, updates)
   - Data updates at regular intervals (1-2 seconds)
   - No page refresh required

2. **Live Dashboard Interface**
   - Display real-time system metrics (CPU, memory, network)
   - Show live activity feed
   - Display connection statistics
   - Visualize data with charts
   - Update UI automatically as data arrives

3. **Interactive Controls**
   - Start/stop data streams
   - Pause/resume updates
   - Clear activity feed
   - Manual data refresh

4. **Multi-Client Support**
   - Multiple users can connect simultaneously
   - Each client sees the same data
   - Display active connection count
   - Broadcast updates to all clients

5. **Connection Management**
   - Automatic reconnection on disconnect
   - Exponential backoff for reconnection attempts
   - Connection status indicator
   - Heartbeat/ping-pong to detect dead connections
   - Graceful handling of server restarts

6. **Historical Data**
   - Keep last 50 data points for charts
   - Maintain activity feed history
   - Show data received while disconnected

### Non-Functional Requirements

- **Performance**: 
  - Handle at least 100 concurrent connections
  - UI updates under 100ms latency
  - Minimal CPU usage on client
  
- **Reliability**: 
  - Auto-reconnect on network failure
  - No data loss during reconnection
  - Handle server restarts gracefully
  
- **Usability**: 
  - Clear connection status
  - Smooth animations
  - Responsive design (works on mobile)
  - Intuitive controls
  
- **Scalability**: 
  - Efficient message broadcasting
  - Memory-bounded data storage
  - Handles slow clients without affecting others

## Technical Specifications

**Backend**: Python with `websockets` or `socket.io`  
**Frontend**: HTML5, CSS3, JavaScript (vanilla or with Chart.js)  
**Real-time Protocol**: WebSocket (ws:// or wss://)  
**Data Format**: JSON  
**System Metrics**: `psutil` library (Python)

### WebSocket Message Types

```javascript
// Connection confirmation
{
  "type": "connection",
  "message": "Connected to server",
  "client_count": 5
}

// System metrics
{
  "type": "metrics",
  "cpu": 45.2,
  "memory": 62.8,
  "network_sent": 1024000,
  "network_recv": 2048000,
  "timestamp": "2024-01-15T10:30:00Z"
}

// Activity event
{
  "type": "event",
  "message": "New user connected",
  "level": "info",
  "timestamp": "2024-01-15T10:30:00Z"
}

// Client count update
{
  "type": "client_count",
  "count": 6
}

// Data point for charts
{
  "type": "data",
  "value": 42,
  "label": "Requests",
  "timestamp": "2024-01-15T10:30:00Z"
}

// Ping/pong for keepalive
{
  "type": "ping"
}
{
  "type": "pong"
}
```

## Milestones

### Milestone 1: WebSocket Server (Due: Week 1, Day 1-2)
- [ ] Set up Python WebSocket server
- [ ] Handle client connections
- [ ] Handle client disconnections
- [ ] Broadcast messages to all clients
- [ ] Track connected clients
- [ ] Implement basic error handling

**Success Criteria**: Server accepts connections and broadcasts test messages.

### Milestone 2: System Metrics (Due: Week 1, Day 3-4)
- [ ] Install and configure psutil
- [ ] Collect CPU usage
- [ ] Collect memory usage
- [ ] Collect network I/O statistics
- [ ] Send metrics to clients every second
- [ ] Format metrics as JSON

**Success Criteria**: Server continuously sends system metrics to all clients.

### Milestone 3: Basic Dashboard UI (Due: Week 1, Day 5-7)
- [ ] Create HTML structure
- [ ] Add CSS styling
- [ ] Implement WebSocket client connection
- [ ] Display connection status
- [ ] Show system metrics (text)
- [ ] Display activity feed

**Success Criteria**: Dashboard connects and displays incoming metrics.

### Milestone 4: Data Visualization (Due: Week 2, Day 1-3)
- [ ] Integrate Chart.js library
- [ ] Create real-time line charts
- [ ] Implement data buffering (last 50 points)
- [ ] Create progress bars for metrics
- [ ] Add live counter
- [ ] Smooth chart animations

**Success Criteria**: Dashboard displays live, updating charts.

### Milestone 5: Connection Management (Due: Week 2, Day 4-5)
- [ ] Implement auto-reconnection
- [ ] Add exponential backoff
- [ ] Implement ping/pong heartbeat
- [ ] Show connection status (connected/disconnected)
- [ ] Handle connection errors
- [ ] Queue messages during disconnect

**Success Criteria**: Dashboard reconnects automatically and handles network issues.

### Milestone 6: Polish and Features (Due: Week 2, Day 6-7)
- [ ] Add interactive controls (pause/resume)
- [ ] Improve styling and animations
- [ ] Add responsive design
- [ ] Test with multiple browsers
- [ ] Add error notifications
- [ ] Create comprehensive README

**Success Criteria**: Production-ready dashboard with polished UI.

## Starter Code

### Server (Python with websockets)

```python
#!/usr/bin/env python3
"""
Real-Time Dashboard Server
WebSocket server that streams data to clients.
"""

import asyncio
import websockets
import json

connected_clients = set()

async def handler(websocket):
    """Handle a client connection."""
    # TODO: Add client to set
    # TODO: Send welcome message
    # TODO: Handle incoming messages
    # TODO: Remove client on disconnect
    pass

async def send_metrics():
    """Send system metrics to all clients."""
    while True:
        # TODO: Collect system metrics
        # TODO: Broadcast to all clients
        await asyncio.sleep(1)

async def main():
    """Start the WebSocket server."""
    # TODO: Start background tasks
    # TODO: Start WebSocket server
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
```

### Client (JavaScript)

```javascript
let socket = null;

function connect() {
    socket = new WebSocket('ws://localhost:8765');
    
    socket.onopen = () => {
        console.log('Connected');
        // TODO: Update UI
    };
    
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        // TODO: Handle different message types
    };
    
    socket.onclose = () => {
        console.log('Disconnected');
        // TODO: Attempt reconnection
    };
}

// TODO: Implement message handlers
// TODO: Implement reconnection logic
// TODO: Update UI with incoming data
```

### HTML Structure

```html
<!DOCTYPE html>
<html>
<head>
    <title>Real-Time Dashboard</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="dashboard">
        <header>
            <h1>📊 Real-Time Dashboard</h1>
            <div id="connectionStatus"></div>
        </header>
        
        <div class="widgets">
            <!-- Metrics widget -->
            <div class="widget">
                <h2>System Metrics</h2>
                <div id="metrics"></div>
            </div>
            
            <!-- Chart widget -->
            <div class="widget">
                <h2>Live Data</h2>
                <canvas id="chart"></canvas>
            </div>
            
            <!-- Activity feed -->
            <div class="widget">
                <h2>Activity Feed</h2>
                <div id="feed"></div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="app.js"></script>
</body>
</html>
```

## Testing Checklist

### Functional Testing
- [ ] Server starts without errors
- [ ] Client can connect to server
- [ ] Metrics are sent continuously
- [ ] UI updates in real-time
- [ ] Multiple clients can connect
- [ ] Clients see same data
- [ ] Connection count is accurate
- [ ] Disconnection is handled
- [ ] Reconnection works

### Performance Testing
- [ ] 10 concurrent connections work smoothly
- [ ] UI remains responsive with updates
- [ ] Memory usage is stable (no leaks)
- [ ] CPU usage is reasonable
- [ ] Network bandwidth is acceptable

### Error Handling Testing
- [ ] Server restart handling
- [ ] Network disconnect handling
- [ ] Invalid message handling
- [ ] Client crash handling
- [ ] Slow client handling

### UI Testing
- [ ] Works in Chrome
- [ ] Works in Firefox
- [ ] Works in Safari
- [ ] Works on mobile devices
- [ ] Animations are smooth
- [ ] Charts display correctly
- [ ] Status indicators work

## Rubric

| Criteria | Needs Work (1) | Good (2) | Excellent (3) |
|----------|---------------|----------|---------------|
| **WebSocket Implementation** | Basic connection only | Bidirectional communication works | + Robust error handling + heartbeat |
| **Real-Time Updates** | Manual refresh needed | Auto-updates but laggy | Smooth real-time updates (<100ms) |
| **Multi-Client Support** | Single client only | Multiple clients work | Efficient broadcasting + connection tracking |
| **Connection Management** | No reconnection | Manual reconnection | Auto-reconnect + exponential backoff |
| **Data Visualization** | Text only | Basic charts | Interactive charts + multiple visualizations |
| **UI/UX** | Plain HTML | Styled but basic | Polished, responsive, professional |
| **Code Quality** | Monolithic, unclear | Organized, readable | Modular, well-documented, error handling |

**Scoring**:
- 19-21 points: Excellent (Production-ready)
- 14-18 points: Good (Functional with improvements)
- 7-13 points: Needs Work (Missing key features)
- Below 7: Incomplete

## Extensions (Optional)

### Beginner Extensions
- [ ] Add more metric types (disk usage, temperature)
- [ ] Add timestamp display
- [ ] Color-code activity feed by type
- [ ] Add sound notifications
- [ ] Export data to CSV

### Intermediate Extensions
- [ ] User authentication
- [ ] Multiple dashboard pages
- [ ] Customizable widgets
- [ ] Data filtering options
- [ ] Historical data playback
- [ ] Dark/light theme toggle
- [ ] Configurable update intervals

### Advanced Extensions
- [ ] User accounts with saved preferences
- [ ] Multiple data sources
- [ ] Alert/threshold notifications
- [ ] Widget drag-and-drop
- [ ] Dashboard templates
- [ ] Mobile app version
- [ ] Screen sharing/collaboration mode
- [ ] Data aggregation and analytics
- [ ] Integration with external APIs
- [ ] Real-time log streaming

## Common Pitfalls to Avoid

1. **Not handling disconnections**: Always implement reconnection logic
2. **Memory leaks**: Limit buffered data (e.g., last 50 points only)
3. **Blocking operations**: Use async/await properly, don't block event loop
4. **No error handling**: WebSocket connections fail often, handle it
5. **Slow clients**: Don't let one slow client block others
6. **No heartbeat**: Detect and clean up dead connections
7. **DOM thrashing**: Batch UI updates, use requestAnimationFrame
8. **Not testing with multiple clients**: Always test concurrent connections
9. **Hardcoded URLs**: Make WebSocket URL configurable
10. **No visual feedback**: Always show connection status clearly

## Architecture Considerations

### Server-Side
- Use async/await for concurrent connections
- Implement broadcast efficiently (don't send to each client sequentially)
- Clean up dead connections
- Rate limit data sending
- Handle backpressure (slow clients)

### Client-Side
- Buffer data to smooth out network jitter
- Throttle UI updates (don't update faster than screen refresh)
- Use Web Workers for heavy processing
- Implement proper state management
- Handle visibility API (pause when tab hidden)

## Resources

- [WebSocket Protocol (RFC 6455)](https://tools.ietf.org/html/rfc6455)
- [Python websockets library](https://websockets.readthedocs.io/)
- [JavaScript WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Chart.js Documentation](https://www.chartjs.org/)
- [psutil Documentation](https://psutil.readthedocs.io/)
- [Async Programming in Python](https://docs.python.org/3/library/asyncio.html)
- [Real-Time Web Technologies](https://www.ably.io/topic/websockets)

## Next Steps

Congratulations on completing all three projects! You now have experience with:
- REST APIs (Weather App, URL Shortener)
- WebSockets (Real-Time Dashboard)
- Database operations
- Front-end development
- Real-time data visualization

Consider building your own projects that combine these technologies!

---

[Back to Projects](./README.md)
