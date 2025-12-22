#!/usr/bin/env python3
"""
BASIC RATE LIMITER IMPLEMENTATION
==================================

Simple rate limiting implementation for educational purposes.
"""

from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time

app = Flask(__name__)

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"],
    storage_uri="memory://"  # In-memory storage (dev only)
)

@app.route('/')
def home():
    return '''
    <html>
    <head><title>Rate Limiting Lab</title></head>
    <body>
        <h1>Rate Limiting Lab</h1>
        <p>Test the rate limiter with these endpoints:</p>
        <ul>
            <li>GET /api/data - 10 requests per minute</li>
            <li>GET /api/expensive - 5 requests per hour</li>
            <li>GET /api/unlimited - No rate limit</li>
        </ul>
        <h2>Testing:</h2>
        <pre>
# Test with curl
for i in {1..15}; do
  curl http://localhost:5006/api/data
  echo "Request $i"
done
        </pre>
    </body>
    </html>
    '''

@app.route('/api/data')
@limiter.limit("10 per minute")
def get_data():
    """Rate limited endpoint: 10 requests per minute"""
    return jsonify({
        'message': 'Success',
        'data': 'Sample data',
        'timestamp': time.time()
    })

@app.route('/api/expensive')
@limiter.limit("5 per hour")
def expensive_operation():
    """Rate limited endpoint: 5 requests per hour"""
    # Simulate expensive operation
    time.sleep(0.5)
    return jsonify({
        'message': 'Expensive operation completed',
        'result': 'computed_value'
    })

@app.route('/api/unlimited')
def unlimited():
    """No rate limit (for comparison)"""
    return jsonify({
        'message': 'No rate limit on this endpoint',
        'warning': 'This is vulnerable to abuse!'
    })

@app.errorhandler(429)
def ratelimit_handler(e):
    """Custom handler for rate limit exceeded"""
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': str(e.description),
        'retry_after': e.description.split('Retry after')[1].strip() if 'Retry after' in str(e.description) else 'unknown'
    }), 429

if __name__ == '__main__':
    print("\n" + "="*60)
    print("RATE LIMITING LAB - BASIC IMPLEMENTATION")
    print("="*60)
    print("Server: http://localhost:5006")
    print("\nRate Limits:")
    print("  /api/data      - 10 requests per minute")
    print("  /api/expensive - 5 requests per hour")
    print("  /api/unlimited - No limit (vulnerable)")
    print("="*60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5006)
