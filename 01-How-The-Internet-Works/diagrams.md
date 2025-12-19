# 📊 How The Internet Works - Diagrams

Visual representations to help understand internet fundamentals, IP addresses, DNS, routing, and packets.

## 1. The Internet: Big Picture

Overview of how devices connect to the internet:

```
┌─────────────────────────────────────────────────────────────┐
│                   The Internet                              │
│         (Global Network of Networks)                        │
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│  │  Data    │    │  Web     │    │  Cloud   │            │
│  │  Center  │────│  Server  │────│  Service │            │
│  └──────────┘    └──────────┘    └──────────┘            │
│       │               │                │                   │
│       │    Backbone Routers            │                   │
│       └───────────┬───────────┬────────┘                   │
│                   │           │                            │
│              ┌────┴────┐ ┌────┴────┐                       │
│              │  ISP A  │ │  ISP B  │                       │
│              └────┬────┘ └────┬────┘                       │
│                   │           │                            │
└───────────────────┼───────────┼────────────────────────────┘
                    │           │
          ┌─────────┴──┐   ┌────┴─────────┐
          │ Your Home  │   │ Office       │
          │ Network    │   │ Network      │
          │            │   │              │
          │ ┌────────┐ │   │ ┌──────────┐│
          │ │ Router │ │   │ │  Router  ││
          │ └───┬────┘ │   │ └────┬─────┘│
          │     │      │   │      │      │
          │ ┌───┴────┐ │   │  ┌───┴────┐ │
          │ │Devices │ │   │  │Devices │ │
          │ └────────┘ │   │  └────────┘ │
          └────────────┘   └──────────────┘
```

---

## 2. IP Address Structure (IPv4)

Breaking down an IPv4 address:

```
        192    .    168    .    1    .    100
         │          │          │         │
    Octet 1    Octet 2    Octet 3   Octet 4
    ┌──┴──┐   ┌──┴──┐   ┌──┴──┐   ┌──┴──┐
    │ 8   │   │ 8   │   │ 8   │   │ 8   │  bits
    │ bits│   │ bits│   │ bits│   │ bits│
    └─────┘   └─────┘   └─────┘   └─────┘
    
    Total: 32 bits (4 bytes)
    
    Each octet: 0-255 (2^8 = 256 values)
    
    Binary representation:
    11000000.10101000.00000001.01100100


Network Classes (Traditional):

Class A:   0.0.0.0     to 127.255.255.255   (Large networks)
Class B: 128.0.0.0     to 191.255.255.255   (Medium networks)  
Class C: 192.0.0.0     to 223.255.255.255   (Small networks)

Private IP Ranges (Not routable on internet):
10.0.0.0       to  10.255.255.255    (Class A private)
172.16.0.0     to  172.31.255.255    (Class B private)
192.168.0.0    to  192.168.255.255   (Class C private)
```

---

## 3. IPv4 vs IPv6 Comparison

```
IPv4
────────────────────────────
Format:      192.168.1.1
Length:      32 bits (4 bytes)
Addresses:   ~4.3 billion
Notation:    Decimal (dotted)
Example:     203.0.113.45

┌────────────┬────────────┬────────────┬────────────┐
│  192       │  168       │  1         │  1         │
│  (8 bits)  │  (8 bits)  │  (8 bits)  │  (8 bits)  │
└────────────┴────────────┴────────────┴────────────┘


IPv6
────────────────────────────
Format:      2001:0db8:85a3:0000:0000:8a2e:0370:7334
Length:      128 bits (16 bytes)
Addresses:   ~340 undecillion (340 trillion trillion trillion)
Notation:    Hexadecimal (colon-separated)
Example:     2001:4860:4860::8888 (Google DNS, shortened)

┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
│ 2001 │ 0db8 │ 85a3 │ 0000 │ 0000 │ 8a2e │ 0370 │ 7334 │
│ 16b  │ 16b  │ 16b  │ 16b  │ 16b  │ 16b  │ 16b  │ 16b  │
└──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘

Shorthand rules:
- Leading zeros can be omitted: 0db8 → db8
- Consecutive zeros can be replaced with ::: 0000:0000 → ::
  Example: 2001:0db8:0000:0000:0000:0000:0000:0001
       →   2001:db8::1
```

---

## 4. DNS Resolution Process

Step-by-step DNS lookup for "www.example.com":

```
┌──────────────────────────────────────────────────────────┐
│  User types: www.example.com                             │
└────────────────┬─────────────────────────────────────────┘
                 │
                 ▼
         ┌───────────────┐
         │   Browser     │  1. Check browser cache
         │   Cache       │     Found? Return IP ✓
         └───────┬───────┘     Not found? Continue ↓
                 │
                 ▼
         ┌───────────────┐
         │   OS Cache    │  2. Check operating system cache
         │  (hosts file) │     Found? Return IP ✓
         └───────┬───────┘     Not found? Continue ↓
                 │
                 ▼
         ┌───────────────┐
         │  ISP DNS      │  3. Query ISP's DNS server
         │  Resolver     │     Found in cache? Return IP ✓
         └───────┬───────┘     Not found? Do recursive query ↓
                 │
                 ▼
         ┌───────────────┐
         │  Root DNS     │  4. Query root DNS server
         │   Servers     │     Returns: "Ask .com TLD server"
         │   (.)         │     IP: 192.5.6.30
         └───────┬───────┘
                 │
                 ▼
         ┌───────────────┐
         │  TLD DNS      │  5. Query .com TLD server
         │  (.com)       │     Returns: "Ask example.com's server"
         └───────┬───────┘     IP: 192.12.94.30
                 │
                 ▼
         ┌───────────────┐
         │ Authoritative │  6. Query example.com's DNS
         │   DNS Server  │     Returns: IP = 93.184.216.34
         │ (example.com) │     TTL: 86400 seconds
         └───────┬───────┘
                 │
                 ▼
         ┌───────────────┐
         │  Cache & Use  │  7. ISP caches result for TTL
         │               │     Returns IP to your computer
         └───────────────┘     Computer caches too

Total time: ~100-200ms (first lookup)
           ~1-2ms (cached lookups)


DNS Hierarchy Tree:

                  . (root)
                 /│\
                / │ \
              /   │   \
          .com  .org  .net  .edu  ...
           │
           │
        example.com
           │
        ┌──┴──┐
      www    mail
```

---

## 5. Packet Structure

Anatomy of a data packet:

```
┌───────────────────────────────────────────────────────┐
│                 IP PACKET                             │
├───────────────────────────────────────────────────────┤
│  IP HEADER                                            │
│  ┌─────────────────────────────────────────────────┐ │
│  │ Source IP:      192.168.1.100                   │ │
│  │ Destination IP: 93.184.216.34                   │ │
│  │ Protocol:       TCP                              │ │
│  │ TTL:            64 (hops remaining)             │ │
│  │ Packet ID:      #12345                          │ │
│  │ Flags:          Don't Fragment                   │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  TCP HEADER (if TCP protocol)                        │
│  ┌─────────────────────────────────────────────────┐ │
│  │ Source Port:      52341                         │ │
│  │ Destination Port: 80 (HTTP)                     │ │
│  │ Sequence Number:  #7890                         │ │
│  │ ACK Number:       #4567                         │ │
│  │ Flags:            SYN, ACK                      │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  DATA PAYLOAD                                         │
│  ┌─────────────────────────────────────────────────┐ │
│  │  GET /index.html HTTP/1.1                       │ │
│  │  Host: www.example.com                          │ │
│  │  User-Agent: Mozilla/5.0...                     │ │
│  │  ...                                            │ │
│  │  (Actual content - up to ~1500 bytes total)    │ │
│  └─────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────┘

Maximum Transmission Unit (MTU): Usually 1500 bytes
- IP Header: ~20 bytes
- TCP Header: ~20 bytes
- Data Payload: ~1460 bytes
```

---

## 6. Routing: How Packets Travel

Packet journey from your computer to a web server:

```
Your Computer                                      Web Server
192.168.1.100                                     93.184.216.34
     │                                                   ▲
     │ Packet:                                           │
     │ From: 192.168.1.100                              │
     │ To:   93.184.216.34                              │
     │ Data: "GET /page.html"                           │
     │                                                   │
     ▼                                                   │
┌─────────┐                                        ┌─────────┐
│ Router  │ Hop 1: Home Router                     │  Web    │
│ (Home)  │ Decision: Send to ISP                  │  Server │
└────┬────┘                                        │         │
     │                                              └─────────┘
     ▼                                                   ▲
┌─────────┐                                             │
│   ISP   │ Hop 2: ISP Router                           │
│ Router  │ Decision: Send to regional hub              │
└────┬────┘                                             │
     │                                                   │
     ▼                                                   │
┌─────────┐                                             │
│Regional │ Hop 3-5: Multiple ISP hops                  │
│ Routers │ Decision: Best path toward destination      │
└────┬────┘                                             │
     │                                                   │
     ▼                                                   │
┌─────────┐                                             │
│Internet │ Hop 6-8: Internet backbone                  │
│Backbone │ Decision: Route to destination ISP          │
└────┬────┘                                             │
     │                                                   │
     ▼                                                   │
┌─────────┐                                             │
│ Server  │ Hop 9-10: Destination ISP routers           │
│   ISP   │ Decision: Route to server network           │
└────┬────┘                                             │
     │                                                   │
     └───────────────────────────────────────────────────┘

Each router:
1. Reads destination IP
2. Checks routing table
3. Forwards to next hop
4. Decrements TTL
5. If TTL = 0, drops packet
```

---

## 7. Private vs Public IP Addresses with NAT

How Network Address Translation works:

```
Home Network (Private IPs)          Internet (Public IPs)
────────────────────────────        ────────────────────

┌──────────────────────┐
│  Laptop              │
│  192.168.1.100:5234  │───┐
└──────────────────────┘   │
                           │
┌──────────────────────┐   │      ┌──────────────┐
│  Phone               │   ├─────→│   Router     │
│  192.168.1.101:5235  │───┤      │  (NAT)       │
└──────────────────────┘   │      │              │
                           │      │ Private side:│
┌──────────────────────┐   │      │ 192.168.1.1  │
│  Desktop             │   │      │              │
│  192.168.1.102:5236  │───┘      │ Public side: │
└──────────────────────┘          │ 203.0.113.45 │
                                  └──────┬───────┘
                                         │
              All devices share          │
              one public IP!             │
                                         ▼
                                  ┌──────────────┐
                                  │  Internet    │
                                  │              │
                                  │ Web Server:  │
                                  │ 93.184.216.34│
                                  └──────────────┘

NAT Translation Table:
────────────────────────────────────────────────────
Internal IP:Port      →    External IP:Port
────────────────────────────────────────────────────
192.168.1.100:5234    →    203.0.113.45:10001
192.168.1.101:5235    →    203.0.113.45:10002
192.168.1.102:5236    →    203.0.113.45:10003

Outgoing: Router changes source IP from private to public
Incoming: Router uses table to route response to correct device
```

---

## 8. Data Transmission: File Transfer Example

Sending a 5KB file over the internet:

```
Original File: photo.jpg (5,000 bytes)
                    │
                    │ Break into packets
                    ▼
        ┌───────────┼───────────┐
        │           │           │
    Packet 1    Packet 2    Packet 3   Packet 4
    1460 bytes  1460 bytes  1460 bytes  620 bytes
        │           │           │           │
        └───────────┴───────────┴───────────┘
                    │
            Send across internet
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼           ▼

Route A:          Route B:          Route A:          Route C:
Router A          Router B          Router A          Router D
Router B          Router C          Router C          Router E
Router C          Router D          Router D          Router D
Router D          Router D          Router D          Router D

    │               │               │               │
    └───────────────┴───────────────┴───────────────┘
                        │
              Arrive at destination
                (possibly out of order!)
                        │
                Packet 2 arrives ✓
                Packet 1 arrives ✓
                Packet 4 arrives ✓
                Packet 3 missing ✗
                        │
                Request Packet 3 again
                        │
                Packet 3 arrives ✓
                        │
              Reassemble in correct order
                        │
                    ┌───┴───┐
                Packet 1, 2, 3, 4
                    │
                photo.jpg
              (5,000 bytes) ✓
```

---

## 9. Latency vs Bandwidth

Understanding the difference:

```
LATENCY (Ping Time)
═══════════════════
How long for data to travel

Analogy: Delivery truck speed

Low Latency (10ms):
Your PC ──10ms──> Server
         Quick!

High Latency (200ms):
Your PC ────200ms────> Server
         Slow...

Important for: Gaming, Video calls, Real-time apps


BANDWIDTH (Data Transfer Rate)
═══════════════════════════════
How much data can be sent at once

Analogy: Truck size

Low Bandwidth (1 Mbps):
Your PC ═╤═> Server
         Small pipe

High Bandwidth (100 Mbps):
Your PC ═══════════> Server
         Large pipe

Important for: Downloads, Streaming, Large files


COMBINATION EFFECTS:
═══════════════════

High Latency + Low Bandwidth = ☹️
- Slow response AND can't send much data
- Like slow, small delivery truck
- Bad for everything

Low Latency + Low Bandwidth = 😐
- Quick response but limited data
- Like fast, small delivery truck
- OK for web browsing, bad for downloads

High Latency + High Bandwidth = 😐
- Slow response but lots of data
- Like slow, large delivery truck
- Bad for gaming, OK for downloads

Low Latency + High Bandwidth = 😊
- Quick response and lots of data
- Like fast, large delivery truck
- Ideal for all uses!
```

---

## 10. TCP Three-Way Handshake

How a TCP connection is established:

```
   Client                           Server
(Your Computer)                  (Web Server)
     │                                │
     │        SYN                     │
     │   (Sequence # = 1000)          │
     │───────────────────────────────>│
     │                                │
     │                                │ "OK, I'm ready"
     │                                │
     │      SYN-ACK                   │
     │  (Sequence # = 5000)           │
     │  (Acknowledgment = 1001)       │
     │<───────────────────────────────│
     │                                │
     │ "Great, let's talk!"           │
     │                                │
     │         ACK                    │
     │  (Acknowledgment = 5001)       │
     │───────────────────────────────>│
     │                                │
     │  CONNECTION ESTABLISHED ✓      │
     │                                │
     │      Data Transfer             │
     │<──────────────────────────────>│
     │                                │

Steps:
1. SYN (Synchronize): Client requests connection
2. SYN-ACK: Server acknowledges and confirms
3. ACK: Client acknowledges server's response

Now data can be exchanged reliably!
```

---

## Summary

These diagrams illustrate:
- ✅ Internet infrastructure and connectivity
- ✅ IP address structure (IPv4 and IPv6)
- ✅ DNS resolution process and hierarchy
- ✅ Packet structure and routing
- ✅ Private vs public IPs with NAT
- ✅ Data transmission in packets
- ✅ Latency vs bandwidth concepts
- ✅ TCP connection establishment

**Next:** Apply these concepts in the [exercises](./exercises.md) and verify understanding with the [checkpoint](./checkpoint.md).
