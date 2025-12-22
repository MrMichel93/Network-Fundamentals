#!/usr/bin/env python3
"""
PRACTICE API FOR OWASP ZAP TESTING
===================================

This API contains various vulnerabilities for testing with OWASP ZAP.

Run this API and scan it with ZAP to discover:
- SQL Injection
- XSS
- Missing security headers
- Information disclosure
- And more...
"""

from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'practice_api.db'

def init_db():
    """Initialize database"""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL,
            description TEXT
        )
    ''')
    
    products = [
        ('Laptop', 999.99, 'High-performance laptop'),
        ('Mouse', 29.99, 'Wireless mouse'),
        ('Keyboard', 79.99, 'Mechanical keyboard'),
    ]
    
    for product in products:
        cursor.execute("INSERT INTO products (name, price, description) VALUES (?, ?, ?)", product)
    
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return '''
    <html>
    <head><title>Practice API</title></head>
    <body>
        <h1>Practice API for OWASP ZAP</h1>
        <p>This API is designed for security testing with OWASP ZAP.</p>
        <h2>Endpoints:</h2>
        <ul>
            <li>GET /api/products - List all products</li>
            <li>GET /api/product?id=1 - Get product by ID (vulnerable)</li>
            <li>GET /api/search?q=laptop - Search products (vulnerable)</li>
        </ul>
    </body>
    </html>
    '''

@app.route('/api/products')
def get_products():
    """List all products"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'products': [
            {'id': p[0], 'name': p[1], 'price': p[2], 'description': p[3]}
            for p in products
        ]
    })

@app.route('/api/product')
def get_product():
    """
    ⚠️ EDUCATIONAL VULNERABILITY - DO NOT USE IN PRODUCTION ⚠️
    
    VULNERABLE: SQL Injection in product lookup
    This code is intentionally insecure for learning purposes.
    """
    product_id = request.args.get('id', '1')
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # ⚠️ DANGEROUS: Direct string concatenation enables SQL injection!
    # This is vulnerable code for educational purposes only!
    query = f"SELECT * FROM products WHERE id = {product_id}"
    
    try:
        cursor.execute(query)
        product = cursor.fetchone()
        conn.close()
        
        if product:
            return jsonify({
                'id': product[0],
                'name': product[1],
                'price': product[2],
                'description': product[3]
            })
        return jsonify({'error': 'Not found'}), 404
    except Exception as e:
        # VULNERABLE: Information disclosure
        return jsonify({'error': str(e), 'query': query}), 500

@app.route('/api/search')
def search():
    """VULNERABLE: XSS in search results"""
    query = request.args.get('q', '')
    
    # VULNERABLE: Reflected XSS
    html = f'''
    <html>
    <head><title>Search Results</title></head>
    <body>
        <h1>Search Results for: {query}</h1>
        <p>No products found matching your search.</p>
    </body>
    </html>
    '''
    
    return html

if __name__ == '__main__':
    print("\n" + "="*60)
    print("PRACTICE API FOR OWASP ZAP TESTING")
    print("="*60)
    print("Server: http://localhost:5005")
    print("\nUse OWASP ZAP to scan this API for vulnerabilities!")
    print("="*60 + "\n")
    
    # NOTE: debug=True is intentional for educational lab environment
    # This should NEVER be used in production
    # Lab runs on localhost only (127.0.0.1)
    app.run(debug=True, host='127.0.0.1', port=5005)
