#!/usr/bin/env python3
"""
API Key Authentication Example

This example demonstrates API key-based authentication with rate limiting.
API keys are used to identify and authorize applications/users.

Features:
- API key generation
- Rate limiting per API key
- Usage tracking
- Key revocation

Run: python 03_api_key_auth.py
Test: See exercises.md for testing instructions
"""

from flask import Flask, request, jsonify
import secrets
from datetime import datetime, timedelta
from functools import wraps
from collections import defaultdict
import time

app = Flask(__name__)

# In-memory API key database
api_keys_db = {}

# Rate limiting: tracks requests per API key
rate_limit_store = defaultdict(list)

# Configuration
RATE_LIMIT_REQUESTS = 10  # Max requests
RATE_LIMIT_WINDOW = 60    # Per 60 seconds


def generate_api_key():
    """Generate a secure random API key"""
    return secrets.token_urlsafe(32)


def api_key_required(f):
    """
    Decorator to protect routes that require API key authentication
    Checks for API key in X-API-Key header
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({
                'error': 'Missing API key',
                'message': 'Please provide X-API-Key header'
            }), 401
        
        # Verify API key exists and is active
        if api_key not in api_keys_db:
            return jsonify({
                'error': 'Invalid API key'
            }), 401
        
        key_data = api_keys_db[api_key]
        
        if not key_data['active']:
            return jsonify({
                'error': 'API key has been revoked'
            }), 401
        
        # Store current API key info in request context
        request.current_api_key = api_key
        request.key_owner = key_data['owner']
        
        return f(*args, **kwargs)
    
    return decorated


def rate_limit_check(f):
    """
    Decorator to enforce rate limiting
    Must be used after @api_key_required
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.current_api_key
        current_time = time.time()
        
        # Get request history for this API key
        request_times = rate_limit_store[api_key]
        
        # Remove requests older than the time window
        request_times[:] = [
            req_time for req_time in request_times 
            if current_time - req_time < RATE_LIMIT_WINDOW
        ]
        
        # Check if limit exceeded
        if len(request_times) >= RATE_LIMIT_REQUESTS:
            # Calculate reset time
            oldest_request = min(request_times)
            reset_time = int(oldest_request + RATE_LIMIT_WINDOW - current_time)
            
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': f'Maximum {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW} seconds',
                'retry_after': reset_time
            }), 429
        
        # Record this request
        request_times.append(current_time)
        
        # Update usage stats
        api_keys_db[api_key]['total_requests'] += 1
        api_keys_db[api_key]['last_used'] = datetime.utcnow().isoformat()
        
        return f(*args, **kwargs)
    
    return decorated


@app.route('/api/keys/create', methods=['POST'])
def create_api_key():
    """
    Create a new API key
    
    Request body:
    {
        "owner": "john@example.com",
        "description": "My application API key"
    }
    """
    data = request.json
    
    if not data or not data.get('owner'):
        return jsonify({'error': 'Missing owner information'}), 400
    
    owner = data['owner']
    description = data.get('description', 'No description provided')
    
    # Generate new API key
    api_key = generate_api_key()
    
    # Store API key info
    api_keys_db[api_key] = {
        'owner': owner,
        'description': description,
        'created_at': datetime.utcnow().isoformat(),
        'last_used': None,
        'active': True,
        'total_requests': 0
    }
    
    return jsonify({
        'message': 'API key created successfully',
        'api_key': api_key,
        'owner': owner,
        'description': description,
        'rate_limit': {
            'requests': RATE_LIMIT_REQUESTS,
            'window': f'{RATE_LIMIT_WINDOW} seconds'
        },
        'important': 'Store this key securely. You won\'t be able to see it again.'
    }), 201


@app.route('/api/keys/info')
@api_key_required
def api_key_info():
    """
    Get information about the current API key
    
    Header:
    X-API-Key: your-api-key-here
    """
    api_key = request.current_api_key
    key_data = api_keys_db[api_key]
    
    # Calculate current rate limit usage
    current_time = time.time()
    request_times = rate_limit_store[api_key]
    recent_requests = [
        req_time for req_time in request_times 
        if current_time - req_time < RATE_LIMIT_WINDOW
    ]
    
    return jsonify({
        'owner': key_data['owner'],
        'description': key_data['description'],
        'created_at': key_data['created_at'],
        'last_used': key_data['last_used'],
        'active': key_data['active'],
        'total_requests': key_data['total_requests'],
        'rate_limit': {
            'limit': RATE_LIMIT_REQUESTS,
            'window': RATE_LIMIT_WINDOW,
            'remaining': RATE_LIMIT_REQUESTS - len(recent_requests),
            'used': len(recent_requests)
        }
    }), 200


@app.route('/api/keys/revoke', methods=['POST'])
@api_key_required
def revoke_api_key():
    """
    Revoke the current API key
    
    Header:
    X-API-Key: your-api-key-here
    """
    api_key = request.current_api_key
    
    # Mark key as inactive
    api_keys_db[api_key]['active'] = False
    api_keys_db[api_key]['revoked_at'] = datetime.utcnow().isoformat()
    
    return jsonify({
        'message': 'API key revoked successfully',
        'api_key': api_key[:8] + '...'  # Show only first 8 chars
    }), 200


@app.route('/api/data')
@api_key_required
@rate_limit_check
def get_data():
    """
    Protected endpoint that requires API key and enforces rate limiting
    
    Header:
    X-API-Key: your-api-key-here
    """
    api_key = request.current_api_key
    owner = request.key_owner
    
    # Calculate remaining requests
    current_time = time.time()
    request_times = rate_limit_store[api_key]
    recent_requests = [
        req_time for req_time in request_times 
        if current_time - req_time < RATE_LIMIT_WINDOW
    ]
    
    return jsonify({
        'message': 'Data retrieved successfully',
        'data': {
            'sample_field_1': 'Sample value 1',
            'sample_field_2': 'Sample value 2',
            'timestamp': datetime.utcnow().isoformat()
        },
        'request_info': {
            'authenticated_as': owner,
            'rate_limit_remaining': RATE_LIMIT_REQUESTS - len(recent_requests)
        }
    }), 200


@app.route('/api/weather')
@api_key_required
@rate_limit_check
def get_weather():
    """
    Another protected endpoint - simulates weather API
    
    Query params:
    - city: City name
    
    Header:
    X-API-Key: your-api-key-here
    """
    city = request.args.get('city', 'Unknown')
    
    # Simulate weather data
    import random
    
    return jsonify({
        'city': city,
        'temperature': round(random.uniform(15, 30), 1),
        'conditions': random.choice(['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy']),
        'humidity': random.randint(40, 90),
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/public/health')
def health_check():
    """
    Public endpoint - no authentication required
    """
    return jsonify({
        'status': 'healthy',
        'service': 'API Key Authentication Service',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/')
def home():
    """
    API information endpoint
    """
    return jsonify({
        'service': 'API Key Authentication API',
        'version': '1.0',
        'endpoints': {
            'public': {
                'GET /public/health': 'Health check (no auth)'
            },
            'key_management': {
                'POST /api/keys/create': 'Create new API key (no auth)',
                'GET /api/keys/info': 'Get API key info (requires key)',
                'POST /api/keys/revoke': 'Revoke API key (requires key)'
            },
            'protected': {
                'GET /api/data': 'Get sample data (requires key)',
                'GET /api/weather': 'Get weather data (requires key)'
            }
        },
        'authentication': 'API Key via X-API-Key header',
        'rate_limiting': {
            'limit': RATE_LIMIT_REQUESTS,
            'window': f'{RATE_LIMIT_WINDOW} seconds'
        },
        'documentation': 'See exercises.md for usage examples'
    }), 200


if __name__ == '__main__':
    print("=" * 60)
    print("API Key Authentication Server")
    print("=" * 60)
    print(f"\nRate Limit: {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW} seconds")
    print("\nStarting server on http://localhost:5002")
    print("\nAvailable endpoints:")
    print("  POST   /api/keys/create - Create API key (no auth)")
    print("  GET    /api/keys/info   - Get key info (requires key)")
    print("  POST   /api/keys/revoke - Revoke key (requires key)")
    print("  GET    /api/data        - Get data (requires key)")
    print("  GET    /api/weather     - Get weather (requires key)")
    print("  GET    /public/health   - Health check (public)")
    print("\nFirst, create an API key with:")
    print('  curl -X POST http://localhost:5002/api/keys/create \\')
    print('       -H "Content-Type: application/json" \\')
    print('       -d \'{"owner":"you@example.com","description":"Test key"}\'')
    print("\nSee exercises.md for more usage examples")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5002)
