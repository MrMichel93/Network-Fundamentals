#!/usr/bin/env python3
"""
OAuth 2.0 Example - GitHub OAuth Integration

This example demonstrates OAuth 2.0 authentication flow using GitHub.
Users can "Login with GitHub" instead of creating account credentials.

Features:
- GitHub OAuth integration
- Authorization code flow
- Access token handling
- User profile retrieval from GitHub

Setup:
1. Register OAuth app on GitHub: https://github.com/settings/developers
2. Set callback URL to: http://localhost:5003/callback
3. Copy Client ID and Client Secret
4. Set environment variables or update below

Run: python 04_oauth_example.py
Test: See exercises.md for testing instructions
"""

from flask import Flask, redirect, request, session, jsonify, url_for
import requests
import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# GitHub OAuth Configuration
# Register your app at: https://github.com/settings/developers
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID', 'your-client-id-here')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET', 'your-client-secret-here')
GITHUB_CALLBACK_URL = 'http://localhost:5003/callback'

# GitHub OAuth URLs
GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_API_URL = 'https://api.github.com'


@app.route('/')
def home():
    """
    Home page - shows login status
    """
    if session.get('logged_in'):
        user = session.get('user', {})
        return jsonify({
            'status': 'logged_in',
            'user': {
                'username': user.get('login'),
                'name': user.get('name'),
                'avatar': user.get('avatar_url'),
                'profile_url': user.get('html_url')
            },
            'endpoints': {
                'GET /profile': 'View full profile',
                'GET /repos': 'View user repositories',
                'POST /logout': 'Logout'
            }
        }), 200
    else:
        return jsonify({
            'status': 'not_logged_in',
            'message': 'Welcome! Please login with GitHub',
            'endpoints': {
                'GET /login': 'Start GitHub OAuth login flow'
            }
        }), 200


@app.route('/login')
def login():
    """
    Initiate OAuth login flow
    Redirects user to GitHub authorization page
    """
    # Generate random state for CSRF protection
    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state
    
    # Build GitHub authorization URL
    params = {
        'client_id': GITHUB_CLIENT_ID,
        'redirect_uri': GITHUB_CALLBACK_URL,
        'scope': 'user:email read:user',  # Requested permissions
        'state': state  # CSRF protection
    }
    
    auth_url = f"{GITHUB_AUTHORIZE_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    
    return jsonify({
        'message': 'Redirecting to GitHub for authorization',
        'authorization_url': auth_url,
        'note': 'In a web browser, you would be redirected automatically'
    }), 200


@app.route('/callback')
def callback():
    """
    OAuth callback endpoint
    GitHub redirects here after user authorizes the app
    """
    # Verify state to prevent CSRF attacks
    state = request.args.get('state')
    if state != session.get('oauth_state'):
        return jsonify({'error': 'Invalid state parameter'}), 400
    
    # Get authorization code from GitHub
    code = request.args.get('code')
    if not code:
        error = request.args.get('error', 'unknown')
        error_description = request.args.get('error_description', 'No description')
        return jsonify({
            'error': error,
            'error_description': error_description
        }), 400
    
    # Exchange authorization code for access token
    token_data = {
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'code': code,
        'redirect_uri': GITHUB_CALLBACK_URL
    }
    
    token_headers = {'Accept': 'application/json'}
    
    token_response = requests.post(
        GITHUB_TOKEN_URL,
        data=token_data,
        headers=token_headers
    )
    
    if token_response.status_code != 200:
        return jsonify({
            'error': 'Failed to obtain access token',
            'details': token_response.text
        }), 500
    
    token_json = token_response.json()
    
    if 'error' in token_json:
        return jsonify({
            'error': token_json['error'],
            'error_description': token_json.get('error_description', '')
        }), 400
    
    access_token = token_json.get('access_token')
    
    # Use access token to get user information
    user_headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    
    user_response = requests.get(
        f'{GITHUB_API_URL}/user',
        headers=user_headers
    )
    
    if user_response.status_code != 200:
        return jsonify({
            'error': 'Failed to get user information'
        }), 500
    
    user_data = user_response.json()
    
    # Store user info and token in session
    session['logged_in'] = True
    session['access_token'] = access_token
    session['user'] = {
        'login': user_data.get('login'),
        'name': user_data.get('name'),
        'email': user_data.get('email'),
        'avatar_url': user_data.get('avatar_url'),
        'html_url': user_data.get('html_url'),
        'bio': user_data.get('bio')
    }
    
    return jsonify({
        'message': 'Successfully logged in with GitHub!',
        'user': session['user']
    }), 200


@app.route('/profile')
def profile():
    """
    Get user profile
    Requires authentication via OAuth
    """
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    return jsonify({
        'user': session.get('user')
    }), 200


@app.route('/repos')
def repos():
    """
    Get user's GitHub repositories
    Demonstrates using access token to call GitHub API
    """
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    access_token = session.get('access_token')
    
    # Call GitHub API to get repositories
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    
    repos_response = requests.get(
        f'{GITHUB_API_URL}/user/repos',
        headers=headers,
        params={'per_page': 10, 'sort': 'updated'}
    )
    
    if repos_response.status_code != 200:
        return jsonify({
            'error': 'Failed to fetch repositories'
        }), 500
    
    repos_data = repos_response.json()
    
    # Format repository data
    repos = [{
        'name': repo['name'],
        'description': repo['description'],
        'url': repo['html_url'],
        'stars': repo['stargazers_count'],
        'language': repo['language']
    } for repo in repos_data]
    
    return jsonify({
        'count': len(repos),
        'repositories': repos
    }), 200


@app.route('/logout', methods=['POST'])
def logout():
    """
    Logout - clear session
    """
    if not session.get('logged_in'):
        return jsonify({'error': 'Not logged in'}), 400
    
    username = session.get('user', {}).get('login', 'Unknown')
    
    # Clear session
    session.clear()
    
    return jsonify({
        'message': f'Logged out successfully',
        'username': username
    }), 200


@app.route('/info')
def info():
    """
    OAuth configuration information
    """
    config_status = 'configured' if (
        GITHUB_CLIENT_ID != 'your-client-id-here' and
        GITHUB_CLIENT_SECRET != 'your-client-secret-here'
    ) else 'not_configured'
    
    return jsonify({
        'service': 'GitHub OAuth Example',
        'oauth_provider': 'GitHub',
        'configuration_status': config_status,
        'setup_instructions': {
            'step_1': 'Register app at https://github.com/settings/developers',
            'step_2': f'Set callback URL to {GITHUB_CALLBACK_URL}',
            'step_3': 'Set GITHUB_CLIENT_ID environment variable',
            'step_4': 'Set GITHUB_CLIENT_SECRET environment variable',
            'step_5': 'Restart this server'
        },
        'endpoints': {
            'GET /': 'Home page',
            'GET /login': 'Start OAuth flow',
            'GET /callback': 'OAuth callback (handled automatically)',
            'GET /profile': 'Get user profile (requires auth)',
            'GET /repos': 'Get user repositories (requires auth)',
            'POST /logout': 'Logout'
        },
        'current_session': {
            'logged_in': session.get('logged_in', False),
            'user': session.get('user', {}).get('login') if session.get('logged_in') else None
        }
    }), 200


if __name__ == '__main__':
    print("=" * 60)
    print("GitHub OAuth 2.0 Example")
    print("=" * 60)
    
    if GITHUB_CLIENT_ID == 'your-client-id-here':
        print("\n⚠️  WARNING: GitHub OAuth not configured!")
        print("\nTo use this example:")
        print("1. Register app at: https://github.com/settings/developers")
        print(f"2. Set callback URL to: {GITHUB_CALLBACK_URL}")
        print("3. Set environment variables:")
        print("   export GITHUB_CLIENT_ID='your-client-id'")
        print("   export GITHUB_CLIENT_SECRET='your-client-secret'")
        print("4. Restart this server")
    else:
        print("\n✅ GitHub OAuth configured")
        print(f"   Client ID: {GITHUB_CLIENT_ID[:8]}...")
    
    print(f"\nStarting server on http://localhost:5003")
    print("\nAvailable endpoints:")
    print("  GET    /              - Home")
    print("  GET    /login         - Start OAuth flow")
    print("  GET    /callback      - OAuth callback")
    print("  GET    /profile       - Get profile (auth required)")
    print("  GET    /repos         - Get repos (auth required)")
    print("  POST   /logout        - Logout")
    print("  GET    /info          - Configuration info")
    print("\nSee exercises.md for usage examples")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5003)
