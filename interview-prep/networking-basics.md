# Networking Basics - Interview Questions

Common interview questions about networking fundamentals.

## Junior Level Questions

### Q1: What is the difference between a router and a switch?
**Answer:**
- **Router:** Connects different networks together and routes traffic between them (Layer 3 - Network layer)
- **Switch:** Connects devices within the same network (Layer 2 - Data link layer)

**Follow-up:** Explain how each device makes forwarding decisions.

---

### Q2: Explain the OSI model layers
**Answer:**
The 7 layers from top to bottom:
1. **Application:** User-facing protocols (HTTP, FTP, SMTP)
2. **Presentation:** Data formatting, encryption (SSL/TLS)
3. **Session:** Managing connections/sessions
4. **Transport:** End-to-end communication (TCP, UDP)
5. **Network:** Routing and addressing (IP)
6. **Data Link:** Node-to-node transfer (Ethernet, MAC)
7. **Physical:** Physical transmission (cables, signals)

**Tip:** Mnemonic: "All People Seem To Need Data Processing"

---

### Q3: What is the difference between TCP and UDP?
**Answer:**
- **TCP (Transmission Control Protocol):**
  - Connection-oriented
  - Reliable (guarantees delivery)
  - Ordered (packets arrive in sequence)
  - Slower (more overhead)
  - Use: HTTP, email, file transfer

- **UDP (User Datagram Protocol):**
  - Connectionless
  - Unreliable (no delivery guarantee)
  - Unordered
  - Faster (less overhead)
  - Use: Streaming, gaming, DNS

**Follow-up:** When would you choose one over the other?

---

### Q4: What is a subnet mask?
**Answer:**
A subnet mask determines which part of an IP address identifies the network and which part identifies the host.

Example: IP 192.168.1.100 with subnet mask 255.255.255.0
- Network: 192.168.1.0
- Host: 100
- Can have 254 hosts in this subnet (1-254)

---

### Q5: Explain DNS resolution process
**Answer:**
1. Browser checks its cache
2. OS checks its cache
3. Query sent to recursive resolver (ISP DNS)
4. Resolver queries root DNS server
5. Root points to TLD server (.com)
6. TLD points to authoritative server
7. Authoritative server returns IP
8. IP cached and returned to browser

**Time:** Typically 100-200ms first time, ~1-2ms when cached

---

## Mid-Level Questions

### Q6: What is NAT and why is it used?
**Answer:**
**NAT (Network Address Translation)** allows multiple devices on a private network to share a single public IP address.

**Why:**
- IPv4 address shortage
- Security (hides internal network structure)
- Flexibility (change internal IPs without affecting external)

**Types:**
- Static NAT: One-to-one mapping
- Dynamic NAT: Pool of public IPs
- PAT (Port Address Translation): Most common, maps ports

---

### Q7: Explain the TCP three-way handshake
**Answer:**
1. **SYN:** Client sends SYN packet to server
2. **SYN-ACK:** Server responds with SYN-ACK
3. **ACK:** Client sends ACK back

Connection is now established.

**Follow-up:** How does TCP handle connection termination? (FIN, FIN-ACK)

---

### Q8: What is the difference between a hub, switch, and router?
**Answer:**
- **Hub:** 
  - Layer 1 (Physical)
  - Broadcasts to all ports
  - Collision domain shared
  - Obsolete

- **Switch:**
  - Layer 2 (Data Link)
  - Learns MAC addresses
  - Forwards to specific port
  - Each port is separate collision domain

- **Router:**
  - Layer 3 (Network)
  - Routes between different networks
  - Uses IP addresses
  - Can filter and control traffic

---

## Senior Level Questions

### Q9: How would you troubleshoot a slow network connection?
**Answer:**
Systematic approach:
1. **Identify scope:** Single device or all devices?
2. **Test locally:** Run speed test, check local network
3. **Check physical:** Cable connections, WiFi signal
4. **Use tools:**
   - `ping` - Test connectivity and latency
   - `traceroute` - Find where slowdown occurs
   - `iperf` - Test throughput
   - `netstat` - Check connections
5. **Check logs:** Router, firewall, server logs
6. **Monitor:** Network utilization, bandwidth
7. **Consider:** DNS issues, MTU problems, congestion

---

### Q10: Explain how HTTPS works
**Answer:**
HTTPS = HTTP + TLS/SSL encryption

**Process:**
1. Client initiates HTTPS connection
2. Server sends SSL certificate with public key
3. Client verifies certificate with CA
4. Client generates session key, encrypts with server's public key
5. Server decrypts with private key
6. Both use session key for symmetric encryption
7. All data encrypted with session key

**Why:**
- Encrypts data in transit
- Authenticates server identity
- Prevents man-in-the-middle attacks

---

## Behavioral Questions

### Q11: Describe a time you debugged a network issue
**Framework:**
- **Situation:** Describe the problem
- **Task:** What you needed to accomplish
- **Action:** Steps you took (tools used, approach)
- **Result:** How it was resolved, what you learned

**Example Answer:**
"Users reported intermittent connection drops. I used `ping` to confirm packet loss, then `traceroute` to identify the problematic hop was our ISP's router. Contacted ISP, they found faulty hardware. Learned to systematically isolate problems using network tools."

---

## Tips for Success

### During the Interview
- ✅ Think out loud - explain your reasoning
- ✅ Draw diagrams - visualize the problem
- ✅ Ask clarifying questions - ensure you understand
- ✅ Admit what you don't know - better than guessing
- ✅ Relate to practical experience

### Topics to Review
- OSI model and TCP/IP stack
- Common protocols (HTTP, DNS, DHCP)
- Network troubleshooting tools
- Security basics (TLS, firewalls)
- Routing and switching fundamentals

---

**More interview questions:**
- [HTTP and APIs](./http-and-apis.md)
- [WebSockets](./websockets-realtime.md)
- [Security](./security-questions.md)
