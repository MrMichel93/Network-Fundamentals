# 🌐 Networking Fundamentals Course

Welcome to the **Networking Fundamentals** course! This comprehensive course is designed for beginner to intermediate programmers who want to understand how networked applications communicate.

## 🎯 Course Overview

This course will take you from basic networking concepts to building real-time web applications. You'll learn how data flows across the internet, how to build and consume APIs, and how to create interactive networked applications.

**Estimated Time:** 4-6 weeks (2-3 hours per week)  
**Target Audience:** High school students or self-learners with basic programming knowledge

## 📚 What You'll Learn

### Core Concepts
- How the internet and the web work (IP addresses, DNS, routing, packets)
- HTTP protocol and web communication fundamentals
- URLs, domains, and how browsers work
- Network layers and the OSI model (simplified)

### Developer Tools & Skills
- Browser DevTools (especially Network tab)
- Postman, curl, and HTTPie for API testing
- Reading and working with API documentation
- Debugging network issues

### API Development
- Building and consuming RESTful APIs
- Database integration (SQL and NoSQL)
- CRUD operations with persistence
- API design best practices

### Security
- Authentication vs Authorization
- Session-based and token-based auth (JWT)
- OAuth 2.0 and API keys
- Input validation and sanitization
- SQL injection and XSS prevention
- HTTPS, TLS/SSL, and certificates
- Rate limiting and CORS
- Comprehensive security best practices

### Advanced Topics
- Real-time communication with WebSockets
- Understanding different network protocols (TCP, UDP, FTP, SMTP, SSH)
- Network security standards (OWASP Top 10)
- Defense in depth strategies

## 🗂️ Course Structure

> **📦 Note**: The course has been restructured! See [MIGRATION.md](./MIGRATION.md) for details.

### [00. Prerequisites](./00-Prerequisites/)
Get ready for the course! Learn what you need to know before starting.

### [01. Internet Basics](./01-Internet-Basics/) ✨ NEW
Understand how data travels, IP addresses, DNS, network layers, and the fundamentals of internet communication.

### [02. How The Web Works](./02-How-The-Web-Works/) ✨ NEW
Learn about clients and servers, URLs and domains, and how browsers work behind the scenes.

### [03. Developer Tools Setup](./03-Developer-Tools-Setup/) ✨ NEW
Master browser DevTools, Postman, curl, and HTTPie for testing and debugging networked applications.

### [04. HTTP Fundamentals](./04-HTTP-Fundamentals/)
Deep dive into the HTTP protocol, request/response cycle, methods, status codes, and headers.

### [05. Working With APIs](./05-Working-With-APIs/) ✨ NEW
Make requests with different tools, read API documentation, handle responses, and work with real APIs.

### [06. Authentication and Authorization](./06-Authentication-and-Authorization/) ✨ NEW ⭐ CRITICAL
Learn about session-based auth, JWT tokens, OAuth 2.0, API keys, and security best practices.

### [07. REST API Design](./07-REST-API-Design/)
Master RESTful principles, resource design, CRUD operations, and API best practices.

### [08. Databases for APIs](./08-Databases-for-APIs/) ✨ NEW ⭐ CRITICAL
Connect APIs to databases (SQL and NoSQL), implement data persistence, and design database schemas.

### [09. API Security](./09-API-Security/) ✨ NEW
Input validation, rate limiting, CORS, SQL injection prevention, and XSS protection.

### [10. WebSockets](./10-WebSockets/)
Explore real-time communication, understand when to use WebSockets, and build interactive applications.

### [11. Other Protocols](./11-Other-Protocols/)
Learn about TCP, UDP, FTP, SMTP, SSH protocols and when to use each.

### [12. HTTPS and TLS](./12-HTTPS-and-TLS/) ✨ EXPANDED
Understand encryption, certificates, man-in-the-middle attacks, and how to set up HTTPS.

### [13. Network Security Best Practices](./13-Network-Security-Best-Practices/) ✨ EXPANDED
Comprehensive security review, defense in depth, security testing, and OWASP Top 10.

### Supporting Resources

#### [Debugging Exercises](./debugging-exercises/) ✨ NEW
Tool-specific practice exercises for debugging common networking issues.

#### [API Examples](./api-examples/) ✨ NEW
Sample API implementations you can run locally for hands-on practice.

#### [Security Labs](./security-labs/) ✨ NEW
Practical security exercises and penetration testing scenarios in a safe environment.

#### [Architecture Diagrams](./architecture-diagrams/) ✨ NEW
Visual representations of networking concepts and system architectures.

#### [Interview Prep](./interview-prep/) ✨ NEW
Networking interview questions, answers, and preparation materials.

### [Projects](./Projects/)
Apply your knowledge with three progressive hands-on projects:
1. Weather API Client
2. URL Shortener Service
3. Real-time Dashboard

### [Resources](./Resources/)
Additional materials including glossary, tools guide, and further reading.

## 🛠️ Prerequisites

Before starting this course, you should have:

- Basic programming knowledge in Python or JavaScript
- Familiarity with the command line/terminal
- A text editor or IDE installed
- Python 3.7+ installed on your computer

Don't worry if you're not an expert - we'll guide you through everything!

## 💻 Setup Instructions

1. **Clone this repository:**
   ```bash
   git clone https://github.com/MrMichel93/Network-Fundamentals.git
   cd Network-Fundamentals
   ```

2. **Set up Python environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   python --version
   pip list
   ```

For detailed setup instructions for different operating systems, see [setup.md](./setup.md).

## 📖 How to Use This Course

1. **Follow the modules in order** - Each module builds on previous knowledge
2. **Read the lessons carefully** - Take notes and try to understand concepts before moving to code
3. **Run all code examples** - Type them out yourself rather than copy-pasting
4. **Complete the exercises** - This is where real learning happens!
5. **Build the projects** - Apply multiple concepts together
6. **Use the hints** - If you get stuck, check the expandable hint sections
7. **Review solutions** - After attempting exercises, compare with provided solutions

## 🎓 Learning Path

> **New for 2024**: The course has been expanded from 7 to 14 modules with critical additions in authentication, databases, and security!

```
Prerequisites → Internet Basics → Web Fundamentals → Developer Tools → 
HTTP → APIs → Authentication → REST Design → Databases → 
Security → WebSockets → Other Protocols → HTTPS → Best Practices → Projects
```

### Recommended Pace (8 weeks):

**Week 1: Foundation**
- 00: Prerequisites
- 01: Internet Basics  
- 02: How The Web Works

**Week 2: HTTP & Tools**
- 03: Developer Tools Setup
- 04: HTTP Fundamentals

**Week 3: Working with APIs**
- 05: Working With APIs
- 06: Authentication and Authorization ⭐

**Week 4: Building APIs**
- 07: REST API Design
- 08: Databases for APIs ⭐

**Week 5: Security**
- 09: API Security
- 12: HTTPS and TLS

**Week 6: Advanced Topics**
- 10: WebSockets
- 11: Other Protocols

**Week 7: Security Deep Dive**
- 13: Network Security Best Practices
- Review security modules

**Week 8: Projects**
- Complete the three progressive projects
- Build your own application
- Review and reinforce concepts

## 🧪 Assessment

- **Mini-quizzes** at the end of each module (self-graded)
- **Hands-on exercises** in each lesson (3-5 per module)
- **Three progressive projects** that integrate concepts
- **Final capstone project:** Build a real-time collaborative application

## 🤝 Contributing

Found a bug? Have a suggestion? Want to improve a lesson? Check out our [CONTRIBUTING.md](./CONTRIBUTING.md) guide!

## ❓ FAQ

Having trouble? Check our [FAQ.md](./FAQ.md) for common questions and solutions.

## 📝 License

This course is open source and available for educational purposes.

## 🌟 Get Started!

Ready to dive in? Head over to [00-Prerequisites](./00-Prerequisites/) to begin your networking journey!

---

**Happy Learning! 🚀**

If you have questions or need help, feel free to open an issue in this repository.