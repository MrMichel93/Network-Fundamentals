#!/bin/bash

# curl Examples for HTTP Fundamentals
# This script demonstrates various curl commands for making HTTP requests

echo "╔════════════════════════════════════════════╗"
echo "║   🌐 curl Examples                        ║"
echo "║   HTTP Request Demonstrations             ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Example 1: Simple GET request
echo "========================================"
echo "EXAMPLE 1: Simple GET Request"
echo "========================================"
echo "Command: curl https://api.github.com/users/octocat"
echo ""
curl https://api.github.com/users/octocat
echo ""
echo ""

# Example 2: GET request with pretty-printed JSON (using jq if available)
echo "========================================"
echo "EXAMPLE 2: Pretty JSON (requires jq)"
echo "========================================"
echo "Command: curl https://api.github.com/users/octocat | jq"
echo ""
if command -v jq &> /dev/null; then
    curl -s https://api.github.com/users/octocat | jq '.'
else
    echo "⚠️  jq not installed. Install with: brew install jq (Mac) or apt-get install jq (Linux)"
fi
echo ""
echo ""

# Example 3: Include response headers
echo "========================================"
echo "EXAMPLE 3: Include Headers in Output"
echo "========================================"
echo "Command: curl -i https://httpbin.org/get"
echo ""
curl -i https://httpbin.org/get
echo ""
echo ""

# Example 4: Verbose output (see full request/response)
echo "========================================"
echo "EXAMPLE 4: Verbose Output"
echo "========================================"
echo "Command: curl -v https://httpbin.org/get"
echo ""
curl -v https://httpbin.org/get 2>&1 | head -20
echo "... (truncated for brevity) ..."
echo ""
echo ""

# Example 5: Custom headers
echo "========================================"
echo "EXAMPLE 5: Custom Headers"
echo "========================================"
echo "Command: curl -H 'User-Agent: MyApp/1.0' -H 'Accept: application/json' https://httpbin.org/headers"
echo ""
curl -s -H "User-Agent: MyApp/1.0" -H "Accept: application/json" https://httpbin.org/headers | jq '.' 2>/dev/null || curl -H "User-Agent: MyApp/1.0" -H "Accept: application/json" https://httpbin.org/headers
echo ""
echo ""

# Example 6: POST request with JSON data
echo "========================================"
echo "EXAMPLE 6: POST Request with JSON"
echo "========================================"
echo "Command: curl -X POST -H 'Content-Type: application/json' -d '{\"name\":\"Alice\"}' https://httpbin.org/post"
echo ""
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}' \
  https://httpbin.org/post | jq '.json' 2>/dev/null || curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}' \
  https://httpbin.org/post
echo ""
echo ""

# Example 7: PUT request
echo "========================================"
echo "EXAMPLE 7: PUT Request"
echo "========================================"
echo "Command: curl -X PUT -d '{\"status\":\"updated\"}' https://httpbin.org/put"
echo ""
curl -s -X PUT \
  -H "Content-Type: application/json" \
  -d '{"status":"updated"}' \
  https://httpbin.org/put | jq '.json' 2>/dev/null || curl -X PUT \
  -H "Content-Type: application/json" \
  -d '{"status":"updated"}' \
  https://httpbin.org/put
echo ""
echo ""

# Example 8: DELETE request
echo "========================================"
echo "EXAMPLE 8: DELETE Request"
echo "========================================"
echo "Command: curl -X DELETE https://httpbin.org/delete"
echo ""
curl -s -X DELETE https://httpbin.org/delete | jq '.' 2>/dev/null || curl -X DELETE https://httpbin.org/delete
echo ""
echo ""

# Example 9: Query parameters
echo "========================================"
echo "EXAMPLE 9: Query Parameters"
echo "========================================"
echo "Command: curl 'https://httpbin.org/get?name=Alice&age=25'"
echo ""
curl -s 'https://httpbin.org/get?name=Alice&age=25' | jq '.args' 2>/dev/null || curl 'https://httpbin.org/get?name=Alice&age=25'
echo ""
echo ""

# Example 10: Follow redirects
echo "========================================"
echo "EXAMPLE 10: Follow Redirects"
echo "========================================"
echo "Command: curl -L https://github.com"
echo ""
echo "Without -L: Only gets redirect response"
curl -s -I https://github.com | head -5
echo ""
echo "With -L: Follows redirect to final destination"
curl -s -L -I https://github.com | head -5
echo ""
echo ""

# Example 11: Save response to file
echo "========================================"
echo "EXAMPLE 11: Save to File"
echo "========================================"
echo "Command: curl -o output.json https://api.github.com/users/octocat"
echo ""
curl -s -o /tmp/output.json https://api.github.com/users/octocat
echo "✅ Saved to /tmp/output.json"
ls -lh /tmp/output.json
echo ""
echo ""

# Example 12: Authentication with Bearer token
echo "========================================"
echo "EXAMPLE 12: Bearer Token Authentication"
echo "========================================"
echo "Command: curl -H 'Authorization: Bearer YOUR_TOKEN' https://httpbin.org/bearer"
echo ""
curl -s -H "Authorization: Bearer fake-token-for-demo" https://httpbin.org/bearer | jq '.' 2>/dev/null || curl -H "Authorization: Bearer fake-token-for-demo" https://httpbin.org/bearer
echo ""
echo ""

# Example 13: Test different status codes
echo "========================================"
echo "EXAMPLE 13: Test HTTP Status Codes"
echo "========================================"
echo "Testing different status codes..."
echo ""
for code in 200 201 400 404 500; do
    echo "Status $code:"
    curl -s -o /dev/null -w "  HTTP Status: %{http_code}\n" https://httpbin.org/status/$code
done
echo ""
echo ""

# Example 14: Timing information
echo "========================================"
echo "EXAMPLE 14: Request Timing"
echo "========================================"
echo "Command: curl -w '@-' -o /dev/null -s https://httpbin.org/get"
echo ""
curl -w "\n  DNS Lookup: %{time_namelookup}s\n  Connect: %{time_connect}s\n  Start Transfer: %{time_starttransfer}s\n  Total: %{time_total}s\n" \
     -o /dev/null -s https://httpbin.org/get
echo ""

echo "========================================"
echo "✅ All curl examples completed!"
echo "========================================"
echo ""
echo "💡 Tips:"
echo "  - Add -s for silent mode (no progress bar)"
echo "  - Add -i to include headers in output"
echo "  - Add -v for verbose debugging"
echo "  - Add -L to follow redirects"
echo "  - Use jq to format JSON: curl URL | jq"
echo ""
echo "📚 Learn more: man curl"
