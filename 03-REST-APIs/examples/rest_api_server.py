#!/usr/bin/env python3
"""
RESTful API Server Example using Flask

This example demonstrates a complete REST API for managing books.
It implements all CRUD operations and follows REST best practices.

Requirements:
    pip install flask

Usage:
    python rest_api_server.py
    
Then test with curl or the provided client script.
"""

from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory database (in production, use a real database)
books = {}

# Initialize with some sample data
books['1'] = {
    'id': '1',
    'title': 'Python Crash Course',
    'author': 'Eric Matthes',
    'isbn': '978-1593279288',
    'published_year': 2019,
    'created_at': '2024-01-01T12:00:00Z'
}
books['2'] = {
    'id': '2',
    'title': 'Clean Code',
    'author': 'Robert Martin',
    'isbn': '978-0132350884',
    'published_year': 2008,
    'created_at': '2024-01-01T12:00:00Z'
}


@app.route('/', methods=['GET'])
def home():
    """API home page with documentation."""
    return jsonify({
        'message': 'Welcome to Books REST API',
        'version': '1.0',
        'endpoints': {
            'GET /api/books': 'Get all books',
            'GET /api/books/:id': 'Get a specific book',
            'POST /api/books': 'Create a new book',
            'PUT /api/books/:id': 'Update a book (replace)',
            'PATCH /api/books/:id': 'Update a book (partial)',
            'DELETE /api/books/:id': 'Delete a book'
        }
    }), 200


@app.route('/api/books', methods=['GET'])
def get_books():
    """
    GET /api/books
    Retrieve all books with optional filtering and pagination.
    
    Query parameters:
        - author: Filter by author name
        - year: Filter by published year
        - sort: Sort by field (title, author, year)
        - limit: Number of results (default: 10)
        - offset: Skip results (default: 0)
    """
    # Get query parameters
    author_filter = request.args.get('author')
    year_filter = request.args.get('year')
    sort_by = request.args.get('sort', 'title')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    
    # Filter books
    filtered_books = list(books.values())
    
    if author_filter:
        filtered_books = [b for b in filtered_books if author_filter.lower() in b['author'].lower()]
    
    if year_filter:
        filtered_books = [b for b in filtered_books if str(b['published_year']) == year_filter]
    
    # Sort books
    if sort_by in ['title', 'author', 'published_year']:
        filtered_books.sort(key=lambda x: x.get(sort_by, ''))
    
    # Paginate
    total = len(filtered_books)
    paginated_books = filtered_books[offset:offset + limit]
    
    return jsonify({
        'data': paginated_books,
        'meta': {
            'total': total,
            'limit': limit,
            'offset': offset
        }
    }), 200


@app.route('/api/books/<book_id>', methods=['GET'])
def get_book(book_id):
    """
    GET /api/books/:id
    Retrieve a specific book by ID.
    """
    if book_id not in books:
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': f'Book with ID {book_id} not found'
            }
        }), 404
    
    return jsonify(books[book_id]), 200


@app.route('/api/books', methods=['POST'])
def create_book():
    """
    POST /api/books
    Create a new book.
    
    Required fields: title, author, isbn
    Optional fields: published_year
    """
    # Validate content type
    if not request.is_json:
        return jsonify({
            'error': {
                'code': 'INVALID_CONTENT_TYPE',
                'message': 'Content-Type must be application/json'
            }
        }), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'author', 'isbn']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': f'Missing required field: {field}'
                }
            }), 400
    
    # Check if ISBN already exists
    for book in books.values():
        if book['isbn'] == data['isbn']:
            return jsonify({
                'error': {
                    'code': 'DUPLICATE_ISBN',
                    'message': 'A book with this ISBN already exists'
                }
            }), 409
    
    # Create new book
    book_id = str(uuid.uuid4())[:8]
    new_book = {
        'id': book_id,
        'title': data['title'],
        'author': data['author'],
        'isbn': data['isbn'],
        'published_year': data.get('published_year'),
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    
    books[book_id] = new_book
    
    # Return 201 Created with Location header
    response = jsonify(new_book)
    response.status_code = 201
    response.headers['Location'] = f'/api/books/{book_id}'
    return response


@app.route('/api/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    """
    PUT /api/books/:id
    Update (replace) an entire book resource.
    """
    if book_id not in books:
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': f'Book with ID {book_id} not found'
            }
        }), 404
    
    if not request.is_json:
        return jsonify({
            'error': {
                'code': 'INVALID_CONTENT_TYPE',
                'message': 'Content-Type must be application/json'
            }
        }), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'author', 'isbn']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': f'Missing required field: {field}'
                }
            }), 400
    
    # Update book (replace entirely)
    books[book_id] = {
        'id': book_id,
        'title': data['title'],
        'author': data['author'],
        'isbn': data['isbn'],
        'published_year': data.get('published_year'),
        'created_at': books[book_id]['created_at'],
        'updated_at': datetime.utcnow().isoformat() + 'Z'
    }
    
    return jsonify(books[book_id]), 200


@app.route('/api/books/<book_id>', methods=['PATCH'])
def patch_book(book_id):
    """
    PATCH /api/books/:id
    Partially update a book (only specified fields).
    """
    if book_id not in books:
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': f'Book with ID {book_id} not found'
            }
        }), 404
    
    if not request.is_json:
        return jsonify({
            'error': {
                'code': 'INVALID_CONTENT_TYPE',
                'message': 'Content-Type must be application/json'
            }
        }), 400
    
    data = request.get_json()
    
    # Update only provided fields
    allowed_fields = ['title', 'author', 'isbn', 'published_year']
    for field in allowed_fields:
        if field in data:
            books[book_id][field] = data[field]
    
    books[book_id]['updated_at'] = datetime.utcnow().isoformat() + 'Z'
    
    return jsonify(books[book_id]), 200


@app.route('/api/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    DELETE /api/books/:id
    Delete a book.
    """
    if book_id not in books:
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': f'Book with ID {book_id} not found'
            }
        }), 404
    
    del books[book_id]
    
    # Return 204 No Content (successful deletion with no body)
    return '', 204


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': {
            'code': 'NOT_FOUND',
            'message': 'The requested endpoint does not exist'
        }
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': {
            'code': 'INTERNAL_ERROR',
            'message': 'An internal server error occurred'
        }
    }), 500


if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════╗
    ║   📚 Books REST API Server Started!       ║
    ╠════════════════════════════════════════════╣
    ║   Listening on: http://localhost:5000     ║
    ║   Press Ctrl+C to stop                     ║
    ╚════════════════════════════════════════════╝
    
    Try these commands:
    
    # Get all books
    curl http://localhost:5000/api/books
    
    # Get a specific book
    curl http://localhost:5000/api/books/1
    
    # Create a new book
    curl -X POST http://localhost:5000/api/books \\
      -H "Content-Type: application/json" \\
      -d '{"title":"New Book","author":"John Doe","isbn":"123-456"}'
    
    # Update a book
    curl -X PATCH http://localhost:5000/api/books/1 \\
      -H "Content-Type: application/json" \\
      -d '{"title":"Updated Title"}'
    
    # Delete a book
    curl -X DELETE http://localhost:5000/api/books/1
    """)
    
    app.run(debug=True, port=5000)
