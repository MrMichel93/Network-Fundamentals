#!/usr/bin/env python3
"""
Rate Limiting Test Tools
=========================

Tools for testing rate limiters.
"""

import requests
import time
from datetime import datetime

def test_rate_limit_basic(url, max_requests=15, delay=0.1):
    """
    Test basic rate limiting by making rapid requests.
    
    Args:
        url: Endpoint to test
        max_requests: Number of requests to make
        delay: Delay between requests in seconds
    """
    print(f"\n{'='*60}")
    print(f"Testing: {url}")
    print(f"Making {max_requests} requests with {delay}s delay")
    print(f"{'='*60}\n")
    
    success_count = 0
    rate_limited_count = 0
    
    for i in range(max_requests):
        try:
            response = requests.get(url)
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            if response.status_code == 200:
                success_count += 1
                print(f"[{timestamp}] Request {i+1}: ✓ 200 OK")
            elif response.status_code == 429:
                rate_limited_count += 1
                print(f"[{timestamp}] Request {i+1}: ✗ 429 Rate Limited")
                
                # Show rate limit info
                data = response.json()
                if 'retry_after' in data:
                    print(f"             Retry after: {data['retry_after']}")
            else:
                print(f"[{timestamp}] Request {i+1}: ? {response.status_code}")
            
            time.sleep(delay)
            
        except Exception as e:
            print(f"Request {i+1}: Error - {e}")
    
    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"  Successful:   {success_count}/{max_requests}")
    print(f"  Rate Limited: {rate_limited_count}/{max_requests}")
    print(f"{'='*60}\n")

def test_concurrent_requests(url, num_requests=10):
    """
    Test with concurrent requests.
    """
    import concurrent.futures
    
    print(f"\n{'='*60}")
    print(f"Testing Concurrent Requests: {url}")
    print(f"Making {num_requests} concurrent requests")
    print(f"{'='*60}\n")
    
    def make_request(i):
        try:
            response = requests.get(url)
            return (i, response.status_code)
        except Exception as e:
            return (i, str(e))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(make_request, range(num_requests)))
    
    success = sum(1 for _, status in results if status == 200)
    rate_limited = sum(1 for _, status in results if status == 429)
    
    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"  Successful:   {success}/{num_requests}")
    print(f"  Rate Limited: {rate_limited}/{num_requests}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    BASE_URL = "http://localhost:5006"
    
    print("\n" + "="*60)
    print("RATE LIMITING TEST SUITE")
    print("="*60)
    
    # Test 1: Sequential requests (should hit rate limit)
    test_rate_limit_basic(f"{BASE_URL}/api/data", max_requests=15, delay=0.1)
    
    # Wait a bit before next test
    print("\nWaiting 5 seconds before next test...\n")
    time.sleep(5)
    
    # Test 2: Concurrent requests
    test_concurrent_requests(f"{BASE_URL}/api/data", num_requests=20)
    
    print("\nTesting complete!")
    print("\nNext steps:")
    print("  1. Review the results")
    print("  2. Try testing /api/expensive endpoint")
    print("  3. Compare with /api/unlimited (no rate limit)")
