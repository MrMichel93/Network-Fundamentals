#!/usr/bin/env python3
"""
REST API Client Example

This script demonstrates how to consume a REST API.
Use this with the rest_api_server.py running.

Requirements:
    pip install requests

Usage:
    # Start the server first
    python rest_api_server.py
    
    # Then in another terminal
    python rest_api_client.py
"""

import requests
import json


BASE_URL = 'http://localhost:5000/api'


def print_response(response):
    """Pretty print response details."""
    print(f"\n{'='*60}")
    print(f"Status: {response.status_code} {response.reason}")
    print(f"URL: {response.url}")
    
    if response.status_code != 204:  # 204 has no content
        print(f"\nResponse Body:")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
    print(f"{'='*60}\n")


def get_all_books():
    """Demonstrate GET request for collection."""
    print("\n📖 GET ALL BOOKS")
    response = requests.get(f'{BASE_URL}/books')
    print_response(response)
    return response.json()


def get_book_by_id(book_id):
    """Demonstrate GET request for single resource."""
    print(f"\n📖 GET BOOK {book_id}")
    response = requests.get(f'{BASE_URL}/books/{book_id}')
    print_response(response)
    return response.json() if response.status_code == 200 else None


def create_book():
    """Demonstrate POST request to create resource."""
    print("\n✏️  CREATE NEW BOOK")
    
    new_book = {
        'title': 'Network Fundamentals',
        'author': 'Jane Developer',
        'isbn': '978-1234567890',
        'published_year': 2024
    }
    
    print(f"Sending: {json.dumps(new_book, indent=2)}")
    
    response = requests.post(
        f'{BASE_URL}/books',
        json=new_book,
        headers={'Content-Type': 'application/json'}
    )
    
    print_response(response)
    
    if response.status_code == 201:
        print(f"✅ Book created! Location: {response.headers.get('Location')}")
        return response.json()
    return None


def update_book_put(book_id):
    """Demonstrate PUT request to replace resource."""
    print(f"\n🔄 UPDATE BOOK {book_id} (PUT)")
    
    updated_book = {
        'title': 'Network Fundamentals - Second Edition',
        'author': 'Jane Developer',
        'isbn': '978-1234567890'
    }
    
    response = requests.put(
        f'{BASE_URL}/books/{book_id}',
        json=updated_book
    )
    
    print_response(response)
    return response.json() if response.status_code == 200 else None


def update_book_patch(book_id):
    """Demonstrate PATCH request to partially update resource."""
    print(f"\n🩹 UPDATE BOOK {book_id} (PATCH)")
    
    partial_update = {
        'published_year': 2025
    }
    
    response = requests.patch(
        f'{BASE_URL}/books/{book_id}',
        json=partial_update
    )
    
    print_response(response)
    return response.json() if response.status_code == 200 else None


def delete_book(book_id):
    """Demonstrate DELETE request."""
    print(f"\n🗑️  DELETE BOOK {book_id}")
    
    response = requests.delete(f'{BASE_URL}/books/{book_id}')
    print_response(response)
    
    if response.status_code == 204:
        print("✅ Book deleted successfully!")


def filter_books():
    """Demonstrate filtering with query parameters."""
    print("\n🔍 FILTER BOOKS BY AUTHOR")
    
    response = requests.get(f'{BASE_URL}/books', params={'author': 'Eric'})
    print_response(response)


def paginate_books():
    """Demonstrate pagination."""
    print("\n📄 PAGINATE BOOKS")
    
    response = requests.get(f'{BASE_URL}/books', params={'limit': 1, 'offset': 0})
    print_response(response)


def handle_errors():
    """Demonstrate error handling."""
    print("\n❌ ERROR HANDLING")
    
    # Try to get non-existent book
    print("\nTrying to get non-existent book:")
    response = requests.get(f'{BASE_URL}/books/999')
    print_response(response)
    
    # Try to create book with missing fields
    print("\nTrying to create book with missing fields:")
    response = requests.post(
        f'{BASE_URL}/books',
        json={'title': 'Incomplete Book'}
    )
    print_response(response)
    
    # Try to create duplicate ISBN
    print("\nTrying to create book with duplicate ISBN:")
    response = requests.post(
        f'{BASE_URL}/books',
        json={
            'title': 'Duplicate',
            'author': 'Someone',
            'isbn': '978-1593279288'  # ISBN from sample data
        }
    )
    print_response(response)


def main():
    """Run all examples."""
    print("""
    ╔════════════════════════════════════════════╗
    ║   🔌 REST API Client Examples             ║
    ║   Make sure the server is running!        ║
    ╚════════════════════════════════════════════╝
    """)
    
    try:
        # Check if server is running
        response = requests.get('http://localhost:5000/')
        print("✅ Server is running!\n")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Server is not running!")
        print("Start the server with: python rest_api_server.py")
        return
    
    # Run examples
    try:
        # Read operations
        all_books = get_all_books()
        get_book_by_id('1')
        
        # Create operation
        new_book = create_book()
        if new_book:
            book_id = new_book['id']
            
            # Update operations
            update_book_patch(book_id)
            update_book_put(book_id)
            
            # Delete operation
            delete_book(book_id)
        
        # Query parameters
        filter_books()
        paginate_books()
        
        # Error handling
        handle_errors()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")


if __name__ == '__main__':
    main()
