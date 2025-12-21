# Postman Collections for Authentication Testing

This directory contains Postman collections for testing different authentication methods.

## 📁 Collections

### 1. Session-Auth-Collection.json
Tests session-based authentication with cookies.

**Import into Postman:**
1. Open Postman
2. Click "Import"
3. Select `Session-Auth-Collection.json`
4. Collection will appear in left sidebar

**Usage:**
1. Start the session auth server: `python examples/01_session_auth.py`
2. Run requests in order (1-7)
3. Postman automatically manages cookies

**Variables:**
- `baseUrl`: http://localhost:5000
- `username`: testuser
- `password`: securepass123
- `email`: testuser@example.com

### 2. JWT-Auth-Collection.json
Tests JWT-based authentication with access and refresh tokens.

**Import and Setup:**
1. Import collection into Postman
2. Create environment or use collection variables
3. Start JWT auth server: `python examples/02_jwt_auth.py`

**Automatic Token Management:**
The collection automatically:
- Saves access_token from login response
- Saves refresh_token from login response
- Uses tokens in subsequent requests
- Updates tokens after refresh

**Variables:**
- `baseUrl`: http://localhost:5001
- `username`: jwtuser
- `password`: securepass456
- `email`: jwtuser@example.com
- `access_token`: (auto-populated)
- `refresh_token`: (auto-populated)

## 🚀 Quick Start

### Method 1: Run Entire Collection

1. Import collection
2. Click on collection name
3. Click "Run" button
4. Select requests to run
5. Click "Run Collection"
6. View test results

### Method 2: Run Individual Requests

1. Import collection
2. Make sure server is running
3. Click on individual request
4. Click "Send"
5. View response and test results

## 📊 Test Scripts

Each request includes automated tests that verify:

### Session Auth Tests
- ✅ Correct status codes
- ✅ Session cookies are set
- ✅ Login/logout messages
- ✅ Profile data structure
- ✅ Authentication state

### JWT Auth Tests
- ✅ Tokens are received
- ✅ Token format is correct
- ✅ Bearer authentication works
- ✅ Token refresh works
- ✅ Revoked tokens fail

## 🔧 Customization

### Change Variables

**Method 1: Collection Variables**
1. Click on collection
2. Go to "Variables" tab
3. Edit values
4. Save

**Method 2: Environment**
1. Create new environment
2. Add variables:
   - baseUrl
   - username
   - password
   - email
3. Select environment in top-right dropdown

### Add Custom Tests

Example test script:
```javascript
// Check response time
pm.test("Response time is less than 200ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(200);
});

// Check specific field value
pm.test("Username is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.username).to.eql(pm.variables.get("username"));
});

// Save data for next request
var jsonData = pm.response.json();
pm.environment.set("userId", jsonData.id);
```

## 📝 Creating Your Own Collection

### Basic Structure

```json
{
  "info": {
    "name": "My Auth Collection",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Login",
      "request": {
        "method": "POST",
        "url": "{{baseUrl}}/login",
        "body": {
          "mode": "raw",
          "raw": "{\"username\":\"{{username}}\",\"password\":\"{{password}}\"}"
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test(\"Login successful\", function () {",
              "    pm.response.to.have.status(200);",
              "});"
            ]
          }
        }
      ]
    }
  ]
}
```

## 🎯 Best Practices

1. **Run in Order**: Authentication collections should be run sequentially
2. **Check Environment**: Make sure correct environment is selected
3. **Server Running**: Verify the server is running on correct port
4. **Clean State**: Register new users to avoid conflicts
5. **Review Tests**: Check test results after each request

## 🐛 Troubleshooting

### Connection Refused
```
Error: connect ECONNREFUSED 127.0.0.1:5000
```
**Solution:** Start the authentication server first

### Cookie Not Saved
**Solution:** 
- Check Postman settings
- Go to Settings → General
- Ensure "Automatically follow redirects" is enabled
- Ensure cookies are enabled

### Token Not Found
```
Error: Cannot read property 'access_token' of undefined
```
**Solution:**
- Run "Login" request first
- Check that test script saves token to environment
- Verify environment is selected

### Test Failures
**Solution:**
- Check server is running
- Verify request body format
- Check variable values
- Review server logs for errors

## 📚 Additional Resources

- [Postman Documentation](https://learning.postman.com/)
- [Postman Test Scripts](https://learning.postman.com/docs/writing-scripts/test-scripts/)
- [Collection Runner](https://learning.postman.com/docs/running-collections/intro-to-collection-runs/)
- [Environment Variables](https://learning.postman.com/docs/sending-requests/variables/)

## 💡 Pro Tips

1. **Use Collection Runner** for automated testing
2. **Export results** to share with team
3. **Use Pre-request Scripts** to generate dynamic data
4. **Chain requests** by saving data in variables
5. **Use monitors** for continuous testing

## 🎓 Learning Exercises

1. **Modify tests** to check additional fields
2. **Add new requests** for other endpoints
3. **Create error scenarios** (wrong password, etc.)
4. **Measure performance** with response time tests
5. **Export collection** and share with others

---

Happy testing! 🎉
