# 🏋️ Exercises: Developer Tools Setup

Practice using each of the essential tools for API development and testing.

## Exercise 1: Browser DevTools Network Tab Mastery 🌐

**Objective**: Become proficient with the browser Network tab.

**Tasks**:
1. Open your browser and press F12
2. Navigate to the Network tab
3. Visit https://jsonplaceholder.typicode.com
4. Click on "Posts" in the website
5. Answer these questions:
   - What HTTP method was used?
   - What was the status code?
   - How long did the request take?
   - What is the Content-Type of the response?
   - Can you see the JSON response data?

**Success Criteria**: You can navigate the Network tab and extract key information.

---

## Exercise 2: Postman GET Request 📬

**Objective**: Make your first API request with Postman.

**Tasks**:
1. Open Postman
2. Create a new request
3. Set method to GET
4. URL: `https://api.github.com/users/github`
5. Click Send
6. Explore the response
7. Save the request to a collection named "Practice"

**Questions**:
- What is the status code?
- What is the value of the "login" field?
- How many public repos does this user have?

**Success Criteria**: You successfully made a request and can read the response.

---

## Exercise 3: curl Basics 💻

**Objective**: Make HTTP requests from the command line.

**Tasks**:
1. Open your terminal
2. Run: `curl https://api.github.com/users/octocat`
3. Make it prettier: `curl https://api.github.com/users/octocat | python -m json.tool`
4. Save to file: `curl https://api.github.com/users/octocat -o octocat.json`
5. View headers only: `curl -I https://api.github.com`

**Success Criteria**: You can make basic curl requests and control the output.

---

## Exercise 4: HTTPie Pretty Requests 🎨

**Objective**: Use HTTPie for user-friendly API testing.

**Tasks**:
1. Install HTTPie: `pip install httpie` (if not already installed)
2. Make a request: `http https://api.github.com/users/octocat`
3. Notice the colored, formatted output
4. Try: `http https://httpbin.org/get User-Agent:MyApp`

**Compare**: How is this different from curl?

**Success Criteria**: You appreciate HTTPie's user-friendly output.

---

## Exercise 5: POST Request Challenge 📤

**Objective**: Send data with POST requests using different tools.

**Task**: Create a new post at https://jsonplaceholder.typicode.com/posts

**Data to send**:
```json
{
  "title": "My First API Test",
  "body": "Testing POST requests",
  "userId": 1
}
```

**Try with**:

**Postman**:
1. Method: POST
2. Body → raw → JSON
3. Paste the data
4. Send

**curl**:
```bash
curl -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"My First API Test","body":"Testing POST requests","userId":1}'
```

**HTTPie**:
```bash
http POST https://jsonplaceholder.typicode.com/posts \
  title="My First API Test" \
  body="Testing POST requests" \
  userId:=1
```

**Questions**:
- Which tool was easiest to use?
- What status code did you get? (Should be 201 Created)
- Can you see the created post ID in the response?

**Success Criteria**: You successfully made POST requests with multiple tools.

---

## Exercise 6: Header Investigation 🔍

**Objective**: Learn to set and view HTTP headers.

**Task**: Make a request to https://httpbin.org/headers with custom headers.

**Add these headers**:
- `User-Agent: NetworkFundamentals/1.0`
- `Accept: application/json`
- `X-Custom-Header: TestValue`

**Try with**:

**Postman**:
1. Headers tab → Add each header
2. Send and verify in response

**curl**:
```bash
curl https://httpbin.org/headers \
  -H "User-Agent: NetworkFundamentals/1.0" \
  -H "Accept: application/json" \
  -H "X-Custom-Header: TestValue"
```

**HTTPie**:
```bash
http https://httpbin.org/headers \
  User-Agent:NetworkFundamentals/1.0 \
  Accept:application/json \
  X-Custom-Header:TestValue
```

**Verify**: Check the response - you should see your custom headers echoed back.

**Success Criteria**: You can set custom headers with any tool.

---

## Exercise 7: Tool Comparison 📊

**Objective**: Understand when to use each tool.

**Task**: For each scenario, choose the best tool and explain why.

**Scenarios**:
1. Quickly checking if an API endpoint is working
2. Testing a complex API with authentication and multiple requests
3. Automating API calls in a bash script
4. Learning about a new API with JSON responses
5. Debugging why a web page isn't loading correctly
6. Sharing API examples with a team

<details>
<summary>💡 Suggested Answers</summary>

1. **curl or HTTPie** - Quick command-line check
2. **Postman** - Complex flows, save requests, manage auth
3. **curl** - Easily integrated into scripts
4. **HTTPie** - Beautiful output for learning
5. **Browser DevTools** - See all page resources and errors
6. **Postman** - Collections can be exported/shared

Remember: Multiple tools can often work - choose what you're comfortable with!
</details>

**Success Criteria**: You understand the strengths of each tool.

---

## Challenge Exercise: API Treasure Hunt 🗺️

**Objective**: Combine all tools to explore an API.

**Task**: Explore the JSONPlaceholder API (https://jsonplaceholder.typicode.com)

**Steps**:
1. Use **Browser DevTools** to visit the site and see what endpoints exist
2. Use **Postman** to:
   - Get all posts
   - Get a specific post by ID
   - Create a new post
   - Save these requests in a collection
3. Use **curl** to get all comments for post #1
4. Use **HTTPie** to create a new user

**Deliverable**: Document what you learned:
- What resources does the API provide?
- What HTTP methods are supported?
- What does a typical response look like?

**Success Criteria**: You can independently explore and test an API.

---

## Mini-Quiz: Tool Knowledge ✅

1. **Which tool is best for seeing all resources loaded by a web page?**
   - [ ] Postman
   - [ ] curl
   - [ ] Browser DevTools
   - [ ] HTTPie

2. **Which tool has the simplest syntax for sending JSON data?**
   - [ ] curl
   - [ ] HTTPie
   - [ ] Postman (tie)
   - [ ] Browser

3. **Which tool is best for automation and scripts?**
   - [ ] Postman
   - [ ] Browser DevTools
   - [ ] curl
   - [ ] HTTPie

4. **Which tool requires no installation on most systems?**
   - [ ] Postman
   - [ ] HTTPie
   - [ ] curl
   - [ ] None (all require installation)

5. **Which tool provides a GUI for organizing and sharing API requests?**
   - [ ] curl
   - [ ] HTTPie
   - [ ] Postman
   - [ ] Browser DevTools

<details>
<summary>Show Answers</summary>

1. **C** - Browser DevTools (Network tab shows everything)
2. **B** - HTTPie (simple key=value syntax)
3. **C** - curl (widely available, easy to script)
4. **C** - curl (pre-installed on Mac/Linux, available on Windows)
5. **C** - Postman (Collections feature)

**Scoring**:
- 5/5: Excellent! You understand each tool's purpose!
- 3-4/5: Good! Review the tool comparison.
- 1-2/5: Revisit the lesson and practice more.
</details>

---

## What's Next?

Once you're comfortable with these tools, you're ready to dive into [HTTP Fundamentals](../04-HTTP-Fundamentals/)!

---

[← Back to Lesson](./README.md)
