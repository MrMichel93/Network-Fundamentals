# 🔌 Other Network Protocols

Beyond HTTP and WebSockets, there are many other protocols that power the internet!

## 🎯 Learning Objectives

By the end of this module, you will:
- Understand the difference between TCP and UDP
- Learn about common application protocols (FTP, SMTP, SSH)
- Know when to use each protocol
- Build simple TCP and UDP socket programs
- Understand protocol layers and their purposes

## TCP vs UDP: The Transport Layer

### TCP (Transmission Control Protocol) 📦✅

**Analogy**: Certified mail with tracking

**Characteristics:**
- **Reliable**: Guarantees delivery in correct order
- **Connection-oriented**: Establishes connection before sending data
- **Error checking**: Detects and retransmits lost packets
- **Flow control**: Adjusts speed based on network conditions
- **Slower**: More overhead for reliability

**Use Cases:**
- Web browsing (HTTP/HTTPS)
- Email (SMTP, POP3, IMAP)
- File transfer (FTP)
- Remote access (SSH)
- **When**: Accuracy matters more than speed

**Example**: Loading a web page
- Every packet must arrive
- Order matters (HTML before images)
- OK if slightly slower

### UDP (User Datagram Protocol) 📨💨

**Analogy**: Throwing postcards - fast but might lose some

**Characteristics:**
- **Fast**: Minimal overhead
- **Connectionless**: No handshake required
- **No guarantees**: Packets might be lost or arrive out of order
- **No error recovery**: Lost data stays lost
- **Lower latency**: Great for real-time applications

**Use Cases:**
- Video streaming
- Online gaming
- Voice calls (VoIP)
- DNS lookups
- Live broadcasts
- **When**: Speed matters more than perfection

**Example**: Video call
- Can lose a few frames (hardly noticeable)
- Speed is critical (real-time)
- Retransmitting old data is useless

### Comparison Table

| Feature | TCP | UDP |
|---------|-----|-----|
| Reliability | Guaranteed delivery | No guarantee |
| Order | In-order delivery | May arrive out of order |
| Speed | Slower | Faster |
| Connection | Required | Not required |
| Error checking | Yes | Basic |
| Use case | Web, email, files | Video, voice, gaming |

### When to Use Which?

**Choose TCP when:**
- Data accuracy is critical
- You need guaranteed delivery
- Order matters
- Examples: downloading files, sending emails, loading web pages

**Choose UDP when:**
- Speed is more important than accuracy
- Real-time communication
- Can tolerate some data loss
- Examples: video streaming, gaming, voice calls

## Common Application Protocols

### FTP (File Transfer Protocol) 📁

**Purpose**: Transfer files between computers

**Ports**: 20 (data), 21 (control)

**How it works:**
1. Client connects to FTP server
2. Authenticates with username/password
3. Can upload, download, list files
4. Uses separate connections for commands and data

**Example:**
```bash
# Connect to FTP server
ftp ftp.example.com

# Login
Name: username
Password: ******

# List files
ftp> ls

# Download file
ftp> get filename.txt

# Upload file
ftp> put myfile.txt

# Quit
ftp> bye
```

**Modern alternatives:**
- **SFTP**: FTP over SSH (encrypted)
- **FTPS**: FTP over TLS/SSL (encrypted)
- **SCP**: Secure Copy Protocol

### SMTP (Simple Mail Transfer Protocol) 📧

**Purpose**: Send emails between servers

**Port**: 25 (traditional), 587 (submission), 465 (SSL)

**How it works:**
1. Client connects to SMTP server
2. Provides sender and recipient addresses
3. Sends message content
4. Server forwards to recipient's mail server

**Email journey:**
```
Your email client → Your SMTP server → Recipient's SMTP server → Recipient's mailbox
```

**Related protocols:**
- **POP3 (Post Office Protocol)**: Download emails from server (port 110)
- **IMAP (Internet Message Access Protocol)**: Access emails on server (port 143)

**Example SMTP session:**
```
HELO mail.example.com
MAIL FROM: <sender@example.com>
RCPT TO: <recipient@example.com>
DATA
Subject: Hello
This is the email body.
.
QUIT
```

### SSH (Secure Shell) 🔐

**Purpose**: Secure remote access to computers

**Port**: 22

**Features:**
- Encrypted communication
- Remote command execution
- Secure file transfer (SFTP, SCP)
- Port forwarding
- Tunneling

**Common uses:**
```bash
# Connect to remote server
ssh username@server.com

# Run command on remote server
ssh username@server.com 'ls -la'

# Copy file to remote server
scp file.txt username@server.com:/path/

# Copy file from remote server
scp username@server.com:/path/file.txt .

# Port forwarding (tunnel)
ssh -L 8080:localhost:80 username@server.com
```

**How it works:**
1. Client initiates connection
2. Server sends public key
3. Client and server negotiate encryption
4. User authenticates (password or key)
5. Secure channel established

### DNS (Domain Name System) 🌐

**Purpose**: Translate domain names to IP addresses

**Port**: 53 (UDP for queries, TCP for zone transfers)

**DNS Record Types:**
- **A**: IPv4 address
- **AAAA**: IPv6 address
- **CNAME**: Alias to another domain
- **MX**: Mail server
- **TXT**: Text records (SPF, DKIM, etc.)
- **NS**: Name server

**Example query:**
```bash
# Look up domain
nslookup example.com

# Or use dig
dig example.com

# Reverse lookup (IP to domain)
nslookup 8.8.8.8
```

### DHCP (Dynamic Host Configuration Protocol) 🔄

**Purpose**: Automatically assign IP addresses to devices

**Ports**: 67 (server), 68 (client)

**How it works:**
1. **Discover**: Device broadcasts "I need an IP!"
2. **Offer**: DHCP server offers an IP address
3. **Request**: Device requests that IP
4. **Acknowledge**: Server confirms and assigns IP

**What DHCP provides:**
- IP address
- Subnet mask
- Default gateway
- DNS servers
- Lease time

## Socket Programming

### TCP Socket Example (Python)

**TCP Server:**
```python
import socket

# Create TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 9000))
server.listen(1)

print("TCP Server listening on port 9000...")

while True:
    client, address = server.accept()
    print(f"Connection from {address}")
    
    # Receive data
    data = client.recv(1024)
    print(f"Received: {data.decode()}")
    
    # Send response
    client.send(b"Hello from server!")
    client.close()
```

**TCP Client:**
```python
import socket

# Create TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9000))

# Send data
client.send(b"Hello from client!")

# Receive response
data = client.recv(1024)
print(f"Received: {data.decode()}")

client.close()
```

### UDP Socket Example (Python)

**UDP Server:**
```python
import socket

# Create UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('localhost', 9001))

print("UDP Server listening on port 9001...")

while True:
    # Receive data (no connection needed!)
    data, address = server.recvfrom(1024)
    print(f"Received from {address}: {data.decode()}")
    
    # Send response
    server.sendto(b"Hello from UDP server!", address)
```

**UDP Client:**
```python
import socket

# Create UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send data (no connection needed!)
client.sendto(b"Hello from UDP client!", ('localhost', 9001))

# Receive response
data, server = client.recvfrom(1024)
print(f"Received: {data.decode()}")

client.close()
```

## Protocol Layers (OSI Model Simplified)

```
┌─────────────────────────────────────┐
│  7. Application Layer               │  (HTTP, FTP, SMTP, SSH)
├─────────────────────────────────────┤
│  4. Transport Layer                 │  (TCP, UDP)
├─────────────────────────────────────┤
│  3. Network Layer                   │  (IP, ICMP)
├─────────────────────────────────────┤
│  2. Link Layer                      │  (Ethernet, Wi-Fi)
├─────────────────────────────────────┤
│  1. Physical Layer                  │  (Cables, radio waves)
└─────────────────────────────────────┘
```

**Each layer:**
- Has specific responsibilities
- Communicates with layers above and below
- Is independent (can change without affecting others)

## Port Numbers

**Well-known ports (0-1023):**
- 20/21: FTP
- 22: SSH
- 25: SMTP
- 53: DNS
- 80: HTTP
- 110: POP3
- 143: IMAP
- 443: HTTPS

**Registered ports (1024-49151):**
- Used by specific applications

**Dynamic ports (49152-65535):**
- Temporary ports for client connections

## Code Examples

Check the `examples/` folder for:
- `tcp_socket_server.py` - TCP server
- `tcp_socket_client.py` - TCP client
- `udp_example.py` - UDP client/server

## Summary and Key Takeaways

✅ **TCP** is reliable but slower (web, email, files)  
✅ **UDP** is fast but unreliable (video, gaming, voice)  
✅ **FTP** transfers files (use SFTP for security)  
✅ **SMTP** sends emails between servers  
✅ **SSH** provides secure remote access  
✅ **DNS** translates domain names to IPs  
✅ **Protocols are layered** - each layer has a job

## What's Next?

Learn how to secure your network communications: [Security Basics](../06-Security-Basics/)

---

[← Back: WebSockets](../10-WebSockets/) | [Next: HTTPS and TLS →](../12-HTTPS-and-TLS/)

## Practice

Complete the [exercises](./exercises.md) to work with different protocols!
