# 🏋️ Exercises: Databases for APIs

Practice building database-backed APIs with these hands-on exercises.

## Exercise 1: SQLite Basics 📚

**Objective**: Learn basic SQL commands with SQLite.

**Tasks**:

1. Create a database and table:

```python
import sqlite3

# Connect to database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create books table
cursor.execute('''
    CREATE TABLE books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER,
        isbn TEXT UNIQUE
    )
''')
conn.commit()
```

2. Insert some books:

```python
books = [
    ('1984', 'George Orwell', 1949, '978-0451524935'),
    ('To Kill a Mockingbird', 'Harper Lee', 1960, '978-0061120084'),
    ('The Great Gatsby', 'F. Scott Fitzgerald', 1925, '978-0743273565'),
    ('Pride and Prejudice', 'Jane Austen', 1813, '978-0141439518')
]

cursor.executemany('INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)', books)
conn.commit()
```

3. Practice SELECT queries:

```python
# Get all books
cursor.execute('SELECT * FROM books')
print(cursor.fetchall())

# Get books by specific author
cursor.execute('SELECT * FROM books WHERE author = ?', ('George Orwell',))
print(cursor.fetchall())

# Get books published after 1900
cursor.execute('SELECT * FROM books WHERE year > 1900 ORDER BY year DESC')
print(cursor.fetchall())

# Get only title and author
cursor.execute('SELECT title, author FROM books LIMIT 2')
print(cursor.fetchall())
```

4. Practice UPDATE:

```python
# Update a book's year
cursor.execute('UPDATE books SET year = 1950 WHERE title = "1984"')
conn.commit()
```

5. Practice DELETE:

```python
# Delete a book
cursor.execute('DELETE FROM books WHERE isbn = "978-0743273565"')
conn.commit()

conn.close()
```

**Success Criteria**: 
- You can create tables
- You can insert, select, update, and delete data
- You understand parameterized queries

---

## Exercise 2: Simple Flask API with SQLite 🔌

**Objective**: Build a basic API connected to a database.

**Task**: Create a books API with GET and POST endpoints.

```python
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/books', methods=['GET'])
def get_books():
    conn = get_db()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return jsonify([dict(book) for book in books])

@app.route('/api/books', methods=['POST'])
def create_book():
    data = request.json
    conn = get_db()
    cursor = conn.execute(
        'INSERT INTO books (title, author, year) VALUES (?, ?, ?)',
        (data['title'], data['author'], data.get('year'))
    )
    conn.commit()
    book_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": book_id, "message": "Book created"}), 201

if __name__ == '__main__':
    app.run(debug=True)
```

**Test it**:

```bash
# Start the server
python app.py

# In another terminal, test the API
curl http://localhost:5000/api/books

curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -d '{"title": "1984", "author": "George Orwell", "year": 1949}'
```

**Success Criteria**: 
- API can fetch all books
- API can create new books
- Data persists after server restart

---

## Exercise 3: Complete CRUD Operations ✍️

**Objective**: Implement all CRUD operations with error handling.

**Task**: Extend the books API with UPDATE and DELETE endpoints.

```python
@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = get_db()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(dict(book))

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    conn = get_db()
    conn.execute(
        'UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?',
        (data['title'], data['author'], data.get('year'), book_id)
    )
    conn.commit()
    
    if conn.total_changes == 0:
        conn.close()
        return jsonify({"error": "Book not found"}), 404
    
    conn.close()
    return jsonify({"message": "Book updated"})

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = get_db()
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    
    if conn.total_changes == 0:
        conn.close()
        return jsonify({"error": "Book not found"}), 404
    
    conn.close()
    return jsonify({"message": "Book deleted"})
```

**Test all operations**:

```bash
# Get specific book
curl http://localhost:5000/api/books/1

# Update book
curl -X PUT http://localhost:5000/api/books/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "1984 (Updated)", "author": "George Orwell", "year": 1949}'

# Delete book
curl -X DELETE http://localhost:5000/api/books/1
```

**Success Criteria**: 
- All CRUD operations work
- Proper error handling for not found
- Status codes are correct

---

## Exercise 4: Input Validation 🛡️

**Objective**: Add proper validation and error handling.

**Task**: Enhance the API with validation.

```python
def validate_book_data(data):
    """Validate book input data"""
    errors = []
    
    if not data:
        return ["No data provided"]
    
    if 'title' not in data or not data['title'].strip():
        errors.append("Title is required")
    elif len(data['title']) > 200:
        errors.append("Title must be less than 200 characters")
    
    if 'author' not in data or not data['author'].strip():
        errors.append("Author is required")
    elif len(data['author']) > 100:
        errors.append("Author must be less than 100 characters")
    
    if 'year' in data:
        try:
            year = int(data['year'])
            if year < 1000 or year > 2100:
                errors.append("Year must be between 1000 and 2100")
        except (ValueError, TypeError):
            errors.append("Year must be a number")
    
    return errors

@app.route('/api/books', methods=['POST'])
def create_book_validated():
    data = request.json
    
    # Validate input
    errors = validate_book_data(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Sanitize input
    title = data['title'].strip()
    author = data['author'].strip()
    year = data.get('year')
    
    conn = get_db()
    try:
        cursor = conn.execute(
            'INSERT INTO books (title, author, year) VALUES (?, ?, ?)',
            (title, author, year)
        )
        conn.commit()
        book_id = cursor.lastrowid
        conn.close()
        return jsonify({"id": book_id, "message": "Book created"}), 201
    except sqlite3.IntegrityError as e:
        conn.close()
        return jsonify({"error": str(e)}), 409
```

**Test validation**:

```bash
# Test missing title
curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -d '{"author": "Test Author"}'

# Test invalid year
curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "author": "Author", "year": 3000}'
```

**Success Criteria**: 
- Validation catches invalid data
- Helpful error messages returned
- Database stays clean

---

## Exercise 5: Database Design - Blog System 📝

**Objective**: Design a normalized database for a blog.

**Task**: Create tables for a blog with users, posts, and comments.

```python
def init_blog_db():
    conn = sqlite3.connect('blog.db')
    
    # Users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Posts table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Comments table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Create indexes
    conn.execute('CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id)')
    
    conn.commit()
    conn.close()

init_blog_db()
```

**Success Criteria**: 
- Tables are properly normalized
- Foreign keys establish relationships
- Indexes on frequently queried columns

---

## Exercise 6: Practical Project - Task Manager API 🎯

**Objective**: Build a complete task manager API with full CRUD and tests.

**Requirements**:

1. **Database Schema**:
   - Tasks table with: id, title, description, status, priority, due_date, created_at
   - Status options: "todo", "in_progress", "done"
   - Priority options: "low", "medium", "high"

2. **API Endpoints**:
   - `GET /api/tasks` - Get all tasks (with optional status filter)
   - `GET /api/tasks/<id>` - Get specific task
   - `POST /api/tasks` - Create new task
   - `PUT /api/tasks/<id>` - Update task
   - `PATCH /api/tasks/<id>/status` - Update only status
   - `DELETE /api/tasks/<id>` - Delete task

3. **Features**:
   - Input validation
   - Error handling
   - SQL injection prevention
   - Filtering by status
   - Sorting by priority or due date

**Starter Code**:

```python
from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'todo' CHECK(status IN ('todo', 'in_progress', 'done')),
            priority TEXT DEFAULT 'medium' CHECK(priority IN ('low', 'medium', 'high')),
            due_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# TODO: Implement all endpoints here

if __name__ == '__main__':
    app.run(debug=True)
```

**Testing Script**:

```python
import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_create_task():
    """Test creating a task"""
    task = {
        "title": "Complete Module 08",
        "description": "Finish all database exercises",
        "priority": "high",
        "due_date": "2024-12-31"
    }
    response = requests.post(f'{BASE_URL}/tasks', json=task)
    assert response.status_code == 201
    print("✓ Create task test passed")
    return response.json()['id']

def test_get_all_tasks():
    """Test getting all tasks"""
    response = requests.get(f'{BASE_URL}/tasks')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print("✓ Get all tasks test passed")

def test_get_task(task_id):
    """Test getting a specific task"""
    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200
    assert response.json()['id'] == task_id
    print("✓ Get task test passed")

def test_update_task(task_id):
    """Test updating a task"""
    update = {
        "title": "Complete Module 08 - Updated",
        "status": "in_progress"
    }
    response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=update)
    assert response.status_code == 200
    print("✓ Update task test passed")

def test_delete_task(task_id):
    """Test deleting a task"""
    response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200
    print("✓ Delete task test passed")

def run_all_tests():
    """Run all tests"""
    print("\n🧪 Running Task Manager API Tests\n")
    task_id = test_create_task()
    test_get_all_tasks()
    test_get_task(task_id)
    test_update_task(task_id)
    test_delete_task(task_id)
    print("\n✅ All tests passed!\n")

if __name__ == '__main__':
    run_all_tests()
```

**Success Criteria**:
- All CRUD endpoints implemented
- Input validation works
- All tests pass
- Error handling is comprehensive
- Data persists across server restarts

---

## Exercise 7: Advanced - Notes API with Categories 📓

**Objective**: Build a more complex API with relationships.

**Requirements**:

1. **Database Schema**:
   - Categories table: id, name, color
   - Notes table: id, category_id, title, content, created_at, updated_at
   - One-to-many relationship (category has many notes)

2. **API Endpoints**:
   - Category CRUD operations
   - Notes CRUD operations
   - `GET /api/categories/<id>/notes` - Get all notes in a category
   - Search notes by content

3. **Features**:
   - Cascade delete (deleting category deletes its notes)
   - Full-text search in notes
   - Pagination for notes list

**Challenge**: Implement this without looking at solutions!

**Success Criteria**:
- Foreign key relationships work
- Can fetch notes by category
- Search functionality works
- Proper error handling

---

## Bonus Exercise: SQL Injection Prevention 🔒

**Objective**: Understand SQL injection vulnerabilities.

**Task 1**: Identify the vulnerability

```python
# VULNERABLE CODE - DO NOT USE IN PRODUCTION
@app.route('/api/users/<username>')
def get_user_vulnerable(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return jsonify(cursor.fetchone())
```

**Question**: What happens if someone visits `/api/users/admin' OR '1'='1`?

**Task 2**: Fix the vulnerability

```python
# SAFE CODE
@app.route('/api/users/<username>')
def get_user_safe(username):
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    return jsonify(cursor.fetchone())
```

**Success Criteria**: 
- Understand how SQL injection works
- Always use parameterized queries
- Never concatenate user input into SQL

---

## Additional Resources 📚

- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Database Normalization Guide](https://www.guru99.com/database-normalization.html)
- [MongoDB University](https://university.mongodb.com/)

---

[← Back to Lesson](./README.md)
