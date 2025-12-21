# 🏋️ Exercises: How The Internet Works

These hands-on exercises will help you practice the concepts from this module. Try to complete them on your own first, then check the hints if you get stuck.

## Exercise 1: Discover Your Network 🔍

**Objective**: Learn about your own network configuration.

**Tasks**:
1. Find your private IP address
2. Find your public IP address  
3. Find your default gateway (router) IP address
4. Find your DNS server address
5. Find your MAC address

**Tools**: `ifconfig` (Mac/Linux) or `ipconfig` (Windows), `curl ifconfig.me`

<details>
<summary>💡 Hint</summary>

**Mac/Linux:**
```bash
ifconfig                    # Private IP and MAC address
netstat -nr | grep default  # Default gateway
cat /etc/resolv.conf        # DNS servers
curl ifconfig.me            # Public IP
```

**Windows:**
```bash
ipconfig /all              # Shows everything!
curl ifconfig.me           # Public IP
```
</details>

**Success Criteria**: You should be able to write down at least 4 of these values.

---

## Exercise 2: Ping Different Destinations 🏓

**Objective**: Understand network reachability and latency.

**Tasks**:
1. Ping your router/gateway (should be very fast)
2. Ping a popular website like `google.com`
3. Ping a website in another country (e.g., `bbc.co.uk` if you're in the US)
4. Compare the response times

**Questions to answer**:
- Which ping was fastest? Why?
- What's the typical response time to google.com?
- Did any pings fail? What might cause that?

<details>
<summary>💡 Hint</summary>

```bash
# Ping your gateway (replace with your actual gateway IP)
ping 192.168.1.1

# Ping Google (press Ctrl+C to stop)
ping google.com

# Ping BBC
ping bbc.co.uk

# On Windows, ping automatically stops after 4 requests
# On Mac/Linux, use Ctrl+C to stop
```

**Expected observations**:
- Gateway: <1ms (local network)
- Google: 10-50ms (depends on distance)
- International sites: 100-300ms (much further)
</details>

**Success Criteria**: You understand why local pings are faster than remote pings.

---

## Exercise 3: Trace The Route 🗺️

**Objective**: Visualize how your data travels across the internet.

**Tasks**:
1. Run `traceroute` to `google.com`
2. Count how many hops it takes
3. Identify where the delay increases most
4. Try traceroute to a different continent

**Questions to answer**:
- How many routers did your data pass through?
- Which hop showed the biggest time increase?
- Can you identify your ISP's routers vs backbone routers?

<details>
<summary>💡 Hint</summary>

**Mac/Linux:**
```bash
traceroute google.com
traceroute bbc.co.uk
```

**Windows:**
```bash
tracert google.com
tracert bbc.co.uk
```

**Reading the output**:
- First few hops: Your local network and ISP
- Middle hops: Internet backbone routers
- Last hop: Destination server
- `* * *` means that router didn't respond (normal security measure)
</details>

**Success Criteria**: You can explain the path your data takes to reach a website.

---

## Exercise 4: DNS Detective 🔎

**Objective**: Understand how DNS resolution works.

**Tasks**:
1. Use `nslookup` to find the IP address of `github.com`
2. Look up `youtube.com` - does it have multiple IP addresses?
3. Try looking up `www.example.com` and note the IP
4. Look up your own domain name if you have one

**Questions to answer**:
- Do all domain names resolve to a single IP address?
- What does it mean if a domain has multiple IPs?
- Which DNS server answered your query?

<details>
<summary>💡 Hint</summary>

```bash
nslookup github.com
nslookup youtube.com
nslookup www.example.com
```

**Advanced DNS queries**:
```bash
# Specify which DNS server to use
nslookup github.com 8.8.8.8

# Get more details
nslookup -type=any github.com
```

**Why multiple IPs?**
Large websites have multiple servers for:
- Load balancing (distribute traffic)
- Redundancy (if one fails, others work)
- Geographic distribution (serve users from nearby servers)
</details>

**Success Criteria**: You can look up any domain name and get its IP address.

---

## Exercise 5: Compare Internet Speeds 🚀

**Objective**: Understand latency vs bandwidth.

**Tasks**:
1. Ping a nearby server and note the time
2. Ping a server on another continent and note the time
3. Visit an internet speed test website (like fast.com or speedtest.net)
4. Compare ping times with download speeds

**Questions to answer**:
- Is your ping time related to your download speed?
- Why does geographic distance affect ping but not always download speed?
- What's the difference between latency and bandwidth?

<details>
<summary>💡 Hint</summary>

**Latency vs Bandwidth Analogy**:
- **Latency**: How long it takes for a car to travel from city A to city B
- **Bandwidth**: How many lanes the highway has (how many cars at once)

You can have:
- Low latency + High bandwidth = Fast response, lots of data (ideal!)
- Low latency + Low bandwidth = Fast response, limited data (good for chat)
- High latency + High bandwidth = Slow response, lots of data (satellite internet)
- High latency + Low bandwidth = Slow response, limited data (old dial-up)

**Testing commands**:
```bash
# Test latency
ping google.com

# Test bandwidth (download a file)
curl -o /dev/null http://speedtest.tele2.net/10MB.zip
```
</details>

**Success Criteria**: You can explain the difference between latency (ping time) and bandwidth (download speed).

---

## Exercise 6: Build a Network Diagram 📊

**Objective**: Visualize your home or school network.

**Tasks**:
1. Draw a diagram showing how your computer connects to the internet
2. Include: your device, router, ISP, and a destination server
3. Label IP addresses where you know them
4. Add arrows showing the flow of data

**Components to include**:
- Your computer (with private IP)
- Your router/gateway
- Your ISP's network
- DNS server
- Destination web server

<details>
<summary>💡 Hint</summary>

Your diagram should look something like this:

```
[Your Computer]              [DNS Server]
192.168.1.100               8.8.8.8
      |                         ↑
      |                         | (lookup domain)
      ↓                         |
[Home Router]  ←----------------┘
192.168.1.1
[Public IP: 203.0.113.45]
      |
      ↓
[ISP Router]
      |
      ↓
[Internet Backbone]
      |
      ↓
[Web Server]
(e.g., github.com)
140.82.114.4
```

**Add these labels**:
- "HTTP Request" on arrows going out
- "HTTP Response" on arrows coming back
- "DNS Query" to the DNS server
- "DNS Response" back from DNS
</details>

**Success Criteria**: Someone else can look at your diagram and understand how data flows.

---

## Challenge Exercise: Network Detective 🕵️

**Objective**: Investigate real-world network behavior.

**The Mystery**: A website is loading slowly. Use your tools to diagnose why!

**Steps**:
1. Pick a website (or use `example.com` for testing)
2. Ping the website - is latency normal?
3. Traceroute to the website - where do delays occur?
4. Use `nslookup` - is DNS responding quickly?
5. Try accessing the site in your browser - does it load?

**Write up your findings**:
- What's the round-trip time?
- How many hops to the destination?
- Where do you see the most delay?
- Is the problem with DNS, routing, or the server itself?

<details>
<summary>💡 Hint</summary>

**Diagnostic checklist**:
```bash
# 1. DNS check
nslookup target-website.com
# Is this fast? (Should be <100ms)

# 2. Ping check
ping target-website.com
# Is this reasonable? (<50ms nearby, <200ms far away)

# 3. Route check
traceroute target-website.com  # or tracert on Windows
# Where do delays spike? Look for big jumps between hops

# 4. Multiple tests
ping -c 10 target-website.com  # Mac/Linux
ping -n 10 target-website.com  # Windows
# Are times consistent or varying wildly?
```

**Possible diagnoses**:
- High ping everywhere → Your internet connection is slow
- Delay at specific hop → That router/network is congested
- DNS slow → Try different DNS (8.8.8.8 or 1.1.1.1)
- Can't reach server → Server might be down or blocking pings
</details>

**Success Criteria**: You can identify where network delays occur and explain why.

---

## Mini-Quiz: Test Your Knowledge ✅

Answer these questions to check your understanding:

1. **What is an IP address?**
   - [ ] A website's name
   - [ ] A unique identifier for a device on a network
   - [ ] A type of cable
   - [ ] A security protocol

2. **What does DNS do?**
   - [ ] Encrypts your internet traffic
   - [ ] Translates domain names to IP addresses
   - [ ] Speeds up your internet connection
   - [ ] Blocks malicious websites

3. **What is a packet?**
   - [ ] A small piece of data sent over a network
   - [ ] A network cable
   - [ ] An email attachment
   - [ ] A type of router

4. **What does ping measure?**
   - [ ] Download speed
   - [ ] Round-trip time to a destination
   - [ ] Available bandwidth
   - [ ] Number of packets sent

5. **What's the difference between a private and public IP address?**
   - [ ] Private IPs are faster
   - [ ] Private IPs are used within local networks; public IPs are visible on the internet
   - [ ] Public IPs are more secure
   - [ ] There is no difference

<details>
<summary>Show Answers</summary>

1. **B** - A unique identifier for a device on a network
2. **B** - Translates domain names to IP addresses
3. **A** - A small piece of data sent over a network
4. **B** - Round-trip time to a destination
5. **B** - Private IPs are used within local networks; public IPs are visible on the internet

**Scoring**:
- 5/5: Excellent! You've mastered the basics.
- 3-4/5: Good job! Review the concepts you missed.
- 1-2/5: Review the lesson and try again.
</details>

---

## Solutions

Complete solutions for these exercises can be found in the [solutions folder](../solutions/01-how-the-internet-works-solutions.md).

## What's Next?

Once you've completed these exercises, you're ready to move on to [HTTP Fundamentals](../02-HTTP-Fundamentals/)!

---

[← Back to Lesson](./README.md)
