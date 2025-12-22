# Lab 5: Rate Limiting

## Overview

Rate limiting is a crucial security and stability measure that controls how many requests a client can make to an API within a given time period. This lab teaches you to implement, test, and bypass (ethically) rate limiting mechanisms.

## Learning Objectives

By the end of this lab, you will:
- Understand why rate limiting is important
- Implement various rate limiting strategies
- Test rate limiters with automated tools
- Identify and understand bypass techniques
- Build robust, production-ready rate limiters
- Handle rate limiting in client applications

## Prerequisites

- Basic understanding of HTTP and APIs
- Python 3.7+
- Flask installed (`pip install flask flask-limiter redis`)

## Lab Structure

```
lab5-rate-limiting/
├── README.md (this file)
├── basic_rate_limiter.py (simple implementation)
├── advanced_rate_limiter.py (production-ready)
├── test_tools.py (testing utilities)
├── bypass_techniques.md (educational bypass methods)
└── client_examples.py (handling rate limits)
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install flask flask-limiter redis
   ```

2. **Install Redis (for advanced rate limiting):**
   ```bash
   # macOS
   brew install redis
   brew services start redis
   
   # Linux
   sudo apt-get install redis-server
   sudo systemctl start redis
   
   # Windows
   # Download from https://github.com/microsoftarchive/redis/releases
   ```

3. **Start the application:**
   ```bash
   python3 basic_rate_limiter.py
   ```

## Part 1: Why Rate Limiting?

### Security Benefits

1. **Prevents Brute Force Attacks**
   - Limits login attempts
   - Slows down password guessing
   - Protects against credential stuffing

2. **Mitigates DoS/DDoS**
   - Prevents resource exhaustion
   - Stops abuse of expensive operations
   - Maintains service availability

3. **Prevents Data Scraping**
   - Limits bulk data extraction
   - Protects proprietary information
   - Reduces competitive intelligence gathering

4. **Enforces Fair Usage**
   - Prevents monopolization of resources
   - Ensures equal access for all users
   - Enables freemium business models

### Business Benefits

1. **Cost Control**
   - Limits cloud/bandwidth costs
   - Prevents unexpected billing spikes
   - Enables predictable infrastructure scaling

2. **Quality of Service**
   - Maintains performance for all users
   - Prevents service degradation
   - Enables SLA compliance

## Part 2: Rate Limiting Strategies

### 1. Fixed Window

**How it works:**
- Counts requests in fixed time windows (e.g., per minute)
- Resets counter at window boundary

**Implementation:**
```python
from datetime import datetime, timedelta

class FixedWindowLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}
    
    def is_allowed(self, client_id):
        now = datetime.now()
        window_start = now.replace(second=0, microsecond=0)
        
        key = f"{client_id}:{window_start}"
        
        if key not in self.requests:
            self.requests[key] = 0
        
        if self.requests[key] < self.max_requests:
            self.requests[key] += 1
            return True
        
        return False
```

**Pros:**
- Simple to implement
- Memory efficient
- Easy to understand

**Cons:**
- Burst traffic at window boundaries
- Uneven distribution of requests

### 2. Sliding Window Log

**How it works:**
- Keeps log of request timestamps
- Counts requests in sliding window

**Implementation:**
```python
from collections import deque
from datetime import datetime, timedelta

class SlidingWindowLog:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.logs = {}
    
    def is_allowed(self, client_id):
        now = datetime.now()
        
        if client_id not in self.logs:
            self.logs[client_id] = deque()
        
        # Remove old entries
        cutoff = now - timedelta(seconds=self.window_seconds)
        while self.logs[client_id] and self.logs[client_id][0] < cutoff:
            self.logs[client_id].popleft()
        
        # Check limit
        if len(self.logs[client_id]) < self.max_requests:
            self.logs[client_id].append(now)
            return True
        
        return False
```

**Pros:**
- Accurate rate limiting
- No burst issues
- Fair distribution

**Cons:**
- Higher memory usage
- More complex implementation

### 3. Token Bucket

**How it works:**
- Bucket holds tokens
- Requests consume tokens
- Tokens refill at constant rate
- Allows bursts up to bucket size

**Implementation:**
```python
import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
    
    def is_allowed(self, tokens=1):
        # Refill tokens
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * self.refill_rate
        )
        self.last_refill = now
        
        # Check if enough tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        
        return False
```

**Pros:**
- Allows controlled bursts
- Smooth traffic flow
- Flexible configuration

**Cons:**
- Complex to understand
- Requires careful tuning

### 4. Leaky Bucket

**How it works:**
- Requests added to queue
- Processed at constant rate
- Queue has maximum size

**Implementation:**
```python
from queue import Queue
import time
import threading

class LeakyBucket:
    def __init__(self, capacity, leak_rate):
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.queue = Queue(maxsize=capacity)
        self._start_leak()
    
    def _start_leak(self):
        def leak():
            while True:
                time.sleep(1.0 / self.leak_rate)
                if not self.queue.empty():
                    self.queue.get()
        
        thread = threading.Thread(target=leak, daemon=True)
        thread.start()
    
    def is_allowed(self):
        try:
            self.queue.put_nowait(1)
            return True
        except:
            return False
```

**Pros:**
- Smooth output rate
- Prevents bursts
- Predictable performance

**Cons:**
- Adds latency
- Complex implementation
- Requires background processing

## Part 3: Implementing with Flask-Limiter

### Basic Setup

```python
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# In-memory storage (development only)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/api/data")
@limiter.limit("10 per minute")
def get_data():
    return {"data": "value"}
```

### Redis-backed Storage (Production)

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379"
)

@app.route("/api/expensive")
@limiter.limit("5 per hour")
def expensive_operation():
    # ... expensive computation ...
    return {"result": "data"}
```

### Per-User Rate Limiting

```python
def get_user_id():
    # Get from JWT token, session, or API key
    return request.headers.get('X-User-ID', get_remote_address())

limiter = Limiter(
    app=app,
    key_func=get_user_id
)

@app.route("/api/user/data")
@limiter.limit("100 per hour")
def user_data():
    return {"data": "user-specific"}
```

### Dynamic Rate Limits

```python
def dynamic_limit():
    user_type = get_user_type()
    if user_type == "premium":
        return "1000 per hour"
    elif user_type == "free":
        return "100 per hour"
    else:
        return "10 per hour"

@app.route("/api/search")
@limiter.limit(dynamic_limit)
def search():
    return {"results": []}
```

## Part 4: Testing Rate Limiters

### Manual Testing with curl

```bash
# Test basic rate limit
for i in {1..15}; do
  curl http://localhost:5006/api/data
  echo "Request $i"
  sleep 0.1
done
```

### Automated Testing with Python

```python
import requests
import time

def test_rate_limit():
    url = "http://localhost:5006/api/data"
    
    # Make requests until rate limited
    for i in range(20):
        response = requests.get(url)
        print(f"Request {i+1}: {response.status_code}")
        
        if response.status_code == 429:
            print(f"Rate limited after {i+1} requests")
            print(f"Retry-After: {response.headers.get('Retry-After')}")
            print(f"X-RateLimit-Limit: {response.headers.get('X-RateLimit-Limit')}")
            print(f"X-RateLimit-Remaining: {response.headers.get('X-RateLimit-Remaining')}")
            break
        
        time.sleep(0.1)

test_rate_limit()
```

### Load Testing with Apache Bench

```bash
# 100 requests, 10 concurrent
ab -n 100 -c 10 http://localhost:5006/api/data

# With authentication
ab -n 100 -c 10 -H "Authorization: Bearer TOKEN" \
   http://localhost:5006/api/data
```

### Load Testing with wrk

```bash
# 1000 requests over 10 seconds, 10 connections
wrk -t10 -c10 -d10s http://localhost:5006/api/data

# With custom script
wrk -t10 -c10 -d10s -s script.lua http://localhost:5006/api/data
```

## Part 5: Bypass Techniques (Educational)

⚠️ **Warning:** These techniques are for educational purposes only. Use only on systems you own or have permission to test.

### 1. IP Rotation

**Attack:**
```python
# Using proxy rotation
proxies = ['proxy1.com', 'proxy2.com', 'proxy3.com']
for i in range(100):
    proxy = proxies[i % len(proxies)]
    requests.get(url, proxies={'http': proxy})
```

**Defense:**
- Rate limit by user ID, not just IP
- Detect and block proxy IPs
- Use device fingerprinting

### 2. Distributed Attacks

**Attack:**
```
Use botnet or cloud instances
Multiple IPs simultaneously
Each under rate limit
```

**Defense:**
- Global rate limits
- Pattern detection
- CAPTCHA for suspicious activity

### 3. Header Manipulation

**Attack:**
```python
# Try different headers
headers = [
    {'X-Forwarded-For': '1.2.3.4'},
    {'X-Real-IP': '5.6.7.8'},
    {'X-Client-IP': '9.10.11.12'}
]
```

**Defense:**
- Don't trust client headers
- Use actual client IP
- Validate X-Forwarded-For chain

### 4. Timing Attacks

**Attack:**
```python
# Request right before window resets
# Get double the requests per period
```

**Defense:**
- Use sliding windows
- Implement token bucket
- Monitor burst patterns

## Part 6: Response Headers

### Standard Rate Limit Headers

```python
@app.after_request
def add_rate_limit_headers(response):
    # Current limit
    response.headers['X-RateLimit-Limit'] = '100'
    
    # Remaining requests
    response.headers['X-RateLimit-Remaining'] = '75'
    
    # Window reset time (Unix timestamp)
    response.headers['X-RateLimit-Reset'] = '1640000000'
    
    # When rate limited (429 response)
    if response.status_code == 429:
        response.headers['Retry-After'] = '60'  # seconds
    
    return response
```

### Client Handling

```python
import requests
import time

def make_request_with_retry(url):
    while True:
        response = requests.get(url)
        
        if response.status_code == 429:
            # Rate limited - wait and retry
            retry_after = int(response.headers.get('Retry-After', 60))
            print(f"Rate limited. Waiting {retry_after} seconds...")
            time.sleep(retry_after)
            continue
        
        return response
```

## Best Practices Summary

### ✅ DO:
- Implement rate limiting at multiple layers (app, API gateway, CDN)
- Use Redis or similar for distributed rate limiting
- Return proper 429 status codes
- Include rate limit headers
- Rate limit by user ID when possible
- Different limits for different endpoints
- Allow burst traffic with token bucket
- Log rate limit violations
- Provide clear error messages
- Test thoroughly under load

### ❌ DON'T:
- Rely solely on IP-based limiting
- Use in-memory storage in production
- Forget to handle distributed systems
- Block completely without retry information
- Use same limit for all endpoints
- Ignore authenticated vs unauthenticated
- Forget to monitor rate limit metrics
- Set limits too restrictive
- Ignore bypass attempts in logs

## Additional Resources

- [OWASP API Security - Rate Limiting](https://owasp.org/www-project-api-security/)
- [Flask-Limiter Documentation](https://flask-limiter.readthedocs.io/)
- [Rate Limiting Strategies](https://cloud.google.com/architecture/rate-limiting-strategies-techniques)
- [Redis Rate Limiting](https://redis.io/docs/reference/patterns/distributed-locks/)

## Challenge Exercises

1. Implement a custom rate limiter from scratch
2. Create a distributed rate limiter with Redis
3. Build a rate limit bypass detector
4. Design tiered rate limits (free/pro/enterprise)
5. Implement exponential backoff client

## Next Steps

- Review all security labs completed
- Apply learnings to real projects
- Study [API Security Module](../../09-API-Security/)
- Explore [Network Security Best Practices](../../13-Network-Security-Best-Practices/)

---

**⚠️ Warning:** Always test rate limiting in staging before production!
