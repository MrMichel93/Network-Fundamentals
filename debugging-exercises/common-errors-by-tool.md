# Common Errors and How to Debug Them

A comprehensive guide to identifying and fixing common errors when working with web APIs and network debugging tools.

---

## Browser DevTools Debugging

### Error: Request failed with status 404

**What you see in DevTools:**
- Red text in Network tab
- Status: 404
- Response: "Not Found"

**Debugging steps:**
1. Click on the failed request
2. Check the Request URL - is it spelled correctly?
3. Check the Response tab - does the server say why?
4. Verify the endpoint exists (check API documentation)

**Common causes:**
- Typo in URL
- API endpoint changed
- Wrong HTTP method
- Server not running

---

### Error: CORS policy blocking request

**What you see:**
```
Access to fetch at 'http://api.example.com' from origin 
'http://localhost:3000' has been blocked by CORS policy
```

**What it means:**
Browser is protecting you from potential security issues

**Debugging steps:**
1. Check if server allows your origin
2. Verify server sends CORS headers
3. Check if using correct HTTP method

**Solutions:**
- Configure CORS on server
- Use a proxy in development
- Test with Postman (bypasses CORS)

---

### Error: 401 Unauthorized

**What you see:**
- Status: 401
- Response: "Unauthorized" or "Authentication required"

**Debugging steps:**
1. Check the Headers tab - is Authorization header present?
2. Verify token/API key format (Bearer token, API-Key, etc.)
3. Check if token has expired
4. Confirm credentials are correct

**Common causes:**
- Missing or malformed Authorization header
- Expired session or JWT token
- Wrong authentication scheme (Basic vs Bearer)
- Token not included in request

---

### Error: 500 Internal Server Error

**What you see:**
- Status: 500
- Generic error message or stack trace

**Debugging steps:**
1. Check the Response tab for error details
2. Look at the Payload tab to see what you sent
3. Try the same request with different data
4. Check server logs if you have access

**Common causes:**
- Server-side bug
- Invalid data format sent to server
- Database connection issues
- Missing required fields

---

### Error: Request timeout

**What you see:**
- Request hangs in "pending" state
- Eventually fails with timeout error

**Debugging steps:**
1. Check the Timing tab to see where time was spent
2. Verify server is running and accessible
3. Look for slow database queries or external API calls
4. Check if request size is too large

**Solutions:**
- Increase timeout limit
- Optimize server-side processing
- Use pagination for large datasets
- Implement caching

---

### Error: Mixed Content (HTTP/HTTPS)

**What you see:**
```
Mixed Content: The page at 'https://example.com' was loaded over 
HTTPS, but requested an insecure resource 'http://api.example.com'
```

**Debugging steps:**
1. Identify which resources are using HTTP
2. Check if HTTPS version is available
3. Update URLs to use HTTPS

**Solutions:**
- Use HTTPS for all resources
- Update API endpoint URLs
- Configure server to redirect HTTP to HTTPS

---

### Error: Failed to fetch / Network Error

**What you see:**
- Generic "Failed to fetch" or "Network Error"
- No status code shown

**Debugging steps:**
1. Check Console tab for detailed error
2. Verify internet connection
3. Check if browser extensions are blocking
4. Test in incognito mode

**Common causes:**
- Ad blockers or privacy extensions
- No internet connection
- Server is down
- DNS resolution failure
- Firewall blocking request

---

### Error: 403 Forbidden

**What you see:**
- Status: 403
- Message: "Forbidden" or "Access Denied"

**Debugging steps:**
1. Verify you have permission to access resource
2. Check if API key/token has correct scopes
3. Look for IP restrictions or rate limiting
4. Confirm request method is allowed

**Common causes:**
- Insufficient permissions
- IP address not whitelisted
- API rate limit exceeded
- Resource requires different authentication level

---

### Error: 400 Bad Request

**What you see:**
- Status: 400
- Message: "Bad Request" or validation error

**Debugging steps:**
1. Check the Payload tab - is JSON valid?
2. Verify required fields are included
3. Check data types (string vs number)
4. Look at Response for validation errors

**Common causes:**
- Invalid JSON syntax
- Missing required fields
- Wrong data type for field
- Invalid parameter values

---

### Error: Preflight request failure (OPTIONS)

**What you see:**
- OPTIONS request fails before actual request
- CORS error message

**Debugging steps:**
1. Check if server handles OPTIONS requests
2. Verify CORS headers in OPTIONS response
3. Check if custom headers are allowed
4. Confirm HTTP method is allowed

**Solutions:**
- Configure server to handle OPTIONS
- Add Access-Control-Allow-Headers
- Add Access-Control-Allow-Methods
- Set Access-Control-Max-Age for caching

---

### Error: ERR_CONNECTION_REFUSED

**What you see:**
- Connection refused error
- Cannot reach server

**Debugging steps:**
1. Verify server is running
2. Check port number is correct
3. Confirm firewall isn't blocking
4. Test with curl or Postman

**Common causes:**
- Server not started
- Wrong port number
- Firewall blocking connection
- Server crashed or hung

---

### Error: Large response size warning

**What you see:**
- Warning icon in Network tab
- Slow page load
- Large "Size" column value

**Debugging steps:**
1. Check response size in KB/MB
2. Look at Content-Type (is compression enabled?)
3. Check if response can be paginated
4. Verify images/files are optimized

**Solutions:**
- Enable gzip compression
- Implement pagination
- Optimize images and assets
- Use lazy loading

---

### Error: Cookies not being set

**What you see:**
- Set-Cookie header present but cookie not in Application tab
- Authentication fails on subsequent requests

**Debugging steps:**
1. Check cookie attributes (Secure, SameSite, Domain)
2. Verify you're using HTTPS if Secure flag is set
3. Check if Domain matches current domain
4. Look for SameSite=Strict issues

**Common causes:**
- Secure flag requires HTTPS
- Domain mismatch
- SameSite restrictions
- Cookie expired or invalid

---

### Error: Request headers too large

**What you see:**
- Status: 431 Request Header Fields Too Large
- Request fails to complete

**Debugging steps:**
1. Check size of Authorization header
2. Look for large Cookie headers
3. Remove unnecessary custom headers
4. Check for header duplication

**Solutions:**
- Use shorter tokens
- Clear old cookies
- Implement token refresh to avoid long tokens
- Increase server header size limit

---

### Error: Content-Type mismatch

**What you see:**
- Server returns unexpected data
- Parse errors in JavaScript

**Debugging steps:**
1. Check Response Headers for Content-Type
2. Verify Accept header in request
3. Compare expected vs actual content type
4. Look at raw response data

**Common causes:**
- Server returns HTML instead of JSON
- Wrong Accept header sent
- Server error page instead of API response
- Incorrect Content-Type in POST/PUT

---

## Postman Debugging

### Error: Could not get any response

**Symptoms:**
- Request hangs
- Eventually times out
- "Could not get any response" message

**Debugging steps:**
1. Check if server is running
2. Verify URL and port
3. Check firewall settings
4. Try in browser or curl
5. Disable SSL verification (for local dev only)
6. Check proxy settings

**Common causes:**
- Server not running
- Firewall blocking Postman
- Wrong URL or port
- SSL certificate issues
- Proxy configuration

---

### Error: SSL certificate verification failed

**What you see:**
```
Error: unable to verify the first certificate
```

**Debugging steps:**
1. Check if using self-signed certificate
2. Verify certificate is valid
3. Temporarily disable SSL verification in Settings

**Solutions:**
- Install proper SSL certificate
- Add CA certificate to Postman
- Disable SSL verification (dev only)
- Use HTTP for local development

---

### Error: Variables not resolving

**What you see:**
- `{{variable}}` appears literally in request
- URL shows `{{baseUrl}}` instead of actual value

**Debugging steps:**
1. Check if variable is defined in correct scope
2. Verify variable name spelling
3. Look at environment/globals panel
4. Check which environment is active

**Solutions:**
- Define variable in environment
- Select correct environment
- Check variable scope (environment vs collection vs global)
- Use correct variable syntax `{{varName}}`

---

### Error: Request body not being sent

**What you see:**
- Server says "body is required"
- Request shows no body in Postman

**Debugging steps:**
1. Check Body tab is selected
2. Verify correct body type (raw, form-data, etc.)
3. Check Content-Type header matches body type
4. Look at actual request in Console

**Common causes:**
- Forgot to select body type
- Body type doesn't match Content-Type header
- Selected GET request (which shouldn't have body)
- Body is in wrong format

---

### Error: Authentication token not working

**What you see:**
- 401 Unauthorized despite having token
- Token looks correct

**Debugging steps:**
1. Check Authorization tab - is type correct?
2. Verify token is in correct format (Bearer, API-Key, etc.)
3. Check if token has expired
4. Look at actual headers being sent
5. Test token in different tool (curl, browser)

**Solutions:**
- Use correct authorization type
- Refresh expired token
- Check token prefix (Bearer, Token, etc.)
- Verify token is in correct header

---

### Error: 415 Unsupported Media Type

**What you see:**
- Status: 415
- Server can't process request body

**Debugging steps:**
1. Check Content-Type header
2. Verify body format matches Content-Type
3. Check if server accepts that content type
4. Look at API documentation

**Solutions:**
- Set Content-Type to application/json
- Use correct body format for endpoint
- Match Content-Type to body data type

---

### Error: Collection runner failing

**What you see:**
- Tests pass individually but fail in runner
- Inconsistent results

**Debugging steps:**
1. Check if requests depend on each other
2. Verify delay between requests
3. Look at test scripts for state issues
4. Check if data is being shared correctly

**Solutions:**
- Add delays between requests
- Use proper variable scoping
- Reset state between iterations
- Check test order dependencies

---

### Error: Tests not running

**What you see:**
- Test tab shows no results
- Tests defined but not executing

**Debugging steps:**
1. Check JavaScript syntax in Tests tab
2. Look at Postman Console for errors
3. Verify pm.test() syntax is correct
4. Check if response arrived successfully

**Common causes:**
- JavaScript syntax error
- Using console.log instead of pm.test
- Request failed so tests didn't run
- Tests in Pre-request instead of Tests tab

---

### Error: Form-data not working

**What you see:**
- Server doesn't receive form fields
- 400 Bad Request or missing field errors

**Debugging steps:**
1. Verify form-data is selected (not raw)
2. Check if keys are enabled (checkboxes)
3. Look at Content-Type (should be multipart/form-data)
4. Verify field names match API requirements

**Solutions:**
- Select form-data body type
- Enable checkboxes for all fields
- Use correct field names
- Check for file upload requirements

---

### Error: Response too large to display

**What you see:**
- "Response too large" warning
- Can't view response body

**Debugging steps:**
1. Check response size
2. Try downloading response
3. Add pagination parameters
4. Filter response data

**Solutions:**
- Implement pagination
- Request specific fields only
- Download and view in external editor
- Reduce dataset size

---

### Error: Proxy authentication required

**What you see:**
- Status: 407 Proxy Authentication Required
- Can't reach internet

**Debugging steps:**
1. Check Postman proxy settings
2. Verify corporate proxy credentials
3. Try system proxy vs custom proxy
4. Disable proxy if not needed

**Solutions:**
- Configure proxy in Settings
- Enter proxy credentials
- Use system proxy settings
- Bypass proxy for localhost

---

### Error: Cookie authentication not persisting

**What you see:**
- Login works but subsequent requests fail
- Cookies not being sent

**Debugging steps:**
1. Check if cookies are enabled in Postman
2. Verify cookie domain matches request URL
3. Look in Cookies manager
4. Check for SameSite or Secure flags

**Solutions:**
- Enable cookie handling in Settings
- Use same domain for all requests
- Check cookie attributes
- Use collection variables for session tokens instead

---

### Error: Environment variables overriding collection variables

**What you see:**
- Unexpected variable values
- Variables changing between environments

**Debugging steps:**
1. Check variable scope precedence
2. Hover over {{variable}} to see which value is used
3. Look at both environment and collection variables
4. Check for conflicts

**Understanding scope:**
- Global > Environment > Collection > Local
- Higher precedence wins

---

### Error: Pre-request script failing silently

**What you see:**
- Request doesn't work as expected
- Variables not set

**Debugging steps:**
1. Open Postman Console (View > Show Postman Console)
2. Check for JavaScript errors
3. Add console.log() statements
4. Verify script logic

**Common causes:**
- JavaScript syntax error
- Async operations not handled
- Wrong variable scope (pm.environment vs pm.globals)
- Logic errors

---

### Error: File upload not working

**What you see:**
- File field empty on server
- 400 Bad Request

**Debugging steps:**
1. Verify using form-data (not raw)
2. Check file field type is set to "File"
3. Confirm file is selected
4. Check server expects multipart/form-data

**Solutions:**
- Select form-data body type
- Change field type from "Text" to "File"
- Select actual file
- Match field name with server expectations

---

### Error: Request chaining not working

**What you see:**
- Second request uses wrong data
- Variables not passing between requests

**Debugging steps:**
1. Check if first request completes successfully
2. Verify pm.environment.set() or pm.collectionVariables.set() is used
3. Look at test scripts for variable extraction
4. Check variable syntax in second request

**Solutions:**
- Extract data in Tests tab of first request
- Use pm.environment.set('key', value)
- Reference with {{key}} in next request
- Ensure proper execution order

---

## curl Debugging

### Error: curl: (6) Could not resolve host

**What it means:**
DNS cannot find the domain

**Debugging steps:**
```bash
# Check if domain exists
nslookup example.com

# Check internet connection
ping 8.8.8.8

# Try with IP address directly
curl http://93.184.216.34

# Check /etc/hosts file
cat /etc/hosts | grep example
```

**Common causes:**
- Typo in domain name
- Domain doesn't exist
- DNS server issues
- No internet connection
- Firewall blocking DNS

---

### Error: curl: (7) Failed to connect

**What it means:**
Can't establish TCP connection to server

**Debugging steps:**
```bash
# Check if server is listening on port
telnet example.com 80

# Try different port
curl http://example.com:8080

# Check firewall
curl -v http://example.com

# Test with timeout
curl --connect-timeout 5 http://example.com
```

**Common causes:**
- Server is down
- Wrong port number
- Firewall blocking
- Network unreachable

---

### Error: curl: (35) SSL connect error

**What it means:**
SSL/TLS handshake failed

**Debugging steps:**
```bash
# Check SSL certificate
curl -v https://example.com

# Skip certificate verification (insecure!)
curl -k https://example.com

# Use specific TLS version
curl --tlsv1.2 https://example.com

# Check certificate details
openssl s_client -connect example.com:443
```

**Common causes:**
- Self-signed certificate
- Expired certificate
- Wrong TLS version
- Certificate name mismatch

---

### Error: curl: (3) URL malformed

**What it means:**
Invalid URL syntax

**Debugging steps:**
```bash
# Check URL format
curl "http://example.com/api/users"

# Encode special characters
curl "http://example.com/api/search?q=test%20query"

# Use quotes around URL
curl 'http://example.com/path?param=value&other=value'
```

**Solutions:**
- Add http:// or https:// prefix
- Quote URLs with special characters
- Encode spaces and special characters
- Check for typos

---

### Error: curl: (22) HTTP response code said error

**What it means:**
Server returned 4xx or 5xx status code (when using -f flag)

**Debugging steps:**
```bash
# Remove -f to see actual response
curl http://example.com/api/users

# Add verbose output
curl -v http://example.com/api/users

# Show just headers
curl -I http://example.com/api/users

# Include response headers in output
curl -i http://example.com/api/users
```

**Understanding:**
- -f makes curl fail silently on HTTP errors
- Remove -f to see error message
- Use -v for detailed debugging

---

### Error: curl: (28) Operation timeout

**What it means:**
Request took too long

**Debugging steps:**
```bash
# Increase timeout
curl --max-time 60 http://example.com

# Set connect timeout separately
curl --connect-timeout 10 --max-time 60 http://example.com

# Check response time
curl -w "@curl-time.txt" http://example.com

# Test with head request
curl -I http://example.com
```

**Common causes:**
- Slow server
- Large response
- Network latency
- Default timeout too short

---

### Error: curl: (52) Empty reply from server

**What it means:**
Server accepted connection but sent nothing

**Debugging steps:**
```bash
# Add verbose output
curl -v http://example.com

# Try different protocol version
curl --http1.1 http://example.com

# Check if server is actually running
telnet example.com 80

# Try with different method
curl -X GET http://example.com
```

**Common causes:**
- Server crash
- Wrong protocol version
- Server not fully started
- Backend service down

---

### Error: curl: (56) Recv failure: Connection reset by peer

**What it means:**
Connection was forcibly closed

**Debugging steps:**
```bash
# Retry with verbose
curl -v http://example.com

# Check server logs
# Try with keep-alive disabled
curl -H "Connection: close" http://example.com

# Test with smaller request
curl -X GET http://example.com/health
```

**Common causes:**
- Server timeout
- Reverse proxy reset
- Server crash during request
- Rate limiting

---

### Error: curl: (60) SSL certificate problem

**What it means:**
Can't verify SSL certificate

**Debugging steps:**
```bash
# See certificate details
curl -v https://example.com 2>&1 | grep certificate

# Check certificate chain
openssl s_client -connect example.com:443 -showcerts

# Skip verification (insecure!)
curl -k https://example.com

# Use specific CA bundle
curl --cacert /path/to/ca-bundle.crt https://example.com
```

**Common causes:**
- Self-signed certificate
- Expired certificate
- Missing intermediate certificates
- CA not trusted

---

### Error: Request body not being sent

**What you see:**
Server says no data received

**Debugging steps:**
```bash
# Check data is being sent
curl -v -X POST -d "key=value" http://example.com

# Use --data-binary for files
curl -X POST --data-binary @file.json http://example.com

# Set Content-Type
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}' \
  http://example.com

# Debug with echo
echo '{"key":"value"}' | curl -X POST -d @- http://example.com
```

**Common mistakes:**
- Forgot -d or --data flag
- Wrong Content-Type header
- File path incorrect
- JSON syntax error

---

### Error: JSON parsing error in response

**What you see:**
Can't parse response as JSON

**Debugging steps:**
```bash
# See raw response
curl http://example.com/api/users

# Format JSON output
curl http://example.com/api/users | jq .

# Save response to file
curl -o response.json http://example.com/api/users

# Check Content-Type
curl -I http://example.com/api/users | grep Content-Type
```

**Common causes:**
- Server returns HTML instead of JSON
- Error page instead of API response
- Invalid JSON syntax
- Response is actually empty

---

### Error: Headers not being sent

**What you see:**
Server doesn't receive expected headers

**Debugging steps:**
```bash
# Verify headers are sent
curl -v -H "Authorization: Bearer token123" http://example.com

# Multiple headers
curl -H "Accept: application/json" \
     -H "Authorization: Bearer token123" \
     http://example.com

# Check header format
curl -H "Content-Type: application/json" \
     -d '{"key":"value"}' \
     http://example.com
```

**Common mistakes:**
- Typo in -H flag
- Wrong header format
- Missing quotes around header value
- Header case sensitivity

---

### Error: Redirect not being followed

**What you see:**
Get 301/302 but no final response

**Debugging steps:**
```bash
# Follow redirects
curl -L http://example.com

# Limit redirect count
curl -L --max-redirs 5 http://example.com

# See redirect chain
curl -v -L http://example.com

# Get just headers to see redirect
curl -I http://example.com
```

**Understanding:**
- curl doesn't follow redirects by default
- Use -L or --location to follow
- Check for redirect loops

---

### Error: Cookie not being sent/received

**What you see:**
Authentication fails, session lost

**Debugging steps:**
```bash
# Save cookies to file
curl -c cookies.txt http://example.com/login

# Send cookies from file
curl -b cookies.txt http://example.com/dashboard

# Send specific cookie
curl -b "session=abc123" http://example.com

# Show cookies in response
curl -v http://example.com
```

**Common mistakes:**
- Forgot -b (send) or -c (save) flag
- Cookie file path wrong
- Cookies expired
- Domain mismatch

---

### Error: File download incomplete

**What you see:**
Downloaded file is smaller than expected

**Debugging steps:**
```bash
# Resume download
curl -C - -O http://example.com/large-file.zip

# Show progress
curl -# -O http://example.com/file.zip

# Verify file size
curl -I http://example.com/file.zip | grep Content-Length

# Download with retry
curl --retry 3 -O http://example.com/file.zip
```

**Solutions:**
- Use -C - to resume
- Add --retry for unstable connections
- Check disk space
- Verify network stability

---

## Quick Reference: When to Use Each Tool

| Scenario | Best Tool | Why |
|----------|-----------|-----|
| Web app not loading data | Browser DevTools | See exact requests browser makes |
| Testing API endpoint | Postman | Easy to save, organize, repeat |
| Quick API check | curl | Fastest for simple requests |
| Debugging CORS | Browser DevTools | CORS only affects browsers |
| Testing authentication flow | Postman | Save tokens, chain requests |
| CI/CD pipeline | curl | Scriptable, available everywhere |
| File upload testing | Postman | Easy file selection |
| Checking response headers | curl -I or DevTools | Quick header inspection |
| Performance testing | Browser DevTools | Waterfall view, timing breakdown |
| Debugging SSL issues | curl -v | Detailed SSL handshake info |

---

## General Debugging Workflow

1. **Reproduce the error** - Make sure you can trigger it consistently
2. **Check the basics** - Server running? URL correct? Internet working?
3. **Look at the response** - What does the server say?
4. **Check the request** - What are you sending?
5. **Compare with docs** - Are you following the API specification?
6. **Test in isolation** - Remove complexity, test simplest case
7. **Check the logs** - Server logs, console logs, network logs
8. **Search the error** - Google the exact error message
9. **Ask for help** - Stack Overflow, forums, colleagues

---

[← Back to Debugging Exercises](./README.md)
