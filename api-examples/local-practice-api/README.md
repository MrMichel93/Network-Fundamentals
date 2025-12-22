# 🏠 Local Practice API

A fully-functional REST API that you can run locally for hands-on practice. This API includes authentication, CRUD operations, database integration, and intentional error scenarios for learning.

## 🎯 Features

- ✅ **Complete REST API** - All CRUD operations
- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **SQLite Database** - Built-in database integration
- ✅ **Error Scenarios** - Intentional errors for learning
- ✅ **Input Validation** - Proper request validation
- ✅ **Rate Limiting** - Learn about rate limits
- ✅ **API Documentation** - Self-documenting endpoints
- ✅ **CORS Support** - Ready for frontend integration

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to this directory:**
   ```bash
   cd api-examples/local-practice-api
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python app.py
   ```

4. **Test it works:**
   ```bash
   curl http://localhost:5000/api/health
   ```

The API will be running at `http://localhost:5000`

## 📖 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Authentication

Most endpoints require a JWT token. Get one by registering and logging in.

#### Register a New User
```bash
POST /api/auth/register

{
  "username": "alice",
  "email": "alice@example.com",
  "password": "securepassword123"
}

Response: 201 Created
{
  "message": "User created successfully",
  "user_id": 1
}
```

#### Login
```bash
POST /api/auth/login

{
  "username": "alice",
  "password": "securepassword123"
}

Response: 200 OK
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com"
  }
}
```

#### Using the Token

Include the token in the Authorization header:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:5000/api/users/me
```

### Users API

#### Get Current User
```bash
GET /api/users/me
Authorization: Bearer <token>

Response: 200 OK
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "created_at": "2024-01-01T12:00:00"
}
```

#### Update Current User
```bash
PATCH /api/users/me
Authorization: Bearer <token>

{
  "email": "newemail@example.com"
}

Response: 200 OK
{
  "id": 1,
  "username": "alice",
  "email": "newemail@example.com"
}
```

### Posts API

#### Get All Posts
```bash
GET /api/posts
# Optional query parameters: ?page=1&limit=10&author=alice

Response: 200 OK
{
  "data": [
    {
      "id": 1,
      "title": "My First Post",
      "content": "Hello World!",
      "author": "alice",
      "created_at": "2024-01-01T12:00:00"
    }
  ],
  "meta": {
    "total": 1,
    "page": 1,
    "limit": 10
  }
}
```

#### Get Single Post
```bash
GET /api/posts/:id

Response: 200 OK
{
  "id": 1,
  "title": "My First Post",
  "content": "Hello World!",
  "author": "alice",
  "created_at": "2024-01-01T12:00:00"
}
```

#### Create Post
```bash
POST /api/posts
Authorization: Bearer <token>

{
  "title": "My New Post",
  "content": "This is the content of my post"
}

Response: 201 Created
{
  "id": 2,
  "title": "My New Post",
  "content": "This is the content of my post",
  "author": "alice",
  "created_at": "2024-01-01T13:00:00"
}
```

#### Update Post
```bash
PUT /api/posts/:id
Authorization: Bearer <token>

{
  "title": "Updated Title",
  "content": "Updated content"
}

Response: 200 OK
{
  "id": 1,
  "title": "Updated Title",
  "content": "Updated content",
  "author": "alice",
  "updated_at": "2024-01-01T14:00:00"
}
```

#### Delete Post
```bash
DELETE /api/posts/:id
Authorization: Bearer <token>

Response: 204 No Content
```

### Comments API

#### Get Comments for Post
```bash
GET /api/posts/:id/comments

Response: 200 OK
[
  {
    "id": 1,
    "post_id": 1,
    "author": "bob",
    "content": "Great post!",
    "created_at": "2024-01-01T15:00:00"
  }
]
```

#### Add Comment to Post
```bash
POST /api/posts/:id/comments
Authorization: Bearer <token>

{
  "content": "This is my comment"
}

Response: 201 Created
{
  "id": 2,
  "post_id": 1,
  "author": "alice",
  "content": "This is my comment",
  "created_at": "2024-01-01T16:00:00"
}
```

### Testing Endpoints

#### Health Check
```bash
GET /api/health

Response: 200 OK
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

#### Echo Endpoint
```bash
POST /api/test/echo

{
  "message": "Hello API!"
}

Response: 200 OK
{
  "echo": {
    "message": "Hello API!"
  },
  "received_at": "2024-01-01T12:00:00"
}
```

#### Test Error Scenarios
```bash
# 400 Bad Request
GET /api/test/error/400

# 401 Unauthorized
GET /api/test/error/401

# 404 Not Found
GET /api/test/error/404

# 500 Internal Server Error
GET /api/test/error/500

# Rate Limit (429)
GET /api/test/rate-limit
# Make 6+ requests in quick succession
```

## 🧪 Practice Exercises

### Exercise 1: Basic CRUD
1. Register a new user
2. Login and get a token
3. Create 3 posts
4. List all posts
5. Update one post
6. Delete one post

### Exercise 2: Error Handling
1. Try to access `/api/users/me` without a token
2. Try to create a post with missing fields
3. Try to delete someone else's post
4. Trigger various error endpoints

### Exercise 3: Filtering and Pagination
1. Create 20 posts with different authors
2. Use pagination to get posts 10 at a time
3. Filter posts by specific author
4. Implement client-side pagination

### Exercise 4: Build a Client
Create a Python client that:
- Handles authentication (stores token)
- Provides methods for all CRUD operations
- Has proper error handling
- Uses requests.Session for efficiency

**Starter code:**
```python
import requests

class APIClient:
    def __init__(self, base_url='http://localhost:5000/api'):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None
    
    def register(self, username, email, password):
        # TODO: Implement
        pass
    
    def login(self, username, password):
        # TODO: Implement and store token
        pass
    
    def get_posts(self, page=1, limit=10):
        # TODO: Implement
        pass
    
    def create_post(self, title, content):
        # TODO: Implement with auth
        pass
```

### Exercise 5: Break and Fix
This API is designed for learning. Try to:
1. Find edge cases that cause errors
2. Trigger rate limits
3. Send malformed data
4. Test authentication bypass attempts
5. Learn from error messages

## 🔧 Customization

### Modify the Database

The database is in `practice_api.db`. You can:
- View/edit with SQLite browser
- Reset by deleting the file
- Add custom tables
- Seed with test data

### Add New Endpoints

Edit `app.py` to add your own endpoints:

```python
@app.route('/api/custom/endpoint', methods=['GET'])
def custom_endpoint():
    return jsonify({'message': 'Custom endpoint!'})
```

### Change Settings

Edit these constants in `app.py`:
- `SECRET_KEY` - JWT secret (change for production!)
- `RATE_LIMIT` - Requests per minute
- `TOKEN_EXPIRY` - How long tokens last

## 🐛 Common Issues

### Port Already in Use
```bash
# Change port in app.py or kill existing process
lsof -ti:5000 | xargs kill
```

### Database Locked
```bash
# Reset database
rm practice_api.db
python app.py  # Will recreate
```

### CORS Errors (Frontend)
The API has CORS enabled. If issues persist, check browser console.

## 📚 Learning Resources

This API demonstrates:
- **REST principles** - Resource-based URLs, HTTP methods
- **JWT Authentication** - Token-based security
- **SQLite** - Lightweight database
- **Flask** - Python web framework
- **Error Handling** - Proper HTTP status codes
- **Validation** - Input checking
- **Rate Limiting** - Request throttling

## 🎓 Next Steps

After mastering this API:
1. Add more features (likes, tags, search)
2. Implement pagination properly
3. Add file upload endpoints
4. Create a frontend (HTML/JavaScript)
5. Deploy to Heroku or Railway
6. Add Redis for caching
7. Implement WebSockets for real-time features

## 🤝 Contributing

Found a bug or want to add a feature? This is your practice API - modify it freely!

## 📄 License

This practice API is free to use, modify, and share for educational purposes.

---

[← Back to API Examples](../README.md) | [Practice APIs List →](../practice-apis.md)
