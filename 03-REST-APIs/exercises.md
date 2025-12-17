# 🏋️ Exercises: REST APIs

Build your REST API skills with these hands-on exercises!

## Exercise 1: Explore a Public REST API 🌍

**Objective**: Learn by exploring a real-world API.

**Tasks**:
1. Explore the GitHub API: `https://api.github.com`
2. Get information about a user: `https://api.github.com/users/octocat`
3. List repositories: `https://api.github.com/users/octocat/repos`
4. Identify the resource hierarchy
5. Note the response structure

<details>
<summary>💡 Hint</summary>

```bash
# Explore the API root
curl https://api.github.com

# Get user info
curl https://api.github.com/users/octocat

# Get user's repos
curl https://api.github.com/users/octocat/repos

# Pretty print with jq (if installed)
curl https://api.github.com/users/octocat | jq '.'
```

**Questions to answer:**
- What fields are in the user object?
- How is pagination handled?
- What headers are returned?
- What status codes do you see?
</details>

**Success Criteria**: You can navigate and understand a real REST API.

---

## Exercise 2: Run the Books API Server 📚

**Objective**: Understand a complete REST API implementation.

**Tasks**:
1. Install Flask: `pip install flask`
2. Run `rest_api_server.py`
3. Test all endpoints using curl
4. Create, read, update, and delete books
5. Test error cases (404, validation errors)

<details>
<summary>💡 Hint</summary>

```bash
# Install Flask
pip install flask

# Start the server
python rest_api_server.py

# In another terminal:
# Get all books
curl http://localhost:5000/api/books

# Get specific book
curl http://localhost:5000/api/books/1

# Create new book
curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -d '{"title":"REST APIs","author":"You","isbn":"123-456"}'

# Update book (PATCH)
curl -X PATCH http://localhost:5000/api/books/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title"}'

# Delete book
curl -X DELETE http://localhost:5000/api/books/1 -i
```
</details>

**Success Criteria**: You can perform all CRUD operations successfully.

---

## Exercise 3: Build a Simple REST API Client 💻

**Objective**: Learn to consume REST APIs programmatically.

**Tasks**:
1. Use the provided `rest_api_client.py` as reference
2. Create your own client that:
   - Lists all books
   - Creates a new book
   - Updates the book
   - Deletes the book
3. Add proper error handling

<details>
<summary>💡 Hint</summary>

```python
import requests

BASE_URL = 'http://localhost:5000/api'

# GET request
response = requests.get(f'{BASE_URL}/books')
if response.status_code == 200:
    books = response.json()
    print(books)

# POST request
new_book = {
    'title': 'My Book',
    'author': 'Me',
    'isbn': '123-456'
}
response = requests.post(f'{BASE_URL}/books', json=new_book)
if response.status_code == 201:
    print('Created:', response.json())

# PATCH request
updates = {'title': 'Updated Title'}
response = requests.patch(f'{BASE_URL}/books/1', json=updates)

# DELETE request
response = requests.delete(f'{BASE_URL}/books/1')
if response.status_code == 204:
    print('Deleted successfully')
```
</details>

**Success Criteria**: Your client successfully interacts with the API.

---

## Exercise 4: Design a REST API 📐

**Objective**: Practice API design principles.

**Scenario**: Design a REST API for a simple blog system with Posts, Comments, and Users.

**Tasks**:
1. Define all endpoints (URL patterns)
2. Specify HTTP methods for each
3. Design the JSON response structure
4. Document expected status codes

<details>
<summary>💡 Hint</summary>

**Example Design:**

**Users:**
- `GET /users` - List all users
- `GET /users/:id` - Get user details
- `POST /users` - Create user
- `PUT /users/:id` - Update user
- `DELETE /users/:id` - Delete user

**Posts:**
- `GET /posts` - List all posts
- `GET /posts/:id` - Get post
- `GET /users/:id/posts` - Get user's posts
- `POST /posts` - Create post
- `PUT /posts/:id` - Update post
- `DELETE /posts/:id` - Delete post

**Comments:**
- `GET /posts/:id/comments` - Get post comments
- `POST /posts/:id/comments` - Add comment
- `PUT /comments/:id` - Update comment
- `DELETE /comments/:id` - Delete comment

**Example Response:**
```json
{
  "id": "123",
  "title": "My First Post",
  "content": "Hello World!",
  "author_id": "456",
  "created_at": "2024-01-01T12:00:00Z",
  "comments_count": 5
}
```
</details>

**Success Criteria**: Your design follows REST principles and is consistent.

---

## Exercise 5: Implement a TODO API 📝

**Objective**: Build your own REST API from scratch.

**Requirements**:
Create a REST API for managing TODO items with:
- Create a TODO
- List all TODOs
- Get specific TODO
- Update TODO (mark as complete)
- Delete TODO

**Fields**: id, title, description, completed, created_at

<details>
<summary>💡 Hint</summary>

```python
from flask import Flask, request, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)
todos = {}

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify({'data': list(todos.values())}), 200

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    
    if 'title' not in data:
        return jsonify({'error': 'Title required'}), 400
    
    todo_id = str(uuid.uuid4())[:8]
    todo = {
        'id': todo_id,
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': False,
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    
    todos[todo_id] = todo
    return jsonify(todo), 201

@app.route('/api/todos/<todo_id>', methods=['GET'])
def get_todo(todo_id):
    if todo_id not in todos:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(todos[todo_id]), 200

@app.route('/api/todos/<todo_id>', methods=['PATCH'])
def update_todo(todo_id):
    if todo_id not in todos:
        return jsonify({'error': 'Not found'}), 404
    
    data = request.get_json()
    if 'completed' in data:
        todos[todo_id]['completed'] = data['completed']
    if 'title' in data:
        todos[todo_id]['title'] = data['title']
    
    return jsonify(todos[todo_id]), 200

@app.route('/api/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    if todo_id not in todos:
        return jsonify({'error': 'Not found'}), 404
    
    del todos[todo_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```
</details>

**Success Criteria**: Your API handles all CRUD operations correctly.

---

## Exercise 6: Add Query Parameters 🔍

**Objective**: Implement filtering and pagination.

**Tasks**:
Enhance your TODO API (from Exercise 5) to support:
1. Filter by completed status: `GET /api/todos?completed=true`
2. Search by title: `GET /api/todos?search=meeting`
3. Pagination: `GET /api/todos?limit=10&offset=20`
4. Sorting: `GET /api/todos?sort=created_at`

<details>
<summary>💡 Hint</summary>

```python
@app.route('/api/todos', methods=['GET'])
def get_todos():
    # Get query parameters
    completed_filter = request.args.get('completed')
    search_query = request.args.get('search')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    sort_by = request.args.get('sort', 'created_at')
    
    # Start with all todos
    result = list(todos.values())
    
    # Apply filters
    if completed_filter is not None:
        is_completed = completed_filter.lower() == 'true'
        result = [t for t in result if t['completed'] == is_completed]
    
    if search_query:
        result = [t for t in result 
                 if search_query.lower() in t['title'].lower()]
    
    # Sort
    if sort_by in ['created_at', 'title']:
        result.sort(key=lambda x: x.get(sort_by, ''))
    
    # Paginate
    total = len(result)
    result = result[offset:offset + limit]
    
    return jsonify({
        'data': result,
        'meta': {
            'total': total,
            'limit': limit,
            'offset': offset
        }
    }), 200
```
</details>

**Success Criteria**: Query parameters filter and paginate correctly.

---

## Challenge Exercise: Build a URL Shortener API 🔗

**Objective**: Create a complete REST API for a real-world service.

**Requirements**:
Build an API that:
1. Creates short URLs: `POST /api/urls` with `{"url": "https://example.com"}`
2. Returns: `{"short_code": "abc123", "url": "https://example.com"}`
3. Redirects: `GET /:short_code` redirects to original URL
4. Lists URLs: `GET /api/urls`
5. Deletes URLs: `DELETE /api/urls/:short_code`
6. Tracks click count

<details>
<summary>💡 Hint</summary>

```python
from flask import Flask, request, jsonify, redirect
import string
import random

app = Flask(__name__)
urls = {}

def generate_short_code():
    """Generate random 6-character code."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

@app.route('/api/urls', methods=['POST'])
def create_short_url():
    data = request.get_json()
    
    if 'url' not in data:
        return jsonify({'error': 'URL required'}), 400
    
    short_code = generate_short_code()
    while short_code in urls:  # Ensure unique
        short_code = generate_short_code()
    
    urls[short_code] = {
        'short_code': short_code,
        'url': data['url'],
        'clicks': 0,
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    
    return jsonify(urls[short_code]), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    if short_code not in urls:
        return jsonify({'error': 'Not found'}), 404
    
    # Increment click count
    urls[short_code]['clicks'] += 1
    
    # Redirect to original URL
    return redirect(urls[short_code]['url'], code=301)

@app.route('/api/urls', methods=['GET'])
def list_urls():
    return jsonify({'data': list(urls.values())}), 200

@app.route('/api/urls/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    if short_code not in urls:
        return jsonify({'error': 'Not found'}), 404
    
    del urls[short_code]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Test it:**
```bash
# Create short URL
curl -X POST http://localhost:5000/api/urls \
  -H "Content-Type: application/json" \
  -d '{"url":"https://github.com"}'

# Visit short URL in browser
# http://localhost:5000/abc123

# List all URLs
curl http://localhost:5000/api/urls
```
</details>

**Success Criteria**: Your URL shortener works end-to-end.

---

## Mini-Quiz ✅

1. **What HTTP method creates a resource?**
   - [ ] GET
   - [ ] POST
   - [ ] PUT
   - [ ] DELETE

2. **What status code indicates successful creation?**
   - [ ] 200
   - [ ] 201
   - [ ] 204
   - [ ] 400

3. **Which is better REST resource naming?**
   - [ ] /getUsers
   - [ ] /users
   - [ ] /Users
   - [ ] /user_list

4. **What's the difference between PUT and PATCH?**
   - [ ] No difference
   - [ ] PUT replaces, PATCH updates partially
   - [ ] PATCH is faster
   - [ ] PUT is more secure

5. **Where should authentication tokens go?**
   - [ ] URL query parameter
   - [ ] Authorization header
   - [ ] Request body
   - [ ] Cookie only

<details>
<summary>Show Answers</summary>

1. **B** - POST creates resources
2. **B** - 201 Created
3. **B** - /users (plural noun, lowercase)
4. **B** - PUT replaces entire resource, PATCH updates specific fields
5. **B** - Authorization header (most secure and standard)

**Scoring:**
- 5/5: REST API expert! 🌟
- 3-4/5: Good understanding! 👍
- 1-2/5: Review the lesson
</details>

---

## Solutions

Complete solutions available in [solutions/03-rest-apis-solutions.md](../solutions/03-rest-apis-solutions.md)

---

[← Back to Lesson](./README.md) | [Next: WebSockets →](../04-WebSockets/)
