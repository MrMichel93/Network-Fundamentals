# Project 2: URL Shortener - Requirements

## Learning Objectives
By completing this project, you will:
- [ ] Design and implement a RESTful API
- [ ] Perform CRUD (Create, Read, Update, Delete) operations
- [ ] Work with SQL databases (SQLite)
- [ ] Implement URL validation and sanitization
- [ ] Handle HTTP redirects (301/302 status codes)
- [ ] Implement collision detection for short codes
- [ ] Track analytics (click counts)
- [ ] Build a stateless API server
- [ ] Use Postman or curl for API testing

## Requirements

### Functional Requirements

1. **Create Short URL**
   - Accept a long URL from user
   - Generate a unique short code (6 characters by default)
   - Allow optional custom short codes
   - Validate URL format
   - Store mapping in database
   - Return short URL to user

2. **Redirect**
   - Accept short code in URL path
   - Look up original URL in database
   - Redirect user to original URL (301 redirect)
   - Increment click counter
   - Handle non-existent short codes gracefully

3. **List URLs**
   - Retrieve all stored short URLs
   - Display short code, original URL, clicks, created date
   - Support pagination for large datasets
   - Optional: Filter by date range

4. **Get URL Details**
   - Retrieve details for a specific short code
   - Display statistics (click count, creation date, last accessed)

5. **Delete URL**
   - Remove a short URL by its short code
   - Confirm deletion was successful
   - Return appropriate HTTP status codes

6. **Track Analytics**
   - Count number of times each short URL is used
   - Store timestamp of creation
   - Optional: Track last accessed time
   - Optional: Track user agent and IP (privacy considerations)

### Non-Functional Requirements

- **Performance**: URL lookup and redirect under 100ms
- **Scalability**: Support at least 10,000 URLs initially
- **Reliability**: Proper database transactions to prevent data loss
- **Security**: 
  - Validate and sanitize all URLs
  - Prevent SQL injection
  - Rate limiting to prevent abuse
  - Prevent access to internal/private URLs
- **Usability**: Clear API documentation with examples
- **Maintainability**: Clean, modular code with proper error handling

## Technical Specifications

**Framework**: Flask (Python) or Express.js (Node.js)  
**Database**: SQLite (for development) or PostgreSQL (for production)  
**API Style**: RESTful  
**Response Format**: JSON  

### Database Schema

```sql
CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_code TEXT UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    clicks INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_short_code ON urls(short_code);
```

### API Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/api/urls` | Create short URL | `{"url": "...", "custom_code": "..."}` | `201 Created` with short URL details |
| GET | `/api/urls` | List all URLs | - | `200 OK` with array of URLs |
| GET | `/api/urls/:code` | Get URL details | - | `200 OK` with URL details or `404 Not Found` |
| DELETE | `/api/urls/:code` | Delete URL | - | `204 No Content` or `404 Not Found` |
| GET | `/:code` | Redirect to original URL | - | `301 Moved Permanently` or `404 Not Found` |

## Milestones

### Milestone 1: Project Setup (Due: Week 1, Day 1)
- [ ] Set up project structure
- [ ] Install dependencies (Flask/Express, database driver)
- [ ] Create database schema
- [ ] Initialize database
- [ ] Create basic Flask/Express app

**Success Criteria**: Server starts successfully and can connect to database.

### Milestone 2: Create Short URL (Due: Week 1, Day 2-3)
- [ ] Implement POST `/api/urls` endpoint
- [ ] Generate random short codes (6 alphanumeric characters)
- [ ] Validate URL format (must start with http:// or https://)
- [ ] Check for duplicate short codes
- [ ] Store URL in database
- [ ] Return JSON response with short URL

**Success Criteria**: Can create short URLs via API and store them in database.

### Milestone 3: Redirect Functionality (Due: Week 1, Day 4)
- [ ] Implement GET `/:code` endpoint
- [ ] Look up short code in database
- [ ] Return 301 redirect to original URL
- [ ] Increment click counter
- [ ] Handle non-existent codes (404)

**Success Criteria**: Short URLs redirect to original URLs and clicks are tracked.

### Milestone 4: List and Get URLs (Due: Week 2, Day 1-2)
- [ ] Implement GET `/api/urls` endpoint
- [ ] Implement GET `/api/urls/:code` endpoint
- [ ] Return properly formatted JSON responses
- [ ] Include all metadata (clicks, timestamps)

**Success Criteria**: Can retrieve all URLs and individual URL details via API.

### Milestone 5: Delete and Error Handling (Due: Week 2, Day 3-4)
- [ ] Implement DELETE `/api/urls/:code` endpoint
- [ ] Add comprehensive error handling
- [ ] Return appropriate HTTP status codes
- [ ] Add input validation for all endpoints
- [ ] Sanitize user input

**Success Criteria**: Can delete URLs and all error cases are handled properly.

### Milestone 6: Polish and Testing (Due: Week 2, Day 5-7)
- [ ] Add custom short code support
- [ ] Implement collision handling
- [ ] Add API documentation
- [ ] Write test cases
- [ ] Add logging
- [ ] Create README with examples

**Success Criteria**: Production-ready API with documentation and tests.

## Starter Code

### Python/Flask Template

```python
from flask import Flask, request, jsonify, redirect
import sqlite3
import string
import random

app = Flask(__name__)
DB_NAME = 'shortener.db'

def init_db():
    """Initialize database with schema."""
    # TODO: Implement database initialization
    pass

def generate_short_code(length=6):
    """Generate random short code."""
    # TODO: Implement code generation
    pass

@app.route('/api/urls', methods=['POST'])
def create_url():
    """Create a new short URL."""
    # TODO: Implement URL creation
    pass

@app.route('/<short_code>')
def redirect_url(short_code):
    """Redirect to original URL."""
    # TODO: Implement redirect logic
    pass

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
```

### JavaScript/Express Template

```javascript
const express = require('express');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const port = 3000;

app.use(express.json());

// Initialize database
function initDb() {
    // TODO: Implement database initialization
}

// Generate random short code
function generateShortCode(length = 6) {
    // TODO: Implement code generation
}

// Create short URL
app.post('/api/urls', (req, res) => {
    // TODO: Implement URL creation
});

// Redirect
app.get('/:code', (req, res) => {
    // TODO: Implement redirect
});

app.listen(port, () => {
    console.log(`URL Shortener listening on port ${port}`);
    initDb();
});
```

## Testing Checklist

### Functional Testing
- [ ] Can create short URL with valid long URL
- [ ] Can create short URL with custom code
- [ ] Random codes are unique
- [ ] Redirects work correctly
- [ ] Click counter increments
- [ ] Can list all URLs
- [ ] Can get details for specific URL
- [ ] Can delete URLs
- [ ] Deleted URLs return 404

### Error Handling Testing
- [ ] Invalid URL format rejected
- [ ] Duplicate custom codes rejected
- [ ] Non-existent short codes return 404
- [ ] Empty request body handled
- [ ] Malformed JSON handled
- [ ] SQL injection attempts blocked
- [ ] Very long URLs handled appropriately

### Edge Cases
- [ ] URLs with special characters
- [ ] URLs with query parameters
- [ ] URLs with fragments (#)
- [ ] Maximum length custom codes
- [ ] Unicode in custom codes
- [ ] Concurrent requests for same custom code

### Security Testing
- [ ] Cannot access internal URLs (localhost, 127.0.0.1, 192.168.x.x)
- [ ] Cannot access file:// URLs
- [ ] SQL injection prevention
- [ ] XSS prevention in returned URLs
- [ ] Rate limiting works

## Rubric

| Criteria | Needs Work (1) | Good (2) | Excellent (3) |
|----------|---------------|----------|---------------|
| **Functionality** | Only create/redirect work | All CRUD operations work | All features + custom codes + analytics |
| **API Design** | Inconsistent endpoints/responses | RESTful with proper HTTP methods | RESTful + proper status codes + well-documented |
| **Database** | Basic storage, no indexes | Proper schema with constraints | Optimized with indexes + transactions |
| **Error Handling** | Returns 500 for errors | Returns appropriate status codes | Comprehensive error handling + validation |
| **Code Quality** | Monolithic, hard to read | Modular with functions | Clean architecture + well-commented |
| **Security** | No validation | Basic URL validation | Input sanitization + SQL injection prevention + URL blacklist |
| **Testing** | No testing | Manual testing with curl | Automated tests + edge cases covered |

**Scoring**:
- 19-21 points: Excellent (Production-ready)
- 14-18 points: Good (Functional with minor improvements needed)
- 7-13 points: Needs Work (Core functionality incomplete)
- Below 7: Incomplete

## Extensions (Optional)

### Beginner Extensions
- [ ] Add expiration dates for URLs (auto-delete after X days)
- [ ] QR code generation for short URLs
- [ ] Simple web interface for creating URLs
- [ ] Export URL list to CSV

### Intermediate Extensions
- [ ] Password-protected URLs (require password to access)
- [ ] Custom vanity domains (short.ly vs custom.com)
- [ ] URL preview page (show destination before redirect)
- [ ] Analytics dashboard (graphs of clicks over time)
- [ ] Bulk URL shortening (upload CSV)
- [ ] API rate limiting per IP
- [ ] URL categories/tags

### Advanced Extensions
- [ ] User accounts and authentication (JWT)
- [ ] API key management for programmatic access
- [ ] Real-time analytics with WebSockets
- [ ] URL health checking (check if destination is still valid)
- [ ] Geographic analytics (track where clicks come from)
- [ ] A/B testing (multiple destinations for same short code)
- [ ] Webhook notifications on URL access
- [ ] Custom redirect rules (time-based, device-based)

## Common Pitfalls to Avoid

1. **Not checking for collisions**: Always verify generated codes are unique
2. **Using 302 instead of 301**: Use 301 for permanent redirects (better for SEO)
3. **No URL validation**: Always validate URLs before storing
4. **Allowing internal URLs**: Prevent access to localhost/private IPs
5. **Not sanitizing input**: Protect against SQL injection and XSS
6. **Poor error messages**: Return helpful, specific error messages
7. **No database indexes**: Always index the short_code column
8. **Not handling concurrent requests**: Use database constraints to prevent duplicates
9. **Forgetting to increment clicks**: Use atomic operations for counters

## Resources

- [REST API Best Practices](https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Express.js Documentation](https://expressjs.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [URL Validation in Python](https://docs.python.org/3/library/urllib.parse.html)
- [HTTP Redirects](https://developer.mozilla.org/en-US/docs/Web/HTTP/Redirections)

## Next Steps

Once you complete this project, move on to [Project 3: Real-Time Dashboard](./03-realtime-dashboard.md) to learn about WebSockets and real-time communication!

---

[Back to Projects](./README.md)
