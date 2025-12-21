# 🏋️ Exercises: Other Network Protocols

Practice working with different network protocols beyond HTTP!

## Exercise 1: TCP vs UDP Comparison 🔍

**Objective**: Understand the practical differences between TCP and UDP.

**Tasks**:
1. Read about TCP and UDP in the lesson
2. Create a comparison table with at least 5 differences
3. List 3 real-world applications for each protocol
4. Explain when you would choose one over the other

**Questions to answer**:
- Why is TCP slower than UDP?
- Can UDP guarantee packet delivery?
- Which protocol requires a connection handshake?

<details>
<summary>💡 Hint</summary>

**TCP Characteristics:**
- Connection-oriented (3-way handshake)
- Reliable delivery guaranteed
- In-order packet delivery
- Error checking and retransmission
- Flow control

**UDP Characteristics:**
- Connectionless (no handshake)
- No delivery guarantee
- Packets may arrive out of order
- Minimal error checking
- No retransmission

**Real-world examples:**
- TCP: Web browsing, email, file downloads, SSH
- UDP: Video streaming, online gaming, VoIP calls, DNS lookups
</details>

**Success Criteria**: You can explain the trade-offs between TCP and UDP.

---

## Exercise 2: TCP Socket Programming 🔌

**Objective**: Build a simple TCP client-server application.

**Tasks**:
1. Run the provided `tcp_socket_server.py` from the examples folder
2. Run the `tcp_socket_client.py` to connect to it
3. Modify the client to send different messages
4. Modify the server to echo back messages in uppercase
5. Test multiple client connections

<details>
<summary>💡 Hint</summary>

```bash
# Terminal 1: Start server
cd examples
python tcp_socket_server.py

# Terminal 2: Run client
python tcp_socket_client.py
```

**Server modification (echo uppercase):**
```python
# In the server code, find where data is received
data = client.recv(1024)
response = data.decode().upper()
client.send(response.encode())
```

**Testing multiple connections:**
```bash
# Open multiple terminals and run the client in each
python tcp_socket_client.py
```
</details>

**Success Criteria**: Your TCP server can handle multiple client connections and process their messages.

---

## Exercise 3: UDP Socket Programming 💨

**Objective**: Experience connectionless communication with UDP.

**Tasks**:
1. Run the provided `udp_example.py`
2. Compare UDP and TCP behavior
3. Test sending multiple messages quickly
4. Observe if any messages are lost (run many times)
5. Modify to send timestamps and measure round-trip time

<details>
<summary>💡 Hint</summary>

```python
# UDP Client with timestamp
import socket
import time

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send with timestamp
start_time = time.time()
message = f"Hello at {start_time}"
client.sendto(message.encode(), ('localhost', 9001))

# Receive response
data, server = client.recvfrom(1024)
end_time = time.time()

print(f"Round-trip time: {(end_time - start_time) * 1000:.2f} ms")
print(f"Received: {data.decode()}")

client.close()
```

**Testing for lost packets:**
```bash
# Send 100 messages and count responses
# UDP doesn't guarantee delivery, but on localhost should be reliable
```
</details>

**Success Criteria**: You understand how UDP differs from TCP in practice.

---

## Exercise 4: DNS Investigation 🌐

**Objective**: Explore how DNS resolution works.

**Tasks**:
1. Use `nslookup` to query different domain names
2. Find A records, AAAA records, and MX records
3. Query different DNS servers (8.8.8.8, 1.1.1.1)
4. Perform a reverse DNS lookup
5. Compare response times from different DNS servers

<details>
<summary>💡 Hint</summary>

```bash
# Basic DNS query
nslookup github.com

# Query specific DNS server
nslookup github.com 8.8.8.8

# Get specific record type
nslookup -type=MX github.com  # Mail servers
nslookup -type=AAAA github.com  # IPv6 addresses

# Reverse DNS lookup
nslookup 8.8.8.8

# Using dig (more detailed)
dig github.com
dig github.com @1.1.1.1  # Query Cloudflare DNS
dig github.com MX  # Mail records
```

**DNS servers to try:**
- 8.8.8.8 (Google DNS)
- 1.1.1.1 (Cloudflare DNS)
- 9.9.9.9 (Quad9 DNS)
</details>

**Success Criteria**: You can query DNS records and understand different record types.

---

## Exercise 5: SSH Practice 🔐

**Objective**: Learn secure remote access with SSH.

**Tasks**:
1. If you have access to a remote server, connect via SSH
2. Run commands remotely using `ssh username@host 'command'`
3. Copy files using `scp` (Secure Copy)
4. Explore SSH key-based authentication (read only, setup optional)
5. Learn about SSH port forwarding

<details>
<summary>💡 Hint</summary>

```bash
# Connect to remote server
ssh username@server.example.com

# Run single command remotely
ssh username@server.example.com 'ls -la'
ssh username@server.example.com 'df -h'

# Copy file TO remote server
scp local_file.txt username@server.example.com:/path/to/destination/

# Copy file FROM remote server
scp username@server.example.com:/path/to/file.txt ./local_directory/

# Copy directory recursively
scp -r local_folder username@server.example.com:/remote/path/

# Port forwarding (tunnel local port 8080 to remote port 80)
ssh -L 8080:localhost:80 username@server.example.com
```

**SSH Key Authentication (advanced):**
```bash
# Generate SSH key pair
ssh-keygen -t rsa -b 4096

# Copy public key to server
ssh-copy-id username@server.example.com

# Connect without password
ssh username@server.example.com
```

**If you don't have a remote server:**
- Research how SSH works
- Read about public/private key cryptography
- Understand the SSH handshake process
</details>

**Success Criteria**: You understand SSH basics and can use it for remote operations.

---

## Exercise 6: Protocol Port Numbers 🔢

**Objective**: Learn common protocol port numbers.

**Tasks**:
1. Create a list of 10 common protocols with their port numbers
2. Use `netstat` or `ss` to see active connections on your machine
3. Identify which services are listening on which ports
4. Try connecting to a local port with `telnet` or `nc` (netcat)

<details>
<summary>💡 Hint</summary>

**Common ports:**
- 20/21: FTP (File Transfer Protocol)
- 22: SSH (Secure Shell)
- 25: SMTP (Simple Mail Transfer Protocol)
- 53: DNS (Domain Name System)
- 80: HTTP (Hypertext Transfer Protocol)
- 110: POP3 (Post Office Protocol)
- 143: IMAP (Internet Message Access Protocol)
- 443: HTTPS (HTTP Secure)
- 3306: MySQL
- 5432: PostgreSQL

```bash
# See active connections (Linux/Mac)
netstat -tuln
# or
ss -tuln

# Windows
netstat -an

# Test connection to a port
telnet example.com 80
# or
nc -zv example.com 80

# Scan local ports (if nmap installed)
nmap localhost
```
</details>

**Success Criteria**: You can identify common ports and check port availability.

---

## Exercise 7: FTP Exploration 📁

**Objective**: Understand file transfer protocols.

**Tasks**:
1. Read about FTP, SFTP, and FTPS differences
2. If available, connect to a public FTP server
3. Practice basic FTP commands: ls, cd, get, put
4. Compare FTP with SFTP security
5. Research modern alternatives to FTP

<details>
<summary>💡 Hint</summary>

**FTP Commands:**
```bash
# Connect to FTP server
ftp ftp.example.com

# Common commands after connecting:
ls          # List files
cd folder   # Change directory
pwd         # Print working directory
get file    # Download file
put file    # Upload file
binary      # Set binary mode for non-text files
ascii       # Set ASCII mode for text files
bye         # Disconnect
```

**SFTP (more secure):**
```bash
# Connect with SFTP
sftp username@server.example.com

# Same commands work: ls, cd, get, put, etc.
```

**Security comparison:**
- FTP: Unencrypted, passwords sent in plain text ❌
- FTPS: FTP with TLS/SSL encryption ✅
- SFTP: FTP over SSH, fully encrypted ✅

**Modern alternatives:**
- SCP (Secure Copy over SSH)
- SFTP (SSH File Transfer Protocol)
- rsync (efficient file synchronization)
- HTTP(S) file uploads
- Cloud storage APIs (S3, Google Cloud Storage)

**Public FTP servers for testing:**
- ftp://speedtest.tele2.net (Anonymous FTP)
- Various university mirrors
</details>

**Success Criteria**: You understand FTP and its secure alternatives.

---

## Exercise 8: Email Protocols Research 📧

**Objective**: Learn how email transmission works.

**Tasks**:
1. Research SMTP, POP3, and IMAP
2. Draw a diagram showing email flow from sender to recipient
3. Explain the difference between POP3 and IMAP
4. Research email headers and what information they contain
5. Learn about SPF, DKIM, and DMARC (email authentication)

<details>
<summary>💡 Hint</summary>

**Email Protocol Roles:**

**SMTP (Port 25, 587, 465):**
- Sends email from client to server
- Transfers email between servers
- "Simple Mail Transfer Protocol"

**POP3 (Port 110, 995 for SSL):**
- Downloads email from server to client
- Typically deletes from server after download
- "Post Office Protocol"

**IMAP (Port 143, 993 for SSL):**
- Accesses email on server
- Keeps messages on server
- Syncs across multiple devices
- "Internet Message Access Protocol"

**Email Flow:**
```
[Your Email Client] --(SMTP)--> [Your Mail Server] 
                                       |
                                    (SMTP)
                                       |
                                       v
                            [Recipient Mail Server]
                                       |
                                  (POP3/IMAP)
                                       |
                                       v
                            [Recipient Email Client]
```

**View email headers:**
Most email clients have "View Source" or "Show Original" option showing:
- From, To, Subject
- Message-ID
- Received: (shows the path the email took)
- SPF, DKIM, DMARC results
- Content-Type
</details>

**Success Criteria**: You understand the complete email delivery process.

---

## Exercise 9: Network Monitoring 📊

**Objective**: Monitor network traffic and connections.

**Tasks**:
1. Use `netstat` or `ss` to view active connections
2. Identify which processes are using the network
3. Monitor network traffic with `tcpdump` (if available)
4. Understand connection states (ESTABLISHED, LISTENING, etc.)
5. Find which ports are open and listening

<details>
<summary>💡 Hint</summary>

```bash
# View all TCP connections (Linux/Mac)
netstat -tan
ss -tan

# View all UDP connections
netstat -uan
ss -uan

# See which programs are using network
sudo netstat -tulpn  # Linux
sudo lsof -i  # Mac
netstat -anb  # Windows (run as admin)

# Monitor network traffic (requires root/admin)
sudo tcpdump -i any port 80
sudo tcpdump -i any host 8.8.8.8

# View listening ports only
netstat -tln
ss -tln

# Windows
netstat -an | findstr LISTENING
```

**Connection States:**
- LISTENING: Waiting for incoming connections
- ESTABLISHED: Active connection
- TIME_WAIT: Connection closed, waiting to ensure all packets received
- CLOSE_WAIT: Remote side closed connection
- SYN_SENT: Attempting to establish connection
</details>

**Success Criteria**: You can monitor and understand network activity on your system.

---

## Exercise 10: Build a Simple Chat Server 💬

**Objective**: Create a multi-client TCP chat application.

**Tasks**:
1. Build a TCP server that accepts multiple clients
2. Broadcast messages from one client to all others
3. Assign usernames to clients
4. Add join/leave notifications
5. Test with multiple client connections

<details>
<summary>💡 Hint</summary>

```python
# Simple Chat Server
import socket
import threading

clients = []
clients_lock = threading.Lock()

def broadcast(message, sender_socket=None):
    """Send message to all clients except sender."""
    with clients_lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message.encode())
                except:
                    clients.remove(client)

def handle_client(client_socket, address):
    """Handle individual client connection."""
    # Ask for username
    client_socket.send(b"Enter username: ")
    username = client_socket.recv(1024).decode().strip()
    
    with clients_lock:
        clients.append(client_socket)
    
    broadcast(f"{username} joined the chat!\n")
    print(f"{username} connected from {address}")
    
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            
            broadcast(f"{username}: {message}", client_socket)
            print(f"{username}: {message}")
    
    except:
        pass
    
    finally:
        with clients_lock:
            clients.remove(client_socket)
        broadcast(f"{username} left the chat.\n")
        client_socket.close()
        print(f"{username} disconnected")

# Create server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 9999))
server.listen(5)

print("Chat server listening on port 9999...")

while True:
    client_socket, address = server.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, address))
    thread.daemon = True
    thread.start()
```

```python
# Simple Chat Client
import socket
import threading

def receive_messages(sock):
    """Receive messages from server."""
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(message, end='')
        except:
            break

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9999))

# Start receive thread
thread = threading.Thread(target=receive_messages, args=(client,))
thread.daemon = True
thread.start()

# Send messages
while True:
    message = input()
    client.send(message.encode())
```

**Testing:**
```bash
# Terminal 1: Start server
python chat_server.py

# Terminal 2, 3, 4: Start multiple clients
python chat_client.py
```
</details>

**Success Criteria**: Multiple clients can chat with each other through your server.

---

## Challenge Exercise: Protocol Analyzer 🔬

**Objective**: Build a tool to analyze network packets.

**Tasks**:
1. Use Python's `socket` library to capture packets
2. Parse TCP/UDP headers
3. Display source/destination IP and port
4. Count packets by protocol type
5. Calculate bandwidth usage

<details>
<summary>💡 Hint</summary>

```python
#!/usr/bin/env python3
import socket
import struct

def analyze_packet(data):
    """Analyze IP packet."""
    # IP Header is first 20 bytes
    ip_header = data[0:20]
    iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
    
    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF
    iph_length = ihl * 4
    
    protocol = iph[6]
    src_addr = socket.inet_ntoa(iph[8])
    dst_addr = socket.inet_ntoa(iph[9])
    
    print(f"\n{'='*50}")
    print(f"IP: {src_addr} → {dst_addr}")
    
    # Protocol number to name
    protocols = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
    protocol_name = protocols.get(protocol, f'Other({protocol})')
    print(f"Protocol: {protocol_name}")
    
    # TCP/UDP header
    if protocol == 6:  # TCP
        tcp_header = data[iph_length:iph_length+20]
        tcph = struct.unpack('!HHLLBBHHH', tcp_header)
        src_port = tcph[0]
        dst_port = tcph[1]
        print(f"TCP: {src_port} → {dst_port}")
    
    elif protocol == 17:  # UDP
        udp_header = data[iph_length:iph_length+8]
        udph = struct.unpack('!HHHH', udp_header)
        src_port = udph[0]
        dst_port = udph[1]
        print(f"UDP: {src_port} → {dst_port}")

# Create raw socket (requires root/admin privileges)
try:
    # Linux
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
except AttributeError:
    # Windows
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    sock.bind(('0.0.0.0', 0))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

print("Capturing packets... Press Ctrl+C to stop")

try:
    while True:
        packet = sock.recvfrom(65565)
        analyze_packet(packet[0])
except KeyboardInterrupt:
    print("\nStopped.")
    sock.close()
```

**Note**: This requires administrator/root privileges!

**Easier alternative:** Use `tcpdump` or Wireshark for packet analysis.
</details>

**Success Criteria**: You understand packet structure and can analyze network traffic.

---

## Mini-Quiz ✅

1. **What is the main difference between TCP and UDP?**
   - [ ] TCP is faster
   - [ ] TCP is reliable, UDP is not
   - [ ] UDP is encrypted
   - [ ] They use different ports

2. **Which protocol is used for email transmission?**
   - [ ] HTTP
   - [ ] FTP
   - [ ] SMTP
   - [ ] SSH

3. **What port does SSH use by default?**
   - [ ] 21
   - [ ] 22
   - [ ] 23
   - [ ] 25

4. **What does DNS do?**
   - [ ] Transfers files
   - [ ] Translates domain names to IP addresses
   - [ ] Encrypts traffic
   - [ ] Sends emails

5. **Which protocol would you use for real-time video streaming?**
   - [ ] TCP
   - [ ] UDP
   - [ ] FTP
   - [ ] SMTP

6. **What is SFTP?**
   - [ ] Simple FTP
   - [ ] Super Fast Transfer Protocol
   - [ ] SSH File Transfer Protocol
   - [ ] Secure File Transmission Process

7. **Which port does HTTPS use?**
   - [ ] 80
   - [ ] 443
   - [ ] 8080
   - [ ] 3000

8. **What is the purpose of a socket in network programming?**
   - [ ] To plug in cables
   - [ ] An endpoint for sending/receiving data
   - [ ] A type of server
   - [ ] A security measure

<details>
<summary>Show Answers</summary>

1. **B** - TCP is reliable, UDP is not (TCP guarantees delivery, UDP doesn't)
2. **C** - SMTP (Simple Mail Transfer Protocol)
3. **B** - 22 (SSH uses port 22 by default)
4. **B** - Translates domain names to IP addresses
5. **B** - UDP (faster, tolerates packet loss)
6. **C** - SSH File Transfer Protocol (secure file transfer over SSH)
7. **B** - 443 (HTTPS uses port 443)
8. **B** - An endpoint for sending/receiving data

**Scoring:**
- 8/8: Protocol expert! 🌟
- 6-7/8: Great understanding! 👍
- 4-5/8: Good start, review the concepts
- 0-3/8: Review the lesson and try again
</details>

---

## Solutions

Complete solutions can be found in [solutions/05-other-protocols-solutions.md](../solutions/05-other-protocols-solutions.md)

---

[← Back to Lesson](./README.md) | [Next: Security Basics →](../06-Security-Basics/)
