# 🏋️ Exercises: WebSockets

Build real-time applications with these hands-on exercises!

## Exercise 1: Connect to WebSocket Server 🔌

**Objective**: Set up and test the basic WebSocket server.

**Tasks**:
1. Run `websocket_server.py`
2. Open `websocket_client.html` in your browser
3. Connect to the server
4. Send messages back and forth
5. Open multiple browser tabs and see messages broadcast

<details>
<summary>💡 Hint</summary>

```bash
# Install dependencies
pip install websockets

# Start the server
python websocket_server.py

# Then open websocket_client.html in your browser
# Try opening multiple tabs to see broadcasting!
```
</details>

**Success Criteria**: You can connect, send messages, and see them appear in real-time.

---

## Exercise 2: Chat Application 💬

**Objective**: Run and test a complete chat application.

**Tasks**:
1. Run `chat_app/chat_server.py`
2. Open `chat_app/chat_client.html` in multiple browser tabs
3. Set different usernames in each tab
4. Send messages and observe:
   - Join/leave notifications
   - User list updates
   - Message broadcasting

<details>
<summary>💡 Hint</summary>

```bash
# Start chat server
cd chat_app
python chat_server.py

# Open chat_client.html in multiple browser tabs
# Use different nicknames in each tab
```

**What to observe:**
- Each user sees when others join/leave
- Messages appear instantly for all users
- User list updates automatically
</details>

**Success Criteria**: Multiple users can chat in real-time.

---

## Exercise 3: Add Typing Indicator ⌨️

**Objective**: Enhance the chat with a "user is typing..." feature.

**Tasks**:
1. Modify the chat client to send a "typing" message when user types
2. Display "Username is typing..." to other users
3. Clear the indicator after 2 seconds of no typing

<details>
<summary>💡 Hint</summary>

**Client-side (JavaScript):**
```javascript
let typingTimer;
const typingDelay = 2000;

messageInput.addEventListener('input', () => {
    // Send typing notification
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: 'typing',
            username: currentUser
        }));
    }
    
    // Clear previous timer
    clearTimeout(typingTimer);
    
    // Set new timer to stop typing
    typingTimer = setTimeout(() => {
        socket.send(JSON.stringify({
            type: 'stop_typing',
            username: currentUser
        }));
    }, typingDelay);
});
```

**Server-side (Python):**
```python
if data['type'] == 'typing':
    typing_msg = {
        'type': 'typing',
        'username': data['username']
    }
    await broadcast(json.dumps(typing_msg), websocket)

elif data['type'] == 'stop_typing':
    stop_typing_msg = {
        'type': 'stop_typing',
        'username': data['username']
    }
    await broadcast(json.dumps(stop_typing_msg), websocket)
```
</details>

**Success Criteria**: Users see when others are typing.

---

## Exercise 4: Build a Live Counter 🔢

**Objective**: Create a shared counter that updates in real-time.

**Requirements**:
- Display a number
- Multiple clients connected
- Anyone can increment/decrement
- All clients see updates instantly

<details>
<summary>💡 Hint</summary>

**Server:**
```python
counter = 0
connected_clients = set()

async def handler(websocket):
    connected_clients.add(websocket)
    
    # Send current counter value
    await websocket.send(json.dumps({
        'type': 'counter',
        'value': counter
    }))
    
    async for message in websocket:
        data = json.dumps(message)
        
        if data['type'] == 'increment':
            counter += 1
        elif data['type'] == 'decrement':
            counter -= 1
        
        # Broadcast new value
        update = json.dumps({
            'type': 'counter',
            'value': counter
        })
        await asyncio.gather(
            *[c.send(update) for c in connected_clients],
            return_exceptions=True
        )
```

**Client:**
```html
<div>
    <h1 id="counter">0</h1>
    <button onclick="increment()">+</button>
    <button onclick="decrement()">-</button>
</div>

<script>
    const socket = new WebSocket('ws://localhost:8000');
    
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        document.getElementById('counter').textContent = data.value;
    };
    
    function increment() {
        socket.send(JSON.stringify({type: 'increment'}));
    }
    
    function decrement() {
        socket.send(JSON.stringify({type: 'decrement'}));
    }
</script>
```
</details>

**Success Criteria**: Counter updates instantly for all connected clients.

---

## Exercise 5: Real-Time Notifications 🔔

**Objective**: Build a notification system.

**Tasks**:
1. Create a server that sends random notifications
2. Client displays notifications as they arrive
3. Show unread count
4. Allow dismissing notifications

<details>
<summary>💡 Hint</summary>

```python
# Server sends notifications periodically
import random

notifications = [
    "New message from Alice",
    "System update available",
    "3 new comments on your post",
    "Meeting in 15 minutes"
]

async def send_notifications(websocket):
    while True:
        await asyncio.sleep(random.randint(5, 15))
        notification = {
            'type': 'notification',
            'id': str(uuid.uuid4()),
            'message': random.choice(notifications),
            'timestamp': datetime.now().isoformat()
        }
        await websocket.send(json.dumps(notification))
```

**Client shows toast notifications:**
```javascript
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'notification') {
        showToast(data.message);
        incrementUnreadCount();
    }
};

function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.remove(), 5000);
}
```
</details>

**Success Criteria**: Notifications appear in real-time.

---

## Exercise 6: Live Dashboard 📊

**Objective**: Create a dashboard that displays live data.

**Requirements**:
- Show system metrics (CPU, memory, connections)
- Update every second
- Display as charts or numbers
- Multiple clients see same data

<details>
<summary>💡 Hint</summary>

```python
import psutil  # pip install psutil
import asyncio

async def send_metrics(websocket):
    """Send system metrics every second."""
    while True:
        metrics = {
            'type': 'metrics',
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory().percent,
            'connections': len(connected_clients),
            'timestamp': datetime.now().isoformat()
        }
        
        await websocket.send(json.dumps(metrics))
        await asyncio.sleep(1)
```

**Client updates UI:**
```javascript
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    document.getElementById('cpu').textContent = data.cpu + '%';
    document.getElementById('memory').textContent = data.memory + '%';
    document.getElementById('connections').textContent = data.connections;
};
```
</details>

**Success Criteria**: Dashboard updates every second with live data.

---

## Challenge Exercise: Collaborative Drawing 🎨

**Objective**: Build a shared whiteboard where multiple users can draw together.

**Requirements**:
- Canvas that multiple users can draw on
- Broadcast drawing actions (mouse movements)
- All users see the same drawing
- Clear button to reset canvas

<details>
<summary>💡 Hint</summary>

**Client:**
```javascript
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let drawing = false;

canvas.addEventListener('mousedown', (e) => {
    drawing = true;
    const pos = {x: e.offsetX, y: e.offsetY};
    socket.send(JSON.stringify({
        type: 'draw_start',
        x: pos.x,
        y: pos.y
    }));
});

canvas.addEventListener('mousemove', (e) => {
    if (!drawing) return;
    
    const pos = {x: e.offsetX, y: e.offsetY};
    socket.send(JSON.stringify({
        type: 'draw_move',
        x: pos.x,
        y: pos.y
    }));
    
    drawLine(lastPos, pos);
    lastPos = pos;
});

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'draw_move') {
        // Draw on canvas
        ctx.beginPath();
        ctx.moveTo(data.fromX, data.fromY);
        ctx.lineTo(data.x, data.y);
        ctx.stroke();
    }
};
```

**Server broadcasts drawing actions:**
```python
async def handler(websocket):
    async for message in websocket:
        data = json.loads(message)
        # Broadcast to all other clients
        await broadcast(message, websocket)
```
</details>

**Success Criteria**: Multiple users can draw on the same canvas simultaneously.

---

## Mini-Quiz ✅

1. **What does WebSocket provide that HTTP doesn't?**
   - [ ] Faster downloads
   - [ ] Bidirectional real-time communication
   - [ ] Better security
   - [ ] Smaller file sizes

2. **When should you use WebSockets?**
   - [ ] Downloading files
   - [ ] Real-time chat
   - [ ] Static websites
   - [ ] File uploads

3. **How do WebSockets start?**
   - [ ] Direct TCP connection
   - [ ] HTTP request that upgrades
   - [ ] UDP packet
   - [ ] Email

4. **What's the WebSocket secure protocol?**
   - [ ] ws://
   - [ ] wss://
   - [ ] https://
   - [ ] tcp://

5. **What happens if a WebSocket disconnects?**
   - [ ] Automatic reconnection
   - [ ] You must implement reconnection
   - [ ] Server restarts
   - [ ] Nothing

<details>
<summary>Show Answers</summary>

1. **B** - Bidirectional real-time communication
2. **B** - Real-time chat (and other real-time features)
3. **B** - HTTP request that upgrades to WebSocket
4. **B** - wss:// (WebSocket Secure)
5. **B** - You must implement reconnection logic

**Scoring:**
- 5/5: WebSocket expert! 🌟
- 3-4/5: Good understanding! 👍
- 1-2/5: Review the lesson
</details>

---

## Solutions

Complete solutions in [solutions/04-websockets-solutions.md](../solutions/04-websockets-solutions.md)

---

[← Back to Lesson](./README.md) | [Next: Other Protocols →](../05-Other-Protocols/)
