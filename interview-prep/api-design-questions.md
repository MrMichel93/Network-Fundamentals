# API Design Interview Questions

A comprehensive collection of API design interview questions with answer frameworks.

## Table of Contents
1. [REST API Fundamentals](#rest-api-fundamentals)
2. [API Design Principles](#api-design-principles)
3. [HTTP Methods & Status Codes](#http-methods--status-codes)
4. [API Versioning](#api-versioning)
5. [Authentication & Authorization](#authentication--authorization)
6. [Error Handling](#error-handling)
7. [Performance & Scalability](#performance--scalability)
8. [Security](#security)
9. [Documentation & Best Practices](#documentation--best-practices)
10. [Practical Design Scenarios](#practical-design-scenarios)

---

## REST API Fundamentals

### 1. What is REST and what are its core principles?
**Answer Framework:**
- **RE**presentational **S**tate **T**ransfer
- Architectural style, not a protocol
- Core principles:
  - **Stateless**: Each request contains all needed information
  - **Client-Server**: Separation of concerns
  - **Cacheable**: Responses must define themselves as cacheable or not
  - **Uniform Interface**: Consistent way to interact with resources
  - **Layered System**: Client can't tell if connected directly to end server
  - **Code on Demand** (optional): Server can extend client functionality

### 2. What makes an API RESTful vs just REST-like?
**Answer Framework:**
- **Truly RESTful**: Follows all REST constraints, including HATEOAS
- **REST-like/RESTish**: Uses HTTP methods and resources but doesn't implement HATEOAS
- Most "REST APIs" are actually REST-like
- HATEOAS example:
```json
{
  "id": 123,
  "name": "Product",
  "links": {
    "self": "/api/products/123",
    "update": "/api/products/123",
    "delete": "/api/products/123",
    "category": "/api/categories/5"
  }
}
```

### 3. What is the difference between a resource and a representation?
**Answer Framework:**
- **Resource**: The conceptual entity (e.g., a user, product)
- **Representation**: How that resource is formatted (JSON, XML, HTML)
- Same resource can have multiple representations
- Client specifies desired representation via `Accept` header
- Server specifies actual representation via `Content-Type` header

### 4. How do you design resource URIs?
**Answer Framework:**
- Use **nouns**, not verbs: `/users` not `/getUsers`
- Use **plural** names for collections: `/products`
- Use **hierarchical** structure for relationships: `/users/123/orders`
- Use **hyphens** for multi-word resources: `/product-categories`
- Keep URIs **lowercase**
- Don't expose implementation details: Avoid `.php`, `.py` extensions
- Examples:
  - Good: `GET /api/v1/users/123/orders`
  - Bad: `GET /api/v1/getUserOrders?userId=123`

### 5. When should you use sub-resources vs query parameters?
**Answer Framework:**
- **Sub-resources**: When accessing a resource that belongs to another
  - `/users/123/orders` - orders belonging to user 123
  - `/posts/456/comments` - comments on post 456
- **Query parameters**: For filtering, sorting, pagination
  - `/products?category=electronics&sort=price&page=2`
  - `/users?role=admin&status=active`
- **Rule of thumb**: If it's a relationship, use sub-resource; if it's filtering/options, use query params

---

## API Design Principles

### 6. What is the principle of least surprise in API design?
**Answer Framework:**
- APIs should behave as developers expect
- Follow conventions and standards
- Examples:
  - `DELETE` should be idempotent
  - `POST` to `/users` should create a user
  - Return `201 Created` with `Location` header after creation
  - Use standard HTTP status codes appropriately

### 7. How do you design for extensibility without breaking existing clients?
**Answer Framework:**
- **Additive changes only**: Add new fields, don't remove old ones
- **Optional fields**: Make new fields optional with sensible defaults
- **Versioning**: Use API versioning for breaking changes
- **Deprecation strategy**: 
  - Mark fields as deprecated in docs
  - Give clients time to migrate (e.g., 6-12 months)
  - Use `Deprecation` and `Sunset` headers
- **Backward compatibility**: New features shouldn't break old behavior

### 8. What is API composition and when should you use it?
**Answer Framework:**
- Combining multiple API calls into a single request/response
- **When to use**:
  - Reduce network round trips
  - Improve mobile/low-bandwidth performance
  - Simplify client code
- **Patterns**:
  - Query parameters: `?include=author,comments`
  - GraphQL-style field selection
  - Batch endpoints: `POST /batch`
- **Trade-offs**: More complex server logic, potential over-fetching

### 9. Should you paginate all collection endpoints?
**Answer Framework:**
- **Yes**, always paginate collections
- Prevents performance issues with large datasets
- **Common strategies**:
  - Offset-based: `?limit=20&offset=40`
  - Page-based: `?page=3&size=20`
  - Cursor-based: `?cursor=abc123&limit=20` (better for real-time data)
- Include metadata in response:
```json
{
  "data": [...],
  "pagination": {
    "total": 1000,
    "page": 3,
    "perPage": 20,
    "totalPages": 50
  }
}
```

### 10. How do you handle partial updates?
**Answer Framework:**
- Use `PATCH` method, not `PUT`
- `PUT` replaces entire resource (requires all fields)
- `PATCH` updates only specified fields
- **Example**:
```http
PATCH /api/users/123
Content-Type: application/json

{
  "email": "newemail@example.com"
}
```
- Consider JSON Patch (RFC 6902) for complex updates:
```json
[
  { "op": "replace", "path": "/email", "value": "new@example.com" },
  { "op": "add", "path": "/tags/-", "value": "premium" }
]
```

---

## HTTP Methods & Status Codes

### 11. Explain idempotency and which HTTP methods are idempotent.
**Answer Framework:**
- **Idempotent**: Multiple identical requests have same effect as single request
- **Idempotent methods**: `GET`, `PUT`, `DELETE`, `HEAD`, `OPTIONS`
- **Not idempotent**: `POST`, `PATCH`
- **Example**: 
  - `DELETE /users/123` - deleting twice has same result as once
  - `POST /users` - creating twice makes two users

### 12. When should you use PUT vs POST vs PATCH?
**Answer Framework:**
- **POST**: Create new resource (non-idempotent)
  - `POST /users` - creates new user
  - Server generates ID
  - Returns `201 Created` with `Location` header
- **PUT**: Replace entire resource (idempotent)
  - `PUT /users/123` - replaces user 123 completely
  - Client provides all fields
  - Can be used to create if client controls ID
- **PATCH**: Partial update (not guaranteed idempotent)
  - `PATCH /users/123` - updates specific fields
  - Only sends changed fields

### 13. What HTTP status code should you return for each scenario?
**Answer Framework:**

**Success (2xx):**
- `200 OK`: Successful GET, PUT, PATCH, DELETE
- `201 Created`: Successful POST (include `Location` header)
- `202 Accepted`: Request accepted but processing not complete
- `204 No Content`: Successful but no response body (often for DELETE)

**Client Errors (4xx):**
- `400 Bad Request`: Invalid syntax, validation errors
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Authenticated but not authorized
- `404 Not Found`: Resource doesn't exist
- `409 Conflict`: Request conflicts with current state (e.g., duplicate email)
- `422 Unprocessable Entity`: Validation errors (better than 400)
- `429 Too Many Requests`: Rate limit exceeded

**Server Errors (5xx):**
- `500 Internal Server Error`: Generic server error
- `502 Bad Gateway`: Invalid response from upstream server
- `503 Service Unavailable`: Temporary overload or maintenance
- `504 Gateway Timeout`: Upstream server timeout

### 14. Should you use 404 or 403 when a resource exists but user lacks access?
**Answer Framework:**
- **Depends on security requirements**
- `403 Forbidden`: More accurate, but reveals resource exists
- `404 Not Found`: More secure, doesn't leak information
- **Best practice**: Use 404 to prevent information disclosure
- **Exception**: If resource visibility is not sensitive, use 403
- Document your choice for consistency

### 15. What's the difference between 401 and 403?
**Answer Framework:**
- **401 Unauthorized**: Authentication required or failed
  - User not logged in
  - Invalid credentials
  - Include `WWW-Authenticate` header
  - Client should retry with valid credentials
- **403 Forbidden**: Authenticated but not authorized
  - User logged in but lacks permission
  - Should NOT retry with same credentials
  - Example: Regular user trying to access admin endpoint

---

## API Versioning

### 16. What are the different API versioning strategies?
**Answer Framework:**

**1. URI Versioning** (most common):
- `https://api.example.com/v1/users`
- Pros: Clear, easy to test different versions
- Cons: Breaks REST principle of resources having single URI

**2. Header Versioning**:
- `Accept: application/vnd.example.v1+json`
- Pros: Clean URIs, follows REST principles
- Cons: Less visible, harder to test

**3. Query Parameter**:
- `https://api.example.com/users?version=1`
- Pros: Flexible, easy to default
- Cons: Can be ignored by clients

**4. Content Negotiation**:
- `Accept: application/json; version=1`
- Pros: RESTful, flexible
- Cons: Complex to implement

**Recommendation**: URI versioning for simplicity and clarity

### 17. When should you create a new API version?
**Answer Framework:**
- **Breaking changes only**:
  - Removing endpoints or fields
  - Changing response structure
  - Changing authentication method
  - Renaming fields
- **Don't version for**:
  - Adding new optional fields
  - Adding new endpoints
  - Bug fixes
  - Performance improvements
- **Strategy**: Maintain 2-3 versions maximum, deprecate old ones

### 18. How do you deprecate an API version?
**Answer Framework:**
1. **Announce early**: 6-12 months notice
2. **Use headers**: 
   - `Deprecation: true`
   - `Sunset: Sat, 31 Dec 2024 23:59:59 GMT`
3. **Update documentation**: Mark as deprecated
4. **Monitor usage**: Track which clients still use old version
5. **Provide migration guide**: Clear upgrade path
6. **Grace period**: Support old version during transition
7. **Communicate**: Email notifications to API consumers
8. **Finally sunset**: Remove old version on announced date

---

## Authentication & Authorization

### 19. What's the difference between authentication and authorization?
**Answer Framework:**
- **Authentication**: "Who are you?"
  - Verifying identity
  - Login with username/password
  - API key verification
  - JWT token validation
- **Authorization**: "What can you do?"
  - Verifying permissions
  - Role-based access control (RBAC)
  - Resource ownership checks
  - Scope-based permissions
- **Example**: User authenticates with password, then authorized to view their own orders but not others'

### 20. What are the common API authentication methods?
**Answer Framework:**

**1. API Keys**:
- Simple, good for server-to-server
- Include in header: `X-API-Key: abc123`
- Cons: No expiration, hard to rotate

**2. Bearer Tokens (JWT)**:
- Stateless, self-contained
- `Authorization: Bearer eyJhbGc...`
- Include expiration, can't revoke easily

**3. OAuth 2.0**:
- Industry standard for delegated access
- Supports multiple flows (Authorization Code, Client Credentials, etc.)
- Separates authentication server from resource server

**4. Basic Auth**:
- Simple but requires HTTPS
- `Authorization: Basic base64(username:password)`
- Suitable for simple use cases, internal APIs

**5. mTLS (Mutual TLS)**:
- Certificate-based, very secure
- Both client and server verify each other
- Good for service-to-service communication

### 21. How do you implement rate limiting?
**Answer Framework:**
- **Why**: Prevent abuse, ensure fair usage, protect infrastructure
- **Strategies**:
  - **Fixed window**: 100 requests per hour (resets at hour boundary)
  - **Sliding window**: Rolling 60-minute window
  - **Token bucket**: More flexible, allows bursts
- **Headers to include**:
  - `X-RateLimit-Limit: 100`
  - `X-RateLimit-Remaining: 87`
  - `X-RateLimit-Reset: 1640000000`
- **Return 429** when exceeded with `Retry-After` header
- **Consider**: Different limits per endpoint, user tier

### 22. Should you use sessions or tokens for a REST API?
**Answer Framework:**
- **Tokens (JWT) preferred** for REST APIs
- **Why**:
  - Stateless (scales better)
  - Works across domains
  - No server-side storage needed
  - Mobile-friendly
- **Sessions** better for:
  - Traditional web apps
  - When you need to revoke immediately
  - When payload size matters (JWTs get large)
- **Hybrid approach**: Use refresh tokens (stored server-side) with short-lived access tokens

---

## Error Handling

### 23. How should you structure error responses?
**Answer Framework:**
- **Consistent format** across all endpoints
- **Include**:
  - HTTP status code
  - Error code (for programmatic handling)
  - Human-readable message
  - Optional: Field-specific errors, debugging info (non-production)
  
**Example**:
```json
{
  "error": {
    "status": 422,
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      },
      {
        "field": "age",
        "message": "Must be at least 18"
      }
    ],
    "timestamp": "2024-01-15T10:30:00Z",
    "path": "/api/users"
  }
}
```

### 24. Should you expose stack traces in error responses?
**Answer Framework:**
- **Never in production**
- Reveals implementation details
- Security risk (paths, libraries, versions)
- **In development**: Okay for debugging
- **Instead**: 
  - Use error tracking service (Sentry, Rollbar)
  - Return correlation ID to client
  - Log full error server-side
  - Client sends correlation ID for support

### 25. How do you handle validation errors?
**Answer Framework:**
- Use `422 Unprocessable Entity` (or `400 Bad Request`)
- Return **all** validation errors, not just first one
- Format should allow client to highlight specific fields
- Include error codes for i18n support
- **Example**:
```json
{
  "status": 422,
  "message": "Validation failed",
  "errors": {
    "email": ["Required field", "Must be valid email"],
    "password": ["Must be at least 8 characters"]
  }
}
```

---

## Performance & Scalability

### 26. How do you optimize API performance?
**Answer Framework:**
- **Caching**:
  - Use `Cache-Control`, `ETag`, `Last-Modified` headers
  - Cache at multiple levels (CDN, server, database)
  - Invalidate caches properly
- **Pagination**: Always paginate collections
- **Field filtering**: Let clients specify needed fields (`?fields=id,name,email`)
- **Compression**: Enable gzip/brotli
- **Database**:
  - Proper indexing
  - Avoid N+1 queries
  - Use connection pooling
- **Async processing**: For slow operations, return `202 Accepted` and process async

### 27. What is the N+1 query problem and how do you solve it?
**Answer Framework:**
- **Problem**: Making N additional queries while iterating results
- **Example**: 
  - 1 query to get users
  - N queries to get each user's posts (inside loop)
- **Solutions**:
  - **Eager loading**: JOIN or fetch related data upfront
  - **DataLoader pattern**: Batch and cache database calls
  - **GraphQL**: Built-in solutions for this problem
- **Detection**: Monitor slow API endpoints, check database query logs

### 28. How do you implement caching in APIs?
**Answer Framework:**
- **HTTP Caching Headers**:
  - `Cache-Control: max-age=3600, public`
  - `ETag: "686897696a7c876b7e"`
  - `Last-Modified: Wed, 21 Oct 2015 07:28:00 GMT`
- **Strategies**:
  - **Time-based**: Cache for fixed duration
  - **Conditional requests**: Use `If-None-Match` (ETag), return `304 Not Modified`
- **Layers**:
  - CDN (Cloudflare, CloudFront)
  - Application (Redis, Memcached)
  - Database query cache
- **Invalidation**: Hardest part
  - Cache keys with version/timestamp
  - Actively purge on updates
  - Set appropriate TTLs

### 29. When should you use async/background processing?
**Answer Framework:**
- **Use when**:
  - Operation takes >2-3 seconds
  - Email sending, file processing, report generation
  - Third-party API calls (unreliable)
  - Batch operations
- **Pattern**:
  1. Accept request, validate immediately
  2. Return `202 Accepted` with job ID
  3. Process in background (queue/worker)
  4. Provide status endpoint: `GET /jobs/{jobId}`
  5. Optional: Webhook callback when complete
- **Example response**:
```json
{
  "status": "processing",
  "jobId": "abc123",
  "statusUrl": "/api/jobs/abc123"
}
```

### 30. How do you design APIs for scalability?
**Answer Framework:**
- **Stateless**: No server-side session storage
- **Horizontal scaling**: Add more servers, not bigger servers
- **Load balancing**: Distribute traffic evenly
- **Caching**: Reduce database load
- **Database**:
  - Read replicas for scaling reads
  - Sharding for scaling writes
  - Connection pooling
- **Rate limiting**: Prevent abuse
- **Async processing**: Offload heavy work
- **Monitoring**: Track performance, identify bottlenecks
- **CDN**: Serve static content from edge locations

---

## Security

### 31. What are the OWASP Top 10 API Security Risks?
**Answer Framework:**
1. **Broken Object Level Authorization**: Check user can access specific resource
2. **Broken Authentication**: Weak auth mechanisms
3. **Broken Object Property Level Authorization**: Mass assignment vulnerabilities
4. **Unrestricted Resource Access**: Missing rate limiting
5. **Broken Function Level Authorization**: Missing role checks
6. **Unrestricted Access to Sensitive Business Flows**: Lack of flow control
7. **Server Side Request Forgery (SSRF)**: API makes unvalidated requests
8. **Security Misconfiguration**: Default configs, verbose errors
9. **Improper Inventory Management**: Undocumented endpoints, old versions
10. **Unsafe Consumption of APIs**: Blindly trusting third-party APIs

### 32. How do you prevent SQL injection in APIs?
**Answer Framework:**
- **Use parameterized queries** (prepared statements)
- **Never** concatenate user input into SQL
- **Input validation**: Allow-list, not block-list
- **ORM frameworks**: Use them correctly (they prevent SQL injection)
- **Example**:
```python
# BAD
query = f"SELECT * FROM users WHERE id = {user_id}"

# GOOD
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```
- **Least privilege**: Database user should have minimal permissions

### 33. What is CORS and how do you configure it securely?
**Answer Framework:**
- **CORS**: Cross-Origin Resource Sharing
- Browser security feature preventing cross-origin requests
- **Headers**:
  - `Access-Control-Allow-Origin`: Specify allowed origins (NOT `*` in production)
  - `Access-Control-Allow-Methods`: Allowed HTTP methods
  - `Access-Control-Allow-Headers`: Allowed request headers
  - `Access-Control-Allow-Credentials`: Allow cookies (requires specific origin)
- **Secure configuration**:
  - Whitelist specific origins, not `*`
  - Only allow necessary methods
  - Don't allow credentials with wildcard origin
  - Set appropriate `max-age` for preflight caching

### 34. How do you protect against XSS in API responses?
**Answer Framework:**
- **Content-Type header**: Set correctly (`application/json`)
- **X-Content-Type-Options: nosniff**: Prevent MIME sniffing
- **Output encoding**: Encode special characters if HTML returned
- **CSP header**: Content-Security-Policy (if serving HTML)
- **Validate input**: Sanitize on input, encode on output
- **JSON-only APIs**: Less XSS risk than HTML responses
- **HTTPOnly cookies**: JavaScript can't access them

### 35. What security headers should every API include?
**Answer Framework:**
```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'none'
Referrer-Policy: no-referrer
Permissions-Policy: geolocation=(), microphone=()
```
- **HTTPS only**: Redirect HTTP to HTTPS
- **HSTS**: Force HTTPS for all future requests
- **Remove**: Server version headers (X-Powered-By, Server)

---

## Documentation & Best Practices

### 36. What should comprehensive API documentation include?
**Answer Framework:**
- **Getting started guide**: Quick tutorial, authentication setup
- **Endpoint reference**:
  - HTTP method, URL pattern
  - Request parameters (path, query, body)
  - Request/response examples
  - Status codes and error cases
  - Rate limits
- **Authentication**: How to obtain and use tokens
- **Versioning policy**: How versions are managed
- **Error codes**: Complete error code reference
- **SDKs/libraries**: Client libraries in popular languages
- **Changelog**: Version history, breaking changes
- **Interactive console**: Try endpoints (Swagger UI, Postman)

### 37. What are API design best practices for error messages?
**Answer Framework:**
- **User-friendly**: Clear, actionable messages
- **Consistent format**: Same structure across all errors
- **Error codes**: For programmatic handling
- **Specific**: "Email already exists" vs "Invalid input"
- **No sensitive data**: Don't leak implementation details
- **Helpful**: Suggest how to fix
- **Localized**: Support multiple languages
- **Example**:
```json
{
  "error": "DUPLICATE_EMAIL",
  "message": "An account with this email already exists",
  "suggestion": "Try logging in or use password reset"
}
```

### 38. Should you use snake_case or camelCase in JSON responses?
**Answer Framework:**
- **No universal standard**, choose one and be consistent
- **camelCase**: JavaScript convention, matches frontend code
- **snake_case**: Python, Ruby convention, more readable
- **Recommendation**: 
  - Follow language conventions of your API's primary consumers
  - Document choice clearly
  - Stick with it consistently
  - Modern: camelCase is more common for web APIs

### 39. How do you handle API backwards compatibility?
**Answer Framework:**
- **Additive changes only** (new fields, endpoints)
- **Optional by default**: New fields should be optional
- **Deprecation period**: Give clients time to migrate
- **Version management**: Major version for breaking changes
- **Don't remove**: Mark as deprecated instead
- **Don't rename**: Add new field, keep old one
- **Test**: Test old clients against new API version
- **Monitor**: Track usage of deprecated features

### 40. What is HATEOAS and should you implement it?
**Answer Framework:**
- **HATEOAS**: Hypermedia As The Engine Of Application State
- Include links to related resources in responses
- **Example**:
```json
{
  "id": 123,
  "name": "John Doe",
  "_links": {
    "self": "/users/123",
    "orders": "/users/123/orders",
    "edit": "/users/123",
    "delete": "/users/123"
  }
}
```
- **Pros**: Self-documenting, discoverable, decouples client from URLs
- **Cons**: Larger responses, more complex, rarely implemented
- **Recommendation**: Optional; most APIs don't implement it

---

## Practical Design Scenarios

### 41. Design an API for a blog platform
**Answer Framework:**

**Resources**:
- Users, Posts, Comments, Tags, Categories

**Endpoints**:
```
GET    /api/v1/posts                  # List posts (paginated)
POST   /api/v1/posts                  # Create post
GET    /api/v1/posts/{id}             # Get post
PUT    /api/v1/posts/{id}             # Update post
DELETE /api/v1/posts/{id}             # Delete post
GET    /api/v1/posts/{id}/comments    # List comments
POST   /api/v1/posts/{id}/comments    # Add comment
GET    /api/v1/users/{id}/posts       # User's posts
GET    /api/v1/tags/{name}/posts      # Posts by tag
```

**Query parameters**:
- Filtering: `?status=published&category=tech`
- Sorting: `?sort=-created_at` (- for descending)
- Pagination: `?page=2&limit=20`
- Field selection: `?fields=id,title,summary`

### 42. How would you design a URL shortener API?
**Answer Framework:**

**Core endpoints**:
```
POST   /api/v1/urls                   # Create short URL
GET    /api/v1/urls/{shortCode}       # Get URL details
GET    /{shortCode}                   # Redirect to original
GET    /api/v1/urls/{shortCode}/stats # View statistics
DELETE /api/v1/urls/{shortCode}       # Delete short URL
```

**Request (create)**:
```json
{
  "originalUrl": "https://example.com/very/long/url",
  "customAlias": "optional-custom-code",
  "expiresAt": "2024-12-31T23:59:59Z"
}
```

**Response**:
```json
{
  "shortCode": "abc123",
  "shortUrl": "https://short.ly/abc123",
  "originalUrl": "https://example.com/very/long/url",
  "createdAt": "2024-01-15T10:30:00Z",
  "expiresAt": "2024-12-31T23:59:59Z"
}
```

**Considerations**:
- Rate limiting (prevent spam)
- Validation (check URL format, prevent malicious sites)
- Analytics (track clicks, referrers)
- Expiration handling
- Custom aliases (check uniqueness)
- Authentication for creating/managing URLs

### 43. Design an API for file uploads
**Answer Framework:**

**Small files** (< 10MB):
```
POST /api/v1/files
Content-Type: multipart/form-data

Response:
{
  "id": "file123",
  "url": "https://cdn.example.com/files/file123.pdf",
  "filename": "document.pdf",
  "size": 2048576,
  "mimeType": "application/pdf"
}
```

**Large files** (multipart/resumable):
```
# 1. Initiate upload
POST /api/v1/uploads
{
  "filename": "video.mp4",
  "size": 524288000,
  "mimeType": "video/mp4"
}

Response:
{
  "uploadId": "upload123",
  "chunkSize": 5242880,
  "uploadUrl": "/api/v1/uploads/upload123/chunks"
}

# 2. Upload chunks
PUT /api/v1/uploads/upload123/chunks/1
Content-Range: bytes 0-5242879/524288000

# 3. Complete upload
POST /api/v1/uploads/upload123/complete
```

**Considerations**:
- Virus scanning
- File type validation
- Size limits
- Presigned URLs (S3)
- Progress tracking
- Resume capability

### 44. How would you design a search API?
**Answer Framework:**

**Endpoint**:
```
GET /api/v1/search?q=query&filters[category]=tech&sort=-relevance&page=1
```

**Request**:
```
GET /api/v1/search
  ?q=javascript
  &type=posts,users
  &filters[category]=programming
  &filters[date_from]=2024-01-01
  &sort=-relevance
  &page=2
  &limit=20
```

**Response**:
```json
{
  "query": "javascript",
  "results": [
    {
      "type": "post",
      "id": 123,
      "title": "JavaScript Best Practices",
      "highlight": "...learn <em>JavaScript</em> effectively...",
      "score": 0.95
    }
  ],
  "facets": {
    "category": {
      "programming": 45,
      "web-dev": 32
    },
    "type": {
      "posts": 67,
      "users": 12
    }
  },
  "pagination": {
    "total": 79,
    "page": 2,
    "limit": 20
  },
  "took": 23
}
```

**Features**:
- Full-text search
- Filters/facets
- Autocomplete endpoint: `GET /api/v1/search/autocomplete?q=java`
- Sorting options
- Highlighting matches
- Type-ahead suggestions

### 45. Design a notification API
**Answer Framework:**

**Endpoints**:
```
GET    /api/v1/notifications           # List notifications
GET    /api/v1/notifications/{id}      # Get notification
PATCH  /api/v1/notifications/{id}      # Mark as read
POST   /api/v1/notifications/mark-read # Bulk mark as read
DELETE /api/v1/notifications/{id}      # Delete notification
GET    /api/v1/notifications/unread-count # Get count
```

**WebSocket** (real-time):
```
wss://api.example.com/v1/notifications/stream
```

**Notification object**:
```json
{
  "id": "notif123",
  "type": "comment",
  "title": "New comment on your post",
  "message": "John Doe commented on 'API Design'",
  "data": {
    "postId": 456,
    "commentId": 789
  },
  "read": false,
  "createdAt": "2024-01-15T10:30:00Z",
  "actionUrl": "/posts/456#comment-789"
}
```

**Considerations**:
- Multiple channels (in-app, email, SMS, push)
- Preferences (user can opt out of types)
- Batching (digest emails)
- Real-time delivery (WebSocket)
- Expiration/cleanup
- Read/unread tracking

### 46. How would you implement API analytics?
**Answer Framework:**

**Endpoints**:
```
GET /api/v1/analytics/overview
GET /api/v1/analytics/endpoints
GET /api/v1/analytics/errors
GET /api/v1/analytics/users
```

**Metrics to track**:
- **Usage**: Requests per endpoint, method distribution
- **Performance**: Response times (avg, p50, p95, p99)
- **Errors**: Error rates, status code distribution
- **Users**: Active users, top consumers
- **Geography**: Requests by location
- **Trends**: Over time (hourly, daily, monthly)

**Example response**:
```json
{
  "period": "last_7_days",
  "totalRequests": 1500000,
  "avgResponseTime": 120,
  "errorRate": 0.02,
  "topEndpoints": [
    {
      "endpoint": "/api/v1/posts",
      "requests": 450000,
      "avgResponseTime": 85
    }
  ],
  "statusCodes": {
    "200": 1200000,
    "404": 15000,
    "500": 3000
  }
}
```

**Implementation**:
- Middleware to log all requests
- Time-series database (InfluxDB, TimescaleDB)
- Async processing (don't slow down API)
- Sampling for high-traffic APIs
- Dashboards (Grafana)

### 47. Design a webhook system
**Answer Framework:**

**Endpoints**:
```
POST   /api/v1/webhooks              # Register webhook
GET    /api/v1/webhooks              # List webhooks
GET    /api/v1/webhooks/{id}         # Get webhook
PUT    /api/v1/webhooks/{id}         # Update webhook
DELETE /api/v1/webhooks/{id}         # Delete webhook
GET    /api/v1/webhooks/{id}/deliveries # View delivery history
POST   /api/v1/webhooks/{id}/test    # Test webhook
```

**Register webhook**:
```json
{
  "url": "https://myapp.com/webhooks/receiver",
  "events": ["post.created", "post.updated", "comment.created"],
  "secret": "optional-signing-secret"
}
```

**Webhook payload**:
```json
{
  "id": "evt_123",
  "type": "post.created",
  "createdAt": "2024-01-15T10:30:00Z",
  "data": {
    "id": 456,
    "title": "New Post",
    "author": "John Doe"
  }
}
```

**Headers sent**:
```
X-Webhook-Id: evt_123
X-Webhook-Signature: sha256=abc123...
X-Webhook-Event: post.created
```

**Considerations**:
- Retry logic (exponential backoff)
- Signature verification (HMAC)
- Delivery confirmation
- Timeout handling (5-10 seconds)
- Ordering guarantees
- Rate limiting callbacks
- Dead letter queue
- Idempotency (send idempotency key)

### 48. How would you design a multi-tenant API?
**Answer Framework:**

**Approaches**:

**1. Subdomain-based**:
- `https://acme.api.example.com`
- `https://widget.api.example.com`

**2. Path-based**:
- `https://api.example.com/acme/...`
- `https://api.example.com/widget/...`

**3. Header-based**:
- `X-Tenant-ID: acme`
- All tenants use same domain

**4. Token-based**:
- JWT includes tenant ID
- Extract from auth token

**Considerations**:
- **Data isolation**: Separate databases vs shared with tenant_id
- **Rate limiting**: Per-tenant limits
- **Customization**: Tenant-specific features
- **Billing**: Track usage per tenant
- **Security**: Prevent cross-tenant data leaks
- **Performance**: Query optimization with proper indexing

**Recommended**: Token-based (tenant in JWT) with shared database and tenant_id on all tables

### 49. Design an API for a payment processing system
**Answer Framework:**

**Endpoints**:
```
POST   /api/v1/payments              # Create payment
GET    /api/v1/payments/{id}         # Get payment status
POST   /api/v1/payments/{id}/refund  # Refund payment
GET    /api/v1/payments              # List payments
POST   /api/v1/payment-methods       # Add payment method
GET    /api/v1/payment-methods       # List payment methods
```

**Create payment**:
```json
{
  "amount": 5000,
  "currency": "USD",
  "paymentMethod": "pm_abc123",
  "description": "Order #12345",
  "metadata": {
    "orderId": "12345",
    "customerId": "cust_789"
  },
  "idempotencyKey": "unique-key-12345"
}
```

**Response**:
```json
{
  "id": "pay_abc123",
  "status": "succeeded",
  "amount": 5000,
  "currency": "USD",
  "created": "2024-01-15T10:30:00Z",
  "receiptUrl": "https://pay.example.com/receipts/pay_abc123"
}
```

**Status values**: `pending`, `processing`, `succeeded`, `failed`, `refunded`

**Critical considerations**:
- **Idempotency**: Prevent duplicate charges
- **Webhooks**: Notify on status changes
- **Security**: PCI compliance, tokenization
- **Retry logic**: Handle network failures
- **Atomic operations**: Payment + order confirmation together
- **Audit trail**: Log all operations
- **Currency handling**: Avoid floating point, use cents/minor units
- **Testing**: Sandbox mode, test card numbers

### 50. How do you design for API observability?
**Answer Framework:**

**Three pillars**:

**1. Logging**:
- Request/response logs
- Error logs with stack traces
- Structured logging (JSON)
- Correlation IDs across services
- Log levels (DEBUG, INFO, WARN, ERROR)

**2. Metrics**:
- Request rate, error rate, duration (RED method)
- Resource utilization (CPU, memory, connections)
- Business metrics (signups, conversions)
- Custom metrics (items_sold, revenue)
- Time series data

**3. Tracing**:
- Distributed tracing (OpenTelemetry)
- Track request across microservices
- Identify bottlenecks
- Visualize service dependencies

**Headers for correlation**:
```
X-Request-ID: unique-request-id
X-Correlation-ID: trace-id-across-services
```

**Response time breakdown**:
```json
{
  "data": {...},
  "meta": {
    "requestId": "req_123",
    "timing": {
      "total": 245,
      "database": 180,
      "cache": 15,
      "external": 50
    }
  }
}
```

**Tools**: Prometheus, Grafana, ELK Stack, Datadog, New Relic, Jaeger

---

## Bonus Questions

### 51. What is GraphQL and when should you use it over REST?
**Answer Framework:**
- **GraphQL**: Query language for APIs, single endpoint
- **Advantages**:
  - Client specifies exactly what fields they need
  - No over-fetching or under-fetching
  - Single request for multiple resources
  - Strong typing, introspection
- **Use GraphQL when**:
  - Complex, nested data requirements
  - Mobile apps (minimize data transfer)
  - Rapid frontend iteration
  - Multiple clients with different needs
- **Use REST when**:
  - Simple CRUD operations
  - Caching is critical (HTTP caching works well)
  - Team unfamiliar with GraphQL
  - File uploads (simpler in REST)

### 52. How do you handle API breaking changes in production?
**Answer Framework:**
1. **Avoid if possible**: Use API versioning from start
2. **If unavoidable**:
   - Release new version (v2) alongside old (v1)
   - **Dual write**: Update both versions temporarily
   - Migrate clients gradually
   - Monitor v1 usage
   - Announce sunset date
   - Provide migration guide
   - Maintain v1 for grace period (6-12 months)
   - Finally deprecate v1
3. **Communication**: Email lists, blog posts, deprecation warnings
4. **Automation**: Tools to detect old version usage

### 53. What is the difference between URI and URL?
**Answer Framework:**
- **URI** (Uniform Resource Identifier): Identifies a resource
  - Can be a name (URN) or locator (URL)
  - Example: `urn:isbn:0451450523`
- **URL** (Uniform Resource Locator): Locates a resource
  - Subset of URI
  - Includes access method
  - Example: `https://api.example.com/users/123`
- **All URLs are URIs, but not all URIs are URLs**
- In practice, most APIs use URLs

### 54. How would you implement soft delete in an API?
**Answer Framework:**
- Add `deleted_at` timestamp field (NULL when not deleted)
- **DELETE endpoint** sets `deleted_at` instead of removing row
- **GET endpoints** filter out deleted items by default
- **Query parameter** to include deleted: `?include_deleted=true`
- **Restore endpoint**: `POST /api/v1/posts/{id}/restore`
- **Permanent delete** (admin only): `DELETE /api/v1/posts/{id}?permanent=true`
- **Benefits**: Audit trail, undo capability, data recovery
- **Cons**: Database bloat, more complex queries

### 55. What is content negotiation and how do you implement it?
**Answer Framework:**
- Client and server agree on response format
- **Request headers**:
  - `Accept: application/json` (preferred format)
  - `Accept: application/xml`
  - `Accept: text/html`
  - `Accept: application/json, application/xml;q=0.9` (with quality values)
- **Response**:
  - `Content-Type: application/json`
  - Return format client requested
  - `406 Not Acceptable` if can't provide requested format
- **Use cases**: 
  - Same endpoint returns JSON or XML
  - API versioning via media types
  - Language negotiation (`Accept-Language`)

---

## Summary Checklist

When designing an API, ensure you've considered:

- ✅ **Resources**: Named with nouns, hierarchical structure
- ✅ **HTTP Methods**: Correct method for each operation
- ✅ **Status Codes**: Appropriate codes for all scenarios
- ✅ **Versioning**: Strategy chosen and implemented
- ✅ **Authentication**: Secure method implemented
- ✅ **Authorization**: Proper permission checks
- ✅ **Error Handling**: Consistent, helpful error responses
- ✅ **Validation**: Input validation on all endpoints
- ✅ **Pagination**: All collection endpoints paginated
- ✅ **Rate Limiting**: Prevent abuse
- ✅ **Caching**: Appropriate cache headers
- ✅ **Security**: HTTPS, input sanitization, CORS configured
- ✅ **Documentation**: Complete API reference
- ✅ **Monitoring**: Logging, metrics, alerting
- ✅ **Testing**: Unit, integration, and load tests

---

**Remember**: Good API design is about consistency, clarity, and developer experience. When in doubt, follow established conventions and industry standards.
