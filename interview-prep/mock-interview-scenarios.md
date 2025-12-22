# Mock Interview Scenarios

Complete mock interview scenarios with role descriptions, questions, expected answers, follow-ups, and evaluation criteria.

---

## Table of Contents
1. [Junior Backend Developer - API Development](#scenario-1-junior-backend-developer---api-development)
2. [Full Stack Developer - REST API Design](#scenario-2-full-stack-developer---rest-api-design)
3. [Senior Backend Engineer - System Design](#scenario-3-senior-backend-engineer---system-design)
4. [DevOps Engineer - Network Troubleshooting](#scenario-4-devops-engineer---network-troubleshooting)
5. [API Platform Engineer - Security & Scale](#scenario-5-api-platform-engineer---security--scale)

---

## Scenario 1: Junior Backend Developer - API Development

### Role Description
**Position**: Junior Backend Developer  
**Company**: SaaS startup building a task management application  
**Team Size**: 5 engineers  
**Tech Stack**: Python/Flask, PostgreSQL, REST APIs  
**Experience Required**: 0-2 years

### Interview Format
- 45 minutes total
- 15 minutes: Networking fundamentals
- 20 minutes: Practical API questions
- 10 minutes: Debugging scenario

---

### Question 1: What happens when you make an API call?

**Expected Answer:**
The candidate should explain the basic request-response cycle:

1. **DNS Resolution**: Convert domain name to IP address
2. **TCP Connection**: Three-way handshake (SYN, SYN-ACK, ACK)
3. **HTTP Request**: Client sends request with method, headers, and body
4. **Server Processing**: Server receives, validates, processes request
5. **HTTP Response**: Server sends back status code, headers, and body
6. **Connection Close**: Connection closed or kept alive for reuse

**Minimum Acceptable:**
- Mentions DNS lookup
- Understands client sends request, server sends response
- Knows what HTTP is

**Strong Answer Includes:**
- TCP handshake details
- Mention of HTTPS/TLS encryption
- HTTP headers and their purpose
- Status codes

**Red Flags:**
- Can't explain basic request/response
- Doesn't know what DNS is
- Confuses HTTP with other protocols

---

### Question 2: You need to create an endpoint to get a user's tasks. What would the endpoint look like?

**Expected Answer:**
```
GET /api/users/{userId}/tasks
```

Or alternatively:
```
GET /api/tasks?userId={userId}
```

The candidate should explain:
- **GET method** because we're retrieving data
- **RESTful resource naming** (plural nouns)
- **Path parameters** for user ID in the first approach
- **Query parameters** for filtering in the second approach

**Follow-up Question 1:**
"What if you wanted to support pagination?"

**Expected Answer:**
```
GET /api/users/{userId}/tasks?page=1&limit=20
```

Should mention:
- Query parameters for pagination
- Default values (e.g., limit=20 if not specified)
- Response should include total count

**Follow-up Question 2:**
"What status code should this return?"

**Expected Answer:**
- **200 OK** for successful retrieval
- **404 Not Found** if user doesn't exist
- **401 Unauthorized** if not authenticated
- **403 Forbidden** if user can't access another user's tasks

**Strong Answer Includes:**
- Discusses authorization (can user A see user B's tasks?)
- Mentions filtering options (status, priority, due date)
- Pagination metadata in response

---

### Question 3: How would you create a new task?

**Expected Answer:**
```
POST /api/tasks

Request Body:
{
  "title": "Complete API documentation",
  "description": "Write docs for all endpoints",
  "dueDate": "2024-01-31",
  "priority": "high",
  "userId": 123
}

Response (201 Created):
{
  "id": 456,
  "title": "Complete API documentation",
  "description": "Write docs for all endpoints",
  "dueDate": "2024-01-31",
  "priority": "high",
  "userId": 123,
  "createdAt": "2024-01-15T10:30:00Z",
  "status": "pending"
}
```

Should explain:
- **POST method** for creating resources
- **201 Created** status code
- **Location header**: `/api/tasks/456`
- Return created resource with generated fields (id, timestamps)

**Follow-up Question:**
"What validation would you do before creating the task?"

**Expected Answer:**
- **Required fields**: title, userId
- **Field formats**: dueDate is valid date, userId is integer
- **Business rules**: 
  - User exists
  - Title not empty
  - Priority is one of: low, medium, high
  - Due date not in the past
- **Return 422** Unprocessable Entity for validation errors
- **Return 400** Bad Request for malformed JSON

**Strong Answer Includes:**
- Sanitize inputs to prevent injection attacks
- Check user permissions (can only create tasks for yourself)
- Set default values (status = "pending")

---

### Question 4: Debugging Scenario - API Returns 500 Error

**Scenario:**
You deployed a new endpoint yesterday:
```
GET /api/users/{userId}/stats
```

Today, users report getting 500 errors intermittently. What do you check?

**Expected Answer:**
Candidate should outline a systematic debugging approach:

1. **Check logs**:
   - Error messages and stack traces
   - Look for patterns (specific users? times?)

2. **Reproduce locally**:
   - Try with different user IDs
   - Check if certain data causes errors

3. **Common causes**:
   - **Database issues**: Missing data, null values
   - **Type errors**: Expecting integer, got string
   - **Division by zero**: Calculating averages with zero tasks
   - **Timeout**: Query too slow
   - **External API**: Third-party service down

4. **Immediate fix**:
   - Add error handling
   - Return 503 if external dependency down
   - Add null checks

5. **Prevention**:
   - Add tests for edge cases
   - Better error handling
   - Input validation

**Follow-up:**
"The logs show: 'TypeError: unsupported operand type(s) for /: 'int' and 'NoneType''. What's the issue?"

**Expected Answer:**
- Trying to divide by None (null value)
- Probably calculating average: `total_points / task_count`
- User might have zero tasks, `task_count` is None or 0
- **Fix**: Check for None/0 before division
```python
if task_count and task_count > 0:
    average = total_points / task_count
else:
    average = 0
```

---

### Evaluation Criteria

**Pass (Hire):**
- ✅ Understands basic HTTP request/response
- ✅ Can design simple RESTful endpoints
- ✅ Knows basic status codes (200, 201, 404, 500)
- ✅ Understands GET vs POST
- ✅ Can think through debugging systematically
- ✅ Shows willingness to learn

**Strong Pass (Definitely Hire):**
- All of the above, plus:
- ✅ Mentions security concerns (authentication, authorization)
- ✅ Discusses validation and error handling
- ✅ Understands HTTP methods and when to use each
- ✅ Mentions testing and prevention
- ✅ Good communication skills

**Fail (Do Not Hire):**
- ❌ Can't explain basic HTTP
- ❌ Doesn't understand REST principles
- ❌ No systematic approach to debugging
- ❌ Can't design a simple endpoint
- ❌ Doesn't know common status codes

---

## Scenario 2: Full Stack Developer - REST API Design

### Role Description
**Position**: Full Stack Developer  
**Company**: E-commerce platform  
**Team Size**: 8-10 engineers  
**Tech Stack**: Node.js/Express, React, MongoDB, REST APIs  
**Experience Required**: 2-4 years

### Interview Format
- 60 minutes total
- 15 minutes: REST API principles
- 30 minutes: Design exercise
- 15 minutes: Security and performance

---

### Question 1: Design an API for a shopping cart

**Scenario:**
Design a RESTful API for a shopping cart system. Users should be able to:
- Add items to cart
- Remove items from cart
- Update quantity
- View cart
- Clear cart

**Expected Answer:**

**Endpoints:**
```
GET    /api/cart                    # View current user's cart
POST   /api/cart/items              # Add item to cart
PATCH  /api/cart/items/{itemId}     # Update quantity
DELETE /api/cart/items/{itemId}     # Remove item from cart
DELETE /api/cart                    # Clear entire cart
POST   /api/cart/checkout           # Proceed to checkout
```

**Data Models:**

Cart:
```json
{
  "userId": 123,
  "items": [
    {
      "id": "item-1",
      "productId": 456,
      "productName": "Laptop",
      "quantity": 1,
      "price": 999.99,
      "addedAt": "2024-01-15T10:30:00Z"
    }
  ],
  "totalItems": 1,
  "subtotal": 999.99,
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

Add Item Request:
```json
POST /api/cart/items

{
  "productId": 456,
  "quantity": 1
}

Response (201 Created):
{
  "id": "item-1",
  "productId": 456,
  "productName": "Laptop",
  "quantity": 1,
  "price": 999.99,
  "addedAt": "2024-01-15T10:30:00Z"
}
```

Update Quantity:
```json
PATCH /api/cart/items/item-1

{
  "quantity": 2
}

Response (200 OK):
{
  "id": "item-1",
  "quantity": 2,
  "price": 999.99
}
```

**Follow-up Question 1:**
"Should the cart be associated with a session or a user account?"

**Expected Answer:**
- **Session-based (guest cart)**:
  - Pros: No login required, faster checkout
  - Cons: Lost when cookies cleared, can't access from multiple devices
  - Implementation: Store cart ID in cookie/session
  
- **User-based (authenticated)**:
  - Pros: Persistent, multi-device, can save for later
  - Cons: Requires account, login friction
  - Implementation: Associate cart with userId

- **Hybrid approach** (best):
  - Guest cart stored in session
  - Merge with user cart on login
  - Persist after login

**Follow-up Question 2:**
"What happens if a product's price changes while it's in the cart?"

**Expected Answer:**
Options to consider:
1. **Lock price at add time** (store price in cart)
   - User sees same price until checkout
   - Clear communication: "Price may change at checkout"
   
2. **Always use current price**:
   - Recalculate on every view
   - Show price change notification
   
3. **Hybrid**:
   - Store original price
   - Show both old and new price if changed
   - Let user decide to proceed

Should also mention:
- Handle out-of-stock items
- Stock quantity validation at checkout
- Price verification before payment

**Follow-up Question 3:**
"How would you handle race conditions when multiple requests try to update the cart simultaneously?"

**Expected Answer:**
- **Optimistic locking**:
  - Include version number in cart
  - Update only if version matches
  - Return 409 Conflict if version mismatch
  
- **Database transactions**:
  - Atomic operations
  - Row-level locking
  
- **Last write wins**:
  - Simpler but can lose data
  - Acceptable for some use cases

Example with versioning:
```json
PATCH /api/cart/items/item-1

{
  "quantity": 2,
  "version": 5
}

If current version is 6:
Response (409 Conflict):
{
  "error": "Cart was modified. Please refresh and try again.",
  "currentVersion": 6
}
```

---

### Question 2: Authentication and Security

**Question:**
"How would you secure the shopping cart API?"

**Expected Answer:**

**1. Authentication:**
- **JWT tokens** for API authentication
- Short-lived access tokens (15 min)
- Refresh tokens for extending sessions
- Secure, HTTPOnly cookies for tokens

**2. Authorization:**
- Users can only access their own cart
- Verify userId in token matches cart owner
```javascript
if (cart.userId !== req.user.id) {
  return res.status(403).json({ error: 'Forbidden' });
}
```

**3. Input Validation:**
- Validate product IDs exist
- Quantity must be positive integer
- Quantity within limits (e.g., max 99 per item)
- Sanitize inputs to prevent injection

**4. Rate Limiting:**
- Prevent cart manipulation abuse
- E.g., 100 requests per minute per user
- Return 429 Too Many Requests

**5. HTTPS:**
- All API calls over HTTPS
- Encrypt data in transit

**6. CORS:**
- Whitelist allowed origins
- Don't use wildcard `*` in production

**7. Price Verification:**
- NEVER trust client for prices
- Always fetch current price from database
- Recalculate totals server-side

**Follow-up:**
"Why can't you trust prices from the client?"

**Expected Answer:**
- Client can be manipulated (browser DevTools)
- Attacker could change price to $0.01
- Always treat client input as untrusted
- Server is source of truth for prices
- Example attack:
```javascript
// Attacker modifies request:
{
  "productId": 456,
  "quantity": 1,
  "price": 0.01  // ❌ NEVER accept price from client
}
```

---

### Question 3: Performance and Caching

**Question:**
"Your shopping cart API is slow. How would you improve performance?"

**Expected Answer:**

**1. Database Optimization:**
- **Indexes**: On userId, productId
- **Denormalize**: Store product name/price in cart (avoid JOINs)
- **Connection pooling**: Reuse database connections

**2. Caching:**
- **Redis** for cart data (fast in-memory)
- Cache user's cart for 30 minutes
- Invalidate on updates
```javascript
// Pseudo-code
const cart = await redis.get(`cart:${userId}`);
if (cart) return JSON.parse(cart);

const cartFromDB = await db.getCart(userId);
await redis.setex(`cart:${userId}`, 1800, JSON.stringify(cartFromDB));
return cartFromDB;
```

**3. API Response Optimization:**
- **Pagination**: If cart has many items
- **Field filtering**: Return only needed fields
- **Compression**: Enable gzip

**4. Reduce Database Queries:**
- **Batch operations**: Update multiple items in one query
- **Eager loading**: Fetch product details with cart in single query
- Avoid N+1 queries

**5. Async Operations:**
- Update analytics asynchronously
- Send notifications via queue

**Follow-up:**
"When should you invalidate the cache?"

**Expected Answer:**
Invalidate cache when:
- User adds/removes/updates items
- Product price changes (if caching prices)
- Checkout completed (cart cleared)
- After timeout (TTL)

Cache invalidation strategies:
- **Write-through**: Update cache on every write
- **Write-behind**: Write to DB, invalidate cache
- **TTL**: Expire after time period

---

### Evaluation Criteria

**Pass (Hire):**
- ✅ Designs RESTful endpoints correctly
- ✅ Considers edge cases (price changes, stock)
- ✅ Understands authentication vs authorization
- ✅ Knows basic security practices
- ✅ Can identify performance bottlenecks
- ✅ Explains trade-offs in design decisions

**Strong Pass (Definitely Hire):**
- All of the above, plus:
- ✅ Discusses race conditions and solutions
- ✅ Detailed caching strategy
- ✅ Mentions specific security vulnerabilities
- ✅ Considers scalability
- ✅ Good system design thinking

**Fail (Do Not Hire):**
- ❌ Can't design basic CRUD endpoints
- ❌ Doesn't understand REST principles
- ❌ No awareness of security risks
- ❌ Trusts client-provided data (prices)
- ❌ No consideration for performance

---

## Scenario 3: Senior Backend Engineer - System Design

### Role Description
**Position**: Senior Backend Engineer  
**Company**: Social media platform (50M+ users)  
**Team Size**: 15-20 engineers across multiple teams  
**Tech Stack**: Microservices, Go/Python, PostgreSQL, Redis, Kafka  
**Experience Required**: 5+ years

### Interview Format
- 60 minutes total
- 10 minutes: Architecture discussion
- 35 minutes: System design exercise
- 15 minutes: Trade-offs and scaling

---

### Question 1: Design a URL Shortener (like bit.ly)

**Requirements:**
- Shorten long URLs to short codes (e.g., `short.ly/abc123`)
- Redirect short URLs to original URLs
- Track click analytics
- Handle 100M URLs, 10K requests/second
- 99.9% uptime

**Expected Answer:**

**1. API Design:**
```
POST   /api/v1/urls           # Create short URL
GET    /api/v1/urls/{code}    # Get URL details
GET    /{code}                # Redirect to original
DELETE /api/v1/urls/{code}    # Delete short URL
GET    /api/v1/urls/{code}/stats # Analytics
```

**2. Data Model:**
```javascript
URL {
  id: string (UUID)
  shortCode: string (indexed, unique)
  originalUrl: string
  userId: string
  createdAt: timestamp
  expiresAt: timestamp (optional)
  clicks: number
}

Click {
  id: string
  shortCode: string
  timestamp: timestamp
  ipAddress: string
  userAgent: string
  referrer: string
  country: string
}
```

**3. Short Code Generation:**

**Approach 1: Random String**
```python
import random, string

def generate_code(length=7):
    chars = string.ascii_letters + string.digits
    code = ''.join(random.choice(chars) for _ in range(length))
    # Check if exists in DB, regenerate if collision
    return code
```
- Pros: Simple, unpredictable
- Cons: Possible collisions, need to check DB

**Approach 2: Base62 Encoding**
```python
def encode_base62(num):
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if num == 0: return chars[0]
    result = ""
    while num:
        result = chars[num % 62] + result
        num //= 62
    return result

# Use auto-incrementing ID or distributed ID generator
short_code = encode_base62(database_id)
```
- Pros: Guaranteed unique, predictable length
- Cons: Sequential (can guess next URL), reveals count

**Approach 3: Hash + Truncate**
```python
import hashlib

def generate_code(url):
    hash_obj = hashlib.md5(url.encode())
    hash_hex = hash_obj.hexdigest()
    return hash_hex[:7]  # First 7 characters
```
- Pros: Same URL always gets same code (dedupe)
- Cons: Collisions possible with truncation

**Recommendation**: Use base62 with distributed ID generator (e.g., Snowflake, Twitter's solution)

**Follow-up Question 1:**
"How would you handle 10K requests/second for redirects?"

**Expected Answer:**

**1. Caching Strategy:**
- **Cache popular URLs** in Redis
- **TTL**: 1 hour
- **Cache hit ratio**: Aim for 80%+
- Reduces database load significantly

```python
def redirect(short_code):
    # 1. Check cache
    url = redis.get(f"url:{short_code}")
    if url:
        track_click_async(short_code)  # Don't block redirect
        return redirect(url)
    
    # 2. Query database
    url_obj = db.query("SELECT originalUrl FROM urls WHERE shortCode = ?", short_code)
    if not url_obj:
        return 404
    
    # 3. Cache for future
    redis.setex(f"url:{short_code}", 3600, url_obj.originalUrl)
    
    # 4. Track click asynchronously
    track_click_async(short_code)
    
    # 5. Redirect
    return redirect(url_obj.originalUrl)
```

**2. Database:**
- **Read replicas**: Distribute read load
- **Index** on shortCode (fast lookups)
- **Partitioning**: Shard by shortCode prefix

**3. CDN:**
- Cache redirects at edge locations
- Serve from nearest geographic location

**4. Async Analytics:**
- Don't update click count in sync path
- Push to message queue (Kafka/RabbitMQ)
- Process analytics in background workers

**Follow-up Question 2:**
"How do you ensure short codes are unique across multiple servers?"

**Expected Answer:**

**Problem**: Multiple servers generating codes simultaneously might create duplicates.

**Solutions:**

**1. Database Unique Constraint:**
- Add UNIQUE index on shortCode
- Handle duplicate key errors
- Retry with new code
- Simple but adds latency

**2. Distributed ID Generator:**
- **Twitter Snowflake**: 64-bit IDs
  - Timestamp (41 bits)
  - Machine ID (10 bits)
  - Sequence (12 bits)
- Guaranteed unique across cluster
- Convert to base62 for short code

**3. Pre-generated Pool:**
- Generate millions of codes offline
- Store in database
- Servers claim codes atomically
- Replenish pool when low

**4. Partitioning:**
- Assign each server a range/prefix
- Server 1: codes starting with 'a'
- Server 2: codes starting with 'b'
- Simpler but less flexible

**Recommendation**: Distributed ID generator (Snowflake-style) for scalability

**Follow-up Question 3:**
"How would you implement analytics without slowing down redirects?"

**Expected Answer:**

**1. Async Processing:**
```python
def track_click_async(short_code, request_data):
    # Don't wait for DB write
    message = {
        'shortCode': short_code,
        'timestamp': now(),
        'ipAddress': request_data.ip,
        'userAgent': request_data.user_agent,
        'referrer': request_data.referrer
    }
    kafka.produce('clicks-topic', message)
```

**2. Background Workers:**
- Consume from Kafka
- Batch insert to database (e.g., 1000 clicks at once)
- Update aggregate stats (clicks per day/hour)

**3. Time-series Database:**
- Use InfluxDB or TimescaleDB for analytics
- Optimized for time-based queries
- Better than relational DB for this use case

**4. Pre-aggregation:**
- Compute hourly/daily stats
- Store in summary tables
- API queries summary tables (fast)
- Don't query raw click events

**5. Sampling:**
- For very high traffic URLs, sample clicks
- Track 1 in 10 clicks
- Extrapolate for estimates
- Trade accuracy for performance

---

### Question 2: Scalability and Reliability

**Question:**
"Your URL shortener now has 1 billion URLs. How do you scale?"

**Expected Answer:**

**1. Database Sharding:**
- **Shard by shortCode hash**
- Distribute across multiple databases
- Each shard handles subset of URLs
```
shard_id = hash(short_code) % num_shards
database = shards[shard_id]
```

**2. Read/Write Separation:**
- **Write master**: Handle creates/deletes
- **Read replicas**: Handle redirects (most traffic)
- Async replication
- Eventual consistency acceptable for analytics

**3. Caching Layers:**
- **L1**: Application memory (LRU cache)
- **L2**: Redis cluster
- **L3**: CDN edge caches
- Multi-level reduces database hits

**4. Rate Limiting:**
- Prevent abuse (spam URL creation)
- Per-user limits: 100 URLs/hour
- Per-IP limits: 1000 redirects/minute
- Use token bucket algorithm

**5. Monitoring and Alerting:**
- Track latency (p50, p95, p99)
- Error rates
- Cache hit ratios
- Database connection pool saturation
- Alert on anomalies

**6. Auto-scaling:**
- Scale web servers based on traffic
- Kubernetes horizontal pod autoscaler
- Add database replicas during peak

**Follow-up:**
"What if a URL goes viral and gets 100K requests/second?"

**Expected Answer:**

**Hot Key Problem**:
- Single URL getting massive traffic
- Overwhelms even with caching

**Solutions:**
1. **Cache at multiple levels**:
   - CDN (CloudFlare, CloudFront)
   - Local cache on each server
   - Reduces backend load to near zero

2. **Static redirect page**:
   - Serve HTML with meta refresh
   - Completely static, cacheable
   - No backend hit needed

3. **Dedicated cache for hot URLs**:
   - Separate Redis instance
   - Higher resources
   - Monitor top URLs, cache aggressively

4. **Degraded analytics**:
   - Stop tracking every click
   - Sample heavily (1 in 1000)
   - Or pause analytics temporarily

---

### Evaluation Criteria

**Pass (Hire as Senior):**
- ✅ Designs scalable system architecture
- ✅ Considers multiple approaches and trade-offs
- ✅ Identifies bottlenecks proactively
- ✅ Understands caching strategies
- ✅ Discusses database scaling (sharding, replication)
- ✅ Considers edge cases and failure modes
- ✅ Mentions monitoring and observability

**Strong Pass (Definitely Hire / Tech Lead Level):**
- All of the above, plus:
- ✅ Calculates capacity requirements
- ✅ Discusses CAP theorem trade-offs
- ✅ Multi-region deployment strategy
- ✅ Detailed failure recovery plans
- ✅ Cost optimization considerations
- ✅ Excellent communication and diagrams

**Fail (Do Not Hire for Senior Role):**
- ❌ Doesn't scale beyond single server
- ❌ No caching strategy
- ❌ Doesn't consider high traffic scenarios
- ❌ No awareness of distributed systems challenges
- ❌ Can't articulate trade-offs
- ❌ Focuses only on happy path

---

## Scenario 4: DevOps Engineer - Network Troubleshooting

### Role Description
**Position**: DevOps/SRE Engineer  
**Company**: Cloud infrastructure provider  
**Team Size**: 6-8 SREs  
**Focus**: API infrastructure, monitoring, incident response  
**Experience Required**: 3-5 years

### Interview Format
- 60 minutes total
- 20 minutes: Networking fundamentals
- 25 minutes: Troubleshooting scenarios
- 15 minutes: Monitoring and alerting

---

### Question 1: API is returning 504 Gateway Timeout errors

**Scenario:**
Your API gateway is returning 504 Gateway Timeout errors to clients. Backend services appear healthy. How do you troubleshoot?

**Expected Answer:**

**Systematic Approach:**

**1. Gather Information:**
- When did it start?
- Is it affecting all requests or specific endpoints?
- What percentage of requests are failing?
- Any recent deployments?

**2. Check API Gateway:**
```bash
# Check gateway logs
kubectl logs -n api-gateway gateway-pod-xyz --tail=100

# Look for timeout settings
curl -v https://api.example.com/health
# Note: "Timeout" in error message

# Check gateway config
cat /etc/nginx/nginx.conf | grep timeout
proxy_read_timeout 30s;  # Maybe too short?
```

**3. Check Backend Services:**
```bash
# Check if backend is reachable
curl -v http://backend-service:8080/health

# Check response time
time curl http://backend-service:8080/api/slow-endpoint

# Check service status
kubectl get pods -n backend
kubectl describe pod backend-pod-123
```

**4. Check Network:**
```bash
# Test connectivity
ping backend-service.namespace.svc.cluster.local

# Trace route
traceroute backend-service

# Check DNS resolution
nslookup backend-service
dig backend-service.namespace.svc.cluster.local

# Check firewall rules
iptables -L -n
```

**5. Common Causes:**
- **Gateway timeout too short**: Backend needs 60s, gateway times out at 30s
- **Backend slow**: Database query taking too long
- **Network latency**: High latency between gateway and backend
- **Connection pool exhaustion**: All connections busy
- **DNS issues**: Slow DNS resolution

**6. Immediate Mitigation:**
```bash
# Increase gateway timeout temporarily
kubectl edit configmap gateway-config
# Set proxy_read_timeout to 60s
kubectl rollout restart deployment/api-gateway

# Scale up backend if overloaded
kubectl scale deployment backend --replicas=10
```

**Follow-up Question 1:**
"Logs show the backend is responding in 200ms, but clients see 30-second timeouts. What's happening?"

**Expected Answer:**

**Likely Issue**: Connection pool exhaustion or network saturation

**Investigation:**
```bash
# Check connection pool stats
curl http://gateway:9090/metrics | grep connection_pool
# active_connections: 1000
# max_connections: 1000  # ← FULL!

# Check network saturation
ifconfig eth0
# Look for errors, dropped packets

netstat -an | grep ESTABLISHED | wc -l
# Count of established connections

# Check gateway resource usage
top  # CPU at 100%?
free -m  # Out of memory?
```

**Solutions:**
- Increase connection pool size
- Add more gateway instances
- Implement connection keep-alive
- Check for connection leaks (not closing properly)

**Follow-up Question 2:**
"How would you prevent this from happening again?"

**Expected Answer:**

**1. Monitoring:**
- Track gateway timeout rates
- Alert on timeout > 1%
- Monitor backend response times (p50, p95, p99)
- Track connection pool utilization

**2. Load Testing:**
- Regular load tests to find limits
- Gradually increase timeout values based on p99 latency
- Test failure scenarios

**3. Circuit Breaker:**
- Implement circuit breaker pattern
- Fail fast instead of waiting for timeout
- Return 503 immediately when backend is down

**4. Auto-scaling:**
- Scale backend based on response time
- Scale gateway based on connection pool usage

**5. Timeouts Configuration:**
```yaml
# Gateway config
proxy_connect_timeout: 5s
proxy_send_timeout: 60s
proxy_read_timeout: 60s

# Backend config
request_timeout: 55s  # Less than gateway
database_query_timeout: 30s  # Less than request timeout
```

---

### Question 2: Intermittent 502 Bad Gateway Errors

**Scenario:**
Users report intermittent 502 Bad Gateway errors. Happens randomly, about 5% of requests. How do you debug?

**Expected Answer:**

**1. Reproduce the Issue:**
```bash
# Make many requests, look for pattern
for i in {1..100}; do
  curl -s -o /dev/null -w "%{http_code}\n" https://api.example.com/endpoint
done

# Check if specific pods failing
while true; do
  curl -H "Host: api.example.com" http://$POD_IP:8080/health
  sleep 1
done
```

**2. Check Load Balancer/Gateway:**
```bash
# Check upstream health checks
kubectl logs -n ingress nginx-ingress-controller | grep "upstream"
# Look for: "upstream timed out" or "no live upstreams"

# Check health check configuration
kubectl describe ingress api-ingress
# Annotations for health check path, interval, timeout
```

**3. Possible Causes:**

**a) Pod Restarts (Crash Loop):**
```bash
kubectl get pods -n backend
# Look for RESTARTS column > 0

kubectl logs backend-pod-xyz --previous
# Check logs from crashed container

kubectl describe pod backend-pod-xyz
# Look for OOMKilled, CrashLoopBackOff
```

**b) Aggressive Health Checks:**
```yaml
# Health check failing pods prematurely
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 10  # Too short?
  periodSeconds: 5
  timeoutSeconds: 1  # Too aggressive?
  failureThreshold: 3
```

**c) Zero-Downtime Deployment Issues:**
- New pods starting before ready
- Old pods terminating too quickly
- No preStop hook for graceful shutdown

**d) Resource Limits:**
```bash
kubectl top pods -n backend
# Check CPU/Memory usage near limits
```

**4. Solutions:**

**Graceful Shutdown:**
```yaml
lifecycle:
  preStop:
    exec:
      command: ["/bin/sh", "-c", "sleep 10"]
# Give load balancer time to remove pod from pool
```

**Adjust Health Checks:**
```yaml
livenessProbe:
  initialDelaySeconds: 30  # Wait for app to start
  timeoutSeconds: 3
  failureThreshold: 5  # More lenient

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  periodSeconds: 5
  successThreshold: 1
  failureThreshold: 2
```

**Circuit Breaker:**
- Don't send traffic to failing pods
- Remove from load balancer faster

---

### Question 3: High API Latency During Peak Hours

**Scenario:**
API response time goes from 100ms to 5 seconds during peak hours (6-8 PM). How do you investigate and fix?

**Expected Answer:**

**1. Identify Bottleneck:**

**Check Metrics:**
```bash
# Application metrics
curl http://backend:9090/metrics | grep http_request_duration
# Breakdown by endpoint

# Database metrics
show processlist;  # MySQL
# Look for slow queries

# Check slow query log
tail -f /var/log/mysql/slow-query.log
```

**2. Common Bottlenecks:**

**a) Database:**
```sql
-- Slow queries
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
-- Missing index!

-- Create index
CREATE INDEX idx_users_email ON users(email);

-- Connection pool exhausted
SHOW STATUS LIKE 'Threads_connected';
-- At max_connections limit
```

**b) N+1 Query Problem:**
```python
# BAD: Fetching users and their posts
users = User.query.all()  # 1 query
for user in users:
    posts = user.posts  # N queries!

# GOOD: Eager loading
users = User.query.options(joinedload(User.posts)).all()  # 1 query
```

**c) No Caching:**
```python
# Add caching for expensive operations
@cache.memoize(timeout=300)
def get_user_stats(user_id):
    # Expensive aggregation query
    return db.query(...)
```

**d) Synchronous External API Calls:**
```python
# BAD: Synchronous
result = requests.get('https://slow-api.com/data')

# GOOD: Async or background job
result = await async_http_client.get('https://slow-api.com/data')
# Or use Celery for background processing
```

**3. Solutions:**

**Scale Horizontally:**
```bash
# Add more application servers
kubectl scale deployment backend --replicas=10

# Add database read replicas
# Route read queries to replicas
```

**Connection Pooling:**
```python
# Configure database connection pool
SQLALCHEMY_POOL_SIZE = 20
SQLALCHEMY_MAX_OVERFLOW = 10
SQLALCHEMY_POOL_TIMEOUT = 30
```

**Rate Limiting:**
```python
# Limit expensive endpoints
@app.route('/api/expensive')
@limiter.limit("10 per minute")
def expensive_endpoint():
    ...
```

**Async Processing:**
```python
# For slow operations
@app.route('/api/report')
def generate_report():
    job = queue.enqueue(generate_report_task, user_id)
    return {
        'jobId': job.id,
        'status': 'processing',
        'statusUrl': f'/api/jobs/{job.id}'
    }, 202
```

---

### Evaluation Criteria

**Pass (Hire):**
- ✅ Systematic troubleshooting approach
- ✅ Knows relevant tools (curl, kubectl, logs)
- ✅ Understands network layers
- ✅ Can identify common issues (timeouts, health checks)
- ✅ Proposes monitoring and prevention
- ✅ Good communication of technical details

**Strong Pass (Definitely Hire):**
- All of the above, plus:
- ✅ Deep knowledge of Kubernetes/cloud networking
- ✅ Experience with specific tools (Prometheus, Grafana)
- ✅ Discusses trade-offs in solutions
- ✅ Proactive about prevention
- ✅ Shows incident response best practices

**Fail (Do Not Hire):**
- ❌ No systematic approach (random guessing)
- ❌ Unfamiliar with basic networking concepts
- ❌ Can't use common debugging tools
- ❌ Doesn't consider monitoring
- ❌ Jumps to solutions without investigation

---

## Scenario 5: API Platform Engineer - Security & Scale

### Role Description
**Position**: API Platform Engineer  
**Company**: Fintech company (payments API)  
**Team Size**: 12-15 engineers  
**Focus**: Public API platform, security, compliance, scale  
**Experience Required**: 5-7 years

### Interview Format
- 60 minutes total
- 15 minutes: Security fundamentals
- 30 minutes: Design secure, scalable API platform
- 15 minutes: Compliance and incident response

---

### Question 1: Design a secure API authentication system

**Scenario:**
Design an authentication system for a public payments API that will be used by thousands of third-party developers.

**Expected Answer:**

**1. Authentication Method: OAuth 2.0 + API Keys**

**For server-to-server (most payment APIs):**
```
Client Credentials Flow:

1. Developer creates app in portal
2. Gets client_id and client_secret
3. Exchanges for access token:

POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id=abc123
&client_secret=secret456
&scope=payments:read payments:write

Response:
{
  "access_token": "eyJhbGc...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "payments:read payments:write"
}

4. Use token in API requests:
GET /api/v1/payments
Authorization: Bearer eyJhbGc...
```

**2. Security Requirements:**

**a) Token Properties:**
- **Short-lived**: 1 hour expiration
- **JWT format**: Self-contained, verifiable
- **Scope-based**: Limited permissions
- **Signed**: HS256 or RS256

**b) Secrets Management:**
- **Never store plain text**: Hash client secrets (bcrypt)
- **Rotate regularly**: Support multiple active secrets
- **Secure generation**: Cryptographically random
- **Transmission**: Only over HTTPS

**c) Rate Limiting:**
```yaml
# Per client limits
rate_limits:
  default:
    requests_per_minute: 100
    requests_per_hour: 5000
  
  premium_tier:
    requests_per_minute: 1000
    requests_per_hour: 50000
```

**d) IP Whitelisting:**
- Allow clients to whitelist IP addresses
- Additional layer of security
- Reject requests from non-whitelisted IPs

**3. Additional Security Measures:**

**Request Signing:**
```python
# Client signs request with secret
import hmac, hashlib

timestamp = str(int(time.time()))
signature_string = f"{method}\n{path}\n{timestamp}\n{body}"
signature = hmac.new(
    client_secret.encode(),
    signature_string.encode(),
    hashlib.sha256
).hexdigest()

# Headers
X-Timestamp: 1640000000
X-Signature: abc123...

# Server validates:
# 1. Timestamp within 5 minutes
# 2. Signature matches
# 3. Request hasn't been replayed (nonce/timestamp tracking)
```

**Webhook Verification:**
```python
# When sending webhooks to client, sign payload
def sign_webhook(payload, secret):
    signature = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature

# Client verifies signature to ensure from legitimate source
```

**Follow-up Question 1:**
"How do you handle compromised API keys?"

**Expected Answer:**

**1. Detection:**
- Monitor for unusual patterns:
  - Requests from unexpected IPs
  - Spike in traffic
  - Access to unusual resources
  - Failed authentication attempts
  
**2. Immediate Response:**
```python
# Revoke compromised key
def revoke_api_key(key_id):
    db.update(api_keys).where(id=key_id).set(status='revoked')
    cache.delete(f"key:{key_id}")  # Invalidate cache
    audit_log.write({
        'action': 'key_revoked',
        'key_id': key_id,
        'reason': 'compromised',
        'timestamp': now()
    })
```

**3. Client Notification:**
- Email developer immediately
- Show alert in developer portal
- Provide steps to rotate keys

**4. Rotation Process:**
- Generate new key
- Grace period: Both keys valid for 24-48 hours
- Client updates production with new key
- Old key expires automatically

**5. Prevention:**
- Educate developers: Never commit keys to Git
- Provide key scanning tools
- Regularly audit key usage
- Require key rotation every 90 days

**Follow-up Question 2:**
"How do you ensure PCI DSS compliance for payment card data?"

**Expected Answer:**

**Critical Principles:**

**1. Never Store Sensitive Card Data:**
```python
# BAD - Never do this!
{
  "card_number": "4242424242424242",
  "cvv": "123",
  "expiry": "12/25"
}

# GOOD - Use tokenization
{
  "card_token": "tok_abc123xyz",  # One-time use token
  "last4": "4242",
  "brand": "visa"
}
```

**2. Tokenization Flow:**
```
Client-Side:
1. Collect card details in form
2. Send directly to payment processor (Stripe, Braintree)
3. Receive token
4. Send token to your API

Your API:
1. Receives token only (never raw card data)
2. Uses token to charge via payment processor
3. Stores token reference if needed
```

**3. Network Segmentation:**
- API servers never handle raw card data
- If must handle, use dedicated PCI-compliant environment
- Firewall rules isolate sensitive systems

**4. Encryption:**
- **TLS 1.2+** for all data in transit
- **AES-256** for data at rest (if storing tokens)
- **Field-level encryption** for sensitive fields

**5. Audit Logging:**
```python
# Log all access to payment data
audit_log = {
    'timestamp': '2024-01-15T10:30:00Z',
    'action': 'payment_created',
    'actor': 'api_client_abc123',
    'resource': 'payment_xyz789',
    'ip_address': '192.168.1.1',
    'result': 'success'
}
```

**6. Access Control:**
- Least privilege principle
- MFA for admin access
- Regular access reviews
- Separate production/development environments

---

### Question 2: Design for 10,000 requests/second with 99.99% uptime

**Expected Answer:**

**Architecture:**

```
┌─────────────┐
│   Clients   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│     CDN     │  CloudFlare/CloudFront
│  (DDoS      │  - DDoS protection
│   Protection│  - Rate limiting
│   & Caching)│  - SSL termination
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ API Gateway │  Multiple availability zones
│   (Load     │  - Authentication
│   Balancer) │  - Rate limiting
│             │  - Request routing
└──────┬──────┘
       │
       ├───────┬───────┬───────┐
       ▼       ▼       ▼       ▼
    ┌───┐   ┌───┐   ┌───┐   ┌───┐
    │API│   │API│   │API│   │API│  Auto-scaling (10-100 instances)
    │   │   │   │   │   │   │   │  - Stateless
    └─┬─┘   └─┬─┘   └─┬─┘   └─┬─┘  - Containerized (Kubernetes)
      │       │       │       │
      └───────┴───────┴───────┘
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
    ┌──────┐  ┌──────┐  ┌──────┐
    │Redis │  │ DB   │  │Queue │
    │Cluster  │Master│  │Kafka │
    └──────┘  └──┬───┘  └──────┘
                 │
           ┌─────┴─────┐
           ▼           ▼
       ┌──────┐    ┌──────┐
       │Read  │    │Read  │
       │Replica    │Replica
       └──────┘    └──────┘
```

**1. High Availability:**

**Multi-Region Deployment:**
- **Active-Active**: Both regions serve traffic
- **Geographic load balancing**: Route to nearest region
- **Automatic failover**: If one region down, route to other

**Database:**
```yaml
# Master-replica setup
master:
  region: us-east-1
  replicas:
    - us-east-1b
    - us-east-1c
  
slave_master:  # For other region
  region: eu-west-1
  replicas:
    - eu-west-1a
    - eu-west-1b

# Async replication between regions
```

**2. Performance:**

**Caching Strategy:**
```python
# Multi-level caching

# L1: In-memory (application)
from functools import lru_cache
@lru_cache(maxsize=1000)
def get_merchant(merchant_id):
    return db.query(...)

# L2: Redis (distributed)
def get_payment(payment_id):
    cached = redis.get(f"payment:{payment_id}")
    if cached:
        return json.loads(cached)
    
    payment = db.query(...)
    redis.setex(f"payment:{payment_id}", 300, json.dumps(payment))
    return payment

# L3: CDN (for public endpoints)
# Cache-Control: public, max-age=60
```

**Database Optimization:**
```sql
-- Indexing
CREATE INDEX idx_payments_merchant ON payments(merchant_id, created_at);
CREATE INDEX idx_payments_status ON payments(status);

-- Partitioning (by date)
CREATE TABLE payments_2024_01 PARTITION OF payments
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Read/write splitting
# Writes go to master
# Reads go to replicas (distributed)
```

**3. Scalability:**

**Auto-scaling:**
```yaml
# Kubernetes HPA (Horizontal Pod Autoscaler)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-scaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 10
  maxReplicas: 100
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
```

**4. Reliability (99.99% = 52 min downtime/year):**

**Circuit Breaker:**
```python
from pybreaker import CircuitBreaker

db_breaker = CircuitBreaker(
    fail_max=5,
    timeout_duration=60
)

@db_breaker
def query_database():
    return db.execute(query)

# If 5 failures, circuit opens
# Return fallback response instead of hammering DB
```

**Health Checks:**
```python
@app.route('/health')
def health():
    checks = {
        'database': check_db(),
        'redis': check_redis(),
        'queue': check_kafka()
    }
    
    if all(checks.values()):
        return {'status': 'healthy'}, 200
    else:
        return {'status': 'degraded', 'checks': checks}, 503
```

**Graceful Degradation:**
```python
# If payment processor down, queue for later
try:
    result = payment_processor.charge(token, amount)
except PaymentProcessorError:
    queue.enqueue('process_payment', token, amount)
    return {
        'status': 'pending',
        'message': 'Payment queued for processing'
    }, 202
```

**5. Monitoring:**

```yaml
# Metrics to track
- request_rate
- error_rate
- latency (p50, p95, p99)
- availability
- cache_hit_ratio
- database_connection_pool_usage
- queue_depth

# Alerts
- error_rate > 1% for 5 minutes
- latency p99 > 1000ms for 5 minutes
- availability < 99.9% for 1 minute
- queue_depth > 10000
```

---

### Question 3: Incident Response - Data Breach

**Scenario:**
Your security team detects that API keys for 100 merchants were leaked on GitHub. What do you do?

**Expected Answer:**

**Immediate Actions (First 15 minutes):**

**1. Assess Scope:**
```bash
# Identify affected API keys
grep -r "pk_live_" leaked_repo/

# Get list of compromised key IDs
compromised_keys = [
    'key_abc123',
    'key_def456',
    # ...
]
```

**2. Revoke Keys:**
```python
# Immediately revoke all compromised keys
for key_id in compromised_keys:
    db.update(api_keys).where(id=key_id).set(
        status='revoked',
        revoked_at=now(),
        revoke_reason='security_incident_2024_01_15'
    )
    
    # Invalidate all caches
    cache.delete(f"key:{key_id}")
    
    # Block any in-flight requests
    firewall.block_key(key_id)
```

**3. Audit Recent Activity:**
```sql
-- Check for suspicious activity in last 24 hours
SELECT 
    request_id,
    api_key_id,
    endpoint,
    ip_address,
    timestamp,
    response_code
FROM api_logs
WHERE 
    api_key_id IN (compromised_keys)
    AND timestamp > NOW() - INTERVAL '24 hours'
ORDER BY timestamp DESC;

-- Look for:
-- - Unusual endpoints accessed
-- - High volume of requests
-- - Requests from unexpected IPs
-- - Sensitive data accessed (customer data, payments)
```

**Short-term Actions (1-4 hours):**

**4. Notify Affected Merchants:**
```python
# Email template
email = {
    'subject': 'URGENT: API Key Security Incident',
    'body': '''
        We detected that your API key was exposed in a public repository.
        
        We have immediately revoked the compromised key for your protection.
        
        Please:
        1. Generate a new API key in your dashboard
        2. Update your production systems with the new key
        3. Review your recent transaction history for any unauthorized activity
        4. Contact support if you see suspicious activity
        
        We apologize for the inconvenience.
        '''
}

for merchant in affected_merchants:
    send_email(merchant.email, email)
    
    # Also show banner in dashboard
    dashboard.show_alert(merchant.id, 'key_revoked')
```

**5. Forensics:**
- When was repo first made public?
- Who had access to the leaked keys?
- Were keys used after leak?
- Was data exfiltrated?

**6. Generate Replacement Keys:**
```python
# Automatically generate new keys
for merchant in affected_merchants:
    new_key = generate_api_key()
    db.insert(api_keys).values(
        merchant_id=merchant.id,
        key=hash(new_key),
        status='active',
        created_at=now()
    )
    
    # Send new key via secure channel
    send_secure_email(merchant.email, new_key)
```

**Long-term Actions (1-7 days):**

**7. Post-Incident Review:**
- Timeline of events
- Root cause analysis
- What went wrong?
- What went right?
- Lessons learned

**8. Improvements:**

**a) Prevention:**
```python
# Implement key format that's easily detectable
# Old: sk_live_abc123
# New: sk_live_prod_1234567890abcdef_ghij

# Easier to scan GitHub for leaks
github_scanner.add_pattern(r'sk_live_prod_[a-z0-9]{16}_[a-z0-9]{4}')
```

**b) Detection:**
- Monitor GitHub, Pastebin for leaked keys
- Automated scanning service
- Alert within minutes of detection

**c) Rotation Policy:**
- Mandatory key rotation every 90 days
- Show age of keys in dashboard
- Email reminders

**d) Developer Education:**
- Documentation on secret management
- Never commit keys to Git
- Use environment variables
- Tools: git-secrets, truffleHog

**e) Incident Response Playbook:**
```markdown
# API Key Leak Response Playbook

1. Revoke compromised keys (< 5 min)
2. Audit logs for suspicious activity (< 15 min)
3. Notify affected merchants (< 1 hour)
4. Generate replacement keys (< 2 hours)
5. Forensic analysis (< 24 hours)
6. Post-incident review (< 7 days)
7. Implement preventions (< 30 days)
```

**9. Compliance Requirements:**
- Document incident for auditors
- Report to relevant authorities if customer data accessed
- Update security policies
- Board/executive notification

---

### Evaluation Criteria

**Pass (Hire):**
- ✅ Understands OAuth 2.0 and API authentication
- ✅ Security-first mindset
- ✅ Can design for scale (caching, load balancing)
- ✅ Knows compliance basics (PCI DSS)
- ✅ Systematic incident response approach
- ✅ Considers monitoring and observability

**Strong Pass (Definitely Hire):**
- All of the above, plus:
- ✅ Deep security knowledge (request signing, zero-trust)
- ✅ Multi-region, high-availability architecture
- ✅ Detailed incident response with timeline
- ✅ Proactive about prevention
- ✅ Understands business impact of decisions
- ✅ Excellent risk assessment

**Fail (Do Not Hire):**
- ❌ Weak security fundamentals
- ❌ No consideration for compliance
- ❌ Can't scale beyond single server
- ❌ No incident response experience
- ❌ Doesn't prioritize security over convenience
- ❌ No awareness of industry standards

---

## General Interview Tips

### For Candidates:

**1. Clarify Requirements:**
- Ask questions before diving in
- Understand scope and constraints
- Clarify ambiguous terms

**2. Think Out Loud:**
- Explain your reasoning
- Discuss trade-offs
- Show your thought process

**3. Start Simple:**
- Basic solution first
- Then optimize and scale
- Don't over-engineer initially

**4. Consider Edge Cases:**
- What if traffic spikes?
- What if database is down?
- What if input is malicious?

**5. Discuss Trade-offs:**
- "We could do X which is simpler, or Y which scales better"
- Show you understand pros/cons
- No single "right" answer

**6. Be Honest:**
- If you don't know, say so
- "I haven't worked with that, but I would approach it by..."
- Show willingness to learn

### For Interviewers:

**1. Set Candidate at Ease:**
- Explain format upfront
- Encourage questions
- It's a conversation, not interrogation

**2. Listen for Depth:**
- Can they explain *why*, not just *what*?
- Do they understand trade-offs?
- Can they adapt to new requirements?

**3. Give Hints if Stuck:**
- "What if we had 1000x more traffic?"
- "How would caching help here?"
- You want to see their best work

**4. Focus on Process:**
- How they think, not just final answer
- Communication skills matter
- Can they learn and adapt?

**5. Be Fair:**
- Compare to job requirements
- Not "would I want to work with them" but "can they do the job"
- Account for nervousness

---

## Summary

These mock interview scenarios cover:
- ✅ Junior to senior level positions
- ✅ Backend, full stack, DevOps, and platform roles
- ✅ Fundamental concepts to advanced system design
- ✅ Security, scalability, and reliability
- ✅ Practical troubleshooting and debugging
- ✅ Real-world incident response

**Key Takeaways:**
1. **Fundamentals matter**: TCP/IP, HTTP, REST
2. **Security is critical**: Never an afterthought
3. **Think systematically**: Debug methodically
4. **Scale early**: Design for growth from day one
5. **Communicate clearly**: Explain your reasoning
6. **Learn continuously**: Technology evolves rapidly

Good luck with your networking interviews! 🚀
