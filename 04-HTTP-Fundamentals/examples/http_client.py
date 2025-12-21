#!/usr/bin/env python3
"""
HTTP Client Example

This script demonstrates how to make HTTP requests using Python's requests library.
It shows different HTTP methods, headers, and how to handle responses.

Requirements:
    pip install requests

Usage:
    python http_client.py
"""

import requests
import json


def example_get_request():
    """
    Demonstrate a simple GET request.
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Simple GET Request")
    print("="*60)
    
    # Make a GET request to a public API
    url = "https://api.github.com/users/octocat"
    response = requests.get(url)
    
    # Print response details
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers['Content-Type']}")
    print(f"\nResponse Body (first 200 chars):")
    print(response.text[:200] + "...")
    
    # Parse JSON response
    data = response.json()
    print(f"\nUser Info:")
    print(f"  - Name: {data.get('name')}")
    print(f"  - Bio: {data.get('bio')}")
    print(f"  - Public Repos: {data.get('public_repos')}")


def example_get_with_parameters():
    """
    Demonstrate GET request with query parameters.
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: GET Request with Parameters")
    print("="*60)
    
    # Make a GET request with query parameters
    url = "https://api.github.com/search/repositories"
    params = {
        'q': 'language:python',
        'sort': 'stars',
        'order': 'desc',
        'per_page': 3
    }
    
    response = requests.get(url, params=params)
    
    print(f"Request URL: {response.url}")
    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    print(f"\nTop 3 Python Repositories:")
    for item in data['items']:
        print(f"  - {item['name']}: ⭐ {item['stargazers_count']}")


def example_get_with_headers():
    """
    Demonstrate GET request with custom headers.
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: GET Request with Custom Headers")
    print("="*60)
    
    url = "https://api.github.com/users/octocat"
    
    # Custom headers
    headers = {
        'User-Agent': 'NetworkingFundamentals-Tutorial',
        'Accept': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    
    print(f"Request Headers Sent:")
    for key, value in headers.items():
        print(f"  {key}: {value}")
    
    print(f"\nResponse Headers Received (selected):")
    print(f"  Content-Type: {response.headers.get('Content-Type')}")
    print(f"  Cache-Control: {response.headers.get('Cache-Control')}")
    print(f"  X-RateLimit-Remaining: {response.headers.get('X-RateLimit-Remaining')}")


def example_post_request():
    """
    Demonstrate POST request with JSON data.
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: POST Request with JSON Data")
    print("="*60)
    
    # Using a test API that echoes back what you send
    url = "https://httpbin.org/post"
    
    # Data to send
    data = {
        'username': 'alice',
        'email': 'alice@example.com',
        'age': 25
    }
    
    # Make POST request
    response = requests.post(url, json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Request Method: {response.request.method}")
    
    result = response.json()
    print(f"\nData Sent:")
    print(json.dumps(data, indent=2))
    print(f"\nData Received by Server:")
    print(json.dumps(result['json'], indent=2))


def example_put_request():
    """
    Demonstrate PUT request to update data.
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: PUT Request")
    print("="*60)
    
    url = "https://httpbin.org/put"
    
    # Updated data
    data = {
        'user_id': 123,
        'name': 'Alice Smith',
        'status': 'active'
    }
    
    response = requests.put(url, json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Request Method: {response.request.method}")
    print(f"\nUpdated Data:")
    print(json.dumps(response.json()['json'], indent=2))


def example_delete_request():
    """
    Demonstrate DELETE request.
    """
    print("\n" + "="*60)
    print("EXAMPLE 6: DELETE Request")
    print("="*60)
    
    url = "https://httpbin.org/delete"
    
    response = requests.delete(url)
    
    print(f"Status Code: {response.status_code}")
    print(f"Request Method: {response.request.method}")
    print(f"Response: {response.text[:100]}...")


def example_error_handling():
    """
    Demonstrate error handling for HTTP requests.
    """
    print("\n" + "="*60)
    print("EXAMPLE 7: Error Handling")
    print("="*60)
    
    # Try to request a non-existent endpoint
    url = "https://api.github.com/users/this-user-definitely-does-not-exist-12345"
    
    try:
        response = requests.get(url, timeout=5)
        
        # Check if request was successful
        if response.status_code == 200:
            print("✅ Request successful!")
            print(response.json())
        elif response.status_code == 404:
            print("❌ 404 Not Found")
            print("The requested resource does not exist.")
        else:
            print(f"⚠️  Received status code: {response.status_code}")
        
        # Alternative: raise exception for bad status codes
        response.raise_for_status()
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Could not connect to server")
    except requests.exceptions.Timeout:
        print("❌ Timeout: Request took too long")
    except requests.exceptions.RequestException as e:
        print(f"❌ An error occurred: {e}")


def example_response_details():
    """
    Demonstrate accessing various response details.
    """
    print("\n" + "="*60)
    print("EXAMPLE 8: Response Details")
    print("="*60)
    
    url = "https://httpbin.org/get"
    response = requests.get(url)
    
    print(f"Status Code: {response.status_code}")
    print(f"Reason: {response.reason}")
    print(f"URL: {response.url}")
    print(f"Encoding: {response.encoding}")
    print(f"Response Time: {response.elapsed.total_seconds()} seconds")
    
    print(f"\nResponse Headers:")
    for key, value in list(response.headers.items())[:5]:
        print(f"  {key}: {value}")
    
    print(f"\nCookies: {dict(response.cookies)}")


def main():
    """
    Run all examples.
    """
    print("""
    ╔════════════════════════════════════════════╗
    ║   🌐 HTTP Client Examples                 ║
    ║   Demonstrating requests library          ║
    ╚════════════════════════════════════════════╝
    """)
    
    try:
        example_get_request()
        example_get_with_parameters()
        example_get_with_headers()
        example_post_request()
        example_put_request()
        example_delete_request()
        example_error_handling()
        example_response_details()
        
        print("\n" + "="*60)
        print("✅ All examples completed!")
        print("="*60)
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ An error occurred: {e}")
        print("Make sure you have internet connection and requests library installed.")
        print("Install with: pip install requests")


if __name__ == '__main__':
    main()
