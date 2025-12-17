# 📊 Project 3: Real-Time Dashboard

**Difficulty**: Advanced  
**Time**: 6-8 hours  
**Concepts**: WebSockets, real-time data, async programming, full-stack

## Project Description

Build a real-time dashboard that displays live data using WebSockets. Think of it like a system monitoring tool, live sports scores, or stock ticker - data updates instantly without refreshing the page.

## Learning Objectives

- Implement WebSocket server and client
- Handle real-time bidirectional communication
- Build a responsive front-end dashboard
- Manage multiple concurrent connections
- Process and visualize streaming data
- Handle connection management and reconnection

## Requirements

### Functional Requirements

1. **Real-time data streaming** from server to multiple clients
2. **Live dashboard** with multiple data widgets
3. **Interactive controls** to start/stop data streams
4. **Multiple clients** can connect simultaneously
5. **Automatic reconnection** if connection drops
6. **Historical data view** (last 50 data points)

### Dashboard Widgets

- System metrics (CPU, Memory, Network)
- Live message feed
- Real-time counter
- Active connections count
- Data visualization (charts)

## Project Structure

```
realtime-dashboard/
├── server.py           # WebSocket server
├── static/
│   ├── index.html     # Dashboard UI
│   ├── style.css      # Styling
│   └── app.js         # Client-side logic
├── requirements.txt
└── README.md
```

## Implementation Guide

### Step 1: WebSocket Server

```python
#!/usr/bin/env python3
"""
Real-Time Dashboard Server

Streams system metrics and demo data to connected clients.
"""

import asyncio
import websockets
import json
import psutil
import random
from datetime import datetime

connected_clients = set()

async def get_system_metrics():
    """Get current system metrics."""
    return {
        'type': 'metrics',
        'cpu': psutil.cpu_percent(interval=0.1),
        'memory': psutil.virtual_memory().percent,
        'network_sent': psutil.net_io_counters().bytes_sent,
        'network_recv': psutil.net_io_counters().bytes_recv,
        'timestamp': datetime.now().isoformat()
    }

async def get_random_data():
    """Generate random data for demo purposes."""
    return {
        'type': 'data',
        'value': random.randint(1, 100),
        'label': random.choice(['Sales', 'Users', 'Requests', 'Views']),
        'timestamp': datetime.now().isoformat()
    }

async def broadcast(message):
    """Broadcast message to all connected clients."""
    if connected_clients:
        await asyncio.gather(
            *[client.send(message) for client in connected_clients],
            return_exceptions=True
        )

async def send_metrics():
    """Continuously send metrics to all clients."""
    while True:
        metrics = await get_system_metrics()
        await broadcast(json.dumps(metrics))
        await asyncio.sleep(1)

async def send_random_data():
    """Continuously send random data."""
    while True:
        data = await get_random_data()
        await broadcast(json.dumps(data))
        await asyncio.sleep(2)

async def handler(websocket):
    """Handle a WebSocket connection."""
    # Register client
    connected_clients.add(websocket)
    client_id = id(websocket)
    print(f"✅ Client {client_id} connected. Total: {len(connected_clients)}")
    
    # Send initial connection info
    await websocket.send(json.dumps({
        'type': 'connection',
        'message': 'Connected to dashboard server',
        'client_count': len(connected_clients)
    }))
    
    # Notify all clients about connection count update
    await broadcast(json.dumps({
        'type': 'client_count',
        'count': len(connected_clients)
    }))
    
    try:
        # Keep connection open and handle incoming messages
        async for message in websocket:
            data = json.loads(message)
            
            if data.get('type') == 'ping':
                await websocket.send(json.dumps({'type': 'pong'}))
            
            elif data.get('type') == 'request_metrics':
                metrics = await get_system_metrics()
                await websocket.send(json.dumps(metrics))
    
    except websockets.exceptions.ConnectionClosed:
        pass
    
    finally:
        # Unregister client
        connected_clients.remove(websocket)
        print(f"👋 Client {client_id} disconnected. Remaining: {len(connected_clients)}")
        
        # Notify remaining clients
        await broadcast(json.dumps({
            'type': 'client_count',
            'count': len(connected_clients)
        }))

async def main():
    """Start the dashboard server."""
    print("""
    ╔════════════════════════════════════════════╗
    ║   📊 Real-Time Dashboard Server           ║
    ╠════════════════════════════════════════════╣
    ║   WebSocket: ws://localhost:8765          ║
    ║   Dashboard: http://localhost:8000        ║
    ╚════════════════════════════════════════════╝
    """)
    
    # Start background tasks
    asyncio.create_task(send_metrics())
    asyncio.create_task(send_random_data())
    
    # Start WebSocket server
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
```

### Step 2: Dashboard HTML (index.html)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>📊 Real-Time Dashboard</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="dashboard">
        <header>
            <h1>📊 Real-Time Dashboard</h1>
            <div class="status">
                <span id="connectionStatus" class="disconnected">●</span>
                <span id="clientCount">0 clients</span>
            </div>
        </header>
        
        <div class="widgets">
            <!-- System Metrics -->
            <div class="widget">
                <h2>💻 System Metrics</h2>
                <div class="metric">
                    <span>CPU:</span>
                    <div class="progress-bar">
                        <div id="cpuBar" class="progress-fill"></div>
                    </div>
                    <span id="cpuValue">0%</span>
                </div>
                <div class="metric">
                    <span>Memory:</span>
                    <div class="progress-bar">
                        <div id="memoryBar" class="progress-fill"></div>
                    </div>
                    <span id="memoryValue">0%</span>
                </div>
            </div>
            
            <!-- Live Counter -->
            <div class="widget">
                <h2>🔢 Live Counter</h2>
                <div class="big-number" id="counter">0</div>
            </div>
            
            <!-- Activity Feed -->
            <div class="widget feed-widget">
                <h2>📡 Activity Feed</h2>
                <div id="activityFeed" class="feed"></div>
            </div>
            
            <!-- Data Chart -->
            <div class="widget chart-widget">
                <h2>📈 Live Data</h2>
                <canvas id="dataChart"></canvas>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="app.js"></script>
</body>
</html>
```

### Step 3: Client JavaScript (app.js)

```javascript
let socket = null;
let reconnectAttempts = 0;
const maxReconnectDelay = 30000;
let chart = null;
const dataPoints = [];
const maxDataPoints = 50;

// Initialize
function init() {
    setupChart();
    connect();
}

// Setup Chart.js
function setupChart() {
    const ctx = document.getElementById('dataChart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Live Data',
                data: [],
                borderColor: '#667eea',
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Connect to WebSocket
function connect() {
    socket = new WebSocket('ws://localhost:8765');
    
    socket.onopen = () => {
        console.log('Connected to dashboard server');
        updateConnectionStatus(true);
        reconnectAttempts = 0;
    };
    
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleMessage(data);
    };
    
    socket.onclose = () => {
        console.log('Disconnected from server');
        updateConnectionStatus(false);
        reconnect();
    };
    
    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
}

// Handle incoming messages
function handleMessage(data) {
    switch(data.type) {
        case 'connection':
            addToFeed(data.message, 'success');
            break;
        
        case 'metrics':
            updateMetrics(data);
            break;
        
        case 'data':
            updateChart(data);
            incrementCounter();
            addToFeed(`New ${data.label}: ${data.value}`, 'info');
            break;
        
        case 'client_count':
            updateClientCount(data.count);
            break;
        
        case 'pong':
            console.log('Pong received');
            break;
    }
}

// Update system metrics
function updateMetrics(data) {
    document.getElementById('cpuValue').textContent = data.cpu.toFixed(1) + '%';
    document.getElementById('cpuBar').style.width = data.cpu + '%';
    
    document.getElementById('memoryValue').textContent = data.memory.toFixed(1) + '%';
    document.getElementById('memoryBar').style.width = data.memory + '%';
}

// Update chart
function updateChart(data) {
    dataPoints.push(data.value);
    if (dataPoints.length > maxDataPoints) {
        dataPoints.shift();
    }
    
    chart.data.labels = dataPoints.map((_, i) => i);
    chart.data.datasets[0].data = dataPoints;
    chart.update();
}

// Increment counter
let counter = 0;
function incrementCounter() {
    counter++;
    document.getElementById('counter').textContent = counter;
}

// Add to activity feed
function addToFeed(message, type = 'info') {
    const feed = document.getElementById('activityFeed');
    const time = new Date().toLocaleTimeString();
    const item = document.createElement('div');
    item.className = `feed-item ${type}`;
    item.innerHTML = `<span class="time">${time}</span> ${message}`;
    feed.insertBefore(item, feed.firstChild);
    
    // Keep only last 20 items
    while (feed.children.length > 20) {
        feed.removeChild(feed.lastChild);
    }
}

// Update connection status
function updateConnectionStatus(connected) {
    const status = document.getElementById('connectionStatus');
    status.className = connected ? 'connected' : 'disconnected';
}

// Update client count
function updateClientCount(count) {
    document.getElementById('clientCount').textContent = `${count} clients`;
}

// Reconnect with exponential backoff
function reconnect() {
    const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), maxReconnectDelay);
    reconnectAttempts++;
    
    console.log(`Reconnecting in ${delay/1000} seconds...`);
    addToFeed(`Reconnecting in ${delay/1000}s...`, 'warning');
    
    setTimeout(connect, delay);
}

// Send heartbeat
setInterval(() => {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: 'ping' }));
    }
}, 30000);

// Initialize on load
window.addEventListener('load', init);
```

## Features to Add

### ⭐ Level 1: Basic Features
- [x] Real-time system metrics
- [x] Live data visualization
- [x] Activity feed
- [x] Connection management

### ⭐⭐ Level 2: Intermediate Features
- [ ] User controls (pause/resume)
- [ ] Multiple chart types
- [ ] Data export (CSV/JSON)
- [ ] Notifications/alerts
- [ ] Theme switcher (dark/light)

### ⭐⭐⭐ Level 3: Advanced Features
- [ ] User authentication
- [ ] Multiple dashboards
- [ ] Custom widget configuration
- [ ] Data filtering
- [ ] Historical data playback
- [ ] Dashboard sharing

## Testing

1. Start the server: `python server.py`
2. Serve the static files: `python -m http.server 8000`
3. Open multiple browser tabs to `http://localhost:8000`
4. Watch data stream in real-time
5. Test disconnection/reconnection

## Success Criteria

- ✅ Real-time data streaming works
- ✅ Multiple clients can connect
- ✅ Dashboard updates without refresh
- ✅ Handles disconnections gracefully
- ✅ Auto-reconnects on connection loss
- ✅ Displays system metrics accurately
- ✅ Responsive and visually appealing UI

## Congratulations! 🎉

You've completed all three projects! You now have hands-on experience with:
- REST APIs and HTTP
- WebSockets and real-time communication
- Database operations
- Full-stack development

---

[Back to Projects](./README.md)
