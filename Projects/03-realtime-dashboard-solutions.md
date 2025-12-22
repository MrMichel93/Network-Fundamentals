# Real-Time Dashboard - Solutions

This document provides three different implementations of the Real-Time Dashboard, each demonstrating different levels of complexity and WebSocket mastery.

## Approach 1: Beginner (Basic but Working)

A simple implementation to understand WebSocket basics and get a working real-time dashboard.

### Features
- WebSocket server with Python
- Basic client connection
- Real-time data streaming
- Simple HTML dashboard
- Connection management

### Server Code (server.py)

```python
#!/usr/bin/env python3
"""
Real-Time Dashboard Server - Beginner Approach
Simple WebSocket server that broadcasts system metrics.
"""

import asyncio
import websockets
import json
import random
from datetime import datetime

# Store all connected clients
connected_clients = set()

async def get_system_metrics():
    """Get current system metrics (simplified with random data)."""
    return {
        'type': 'metrics',
        'cpu': random.uniform(10, 90),
        'memory': random.uniform(30, 80),
        'timestamp': datetime.now().isoformat()
    }

async def broadcast(message):
    """Send message to all connected clients."""
    if connected_clients:
        # Send to all clients simultaneously
        await asyncio.gather(
            *[client.send(message) for client in connected_clients],
            return_exceptions=True
        )

async def send_metrics_loop():
    """Continuously send metrics to all clients."""
    while True:
        metrics = await get_system_metrics()
        message = json.dumps(metrics)
        await broadcast(message)
        await asyncio.sleep(1)  # Send every second

async def handler(websocket):
    """Handle a WebSocket connection."""
    # Add client to our set
    connected_clients.add(websocket)
    print(f"✅ Client connected. Total clients: {len(connected_clients)}")
    
    # Send welcome message
    welcome = {
        'type': 'connection',
        'message': 'Connected to dashboard',
        'client_count': len(connected_clients)
    }
    await websocket.send(json.dumps(welcome))
    
    # Notify all clients about new connection count
    count_update = {
        'type': 'client_count',
        'count': len(connected_clients)
    }
    await broadcast(json.dumps(count_update))
    
    try:
        # Keep connection alive and handle incoming messages
        async for message in websocket:
            # Echo back or handle specific commands
            data = json.loads(message)
            print(f"Received: {data}")
            
            if data.get('type') == 'ping':
                await websocket.send(json.dumps({'type': 'pong'}))
    
    except websockets.exceptions.ConnectionClosed:
        pass
    
    finally:
        # Remove client when disconnected
        connected_clients.remove(websocket)
        print(f"👋 Client disconnected. Remaining: {len(connected_clients)}")
        
        # Notify remaining clients
        count_update = {
            'type': 'client_count',
            'count': len(connected_clients)
        }
        await broadcast(json.dumps(count_update))

async def main():
    """Start the WebSocket server."""
    print("="*50)
    print("📊 Real-Time Dashboard Server")
    print("="*50)
    print("WebSocket: ws://localhost:8765")
    print("Dashboard: Open index.html in browser")
    print("="*50)
    
    # Start background task to send metrics
    asyncio.create_task(send_metrics_loop())
    
    # Start WebSocket server
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
```

### Client Code (index.html)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 Real-Time Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .dashboard {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #333;
        }
        
        .status {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #ccc;
        }
        
        .status-indicator.connected {
            background: #10b981;
            box-shadow: 0 0 10px #10b981;
        }
        
        .widgets {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .widget {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .widget h2 {
            margin-bottom: 15px;
            color: #667eea;
        }
        
        .metric {
            margin: 15px 0;
        }
        
        .metric-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
            color: #666;
        }
        
        .progress-bar {
            height: 20px;
            background: #e5e7eb;
            border-radius: 10px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.3s ease;
        }
        
        .feed {
            max-height: 300px;
            overflow-y: auto;
        }
        
        .feed-item {
            padding: 10px;
            margin: 5px 0;
            background: #f3f4f6;
            border-radius: 5px;
            font-size: 14px;
        }
        
        .feed-item .time {
            color: #667eea;
            font-weight: bold;
            margin-right: 10px;
        }
        
        .big-number {
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <header>
            <h1>📊 Real-Time Dashboard</h1>
            <div class="status">
                <div id="statusIndicator" class="status-indicator"></div>
                <span id="statusText">Connecting...</span>
                <span id="clientCount">0 clients</span>
            </div>
        </header>
        
        <div class="widgets">
            <!-- System Metrics -->
            <div class="widget">
                <h2>💻 System Metrics</h2>
                <div class="metric">
                    <div class="metric-label">
                        <span>CPU Usage</span>
                        <span id="cpuValue">0%</span>
                    </div>
                    <div class="progress-bar">
                        <div id="cpuBar" class="progress-fill" style="width: 0%"></div>
                    </div>
                </div>
                <div class="metric">
                    <div class="metric-label">
                        <span>Memory Usage</span>
                        <span id="memoryValue">0%</span>
                    </div>
                    <div class="progress-bar">
                        <div id="memoryBar" class="progress-fill" style="width: 0%"></div>
                    </div>
                </div>
            </div>
            
            <!-- Live Counter -->
            <div class="widget">
                <h2>🔢 Updates Received</h2>
                <div class="big-number" id="counter">0</div>
            </div>
            
            <!-- Activity Feed -->
            <div class="widget">
                <h2>📡 Activity Feed</h2>
                <div id="feed" class="feed"></div>
            </div>
        </div>
    </div>
    
    <script>
        let socket = null;
        let reconnectAttempts = 0;
        let updateCounter = 0;
        
        // Connect to WebSocket server
        function connect() {
            socket = new WebSocket('ws://localhost:8765');
            
            socket.onopen = () => {
                console.log('Connected to server');
                updateStatus(true);
                reconnectAttempts = 0;
                addToFeed('Connected to server', 'success');
            };
            
            socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                handleMessage(data);
            };
            
            socket.onclose = () => {
                console.log('Disconnected from server');
                updateStatus(false);
                addToFeed('Disconnected from server', 'error');
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
                    addToFeed(data.message, 'info');
                    break;
                
                case 'metrics':
                    updateMetrics(data);
                    updateCounter++;
                    document.getElementById('counter').textContent = updateCounter;
                    break;
                
                case 'client_count':
                    document.getElementById('clientCount').textContent = 
                        `${data.count} client${data.count !== 1 ? 's' : ''}`;
                    break;
                
                case 'pong':
                    console.log('Pong received');
                    break;
            }
        }
        
        // Update system metrics display
        function updateMetrics(data) {
            const cpu = data.cpu.toFixed(1);
            const memory = data.memory.toFixed(1);
            
            document.getElementById('cpuValue').textContent = cpu + '%';
            document.getElementById('cpuBar').style.width = cpu + '%';
            
            document.getElementById('memoryValue').textContent = memory + '%';
            document.getElementById('memoryBar').style.width = memory + '%';
        }
        
        // Update connection status
        function updateStatus(connected) {
            const indicator = document.getElementById('statusIndicator');
            const text = document.getElementById('statusText');
            
            if (connected) {
                indicator.classList.add('connected');
                text.textContent = 'Connected';
            } else {
                indicator.classList.remove('connected');
                text.textContent = 'Disconnected';
            }
        }
        
        // Add item to activity feed
        function addToFeed(message, type) {
            const feed = document.getElementById('feed');
            const time = new Date().toLocaleTimeString();
            const item = document.createElement('div');
            item.className = 'feed-item';
            item.innerHTML = `<span class="time">${time}</span>${message}`;
            
            feed.insertBefore(item, feed.firstChild);
            
            // Keep only last 20 items
            while (feed.children.length > 20) {
                feed.removeChild(feed.lastChild);
            }
        }
        
        // Reconnect with delay
        function reconnect() {
            const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000);
            reconnectAttempts++;
            
            console.log(`Reconnecting in ${delay/1000} seconds...`);
            addToFeed(`Reconnecting in ${delay/1000}s...`, 'info');
            
            setTimeout(connect, delay);
        }
        
        // Send heartbeat every 30 seconds
        setInterval(() => {
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({ type: 'ping' }));
            }
        }, 30000);
        
        // Connect when page loads
        window.addEventListener('load', connect);
    </script>
</body>
</html>
```

### Running the Application

1. Install dependencies:
```bash
pip install websockets
```

2. Start the server:
```bash
python server.py
```

3. Open `index.html` in a web browser

### Pros
✅ Simple and easy to understand  
✅ Complete working example  
✅ Good for learning WebSocket basics  
✅ Self-contained (no build tools needed)  

### Cons
❌ Uses random data instead of real metrics  
❌ No data visualization (charts)  
❌ Basic styling  
❌ No advanced features  

---

## Approach 2: Intermediate (Better Practices)

This approach adds real system metrics, data visualization with charts, and better code organization.

### Additional Features
- Real system metrics using psutil
- Live charts with Chart.js
- Better error handling
- Improved UI design
- Multiple data streams

### Enhanced Server (server.py)

```python
#!/usr/bin/env python3
"""
Real-Time Dashboard Server - Intermediate Approach
WebSocket server with real system metrics and multiple data streams.
"""

import asyncio
import websockets
import json
import psutil
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

connected_clients = set()

async def get_system_metrics():
    """Get real system metrics using psutil."""
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        # Use platform-appropriate disk path
        try:
            disk = psutil.disk_usage('/')
        except:
            # Fallback for Windows
            import os
            disk = psutil.disk_usage(os.path.abspath(os.sep))
        net_io = psutil.net_io_counters()
        
        return {
            'type': 'metrics',
            'cpu': cpu_percent,
            'memory': memory.percent,
            'disk': disk.percent,
            'network_sent': net_io.bytes_sent,
            'network_recv': net_io.bytes_recv,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return None

async def get_random_data():
    """Generate random data for demo charts."""
    import random
    return {
        'type': 'data',
        'value': random.randint(20, 100),
        'label': random.choice(['Requests', 'Users', 'Sales', 'Views']),
        'timestamp': datetime.now().isoformat()
    }

async def broadcast(message):
    """Broadcast message to all connected clients."""
    if not connected_clients:
        return
    
    # Send to all clients concurrently
    results = await asyncio.gather(
        *[client.send(message) for client in connected_clients],
        return_exceptions=True
    )
    
    # Check for errors
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.warning(f"Error sending to client: {result}")

async def send_metrics():
    """Continuously send system metrics."""
    logger.info("Starting metrics broadcast")
    while True:
        try:
            metrics = await get_system_metrics()
            if metrics:
                await broadcast(json.dumps(metrics))
            await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Error in metrics loop: {e}")
            await asyncio.sleep(1)

async def send_random_data():
    """Continuously send random data."""
    logger.info("Starting random data broadcast")
    while True:
        try:
            data = await get_random_data()
            await broadcast(json.dumps(data))
            await asyncio.sleep(2)
        except Exception as e:
            logger.error(f"Error in data loop: {e}")
            await asyncio.sleep(2)

async def handler(websocket):
    """Handle WebSocket connection."""
    client_id = id(websocket)
    
    # Register client
    connected_clients.add(websocket)
    logger.info(f"Client {client_id} connected. Total: {len(connected_clients)}")
    
    # Send welcome message
    welcome = {
        'type': 'connection',
        'message': 'Connected to Real-Time Dashboard',
        'client_id': client_id,
        'client_count': len(connected_clients)
    }
    await websocket.send(json.dumps(welcome))
    
    # Notify all clients of connection count
    await broadcast(json.dumps({
        'type': 'client_count',
        'count': len(connected_clients)
    }))
    
    try:
        # Handle incoming messages
        async for message in websocket:
            try:
                data = json.loads(message)
                logger.debug(f"Received from {client_id}: {data}")
                
                if data.get('type') == 'ping':
                    await websocket.send(json.dumps({'type': 'pong'}))
                
                elif data.get('type') == 'request_metrics':
                    metrics = await get_system_metrics()
                    if metrics:
                        await websocket.send(json.dumps(metrics))
            
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON from client {client_id}")
            
            except Exception as e:
                logger.error(f"Error handling message from {client_id}: {e}")
    
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Client {client_id} connection closed normally")
    
    except Exception as e:
        logger.error(f"Error with client {client_id}: {e}")
    
    finally:
        # Unregister client
        connected_clients.remove(websocket)
        logger.info(f"Client {client_id} disconnected. Remaining: {len(connected_clients)}")
        
        # Notify remaining clients
        await broadcast(json.dumps({
            'type': 'client_count',
            'count': len(connected_clients)
        }))

async def cleanup_dead_connections():
    """Periodically clean up dead connections."""
    while True:
        await asyncio.sleep(60)
        
        dead_clients = []
        for client in connected_clients:
            if client.closed:
                dead_clients.append(client)
        
        for client in dead_clients:
            connected_clients.remove(client)
            logger.info(f"Cleaned up dead connection")

async def main():
    """Start the dashboard server."""
    logger.info("="*60)
    logger.info("📊 Real-Time Dashboard Server v2.0")
    logger.info("="*60)
    logger.info("WebSocket: ws://localhost:8765")
    logger.info("Open static/index.html in browser")
    logger.info("="*60)
    
    # Start background tasks
    asyncio.create_task(send_metrics())
    asyncio.create_task(send_random_data())
    asyncio.create_task(cleanup_dead_connections())
    
    # Start WebSocket server
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
```

### Enhanced Client with Charts (app.js)

```javascript
// Dashboard Application - Intermediate Approach

let socket = null;
let reconnectAttempts = 0;
const maxReconnectDelay = 30000;
let chart = null;
const dataPoints = [];
const maxDataPoints = 50;

// Initialize dashboard
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
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 500
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Connect to WebSocket
function connect() {
    socket = new WebSocket('ws://localhost:8765');
    
    socket.onopen = () => {
        console.log('✅ Connected to dashboard server');
        updateConnectionStatus(true);
        reconnectAttempts = 0;
    };
    
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleMessage(data);
    };
    
    socket.onclose = () => {
        console.log('❌ Disconnected from server');
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
            addToFeed(`New ${data.label}: ${data.value}`, 'info');
            break;
        
        case 'client_count':
            updateClientCount(data.count);
            break;
        
        case 'pong':
            console.log('💓 Heartbeat OK');
            break;
    }
}

// Update system metrics
function updateMetrics(data) {
    // CPU
    const cpuValue = data.cpu.toFixed(1);
    document.getElementById('cpuValue').textContent = cpuValue + '%';
    document.getElementById('cpuBar').style.width = cpuValue + '%';
    
    // Memory
    const memValue = data.memory.toFixed(1);
    document.getElementById('memoryValue').textContent = memValue + '%';
    document.getElementById('memoryBar').style.width = memValue + '%';
    
    // Disk (if element exists)
    if (data.disk && document.getElementById('diskValue')) {
        const diskValue = data.disk.toFixed(1);
        document.getElementById('diskValue').textContent = diskValue + '%';
        document.getElementById('diskBar').style.width = diskValue + '%';
    }
}

// Update chart with new data
function updateChart(data) {
    dataPoints.push(data.value);
    
    // Keep only last N points
    if (dataPoints.length > maxDataPoints) {
        dataPoints.shift();
    }
    
    // Update chart
    chart.data.labels = dataPoints.map((_, i) => i);
    chart.data.datasets[0].data = dataPoints;
    chart.update('none'); // No animation for smooth updates
}

// Update connection status
function updateConnectionStatus(connected) {
    const indicator = document.getElementById('statusIndicator');
    const text = document.getElementById('statusText');
    
    if (connected) {
        indicator.classList.add('connected');
        text.textContent = 'Connected';
    } else {
        indicator.classList.remove('connected');
        text.textContent = 'Disconnected';
    }
}

// Update client count
function updateClientCount(count) {
    document.getElementById('clientCount').textContent = 
        `${count} client${count !== 1 ? 's' : ''}`;
}

// Add item to activity feed
function addToFeed(message, type = 'info') {
    const feed = document.getElementById('feed');
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

// Reconnect with exponential backoff
function reconnect() {
    const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), maxReconnectDelay);
    reconnectAttempts++;
    
    console.log(`🔄 Reconnecting in ${delay/1000} seconds...`);
    addToFeed(`Reconnecting in ${delay/1000}s...`, 'warning');
    
    setTimeout(connect, delay);
}

// Send heartbeat
setInterval(() => {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: 'ping' }));
    }
}, 30000);

// Pause updates when tab is hidden
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        console.log('⏸️  Tab hidden, pausing updates');
    } else {
        console.log('▶️  Tab visible, resuming updates');
    }
});

// Initialize on load
window.addEventListener('load', init);
```

### Pros
✅ Real system metrics with psutil  
✅ Live charts with Chart.js  
✅ Better error handling and logging  
✅ Clean separation of concerns  
✅ Multiple data streams  
✅ Heartbeat mechanism  

### Cons
❌ No user authentication  
❌ No data persistence  
❌ No configuration options  

---

## Approach 3: Advanced (Production-Ready)

This approach implements enterprise-level features including authentication, data persistence, configuration, and horizontal scalability.

### Additional Features
- User authentication with JWT
- Redis for pub/sub (multi-server support)
- PostgreSQL for data persistence
- Environment-based configuration
- Comprehensive logging
- Health check endpoint
- Docker support
- Prometheus metrics

### Key Highlights

```python
# Advanced features include:

# 1. Authentication
class AuthMiddleware:
    """Verify JWT tokens for WebSocket connections."""
    
    async def authenticate(self, websocket):
        # Check authorization header
        # Verify JWT token
        # Return user info or reject
        pass

# 2. Redis Pub/Sub for horizontal scaling
class MessageBroker:
    """Use Redis for message broadcasting across multiple servers."""
    
    async def publish(self, channel, message):
        await self.redis.publish(channel, message)
    
    async def subscribe(self, channel):
        async for message in self.pubsub.listen():
            await self.handle_message(message)

# 3. Data persistence
class MetricsStore:
    """Store metrics in PostgreSQL for historical analysis."""
    
    async def save_metric(self, metric_type, value, timestamp):
        await self.db.execute(
            "INSERT INTO metrics (type, value, timestamp) VALUES ($1, $2, $3)",
            metric_type, value, timestamp
        )

# 4. Configuration management
@dataclass
class Config:
    """Centralized configuration from environment."""
    
    ws_host: str = os.getenv('WS_HOST', 'localhost')
    ws_port: int = int(os.getenv('WS_PORT', 8765))
    redis_url: str = os.getenv('REDIS_URL', 'redis://localhost')
    db_url: str = os.getenv('DATABASE_URL')
    jwt_secret: str = os.getenv('JWT_SECRET')
```

### Pros
✅ Production-ready architecture  
✅ Horizontal scalability  
✅ Authentication and authorization  
✅ Data persistence  
✅ Monitoring and metrics  
✅ Docker support  
✅ Comprehensive documentation  

### Cons
❌ Complex setup  
❌ Requires multiple services (Redis, PostgreSQL)  
❌ Higher resource requirements  
❌ Steeper learning curve  

---

## Comparison

| Aspect | Approach 1 | Approach 2 | Approach 3 |
|--------|-----------|------------|------------|
| **Lines of Code** | ~300 | ~600 | ~1500+ |
| **Dependencies** | websockets only | + psutil, Chart.js | + Redis, PostgreSQL, JWT |
| **System Metrics** | Random data | Real with psutil | Real + historical |
| **Visualization** | None | Charts with Chart.js | Advanced dashboards |
| **Scaling** | Single server | Single server | Multi-server with Redis |
| **Authentication** | None | None | JWT-based |
| **Data Persistence** | None | In-memory | PostgreSQL |
| **Configuration** | Hardcoded | Basic | Environment-based |
| **Monitoring** | Console logs | Structured logging | Prometheus metrics |
| **Deployment** | Local only | PM2/systemd | Docker + Kubernetes |
| **Suitable For** | Learning | Small apps | Production systems |

## When to Use Each Approach

### Use Approach 1 when:
- Learning WebSocket basics
- Building a quick prototype
- Need simple real-time updates
- Don't need real metrics

### Use Approach 2 when:
- Building a real application
- Need actual system monitoring
- Want good visualizations
- Single server is sufficient

### Use Approach 3 when:
- Deploying to production
- Need multi-server support
- Require authentication
- Want historical data
- Need high availability
- Working in a team

## Learning Path

1. **Start with Approach 1**: Understand WebSocket fundamentals
2. **Progress to Approach 2**: Add real features and visualizations
3. **Study Approach 3**: Learn production patterns and scalability

Each approach demonstrates progressive mastery of real-time web technologies!

---

[Back to Requirements](./03-realtime-dashboard-requirements.md) | [Back to Projects](./README.md)
