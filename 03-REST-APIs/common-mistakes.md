# ⚠️ Common Mistakes - REST APIs

Learn from these common pitfalls when designing and consuming RESTful APIs.

## API Design Mistakes

### 1. Non-RESTful URLs

**Mistake:**
```
POST /createUser
GET /getUser/123
POST /updateUser/123
POST /deleteUser/123
```

**Why it's wrong:**
- Not using HTTP methods properly
- Verbs in URLs (should be nouns)
- Not following REST conventions

**Correct:**
```
POST   /users         # Create
GET    /users/123     # Read
PUT    /users/123     # Update
DELETE /users/123     # Delete
```

**Lesson:** Use nouns for resources, HTTP methods for actions.

---

### 2. Not Versioning APIs

**Mistake:**
```
https://api.example.com/users
```

**Why it's wrong:**
- Breaking changes affect all clients
- No migration path
- Impossible to maintain backwards compatibility

**Correct:**
```
https://api.example.com/v1/users
https://api.example.com/v2/users

# Or in header
GET /users
Accept: application/vnd.example.v1+json
```

**Lesson:** Always version your APIs from the start.

---

### 3. Returning Arrays as Top-Level Response

**Mistake:**
```json
[
  {"id": 1, "name": "Alice"},
  {"id": 2, "name": "Bob"}
]
```

**Why it's wrong:**
- Can't add metadata (pagination, total count)
- Can't add error information
- Security risk (JSON hijacking in old browsers)

**Correct:**
```json
{
  "data": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ],
  "total": 2,
  "page": 1,
  "per_page": 10
}
```

**Lesson:** Wrap arrays in an object to allow future extensions.

---

### 4. Inconsistent Naming Conventions

**Mistake:**
```json
{
  "user_name": "Alice",
  "userEmail": "alice@example.com",
  "UserAge": 25,
  "USER_ID": 123
}
```

**Why it's wrong:**
- Confusing for API consumers
- Hard to parse consistently
- Looks unprofessional

**Correct (choose one and stick to it):**
```json
// snake_case
{
  "user_name": "Alice",
  "user_email": "alice@example.com",
  "user_age": 25,
  "user_id": 123
}

// camelCase (more common in JSON)
{
  "userName": "Alice",
  "userEmail": "alice@example.com",
  "userAge": 25,
  "userId": 123
}
```

**Lesson:** Pick one naming convention and use it consistently.

---

## Error Handling Mistakes

### 5. Poor Error Responses

**Mistake:**
```json
{
  "error": "Error occurred"
}
```

**Why it's wrong:**
- No error code
- No helpful details
- Hard to debug

**Correct:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email address",
    "field": "email",
    "timestamp": "2023-12-19T10:30:00Z"
  }
}
```

**Lesson:** Provide detailed, actionable error information.

---

### 6. Not Using Proper Status Codes

**Mistake:**
```python
# Returning 200 for everything
return {"error": "Not found"}, 200
return {"status": "success"}, 200
```

**Why it's wrong:**
- Clients can't handle errors properly
- Breaks HTTP semantics
- Confusing for debugging

**Correct:**
```python
# Use appropriate status codes
return {"error": "Not found"}, 404
return {"error": "Unauthorized"}, 401
return {"error": "Bad request"}, 400
return {"data": user}, 200
return {"data": new_user}, 201  # Created
```

**Lesson:** Status codes are meaningful. Use them correctly.

---

## Authentication Mistakes

### 7. Storing Passwords in Plain Text

**Mistake:**
```python
users_db = {
    "alice": {"password": "password123"}  # Plain text!
}
```

**Why it's wrong:**
- Massive security vulnerability
- If database is compromised, all passwords exposed
- Legal and regulatory issues

**Correct:**
```python
from werkzeug.security import generate_password_hash, check_password_hash

users_db = {
    "alice": {
        "password_hash": generate_password_hash("password123")
    }
}

# Verify password
check_password_hash(users_db["alice"]["password_hash"], entered_password)
```

**Lesson:** Always hash passwords. Never store them in plain text.

---

### 8. Not Protecting API Endpoints

**Mistake:**
```python
@app.route('/users/<id>/delete')
def delete_user(id):
    # Anyone can delete any user!
    delete_from_db(id)
```

**Why it's wrong:**
- No authentication check
- No authorization check
- Security disaster

**Correct:**
```python
@app.route('/users/<id>', methods=['DELETE'])
@require_authentication
def delete_user(id):
    current_user = get_current_user()
    
    # Check if user can delete (authorization)
    if not current_user.is_admin and current_user.id != id:
        return {"error": "Unauthorized"}, 403
    
    delete_from_db(id)
    return {"message": "User deleted"}, 200
```

**Lesson:** Always implement authentication and authorization.

---

## Request/Response Mistakes

### 9. Not Implementing Pagination

**Mistake:**
```python
@app.route('/users')
def get_users():
    # Returns ALL users, even millions!
    return jsonify(User.query.all())
```

**Why it's wrong:**
- Massive response sizes
- Slow performance
- Memory issues
- Poor user experience

**Correct:**
```python
@app.route('/users')
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    users = User.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'data': [u.to_dict() for u in users.items],
        'page': page,
        'per_page': per_page,
        'total': users.total,
        'pages': users.pages
    })
```

**Lesson:** Always paginate large datasets.

---

### 10. Not Supporting Filtering/Sorting

**Mistake:**
```python
# No way to filter or sort
GET /users  # Returns all users in random order
```

**Why it's wrong:**
- Clients have to filter/sort client-side
- Wasteful data transfer
- Poor API design

**Correct:**
```python
# Support query parameters
GET /users?role=admin&sort=created_at&order=desc
GET /users?search=alice&limit=10

@app.route('/users')
def get_users():
    role = request.args.get('role')
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    
    query = User.query
    
    if role:
        query = query.filter_by(role=role)
    
    if order == 'desc':
        query = query.order_by(desc(getattr(User, sort_by)))
    else:
        query = query.order_by(asc(getattr(User, sort_by)))
    
    return jsonify([u.to_dict() for u in query.all()])
```

**Lesson:** Support filtering, sorting, and searching.

---

## Best Practices

### ✅ Do's
1. **Use RESTful conventions** (nouns, HTTP methods)
2. **Version your API** from the start
3. **Return meaningful errors** with proper status codes
4. **Implement pagination** for lists
5. **Support filtering/sorting**
6. **Hash passwords** and secure sensitive data
7. **Use consistent naming** conventions
8. **Document your API** (OpenAPI/Swagger)

### ❌ Don'ts
1. **Don't use verbs in URLs**
2. **Don't return 200 for errors**
3. **Don't expose internal structure**
4. **Don't store plain text passwords**
5. **Don't skip authentication/authorization**
6. **Don't return all data without pagination**
7. **Don't break backwards compatibility**
8. **Don't trust user input**

---

## Quick Reference

| Mistake | Impact | Solution |
|---------|--------|----------|
| Non-RESTful URLs | Confusing API | Use nouns + HTTP methods |
| No versioning | Breaking changes | Add version to URL/header |
| Array responses | No metadata | Wrap in object |
| Poor errors | Hard to debug | Detailed error objects |
| No auth | Security risk | Implement auth/authz |
| No pagination | Performance issues | Implement pagination |

**Next:** Review [REST APIs README](./README.md) and complete [exercises](./exercises.md).
