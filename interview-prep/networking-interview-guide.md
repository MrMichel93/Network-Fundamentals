# Networking Concepts Interview Preparation

## Common Question Categories

### 1. Fundamentals
- "Explain how the internet works"
- "What happens when you type google.com in your browser?"
- "What is DNS and how does it work?"
- "Difference between TCP and UDP"

### 2. HTTP/APIs
- "Explain REST and RESTful APIs"
- "What are HTTP status codes?"
- "Difference between GET and POST"
- "What is CORS and why does it exist?"

### 3. Security
- "How does HTTPS work?"
- "What is SQL injection?"
- "Explain authentication vs authorization"
- "What are some ways to secure an API?"

### 4. Debugging
- "How would you debug a failing API call?"
- "User reports slow website - how do you investigate?"
- "API returns 500 error - what do you check?"

## Answer Framework

For "What happens when you type URL in browser":

1. **DNS Resolution**
   - Browser checks cache
   - Queries DNS server
   - Gets IP address

2. **TCP Connection**
   - Three-way handshake
   - SYN, SYN-ACK, ACK

3. **HTTP Request**
   - Browser sends GET request
   - Includes headers

4. **Server Processing**
   - Server receives request
   - Processes it
   - Generates response

5. **HTTP Response**
   - Status code
   - Headers
   - Body (HTML)

6. **Rendering**
   - Browser parses HTML
   - Loads additional resources
   - Renders page

**Interviewer likes:**
- Mentioning caching
- Discussing HTTPS/TLS
- Noting parallel requests
- Understanding depth

**Red flags:**
- Vague answers
- Missing key steps
- Can't explain basics
