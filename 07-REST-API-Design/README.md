# 🔌 REST APIs

Welcome to REST APIs! Now that you understand HTTP, let's learn how to design clean, consistent web services.

## 🎯 Learning Objectives

By the end of this module, you will:
- Understand REST principles and constraints
- Learn about resources and resource design
- Master CRUD operations (Create, Read, Update, Delete)
- Design clean and intuitive API endpoints
- Build a RESTful API using Python
- Learn REST best practices and common patterns
- Understand the difference between REST and other API styles

## What is REST?

**REST (Representational State Transfer)** is an architectural style for designing networked applications. It's not a protocol or standard - it's a set of principles for creating web services.

### Real-World Analogy: Library System 📚

Think of a REST API like a library:
- **Resources**: Books, Members, Loans
- **Operations**: Check out, return, search, add new books
- **Representations**: Book details (title, author, ISBN)
- **Identifiers**: Each book has a unique ID

Just like you interact with a library through specific procedures, clients interact with REST APIs through standard HTTP methods and well-defined URLs.

## REST Principles

### 1. Client-Server Architecture
- Client and server are separate
- They can evolve independently
- Server doesn't care if you're using a browser, mobile app, or curl

### 2. Stateless
- Each request contains all necessary information
- Server doesn't remember previous requests
- Like every conversation starting fresh

### 3. Cacheable
- Responses can be cached for performance
- Reduces server load and improves speed

### 4. Uniform Interface
- Consistent way to interact with resources
- Use standard HTTP methods
- Predictable URL patterns

### 5. Layered System
- Client doesn't know if connected directly to server or through intermediaries
- Proxies, load balancers, etc., can be added transparently

## Resources: The Core of REST

A **resource** is any piece of information that can be named. In REST, everything is a resource.

### Examples of Resources:
- A user: `/users/123`
- A blog post: `/posts/456`
- A list of users: `/users`
- A user's posts: `/users/123/posts`
- A comment on a post: `/posts/456/comments/789`

### Resource Naming Best Practices

✅ **Good Resource Names**:
```
GET /users              # Collection of users
GET /users/123          # Specific user
GET /users/123/posts    # User's posts
GET /posts/456/comments # Post's comments
```

❌ **Bad Resource Names**:
```
GET /getUsers           # Don't use verbs
GET /user-list          # Use plural nouns
GET /api/v1/user/get    # Redundant
GET /users/getAllUsers  # HTTP method already says "get"
```

### Key Principles:
1. **Use nouns, not verbs**: `/users` not `/getUsers`
2. **Use plural nouns**: `/users` not `/user`
3. **Be consistent**: Don't mix `/users` and `/user`
4. **Use hierarchy**: `/users/123/posts` for related resources
5. **Use lowercase**: `/users` not `/Users`
6. **Use hyphens for readability**: `/blog-posts` not `/blogPosts` or `/blog_posts`

## CRUD Operations with HTTP Methods

REST maps HTTP methods to CRUD operations:

| Operation | HTTP Method | URL Pattern       | Example                      |
|-----------|-------------|-------------------|------------------------------|
| **Create**| POST        | `/resources`      | `POST /users`                |
| **Read**  | GET         | `/resources` or `/resources/id` | `GET /users/123` |
| **Update**| PUT/PATCH   | `/resources/id`   | `PUT /users/123`             |
| **Delete**| DELETE      | `/resources/id`   | `DELETE /users/123`          |

### Detailed Examples

#### Create (POST)
```http
POST /users HTTP/1.1
Content-Type: application/json

{
  "name": "Alice",
  "email": "alice@example.com"
}

Response: 201 Created
Location: /users/123
{
  "id": 123,
  "name": "Alice",
  "email": "alice@example.com",
  "created_at": "2024-01-01T12:00:00Z"
}
```

#### Read (GET)
```http
# Get all users
GET /users HTTP/1.1

Response: 200 OK
{
  "users": [
    {"id": 123, "name": "Alice"},
    {"id": 124, "name": "Bob"}
  ]
}

# Get specific user
GET /users/123 HTTP/1.1

Response: 200 OK
{
  "id": 123,
  "name": "Alice",
  "email": "alice@example.com"
}
```

#### Update (PUT)
```http
# Replace entire resource
PUT /users/123 HTTP/1.1
Content-Type: application/json

{
  "name": "Alice Smith",
  "email": "alice.smith@example.com"
}

Response: 200 OK
{
  "id": 123,
  "name": "Alice Smith",
  "email": "alice.smith@example.com",
  "updated_at": "2024-01-02T10:00:00Z"
}
```

#### Update (PATCH)
```http
# Update only specific fields
PATCH /users/123 HTTP/1.1
Content-Type: application/json

{
  "email": "newemail@example.com"
}

Response: 200 OK
{
  "id": 123,
  "name": "Alice",
  "email": "newemail@example.com",
  "updated_at": "2024-01-02T10:00:00Z"
}
```

#### Delete (DELETE)
```http
DELETE /users/123 HTTP/1.1

Response: 204 No Content
```

## Query Parameters for Filtering and Sorting

Use query parameters to filter, sort, and paginate collections:

```http
# Filtering
GET /users?status=active
GET /users?age=25&city=Boston

# Sorting
GET /users?sort=name
GET /users?sort=-created_at  # Descending

# Pagination
GET /users?page=2&limit=20
GET /users?offset=40&limit=20

# Searching
GET /users?q=alice
GET /posts?search=networking

# Multiple parameters
GET /posts?author=alice&status=published&sort=-date&limit=10
```

## HTTP Status Codes in REST APIs

### Success Responses
- **200 OK**: Successful GET, PUT, PATCH, or DELETE
- **201 Created**: Successful POST (resource created)
- **204 No Content**: Successful DELETE (no response body needed)

### Client Error Responses
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Authenticated but not authorized
- **404 Not Found**: Resource doesn't exist
- **405 Method Not Allowed**: Wrong HTTP method
- **409 Conflict**: Conflict with current state (e.g., duplicate email)
- **422 Unprocessable Entity**: Validation errors

### Server Error Responses
- **500 Internal Server Error**: Server encountered an error
- **503 Service Unavailable**: Server temporarily unavailable

## Response Format Best Practices

### Consistent JSON Structure

**Single Resource:**
```json
{
  "id": 123,
  "name": "Alice",
  "email": "alice@example.com",
  "created_at": "2024-01-01T12:00:00Z"
}
```

**Collection:**
```json
{
  "data": [
    {"id": 123, "name": "Alice"},
    {"id": 124, "name": "Bob"}
  ],
  "meta": {
    "total": 150,
    "page": 1,
    "per_page": 20
  }
}
```

**Error Response:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email address",
    "details": [
      {
        "field": "email",
        "error": "Must be a valid email"
      }
    ]
  }
}
```

## Versioning Your API

### URL Path Versioning (Recommended)
```
https://api.example.com/v1/users
https://api.example.com/v2/users
```

### Header Versioning
```http
GET /users HTTP/1.1
Accept: application/vnd.example.v1+json
```

### Query Parameter Versioning
```
https://api.example.com/users?version=1
```

**Best Practice**: Use URL path versioning - it's clearest and easiest to understand.

## REST vs Other API Styles

### REST vs SOAP
- **REST**: Flexible, uses JSON, lightweight, easier to learn
- **SOAP**: Strict protocol, uses XML, more complex, built-in error handling

### REST vs GraphQL
- **REST**: Multiple endpoints, may need multiple requests, simple
- **GraphQL**: Single endpoint, request exactly what you need, steeper learning curve

### REST vs gRPC
- **REST**: Text-based (JSON), human-readable, browser-friendly
- **gRPC**: Binary (Protocol Buffers), faster, requires special tools

**When to use REST:**
- Public APIs
- Simple CRUD operations
- When browser compatibility matters
- When human-readability is important

## HATEOAS (Advanced Concept)

**HATEOAS** = Hypermedia As The Engine Of Application State

Responses include links to related resources:

```json
{
  "id": 123,
  "name": "Alice",
  "links": {
    "self": "/users/123",
    "posts": "/users/123/posts",
    "friends": "/users/123/friends"
  }
}
```

This makes APIs self-documenting and discoverable!

## API Security Basics

### Authentication Methods
1. **API Keys**: Simple token in header or query
2. **Bearer Tokens**: JWT or OAuth tokens
3. **Basic Auth**: Username/password (only over HTTPS)
4. **OAuth 2.0**: Industry standard for authorization

### Example with Bearer Token:
```http
GET /users/me HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Common Pitfalls

❌ **Using GET for operations that modify data**
```
GET /users/123/delete  # Wrong!
DELETE /users/123      # Correct!
```

❌ **Using verbs in URLs**
```
POST /createUser       # Wrong!
POST /users            # Correct!
```

❌ **Inconsistent naming**
```
GET /users
GET /product  # Wrong! Should be plural
```

❌ **Not using proper status codes**
```
200 OK with error message in body  # Confusing!
404 Not Found with error in body    # Clear!
```

## Code Examples

Check the `examples/` folder for:
- `rest_api_server.py` - Complete Flask REST API
- `rest_api_client.py` - Client to consume the API
- `api_design.md` - API design guidelines

## Summary and Key Takeaways

✅ **REST** is an architectural style using HTTP for building APIs  
✅ **Resources** are nouns, identified by URLs  
✅ **HTTP methods** map to CRUD operations  
✅ **Stateless**: Each request is independent  
✅ **Use proper status codes** to indicate results  
✅ **Consistent naming** makes APIs intuitive  
✅ **Query parameters** for filtering, sorting, pagination  
✅ **Version your API** for backward compatibility

## What's Next?

Ready to add real-time features to your apps? Learn about [WebSockets](../04-WebSockets/)!

---

[← Back: Authentication and Authorization](../06-Authentication-and-Authorization/) | [Next: Databases for APIs →](../08-Databases-for-APIs/)

## Practice

Complete the [exercises](./exercises.md) to build your own REST API!
