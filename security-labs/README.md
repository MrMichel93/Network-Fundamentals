# 🛡️ Security Labs

Hands-on security exercises and penetration testing scenarios.

## Purpose

This directory contains practical security exercises where you'll:
- Identify vulnerabilities in real code
- Exploit them safely (in a controlled environment)
- Learn how to fix them properly
- Test your fixes to verify they work

## ⚠️ Important Warning

**The code in this directory contains intentional security vulnerabilities!**

- **NEVER** deploy this code to production
- **NEVER** expose it to the internet
- Only run on localhost (127.0.0.1)
- Use for educational purposes only

## Lab Setup

### Prerequisites

```bash
# Install Python 3.7 or higher
python3 --version

# Install Flask
pip install flask

# Optional: Install testing tools
pip install requests pytest
```

### Running the Vulnerable API

```bash
# Navigate to security-labs directory
cd security-labs

# Run the vulnerable API
python3 vulnerable_api.py
```

The server will start on `http://localhost:5000`

## Lab Exercises

### 📚 Available Labs

Each lab is a complete, hands-on security exercise with vulnerable code, exploitation examples, fixes, and tests.

---

### [Lab 1: SQL Injection](./lab1-sql-injection/)

**What you'll learn:**
- How SQL injection attacks work
- Identifying vulnerable code patterns
- Exploiting SQL injection safely
- Implementing parameterized queries
- Testing security fixes

**Key vulnerabilities:**
- Authentication bypass
- Data extraction (OR-based injection)
- UNION-based SQL injection
- Information disclosure through errors

**Skills gained:**
- Writing secure database queries
- Input validation techniques
- Error handling best practices

[➡️ Start Lab 1](./lab1-sql-injection/)

---

### [Lab 2: XSS (Cross-Site Scripting) Attacks](./lab2-xss-attacks/)

**What you'll learn:**
- Different types of XSS (Stored, Reflected, DOM-based)
- How XSS can steal cookies and session tokens
- Proper output encoding and escaping
- Content Security Policy (CSP) implementation
- Using templating engines securely

**Key vulnerabilities:**
- Stored XSS in comments
- Reflected XSS in search
- Cookie stealing attacks
- Page defacement

**Skills gained:**
- HTML/JavaScript escaping
- Input sanitization
- CSP configuration
- HTTPOnly cookie security

[➡️ Start Lab 2](./lab2-xss-attacks/)

---

### [Lab 3: Broken Authentication](./lab3-broken-authentication/)

**What you'll learn:**
- Common authentication vulnerabilities
- Password storage best practices (bcrypt, salting)
- Secure session management
- JWT implementation and security
- Multi-factor authentication concepts

**Key vulnerabilities:**
- Weak password storage
- Predictable session tokens
- No account lockout
- Session fixation
- Insecure JWT implementation

**Skills gained:**
- Implementing bcrypt password hashing
- Creating secure session tokens
- JWT best practices
- Rate limiting login attempts

[➡️ Start Lab 3](./lab3-broken-authentication/)

---

### [Lab 4: API Security Testing with OWASP ZAP](./lab4-api-security-testing/)

**What you'll learn:**
- Using OWASP ZAP for security testing
- Automated vulnerability scanning
- Manual penetration testing techniques
- Interpreting scan results
- Generating security reports

**Key skills:**
- Installing and configuring ZAP
- Running automated scans
- Manual request testing
- Fuzzing endpoints
- CI/CD integration

**Tools covered:**
- OWASP ZAP
- Proxy interception
- Spider/crawler
- Active scanning
- Report generation

[➡️ Start Lab 4](./lab4-api-security-testing/)

---

### [Lab 5: Rate Limiting](./lab5-rate-limiting/)

**What you'll learn:**
- Why rate limiting is critical
- Different rate limiting algorithms (Token Bucket, Leaky Bucket, Sliding Window)
- Implementing rate limiters with Flask-Limiter
- Testing rate limiters
- Bypass techniques (for educational purposes)

**Key concepts:**
- Fixed window vs sliding window
- Token bucket algorithm
- Redis-backed rate limiting
- Per-user vs per-IP limiting
- Handling rate limit responses

**Skills gained:**
- Implementing production-ready rate limiters
- Load testing APIs
- Preventing DoS attacks
- Building resilient client applications

[➡️ Start Lab 5](./lab5-rate-limiting/)

## 📋 Lab Overview Matrix

| Lab | Topic | Difficulty | Time | Tools Used |
|-----|-------|------------|------|------------|
| 1 | SQL Injection | Beginner | 2-3 hours | Python, Flask, sqlite3 |
| 2 | XSS Attacks | Beginner | 2-3 hours | Python, Flask, JavaScript |
| 3 | Broken Authentication | Intermediate | 3-4 hours | Python, Flask, JWT, bcrypt |
| 4 | API Security Testing | Intermediate | 3-4 hours | OWASP ZAP, Python, Flask |
| 5 | Rate Limiting | Intermediate | 2-3 hours | Python, Flask-Limiter, Redis |

**Total Time:** 12-17 hours

## 🎯 Learning Path

**Recommended Order:**

1. **Start with Lab 1 (SQL Injection)** - Foundation for understanding input validation
2. **Then Lab 2 (XSS)** - Builds on injection concepts, focuses on output encoding
3. **Move to Lab 3 (Authentication)** - Critical for protecting all endpoints
4. **Continue with Lab 5 (Rate Limiting)** - Complements authentication for defense in depth
5. **Finish with Lab 4 (ZAP Testing)** - Comprehensive testing of all learned concepts

**Alternative Path for Tool-First Learners:**

1. Lab 4 (OWASP ZAP) - Learn the tool
2. Use ZAP while doing Labs 1, 2, 3, 5
3. See vulnerabilities from both perspectives

## 🛠️ General Setup

### Install All Dependencies

```bash
# Navigate to security-labs
cd security-labs

# Install all required packages
pip install flask requests pytest markupsafe bleach pyjwt bcrypt flask-limiter redis flask-cors

# Optional: Install OWASP ZAP (for Lab 4)
# Download from https://www.zaproxy.org/download/
```

### Verify Installation

```bash
python3 --version  # Should be 3.7+
python3 -c "import flask; print(flask.__version__)"
python3 -c "import jwt; print(jwt.__version__)"
```

## 🧪 Testing Your Fixes

Each lab includes its own test suite, but you can also test all labs comprehensively:

### Manual Testing Checklist

After completing all labs, verify:

- [ ] SQL injection attacks fail gracefully (Lab 1)
- [ ] XSS payloads are escaped or sanitized (Lab 2)
- [ ] Protected endpoints require authentication (Lab 3)
- [ ] Admin actions require admin role (Lab 3)
- [ ] Rate limiting prevents abuse (Lab 5)
- [ ] Error messages don't leak sensitive info (All labs)
- [ ] Passwords are hashed and never returned (Lab 3)
- [ ] Security headers are set (Lab 2)
- [ ] All user input is validated (Labs 1, 2)
- [ ] ZAP scans show no high-severity issues (Lab 4)

## 📚 Additional Resources

### OWASP Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP ZAP](https://www.zaproxy.org/)

### Security Tools
- [Burp Suite Community Edition](https://portswigger.net/burp/communitydownload)
- [sqlmap](http://sqlmap.org/) - SQL injection testing
- [XSStrike](https://github.com/s0md3v/XSStrike) - XSS detection
- [Nuclei](https://github.com/projectdiscovery/nuclei) - Vulnerability scanner

### Learning Resources
- [PortSwigger Web Security Academy](https://portswigger.net/web-security) - Free training
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/) - Interactive security lessons
- [HackTheBox](https://www.hackthebox.com/) - Practical hacking challenges
- [TryHackMe](https://tryhackme.com/) - Guided security learning

### Books
- "The Web Application Hacker's Handbook" by Dafydd Stuttard & Marcus Pinto
- "Web Security Testing Cookbook" by Paco Hope & Ben Walther
- "API Security in Action" by Neil Madden

## 🎓 Certification Paths

If you enjoy these labs, consider pursuing:

- **CEH (Certified Ethical Hacker)** - General penetration testing
- **OSCP (Offensive Security Certified Professional)** - Advanced pentesting
- **GWAPT (GIAC Web Application Penetration Tester)** - Web app security
- **eWPT (eLearnSecurity Web Application Penetration Tester)** - Practical web security

## 💡 Tips for Success

1. **Take Notes:** Document what you learn in each lab
2. **Try Bypasses:** After fixing, try to bypass your own fixes
3. **Read the Code:** Don't just run exploits - understand the vulnerable code
4. **Compare Versions:** Study the differences between vulnerable and fixed code
5. **Experiment:** Modify the code and see what breaks or improves security
6. **Use Tools:** Get comfortable with security testing tools
7. **Stay Updated:** Security is constantly evolving

## 🤝 Contributing

Found an issue or want to add a lab? See [CONTRIBUTING.md](../CONTRIBUTING.md)

Suggestions for new labs:
- CSRF (Cross-Site Request Forgery)
- XML External Entity (XXE) Injection
- Server-Side Request Forgery (SSRF)
- Insecure Deserialization
- File Upload Vulnerabilities
- Command Injection
- LDAP Injection

## ❓ Troubleshooting

### Common Issues

**Issue:** "Module not found" error
```bash
# Solution: Install missing package
pip install <package-name>
```

**Issue:** Port already in use
```bash
# Solution: Change port in the app or kill the process
# Change port:
app.run(port=5010)

# Or kill process:
# Linux/Mac: lsof -ti:5000 | xargs kill
# Windows: netstat -ano | findstr :5000, then taskkill /PID <PID>
```

**Issue:** Database locked error
```bash
# Solution: Delete and reinitialize database
rm *.db
# Restart the app (it will recreate the database)
```

**Issue:** ZAP won't connect
```bash
# Solution: Check firewall settings and proxy configuration
# Verify ZAP is running on correct port (usually 8080)
```

## 📞 Support

If you have questions:
1. Check the lab's README for specific guidance
2. Review the [main FAQ](../FAQ.md)
3. Search for similar issues in the repository
4. Open an issue with details about your problem

## 🏆 Completion Certificate

After completing all labs:

1. Take screenshots of successful test runs
2. Document key learnings in a blog post or notes
3. Apply these skills to review your own projects
4. Share your experience with the community

**You're now equipped to:**
- Identify common web vulnerabilities
- Perform basic security testing
- Implement secure coding practices
- Use industry-standard security tools
- Think like a security professional

## 🌟 Next Steps

After completing these security labs:

1. **Review Course Modules:**
   - [06. Authentication and Authorization](../06-Authentication-and-Authorization/)
   - [09. API Security](../09-API-Security/)
   - [13. Network Security Best Practices](../13-Network-Security-Best-Practices/)

2. **Build Secure Projects:**
   - Apply security principles to the course projects
   - Add authentication to your URL shortener
   - Secure your real-time chat application

3. **Continue Learning:**
   - Study OWASP Top 10 in depth
   - Practice on platforms like HackTheBox
   - Contribute to security tools
   - Stay updated with security news

4. **Get Certified:**
   - Consider security certifications
   - Build a security portfolio
   - Participate in bug bounty programs (ethically!)

---

**Remember:** With great power comes great responsibility. Use your security knowledge ethically and only test systems you own or have explicit permission to test.

**Happy (Ethical) Hacking! 🛡️**
