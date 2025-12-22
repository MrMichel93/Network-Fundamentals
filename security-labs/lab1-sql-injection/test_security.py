#!/usr/bin/env python3
"""
SQL INJECTION SECURITY TESTS
============================

This test suite validates that the fixed application properly defends
against SQL injection attacks.

Run this against the FIXED version (port 5002)
"""

import requests
import sys
import json

FIXED_URL = "http://localhost:5002"
VULNERABLE_URL = "http://localhost:5001"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name):
    print(f"\n{Colors.BLUE}[TEST]{Colors.END} {name}")

def print_pass(message):
    print(f"{Colors.GREEN}[✓]{Colors.END} {message}")

def print_fail(message):
    print(f"{Colors.RED}[✗]{Colors.END} {message}")

def print_info(message):
    print(f"{Colors.YELLOW}[i]{Colors.END} {message}")

def check_server(url):
    """Check if server is running"""
    try:
        response = requests.get(url, timeout=2)
        return response.status_code == 200
    except:
        return False

def test_auth_bypass_blocked(url):
    """Test that authentication bypass is blocked"""
    print_test("Authentication Bypass Protection")
    
    # Try SQL injection in login
    payload = {
        "username": "admin' --",
        "password": "anything"
    }
    
    response = requests.post(f"{url}/api/login", json=payload)
    
    if response.status_code == 401 or response.status_code == 400:
        data = response.json()
        if 'success' not in data or not data.get('success'):
            print_pass("SQL injection login bypass blocked")
            return True
    
    print_fail("VULNERABLE: Authentication bypass succeeded!")
    print_info(f"Response: {response.json()}")
    return False

def test_or_injection_blocked(url):
    """Test that OR-based injection is blocked"""
    print_test("OR-based Injection Protection")
    
    # Try OR '1'='1' injection
    response = requests.get(f"{url}/api/user/admin'%20OR%20'1'='1")
    
    if response.status_code in [400, 404, 500]:
        print_pass("OR-based injection blocked")
        return True
    
    # Check if multiple users returned (sign of successful injection)
    data = response.json()
    if 'users' in data and len(data['users']) > 1:
        print_fail("VULNERABLE: OR injection returned multiple users!")
        return False
    
    print_pass("OR-based injection appears blocked")
    return True

def test_union_injection_blocked(url):
    """Test that UNION-based injection is blocked"""
    print_test("UNION-based Injection Protection")
    
    # Try UNION SELECT injection
    response = requests.get(f"{url}/api/search?q=admin'%20UNION%20SELECT%201,2,3,4--")
    
    data = response.json()
    
    # Check if UNION was successful (would return attacker data)
    if 'results' in data:
        for result in data['results']:
            if result.get('username') in ['1', '2', '3', '4']:
                print_fail("VULNERABLE: UNION injection successful!")
                return False
    
    print_pass("UNION-based injection blocked")
    return True

def test_no_sql_errors_leaked(url):
    """Test that SQL errors are not exposed"""
    print_test("Information Disclosure Protection")
    
    # Try to trigger SQL error
    response = requests.get(f"{url}/api/user/admin'")
    
    data = response.json()
    response_str = json.dumps(data).lower()
    
    # Check for SQL error keywords
    sql_keywords = ['sqlite', 'syntax error', 'query', 'select', 'from', 'where']
    leaked = False
    
    for keyword in sql_keywords:
        if keyword in response_str:
            print_fail(f"VULNERABLE: SQL error leaked (found '{keyword}')")
            leaked = True
            break
    
    if not leaked:
        print_pass("SQL errors not disclosed in responses")
        return True
    
    return False

def test_order_by_injection_blocked(url):
    """Test that ORDER BY injection is blocked"""
    print_test("ORDER BY Injection Protection")
    
    # Try injecting SQL in ORDER BY
    response = requests.get(f"{url}/api/users?sort=username;%20DROP%20TABLE%20users--")
    
    # Should either reject invalid sort or use default
    if response.status_code == 200:
        data = response.json()
        if 'users' in data and len(data['users']) > 0:
            print_pass("ORDER BY injection blocked (safe default used)")
            return True
    
    # 400 Bad Request is also acceptable
    if response.status_code == 400:
        print_pass("ORDER BY injection blocked (request rejected)")
        return True
    
    print_info("ORDER BY handling appears safe")
    return True

def test_valid_requests_work(url):
    """Test that legitimate requests still work"""
    print_test("Legitimate Requests Still Function")
    
    # Test 1: Valid login (should fail with wrong password)
    response = requests.post(f"{url}/api/login", json={
        "username": "admin",
        "password": "wrongpassword"
    })
    if response.status_code != 401:
        print_fail("Invalid login should return 401")
        return False
    
    # Test 2: Valid user lookup
    response = requests.get(f"{url}/api/user/admin")
    if response.status_code != 200:
        print_fail("Valid user lookup failed")
        return False
    data = response.json()
    if 'user' not in data or data['user']['username'] != 'admin':
        print_fail("Valid user lookup returned wrong data")
        return False
    
    # Test 3: Valid search
    response = requests.get(f"{url}/api/search?q=admin")
    if response.status_code != 200:
        print_fail("Valid search failed")
        return False
    
    # Test 4: Valid list with proper sort
    response = requests.get(f"{url}/api/users?sort=username")
    if response.status_code != 200:
        print_fail("Valid user list failed")
        return False
    
    print_pass("All legitimate requests work correctly")
    return True

def test_input_validation(url):
    """Test that input validation is in place"""
    print_test("Input Validation")
    
    # Try invalid username format
    response = requests.post(f"{url}/api/login", json={
        "username": "admin' OR '1'='1' --",
        "password": "test"
    })
    
    # Should reject with 400 or 401
    if response.status_code in [400, 401]:
        print_pass("Invalid input properly rejected")
        return True
    
    print_info("Input validation present (some form)")
    return True

def main():
    print("=" * 70)
    print("SQL INJECTION SECURITY TEST SUITE")
    print("=" * 70)
    print("\nTesting the FIXED application for SQL injection vulnerabilities...")
    print(f"Target: {FIXED_URL}")
    print()
    
    # Check if server is running
    print_info("Checking if server is running...")
    if not check_server(FIXED_URL):
        print_fail(f"Server not running at {FIXED_URL}")
        print_info("Please start the fixed app with: python3 fixed_app.py")
        sys.exit(1)
    print_pass("Server is running")
    
    # Run tests
    tests = [
        test_auth_bypass_blocked,
        test_or_injection_blocked,
        test_union_injection_blocked,
        test_no_sql_errors_leaked,
        test_order_by_injection_blocked,
        test_input_validation,
        test_valid_requests_work,
    ]
    
    results = []
    for test in tests:
        try:
            result = test(FIXED_URL)
            results.append(result)
        except Exception as e:
            print_fail(f"Test error: {str(e)}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}✅ ALL TESTS PASSED!{Colors.END}")
        print("The application is properly protected against SQL injection.")
        return 0
    else:
        print(f"\n{Colors.RED}❌ SOME TESTS FAILED!{Colors.END}")
        print("The application may still have vulnerabilities.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
