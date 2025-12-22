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

### The Data Persistence Problem

Without a database, your API faces critical limitations:

**❌ Without a Database:**
- **Data disappears when server restarts** - All data stored in memory is lost
- **Can't handle multiple users** - No concurrent access control
- **No data backup** - Data loss is permanent
- **Can't scale** - Limited by server memory

**✅ With a Database:**
- **Persistent storage** - Data survives server restarts
- **Concurrent access** - Multiple users can read/write simultaneously
- **Backup and recovery** - Protect against data loss
- **Scalable** - Handle millions of records efficiently

### Example Comparison

**Problem**: In-memory storage
```python
# This data is lost when server restarts
users = []

@app.route('/users', methods=['POST'])
def create_user():
    users.append(request.json)  # Lost on restart!
    return jsonify({"id": len(users)}), 201
```

**Solution**: Database storage
```python
# This data persists
@app.route('/users', methods=['POST'])
def create_user():
    result = db.users.insert_one(request.json)  # Saved to disk!
    return jsonify({"id": str(result.inserted_id)}), 201
```

### API-Database Architecture Diagram

Here's a visual representation of how APIs interact with databases:

```
API-Database Architecture:

┌──────────┐
│  Client  │
└────┬─────┘
     │ HTTP Request
     ▼
┌─────────────┐     ┌──────────────┐
│   API       │────>│   Database   │
│  (Flask)    │<────│  (SQLite)    │
└─────────────┘     └──────────────┘
     │ SQL Query         │ Result
     │                   │
     │ HTTP Response     │
     ▼                   │
┌──────────┐            │
│  Client  │            │
└──────────┘            │

Request Flow:
1. Client sends POST /api/tasks {"title": "Learn"}
2. API validates input
3. API executes: INSERT INTO tasks...
4. Database stores data, returns ID
5. API responds: {"id": 1, "title": "Learn"}
```

**Architecture Components:**

- **Client**: Web browser, mobile app, or any HTTP client
  - Sends HTTP requests to the API
  - Receives HTTP responses with data

- **API Server**: Application layer (Flask, Django, Node.js)
  - Receives and validates client requests
  - Translates HTTP requests to database queries
  - Processes database results
  - Sends formatted responses to clients

- **Database**: Data storage layer (SQLite, PostgreSQL, MongoDB)
  - Stores persistent data
  - Executes queries (SELECT, INSERT, UPDATE, DELETE)
  - Returns results to API

**Data Flow Example:**
1. Client wants to create a task
2. Sends POST request with task data
3. API validates the data
4. API constructs SQL INSERT query
5. Database saves the task and returns new ID
6. API formats response with task details
7. Client receives confirmation

## Database Basics 📚

### What is a Database?

A **database** is an organized collection of structured data stored electronically. Think of it as a smart filing system that can quickly find, update, and manage your data.

### Key Database Concepts

#### Tables, Rows, and Columns

In SQL databases, data is organized into tables (similar to spreadsheets):

```
Users Table:
┌────┬──────────┬──────────────────┬────────────┐
│ id │ username │ email            │ created_at │
├────┼──────────┼──────────────────┼────────────┤
│  1 │ john     │ john@example.com │ 2024-01-15 │
│  2 │ jane     │ jane@example.com │ 2024-01-16 │
│  3 │ bob      │ bob@example.com  │ 2024-01-17 │
└────┴──────────┴──────────────────┴────────────┘

- Table: Users (the entire structure)
- Columns: id, username, email, created_at (fields)
- Rows: Each user is one row (record)
```

#### Primary Keys

A **primary key** is a unique identifier for each row in a table:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,  -- Unique identifier
    username TEXT UNIQUE,
    email TEXT
);
```

- Must be unique for each row
- Cannot be NULL
- Used to reference rows from other tables

#### Relationships

**One-to-Many Relationship**: One user can have many posts

```
Users Table:                Posts Table:
┌────┬──────────┐          ┌────┬─────────┬────────────┐
│ id │ username │          │ id │ user_id │ title      │
├────┼──────────┤          ├────┼─────────┼────────────┤
│  1 │ john     │◄─────────│  1 │    1    │ My Post    │
│  2 │ jane     │          │  2 │    1    │ Another    │
└────┴──────────┘          │  3 │    2    │ Jane's Post│
                           └────┴─────────┴────────────┘
```

**Many-to-Many Relationship**: Many users can like many posts

```
Users Table:           Likes Table:         Posts Table:
┌────┬──────┐         ┌─────────┬─────────┐  ┌────┬───────┐
│ id │ name │         │ user_id │ post_id │  │ id │ title │
├────┼──────┤         ├─────────┼─────────┤  ├────┼───────┤
│  1 │ john │◄────────│    1    │    1    │──│  1 │ Post1 │
│  2 │ jane │         │    1    │    2    │  │  2 │ Post2 │
└────┴──────┘         │    2    │    1    │──┘
                      └─────────┴─────────┘
```

## SQL Databases 🗃️

### When to Use SQL Databases

**Best for:**
- ✅ **Structured data** with clear relationships
- ✅ **Complex queries** requiring JOINs
- ✅ **ACID transactions** (Atomicity, Consistency, Isolation, Durability)
- ✅ **Data integrity** is critical
- ✅ **Well-defined schema** that doesn't change often

**Examples**: PostgreSQL, MySQL, SQLite

### SQLite for Learning

**SQLite** is perfect for learning because:
- ✅ No setup needed - built into Python
- ✅ Serverless - just a file on disk
- ✅ Full SQL support
- ✅ Great for development and small projects

### Basic SQL Commands

#### SELECT - Read Data

```sql
-- Get all users
SELECT * FROM users;

-- Get specific columns
SELECT username, email FROM users;

-- Get one user by ID
SELECT * FROM users WHERE id = 1;

-- Search by pattern
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- Sort results
SELECT * FROM users ORDER BY created_at DESC;

-- Limit results
SELECT * FROM users LIMIT 10;

-- Combine conditions
SELECT * FROM users 
WHERE created_at > '2024-01-01' 
ORDER BY username 
LIMIT 5;
```

#### INSERT - Create Data

```sql
-- Insert a single user
INSERT INTO users (username, email) 
VALUES ('john', 'john@example.com');

-- Insert multiple users
INSERT INTO users (username, email) VALUES 
    ('jane', 'jane@example.com'),
    ('bob', 'bob@example.com');
```

#### UPDATE - Modify Data

```sql
-- Update one user
UPDATE users 
SET email = 'newemail@example.com' 
WHERE id = 1;

-- Update multiple fields
UPDATE users 
SET username = 'johndoe', email = 'john.doe@example.com' 
WHERE id = 1;

-- Update with condition
UPDATE users 
SET verified = 1 
WHERE email LIKE '%@company.com';
```

#### DELETE - Remove Data

```sql
-- Delete one user
DELETE FROM users WHERE id = 1;

-- Delete multiple users
DELETE FROM users WHERE created_at < '2023-01-01';

-- Delete all (careful!)
DELETE FROM users;
```

### Hands-On SQLite Exercise

Create a simple database and practice SQL commands:

```python
import sqlite3

# Connect to database (creates if doesn't exist)
conn = sqlite3.connect('practice.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER,
        rating REAL
    )
''')

# Insert data
cursor.execute('''
    INSERT INTO books (title, author, year, rating) VALUES 
    ('1984', 'George Orwell', 1949, 4.5),
    ('To Kill a Mockingbird', 'Harper Lee', 1960, 4.8),
    ('The Great Gatsby', 'F. Scott Fitzgerald', 1925, 4.2)
''')
conn.commit()

# Query data
cursor.execute('SELECT * FROM books WHERE rating > 4.3')
for row in cursor.fetchall():
    print(row)

# Update data
cursor.execute('UPDATE books SET rating = 5.0 WHERE title = "1984"')
conn.commit()

# Delete data
cursor.execute('DELETE FROM books WHERE year < 1950')
conn.commit()

conn.close()
```

## NoSQL Databases 📄

### When to Use NoSQL Databases

**Best for:**
- ✅ **Flexible schema** - structure can change
- ✅ **Horizontal scaling** - distribute across many servers
- ✅ **Document-based data** - JSON-like structures
- ✅ **Rapid development** - no schema migrations
- ✅ **Hierarchical data** - nested structures

**Examples**: MongoDB, Redis, DynamoDB, Cassandra

### Brief Introduction to MongoDB

MongoDB stores data as **JSON-like documents**:

```javascript
// A user document in MongoDB
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "username": "john",
  "email": "john@example.com",
  "profile": {
    "age": 30,
    "city": "New York"
  },
  "posts": [
    {
      "title": "My First Post",
      "date": "2024-01-15"
    }
  ],
  "tags": ["developer", "python", "api"]
}
```

**Key Features:**
- Flexible structure - each document can be different
- Nested data - objects within objects
- Arrays of data built-in
- No need to define schema upfront

### When NOT to Use NoSQL

**Avoid NoSQL when:**
- ❌ You need complex JOINs across multiple tables
- ❌ You need strong ACID transactions
- ❌ Your data is highly relational
- ❌ You need complex aggregations
- ❌ Data integrity is absolutely critical

**Example**: A banking system should use SQL, not NoSQL, because:
- Account balances must be exact (ACID transactions)
- Relationships between accounts, transactions, users are complex
- Data integrity is paramount

## Connecting APIs to Databases 🔌

### Python Example with SQLite

Here's a complete example showing how to connect a Flask API to SQLite:

```python
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_db_connection():
    """Create a database connection with Row factory for dict-like access"""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Return dict-like rows
    return conn

def init_db():
    """Initialize the database with tables"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database when app starts
init_db()

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return jsonify([dict(row) for row in users])

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user"""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(dict(user))

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.json
    
    # Validate input
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400
    
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            'INSERT INTO users (name, email) VALUES (?, ?)',
            (data['name'], data['email'])
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return jsonify({"message": "User created", "id": user_id}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Email already exists"}), 400

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user"""
    data = request.json
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400
    
    conn = get_db_connection()
    try:
        conn.execute(
            'UPDATE users SET name = ?, email = ? WHERE id = ?',
            (data['name'], data['email'], user_id)
        )
        conn.commit()
        
        if conn.total_changes == 0:
            conn.close()
            return jsonify({"error": "User not found"}), 404
            
        conn.close()
        return jsonify({"message": "User updated"})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Email already exists"}), 400

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    
    if conn.total_changes == 0:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    conn.close()
    return jsonify({"message": "User deleted"})

if __name__ == '__main__':
    app.run(debug=True)
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

## CRUD Operations with Database 📝

**CRUD** = Create, Read, Update, Delete - the four basic operations for persistent data.

| Operation | HTTP Method | SQL Command | MongoDB Method |
|-----------|-------------|-------------|----------------|
| Create    | POST        | INSERT      | insert_one()   |
| Read      | GET         | SELECT      | find()         |
| Update    | PUT/PATCH   | UPDATE      | update_one()   |
| Delete    | DELETE      | DELETE      | delete_one()   |

### Complete CRUD Examples with Best Practices

#### CREATE - With Validation and Error Handling

```python
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    
    # 1. Input Validation
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
    
    # Validate email format
    if '@' not in data['email']:
        return jsonify({"error": "Invalid email format"}), 400
    
    # 2. Sanitize input (prevent injection)
    name = data['name'].strip()
    email = data['email'].strip().lower()
    
    # 3. Database operation with error handling
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            'INSERT INTO users (name, email) VALUES (?, ?)',
            (name, email)  # Using parameterized queries prevents SQL injection
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            "message": "User created successfully",
            "id": user_id
        }), 201
        
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Email already exists"}), 409

#### READ - With Filtering and Pagination

```python
@app.route('/api/users', methods=['GET'])
def get_users():
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    
    # Calculate offset
    offset = (page - 1) * per_page
    
    conn = get_db_connection()
    
    # Build query with search
    # Note: LIKE with leading wildcards ('%search%') can't use indexes efficiently.
    # For large datasets, consider using full-text search (FTS) for better performance.
    if search:
        query = '''
            SELECT * FROM users 
            WHERE name LIKE ? OR email LIKE ?
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        '''
        search_term = f'%{search}%'
        users = conn.execute(query, (search_term, search_term, per_page, offset)).fetchall()
    else:
        query = 'SELECT * FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?'
        users = conn.execute(query, (per_page, offset)).fetchall()
    
    # Get total count
    total = conn.execute('SELECT COUNT(*) as count FROM users').fetchone()['count']
    conn.close()
    
    return jsonify({
        "users": [dict(row) for row in users],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page
        }
    })

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Validate ID
    if user_id <= 0:
        return jsonify({"error": "Invalid user ID"}), 400
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(dict(user))
```

#### UPDATE - Partial Updates with PATCH

```python
@app.route('/api/users/<int:user_id>', methods=['PATCH'])
def update_user_partial(user_id):
    """Update only provided fields"""
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Build dynamic UPDATE query
    allowed_fields = ['name', 'email']
    updates = []
    values = []
    
    for field in allowed_fields:
        if field in data:
            updates.append(f"{field} = ?")
            values.append(data[field])
    
    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400
    
    # Add user_id to values
    values.append(user_id)
    
    query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
    
    conn = get_db_connection()
    try:
        conn.execute(query, values)
        conn.commit()
        
        if conn.total_changes == 0:
            conn.close()
            return jsonify({"error": "User not found"}), 404
        
        conn.close()
        return jsonify({"message": "User updated successfully"})
        
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Email already exists"}), 409
```

#### DELETE - With Soft Delete Option

```python
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Hard delete a user"""
    if user_id <= 0:
        return jsonify({"error": "Invalid user ID"}), 400
    
    conn = get_db_connection()
    
    # Check if user exists first
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user is None:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    # Delete the user
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User deleted successfully"}), 200

# Alternative: Soft delete (mark as deleted instead of removing)
@app.route('/api/users/<int:user_id>/archive', methods=['POST'])
def archive_user(user_id):
    """Soft delete - mark as deleted but keep data"""
    conn = get_db_connection()
    conn.execute(
        'UPDATE users SET deleted_at = CURRENT_TIMESTAMP WHERE id = ?',
        (user_id,)
    )
    conn.commit()
    
    if conn.total_changes == 0:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    conn.close()
    return jsonify({"message": "User archived"})
```

### SQL Injection Prevention

**❌ NEVER DO THIS** (vulnerable to SQL injection):

```python
# DANGEROUS - DO NOT USE
@app.route('/users/<username>')
def get_user_bad(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"  # VULNERABLE!
    # An attacker could pass: admin' OR '1'='1
    # Resulting query: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
    # This returns ALL users!
```

**✅ ALWAYS DO THIS** (safe with parameterized queries):

```python
# SAFE - Use parameterized queries
@app.route('/users/<username>')
def get_user_safe(username):
    query = "SELECT * FROM users WHERE username = ?"
    user = conn.execute(query, (username,)).fetchone()  # Safe!
    # The database driver handles escaping automatically
```

### Input Validation Best Practices

```python
def validate_user_input(data):
    """Comprehensive input validation"""
    errors = []
    
    # Check required fields
    if 'name' not in data:
        errors.append("Name is required")
    elif len(data['name']) < 2:
        errors.append("Name must be at least 2 characters")
    elif len(data['name']) > 100:
        errors.append("Name must be less than 100 characters")
    
    # Validate email
    if 'email' not in data:
        errors.append("Email is required")
    elif '@' not in data['email'] or '.' not in data['email']:
        errors.append("Invalid email format")
    
    return errors

@app.route('/api/users', methods=['POST'])
def create_user_validated():
    data = request.json
    
    # Validate input
    errors = validate_user_input(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Proceed with creation...
```

## Database Design Basics 📐

### Designing Tables

Good table design is crucial for a maintainable database.

#### Basic Principles

1. **Each table should represent one entity**
   ```sql
   -- Good: Separate tables for separate entities
   CREATE TABLE users (...)
   CREATE TABLE posts (...)
   CREATE TABLE comments (...)
   
   -- Bad: Mixing entities
   CREATE TABLE user_posts_comments (...)
   ```

2. **Use appropriate data types**
   ```sql
   CREATE TABLE products (
       id INTEGER PRIMARY KEY,
       name TEXT NOT NULL,              -- Text for strings
       price REAL NOT NULL,              -- Real for decimals
       stock INTEGER DEFAULT 0,          -- Integer for whole numbers
       created_at TIMESTAMP,             -- Timestamp for dates
       is_active BOOLEAN DEFAULT 1       -- Boolean for true/false
   );
   ```

3. **Define constraints**
   ```sql
   CREATE TABLE users (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       email TEXT UNIQUE NOT NULL,           -- Must be unique and present
       age INTEGER CHECK(age >= 18),         -- Must be 18 or older
       status TEXT DEFAULT 'active',         -- Default value
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

#### Example: E-commerce Database Design

```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL CHECK(price >= 0),
    stock INTEGER DEFAULT 0 CHECK(stock >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total REAL NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Order items table (many-to-many relationship)
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### Normalization (Simplified)

**Normalization** is organizing data to reduce redundancy.

#### ❌ Bad Design (Unnormalized)

```sql
-- Lots of repeated data
CREATE TABLE orders (
    id INTEGER,
    customer_name TEXT,
    customer_email TEXT,
    customer_address TEXT,  -- Repeated for each order
    product_name TEXT,
    product_price REAL
);
```

Problems:
- Customer info repeated in every order
- Hard to update customer details
- Wastes storage space

#### ✅ Good Design (Normalized)

```sql
-- Separate tables, no repetition
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    address TEXT
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

Benefits:
- Each piece of data stored once
- Easy to update customer/product info
- More efficient storage

### Indexes

**Indexes** speed up queries by creating a lookup structure.

#### When to Create Indexes

Create indexes for columns that are:
- ✅ Frequently used in WHERE clauses
- ✅ Used for JOINs
- ✅ Used for sorting (ORDER BY)

```sql
-- Create index on frequently searched column
CREATE INDEX idx_users_email ON users(email);

-- Create index on foreign key
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- Composite index for multiple columns
CREATE INDEX idx_posts_user_date ON posts(user_id, created_at);
```

#### Performance Example

```sql
-- Without index: Scans entire table
SELECT * FROM users WHERE email = 'john@example.com';  -- Slow on large tables

-- With index on email: Direct lookup
CREATE INDEX idx_users_email ON users(email);
SELECT * FROM users WHERE email = 'john@example.com';  -- Fast!
```

⚠️ **Don't over-index**: Too many indexes slow down INSERT, UPDATE, DELETE operations.

### Common Database Patterns

#### 1. Timestamps Pattern

Always track when records are created and modified:

```sql
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger to update updated_at automatically
CREATE TRIGGER update_posts_timestamp 
AFTER UPDATE ON posts
BEGIN
    UPDATE posts SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
```

#### 2. Soft Delete Pattern

Mark records as deleted instead of removing them:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT,
    deleted_at TIMESTAMP NULL  -- NULL means not deleted
);

-- Soft delete
UPDATE users SET deleted_at = CURRENT_TIMESTAMP WHERE id = 1;

-- Query only active users
SELECT * FROM users WHERE deleted_at IS NULL;
```

#### 3. Status/State Pattern

Track the state of records:

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    status TEXT DEFAULT 'pending'  -- pending, processing, shipped, delivered
);

-- Update status
UPDATE orders SET status = 'shipped' WHERE id = 123;
```

#### 4. Audit Trail Pattern

Keep history of all changes:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT,
    name TEXT
);

CREATE TABLE users_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,  -- INSERT, UPDATE, DELETE
    old_value TEXT,
    new_value TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by INTEGER
);
```

#### 5. One-to-Many Pattern

```sql
-- One user can have many posts
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Get user with all their posts
SELECT users.name, posts.title
FROM users
LEFT JOIN posts ON users.id = posts.user_id
WHERE users.id = 1;
```

#### 6. Many-to-Many Pattern

```sql
-- Many students can enroll in many courses
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    title TEXT
);

-- Junction table
CREATE TABLE enrollments (
    student_id INTEGER,
    course_id INTEGER,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
```

## Summary and Key Takeaways

✅ **APIs need databases** for persistent storage, concurrent access, and scalability  
✅ **Database basics**: Tables store data in rows and columns with primary keys for unique identification  
✅ **SQL databases** are best for structured, relational data with complex queries  
✅ **NoSQL databases** offer flexibility and easier horizontal scaling  
✅ **SQLite** is perfect for learning - no setup required, full SQL support  
✅ **Basic SQL commands**: SELECT, INSERT, UPDATE, DELETE with WHERE, ORDER BY, LIMIT  
✅ **CRUD operations** map to HTTP methods: POST/GET/PUT/DELETE  
✅ **Always validate input** before saving to database  
✅ **Prevent SQL injection** using parameterized queries (never string concatenation)  
✅ **Handle errors properly** for better user experience  
✅ **Design tables** with appropriate data types and constraints  
✅ **Normalize data** to reduce redundancy  
✅ **Create indexes** on frequently queried columns for performance  
✅ **Use common patterns**: timestamps, soft deletes, audit trails

## What's Next?

Now that you can store data, you need to learn about **API Security** to protect it!

---

[← Back: REST API Design](../07-REST-API-Design/) | [Next: API Security →](../09-API-Security/)

## Practice

Complete the exercises in [exercises.md](./exercises.md) to build database-backed APIs!
