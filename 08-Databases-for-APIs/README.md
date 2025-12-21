# 🗄️ Databases for APIs

Learn how APIs connect to databases to store and retrieve persistent data.

## 🎯 Learning Objectives

By the end of this module, you will:
- Understand why APIs need databases
- Learn the basics of SQL vs NoSQL databases
- Connect APIs to databases
- Implement CRUD operations with persistence
- Understand database design for APIs

## Why APIs Need Databases 💾

Without a database, your API data disappears when the server restarts!

**Problem**: In-memory storage
```python
# This data is lost when server restarts
users = []

@app.route('/users', methods=['POST'])
def create_user():
    users.append(request.json)  # Lost on restart!
```

**Solution**: Database storage
```python
# This data persists
@app.route('/users', methods=['POST'])
def create_user():
    db.users.insert_one(request.json)  # Saved to disk!
```

## SQL vs NoSQL Basics 🤔

### SQL (Relational) Databases

**Examples**: PostgreSQL, MySQL, SQLite

**Structure**: Tables with rows and columns
```
Users Table:
+----+----------+-------------------+
| id | username | email             |
+----+----------+-------------------+
|  1 | john     | john@example.com  |
|  2 | jane     | jane@example.com  |
+----+----------+-------------------+
```

**When to use**:
- Structured data with relationships
- Need ACID transactions
- Complex queries and joins

### NoSQL Databases

**Examples**: MongoDB, Redis, DynamoDB

**Structure**: Documents (JSON-like)
```javascript
{
  "_id": "507f1f77bcf86cd799439011",
  "username": "john",
  "email": "john@example.com",
  "posts": [...]
}
```

**When to use**:
- Flexible schema
- Rapid development
- Horizontal scaling

## Connecting APIs to Databases 🔌

### Example: Flask + SQLite (SQL)

```python
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row  # Return dict-like rows
    return conn

# Create table
def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL
            )
        ''')

init_db()

# CREATE
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    try:
        with get_db() as db:
            cursor = db.execute(
                'INSERT INTO users (username, email) VALUES (?, ?)',
                (data['username'], data['email'])
            )
            db.commit()
            return jsonify({'id': cursor.lastrowid}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400

# READ (all)
@app.route('/users')
def get_users():
    with get_db() as db:
        users = db.execute('SELECT * FROM users').fetchall()
        return jsonify([dict(user) for user in users])

# READ (one)
@app.route('/users/<int:user_id>')
def get_user(user_id):
    with get_db() as db:
        user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        if user:
            return jsonify(dict(user))
        return jsonify({'error': 'User not found'}), 404

# UPDATE
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    with get_db() as db:
        db.execute(
            'UPDATE users SET username = ?, email = ? WHERE id = ?',
            (data['username'], data['email'], user_id)
        )
        db.commit()
        if db.total_changes == 0:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'message': 'Updated'})

# DELETE
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    with get_db() as db:
        db.execute('DELETE FROM users WHERE id = ?', (user_id,))
        db.commit()
        if db.total_changes == 0:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'message': 'Deleted'})
```

### Example: Flask + MongoDB (NoSQL)

```python
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['myapp']
users_collection = db['users']

# CREATE
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    result = users_collection.insert_one(data)
    return jsonify({'id': str(result.inserted_id)}), 201

# READ (all)
@app.route('/users')
def get_users():
    users = list(users_collection.find())
    # Convert ObjectId to string for JSON serialization
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users)

# READ (one)
@app.route('/users/<user_id>')
def get_user(user_id):
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

# UPDATE
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    result = users_collection.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': data}
    )
    if result.matched_count == 0:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'Updated'})

# DELETE
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = users_collection.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'Deleted'})
```

## CRUD Operations with Persistence ✍️

**CRUD** = Create, Read, Update, Delete

| Operation | HTTP Method | SQL | MongoDB |
|-----------|-------------|-----|---------|
| Create | POST | INSERT | insert_one() |
| Read | GET | SELECT | find() |
| Update | PUT/PATCH | UPDATE | update_one() |
| Delete | DELETE | DELETE | delete_one() |

## Database Design for APIs 📐

### Best Practices

1. **Use appropriate data types**
   ```sql
   CREATE TABLE posts (
       id INTEGER PRIMARY KEY,
       title TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   )
   ```

2. **Create indexes for frequently queried fields**
   ```sql
   CREATE INDEX idx_username ON users(username);
   ```

3. **Validate data before inserting**
   ```python
   if not data.get('email') or '@' not in data['email']:
       return jsonify({'error': 'Invalid email'}), 400
   ```

4. **Handle database errors gracefully**
   ```python
   try:
       db.execute(...)
   except sqlite3.IntegrityError:
       return jsonify({'error': 'Duplicate entry'}), 400
   ```

5. **Use transactions for multiple operations**
   ```python
   with db:  # Automatic transaction
       db.execute('INSERT INTO ...')
       db.execute('UPDATE ...')
       # Both succeed or both roll back
   ```

## Summary and Key Takeaways

✅ APIs need databases for **persistent storage**  
✅ **SQL** databases are great for structured, relational data  
✅ **NoSQL** databases offer flexibility and easier scaling  
✅ Implement **CRUD operations** to manipulate data  
✅ **Validate input** before saving to database  
✅ **Handle errors** properly for better user experience

## What's Next?

Now that you can store data, you need to learn about **API Security** to protect it!

---

[← Back: REST API Design](../07-REST-API-Design/) | [Next: API Security →](../09-API-Security/)

## Practice

Complete the exercises in [exercises.md](./exercises.md) to build database-backed APIs!
