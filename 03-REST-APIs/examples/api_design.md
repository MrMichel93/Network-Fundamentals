# 📐 API Design Guidelines

Best practices and patterns for designing clean, intuitive REST APIs.

## URL Design Patterns

### Resource Hierarchy

```
/resources              # Collection
/resources/:id          # Individual resource
/resources/:id/subresources    # Nested collection
/resources/:id/subresources/:subid    # Nested individual resource
```

**Examples:**
```
GET    /users                   # List all users
GET    /users/123               # Get user 123
GET    /users/123/posts         # Get posts by user 123
GET    /users/123/posts/456     # Get post 456 by user 123
POST   /users/123/posts         # Create post for user 123
```

### Avoid Deep Nesting

❌ **Too deep:**
```
/users/123/posts/456/comments/789/replies/101
```

✅ **Better:**
```
/comments/789/replies/101
# or
/replies?comment_id=789
```

## HTTP Method Usage

### Standard CRUD Operations

| Action | Method | URL | Request Body | Response |
|--------|--------|-----|--------------|----------|
| List | GET | /books | None | 200 + array |
| Read | GET | /books/:id | None | 200 + object |
| Create | POST | /books | JSON object | 201 + created object |
| Replace | PUT | /books/:id | Complete JSON | 200 + updated object |
| Update | PATCH | /books/:id | Partial JSON | 200 + updated object |
| Delete | DELETE | /books/:id | None | 204 (no content) |

### Custom Actions

For actions that don't fit CRUD, use a verb as a sub-resource:

```
POST /users/123/activate
POST /users/123/deactivate
POST /orders/456/cancel
POST /invoices/789/send
```

## Query Parameters

### Filtering

```
GET /books?author=Doe
GET /books?year=2024
GET /books?author=Doe&year=2024
GET /books?published=true
```

### Sorting

```
GET /books?sort=title          # Ascending by title
GET /books?sort=-published_at  # Descending (note the minus)
GET /books?sort=author,title   # Multiple fields
```

### Pagination

**Offset-based:**
```
GET /books?limit=20&offset=40  # Third page (20 per page)
GET /books?page=3&per_page=20  # Alternative
```

**Cursor-based (better for large datasets):**
```
GET /books?cursor=abc123&limit=20
```

### Searching

```
GET /books?q=networking
GET /books?search=python programming
```

### Field Selection

```
GET /users?fields=id,name,email
GET /users/123?fields=id,name
```

### Complete Example

```
GET /books?author=Doe&year=2024&sort=-published_at&limit=10&offset=20
```

## Response Format

### Success Response Structure

**Single Resource:**
```json
{
  "id": "123",
  "title": "Network Fundamentals",
  "author": "Jane Doe",
  "created_at": "2024-01-01T12:00:00Z"
}
```

**Collection:**
```json
{
  "data": [
    {"id": "123", "title": "Book 1"},
    {"id": "124", "title": "Book 2"}
  ],
  "meta": {
    "total": 150,
    "page": 1,
    "per_page": 20,
    "total_pages": 8
  },
  "links": {
    "first": "/books?page=1",
    "prev": null,
    "next": "/books?page=2",
    "last": "/books?page=8"
  }
}
```

### Error Response Structure

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "error": "Invalid email format"
      },
      {
        "field": "age",
        "error": "Must be a positive number"
      }
    ]
  }
}
```

### Consistent Field Naming

✅ **Use snake_case for JSON:**
```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "created_at": "2024-01-01T12:00:00Z"
}
```

❌ **Don't mix formats:**
```json
{
  "firstName": "Jane",
  "last_name": "Doe",
  "CreatedAt": "2024-01-01T12:00:00Z"
}
```

## Status Codes

### Use Appropriate Status Codes

**2xx - Success:**
- `200 OK` - Standard response for successful requests
- `201 Created` - Resource created (POST)
- `204 No Content` - Success with no response body (DELETE)

**3xx - Redirection:**
- `301 Moved Permanently` - Resource permanently moved
- `304 Not Modified` - Cached version is still valid

**4xx - Client Errors:**
- `400 Bad Request` - Malformed request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Authenticated but not authorized
- `404 Not Found` - Resource doesn't exist
- `405 Method Not Allowed` - Wrong HTTP method
- `409 Conflict` - Conflict with current state
- `422 Unprocessable Entity` - Validation errors
- `429 Too Many Requests` - Rate limit exceeded

**5xx - Server Errors:**
- `500 Internal Server Error` - Generic server error
- `502 Bad Gateway` - Invalid response from upstream
- `503 Service Unavailable` - Server temporarily unavailable
- `504 Gateway Timeout` - Upstream timeout

### Status Code Examples

**Creating a resource:**
```http
POST /books HTTP/1.1
Content-Type: application/json

{"title": "New Book", "author": "Jane Doe"}

HTTP/1.1 201 Created
Location: /books/123
Content-Type: application/json

{"id": "123", "title": "New Book", "author": "Jane Doe"}
```

**Validation error:**
```http
POST /books HTTP/1.1
Content-Type: application/json

{"title": ""}

HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title cannot be empty"
  }
}
```

**Resource not found:**
```http
GET /books/999 HTTP/1.1

HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": {
    "code": "NOT_FOUND",
    "message": "Book with ID 999 not found"
  }
}
```

## Versioning

### URL Path Versioning (Recommended)

```
https://api.example.com/v1/books
https://api.example.com/v2/books
```

**Pros:** Clear, easy to understand, works everywhere  
**Cons:** More URLs to manage

### Header Versioning

```http
GET /books HTTP/1.1
Accept: application/vnd.example.v1+json
```

**Pros:** URLs stay clean  
**Cons:** Less obvious, harder to test with browser

### When to Version

- Breaking changes to response format
- Removing fields
- Changing field types
- Changing endpoint behavior

### When NOT to Version

- Adding new optional fields
- Adding new endpoints
- Bug fixes
- Performance improvements

## Authentication and Security

### API Keys (Simple)

```http
GET /books HTTP/1.1
X-API-Key: your-api-key-here
```

### Bearer Tokens (Recommended)

```http
GET /books HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Basic Auth (Over HTTPS only)

```http
GET /books HTTP/1.1
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

### Rate Limiting Headers

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Documentation Best Practices

### Essential Documentation Elements

1. **Base URL:** `https://api.example.com/v1`
2. **Authentication:** How to authenticate
3. **Endpoints:** All available endpoints
4. **Parameters:** Required and optional
5. **Request examples:** With curl or code
6. **Response examples:** Success and error cases
7. **Status codes:** What each means
8. **Rate limits:** How many requests allowed
9. **Errors:** Common errors and solutions

### Example Documentation Template

```markdown
## Get Book

Retrieve a single book by ID.

**Endpoint:** `GET /api/v1/books/:id`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `id` (string, required) - The book ID

**Response: 200 OK**
```json
{
  "id": "123",
  "title": "Network Fundamentals",
  "author": "Jane Doe"
}
```

**Response: 404 Not Found**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Book not found"
  }
}
```

**Example:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.example.com/v1/books/123
```
```

## Testing Your API

### Manual Testing with curl

```bash
# Test GET
curl -i http://localhost:5000/api/books

# Test POST
curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Book","author":"Test"}'

# Test with authentication
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:5000/api/books
```

### Automated Testing

Write tests for:
- Each endpoint
- Success cases
- Error cases
- Edge cases
- Authentication
- Authorization

## Common Pitfalls to Avoid

❌ **Using verbs in URLs**
```
POST /createUser
GET /getUsers
```

❌ **Inconsistent naming**
```
GET /users
GET /product  # Should be /products
```

❌ **Wrong status codes**
```
200 OK with error message in body
```

❌ **Exposing implementation details**
```
GET /api/users.php
GET /api/getUsers?method=json
```

❌ **Not versioning from the start**
```
# Hard to version later if changes needed
```

✅ **Follow REST principles consistently**
✅ **Use proper HTTP methods**
✅ **Use appropriate status codes**
✅ **Version your API from the start**
✅ **Document everything**

## Summary

- **Use nouns** for resources, not verbs
- **Use plural nouns** for consistency
- **Use proper HTTP methods** for CRUD operations
- **Use appropriate status codes** to indicate results
- **Version your API** for maintainability
- **Document thoroughly** for developers
- **Handle errors gracefully** with clear messages
- **Think about your users** - make it intuitive

Following these guidelines will help you build APIs that are:
- Easy to understand
- Easy to use
- Easy to maintain
- Compatible with standard tools
- Scalable as your service grows
