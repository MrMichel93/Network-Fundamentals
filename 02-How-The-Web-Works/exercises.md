# 🏋️ Exercises: How The Web Works

These exercises will help you understand clients, servers, URLs, and browser behavior.

## Exercise 1: URL Dissection 🔍

**Objective**: Master URL structure by breaking down real examples.

**Tasks**:
Analyze these URLs and identify each component:

1. `https://github.com/MrMichel93/Network-Fundamentals`
2. `http://localhost:8080/api/users?page=2&limit=10`
3. `https://www.amazon.com/s?k=networking+books#reviews`
4. `https://mail.google.com:443/mail/u/0/#inbox`

<details>
<summary>💡 Hint</summary>

For each URL, identify:
- Protocol (http or https)
- Domain/Host
- Port (if specified)
- Path
- Query parameters (if any)
- Fragment/Hash (if any)
</details>

**Success Criteria**: You can identify all parts of any URL.

---

## Exercise 2: Browser DevTools Exploration 🛠️

**Objective**: Get comfortable with browser developer tools.

**Tasks**:
1. Open your browser's DevTools (F12)
2. Visit https://example.com
3. Go to the Network tab
4. Refresh the page (Ctrl+R or Cmd+R)
5. Answer these questions:
   - How many HTTP requests were made?
   - What was the total transfer size?
   - How long did the page take to load?
   - What HTTP method was used for the first request?
   - What status code did you receive?

<details>
<summary>💡 Hint</summary>

In the Network tab:
- Each row is one HTTP request
- Click on a request to see details
- Look at the "Headers" tab for method and status
- Bottom of Network tab shows summary (requests, transferred, time)
</details>

**Success Criteria**: You can identify basic network information from DevTools.

---

## Exercise 3: Build URLs 🔨

**Objective**: Practice constructing proper URLs.

**Tasks**:
Build URLs for these scenarios:

1. Secure connection to "mystore.com" homepage
2. Product page for item #42 on mystore.com
3. Search for "blue shirts" on mystore.com
4. Filter search results: blue shirts, size large, under $50
5. Jump to the reviews section of product #42

<details>
<summary>💡 Hint</summary>

Remember the structure:
```
protocol://domain/path?query=parameters#fragment
```

For multiple query parameters, use `&`:
```
?param1=value1&param2=value2
```
</details>

**Success Criteria**: Your URLs follow proper format and accomplish the task.

---

## Exercise 4: Compare HTTP and HTTPS 🔒

**Objective**: Understand the difference between HTTP and HTTPS.

**Tasks**:
1. Visit http://example.com (HTTP) in your browser
2. Look at the address bar - what warning do you see?
3. Visit https://example.com (HTTPS)
4. What changes in the address bar?
5. Use DevTools Network tab - can you see the difference?

**Questions**:
- Which protocol is more secure?
- When should you always use HTTPS?
- What does the padlock icon mean?

<details>
<summary>💡 Hint</summary>

**HTTP**:
- No encryption
- "Not Secure" warning in browser
- Anyone can intercept data

**HTTPS**:
- Encrypted connection
- Padlock icon appears
- Protects sensitive data

**Always use HTTPS for**:
- Login pages
- Payment information
- Personal data
- Anything sensitive
</details>

**Success Criteria**: You can explain why HTTPS is important.

---

## Exercise 5: Trace a Page Load 📊

**Objective**: Understand the sequence of requests when loading a page.

**Tasks**:
1. Open DevTools Network tab
2. Clear it (click the 🚫 icon)
3. Visit a simple website (try https://example.com)
4. Observe the waterfall of requests
5. Answer:
   - Which file loaded first?
   - Were there any CSS or JavaScript files?
   - How many images loaded?
   - What was the total load time?

<details>
<summary>💡 Hint</summary>

In the Network tab:
- Requests appear in chronological order
- First request is usually the HTML document
- Then CSS, JavaScript, images, fonts, etc.
- The waterfall chart shows timing
- Blue line = DOMContentLoaded
- Red line = Load event (everything finished)
</details>

**Success Criteria**: You can explain the sequence of resource loading.

---

## Exercise 6: Cookie Investigation 🍪

**Objective**: See how websites use cookies.

**Tasks**:
1. Open DevTools
2. Go to Application tab (Chrome) or Storage tab (Firefox)
3. Visit your favorite website
4. Look at Cookies section
5. Observe:
   - How many cookies were set?
   - What are their names?
   - When do they expire?
6. Try clearing cookies and reload - what happens?

<details>
<summary>💡 Hint</summary>

**What to look for in cookies**:
- **Name**: What the cookie is called
- **Value**: Data stored (often encoded)
- **Domain**: Which site set it
- **Expires**: When it will be deleted
- **HttpOnly**: If true, JavaScript can't access it (more secure)
- **Secure**: Only sent over HTTPS

Common cookie names:
- `session_id` - Track your session
- `user_id` - Remember who you are
- `preferences` - Remember settings
</details>

**Success Criteria**: You understand what cookies are and can view them.

---

## Exercise 7: Client vs Server Side 🤔

**Objective**: Understand what happens where.

**Categorize these actions** as Client-side or Server-side:

1. Validating an email format before submitting a form
2. Checking if a username is already taken
3. Rendering HTML into a visible page
4. Fetching user data from a database
5. Displaying an alert when you click a button
6. Processing a payment
7. Animating a menu dropdown
8. Logging user actions for analytics

<details>
<summary>💡 Hint</summary>

**Client-side** (happens in the browser):
- Displaying/rendering content
- Form validation (basic)
- Animations and UI interactions
- Running JavaScript

**Server-side** (happens on the server):
- Database operations
- Business logic
- Authentication
- Processing payments
- Secure operations

**Both**:
- Some validation happens on both (client for UX, server for security)
</details>

**Success Criteria**: You understand the client-server division of responsibilities.

---

## Challenge Exercise: Build a Simple URL Shortener Plan 🎯

**Objective**: Design how a URL shortener works.

**Task**: 
Describe how bit.ly or tinyurl.com works. Answer:

1. What happens when you submit a long URL?
2. How does the service create a short code?
3. What happens when someone visits the short URL?
4. Where is the mapping of short→long URL stored?
5. Is this a client-side or server-side operation?

<details>
<summary>💡 Hint</summary>

**URL Shortener Flow**:

1. **User submits long URL** (client → server)
   - POST request with the long URL
   
2. **Server generates short code** (server-side)
   - Random string (e.g., "aBc123")
   - Store mapping in database: aBc123 → https://very-long-url.com/...
   
3. **User gets short URL** (server → client)
   - Return: bit.ly/aBc123
   
4. **Someone clicks short URL** (client → server)
   - GET request to bit.ly/aBc123
   - Server looks up "aBc123" in database
   - Finds original long URL
   - Sends 301 redirect to long URL
   
5. **Browser follows redirect** (automatic)
   - Loads the original long URL

**Key components**:
- Database to store mappings
- Algorithm to generate unique short codes
- Redirect mechanism (HTTP 301/302)
</details>

**Success Criteria**: You can explain the full workflow of a web service.

---

## Mini-Quiz: Test Your Knowledge ✅

1. **What's the difference between the Internet and the Web?**
   - [ ] They're the same thing
   - [ ] Internet is the infrastructure; Web is a service on top of it
   - [ ] Web came first, then the Internet
   - [ ] Internet is only for email

2. **What does HTTPS provide that HTTP doesn't?**
   - [ ] Faster loading
   - [ ] Encryption and security
   - [ ] Better images
   - [ ] Colorful pages

3. **What is a URL fragment (the part after #)?**
   - [ ] Sent to the server for processing
   - [ ] Used by the browser to scroll to a section
   - [ ] An error in the URL
   - [ ] The file extension

4. **When you visit a website, which happens FIRST?**
   - [ ] Browser renders the HTML
   - [ ] DNS lookup to find IP address
   - [ ] CSS files are downloaded
   - [ ] JavaScript executes

5. **Where are cookies stored?**
   - [ ] On the web server
   - [ ] In the cloud
   - [ ] In your browser
   - [ ] In the DNS server

<details>
<summary>Show Answers</summary>

1. **B** - Internet is the infrastructure; Web is a service on top of it
2. **B** - Encryption and security
3. **B** - Used by the browser to scroll to a section
4. **B** - DNS lookup to find IP address
5. **C** - In your browser

**Scoring**:
- 5/5: Excellent! You understand how the web works!
- 3-4/5: Good! Review the concepts you missed.
- 1-2/5: Review the lesson and try again.
</details>

---

## What's Next?

Once you've completed these exercises, you're ready for [Developer Tools Setup](../03-Developer-Tools-Setup/)!

---

[← Back to Lesson](./README.md)
