# 🛡️ Network Security Best Practices

Comprehensive security review and defense-in-depth strategies for networked applications.

## 🎯 Learning Objectives

By the end of this module, you will:
- Understand defense-in-depth strategy
- Apply layered security to applications
- Know security testing techniques
- Follow industry security standards
- Create a security checklist for your projects

## Defense in Depth 🏰

**Concept**: Multiple layers of security, so if one fails, others protect you.

### Defense in Depth Architecture Diagram

Here's a visual representation of layered security architecture:

```
Defense in Depth Security Layers:

                            Internet (Threats)
                                  │
                                  ▼
         ┌────────────────────────────────────────────┐
         │     Layer 1: Network Security              │
         │  ┌──────────────────────────────────────┐  │
         │  │ Firewall (Block suspicious traffic)  │  │
         │  │ DDoS Protection                      │  │
         │  │ VPN (Encrypted tunnels)              │  │
         │  │ Network Segmentation                 │  │
         │  └──────────────────────────────────────┘  │
         └────────────────────────────────────────────┘
                                  │
                                  ▼
         ┌────────────────────────────────────────────┐
         │     Layer 2: Application Security          │
         │  ┌──────────────────────────────────────┐  │
         │  │ HTTPS/TLS (Encrypted communication)  │  │
         │  │ Rate Limiting                        │  │
         │  │ Input Validation                     │  │
         │  │ Authentication & Authorization       │  │
         │  │ CORS Configuration                   │  │
         │  │ Security Headers                     │  │
         │  └──────────────────────────────────────┘  │
         └────────────────────────────────────────────┘
                                  │
                                  ▼
         ┌────────────────────────────────────────────┐
         │     Layer 3: Code Security                 │
         │  ┌──────────────────────────────────────┐  │
         │  │ SQL Injection Prevention             │  │
         │  │ XSS Protection                       │  │
         │  │ CSRF Tokens                          │  │
         │  │ Secure Dependencies                  │  │
         │  │ Error Handling (No data leakage)     │  │
         │  └──────────────────────────────────────┘  │
         └────────────────────────────────────────────┘
                                  │
                                  ▼
         ┌────────────────────────────────────────────┐
         │     Layer 4: Data Security                 │
         │  ┌──────────────────────────────────────┐  │
         │  │ Database Encryption (At rest)        │  │
         │  │ Password Hashing (bcrypt)            │  │
         │  │ Access Control Lists                 │  │
         │  │ Data Backup & Recovery               │  │
         │  │ Audit Logging                        │  │
         │  └──────────────────────────────────────┘  │
         └────────────────────────────────────────────┘
                                  │
                                  ▼
         ┌────────────────────────────────────────────┐
         │     Layer 5: Monitoring & Response         │
         │  ┌──────────────────────────────────────┐  │
         │  │ Security Monitoring                  │  │
         │  │ Intrusion Detection (IDS)            │  │
         │  │ Log Analysis                         │  │
         │  │ Incident Response Plan               │  │
         │  │ Regular Security Audits              │  │
         │  └──────────────────────────────────────┘  │
         └────────────────────────────────────────────┘


Attack Flow with Defense Layers:

Attacker                    Security Layers                    Protected Resource
   |                              |                                    |
   |─── Malicious Request ──────> |                                    |
   |    (SQL Injection)            |                                    |
   |                         Layer 1: Firewall                         |
   |                         ✅ Passes (looks normal)                  |
   |                               |                                    |
   |                         Layer 2: Rate Limit                       |
   |                         ✅ Passes (not too many)                  |
   |                               |                                    |
   |                         Layer 3: Input Validation                 |
   |                         ❌ BLOCKED!                               |
   |                         Detected SQL pattern                      |
   |<─── 400 Bad Request ───       |                                    |
   |    "Invalid input"            |                                    |
   |                               |                                    |
   Attack stopped at Layer 3! ✅  |                                    |


Multi-Layer Protection Example:

Scenario: Attacker tries to access admin panel

Request: GET /admin/users
         No authentication token

Layer 1 (Network): ✅ Allow (valid IP)
Layer 2 (App): ❌ Block (no auth token) → 401 Unauthorized

Request: GET /admin/users
         With stolen/expired token

Layer 1 (Network): ✅ Allow (valid IP)
Layer 2 (App): ✅ Token present
Layer 3 (Code): ❌ Block (token expired) → 401 Unauthorized

Request: GET /admin/users
         With valid user token (not admin)

Layer 1 (Network): ✅ Allow (valid IP)
Layer 2 (App): ✅ Valid token
Layer 3 (Code): ✅ Authenticated
Layer 4 (Data): ❌ Block (not admin) → 403 Forbidden


Security Checklist Flow:

Development Phase:
┌─────────────────────────────────────────┐
│ • Use secure coding practices          │
│ • Implement input validation            │
│ • Add authentication/authorization      │
│ • Use parameterized queries             │
│ • Add rate limiting                     │
│ • Configure CORS properly               │
│ • Hash passwords with bcrypt            │
└─────────────────────────────────────────┘
                  ↓
Testing Phase:
┌─────────────────────────────────────────┐
│ • Test authentication flows             │
│ • Try SQL injection attacks             │
│ • Test XSS vulnerabilities              │
│ • Check rate limiting                   │
│ • Verify HTTPS configuration            │
│ • Review security headers               │
└─────────────────────────────────────────┘
                  ↓
Deployment Phase:
┌─────────────────────────────────────────┐
│ • Enable HTTPS/TLS                      │
│ • Configure firewall rules              │
│ • Set up monitoring/logging             │
│ • Implement backup strategy             │
│ • Enable DDoS protection                │
└─────────────────────────────────────────┘
                  ↓
Maintenance Phase:
┌─────────────────────────────────────────┐
│ • Monitor security logs                 │
│ • Update dependencies regularly         │
│ • Review access logs                    │
│ • Conduct security audits               │
│ • Apply security patches                │
│ • Test incident response plan           │
└─────────────────────────────────────────┘
```

**Key Principles:**

1. **No Single Point of Failure**: If one layer is breached, others protect
2. **Layers Work Together**: Each adds different protection
3. **Assume Breach**: Design assuming attackers will get past some layers
4. **Monitor Everything**: Detect and respond to threats quickly

**Real-World Example:**

Imagine a bank vault:
- **Layer 1**: Security guards at entrance (Network firewall)
- **Layer 2**: ID check at door (Authentication)
- **Layer 3**: PIN pad for vault (Authorization)
- **Layer 4**: Time-locked safe (Data encryption)
- **Layer 5**: Cameras and alarms (Monitoring)

Same principle applies to network security!

## Comprehensive Security Checklist ✅

### 1. Authentication & Access Control

**Do's:**
- ✅ Use strong password hashing (bcrypt, argon2)
- ✅ Implement multi-factor authentication (MFA)
- ✅ Use OAuth for third-party authentication
- ✅ Implement account lockout after failed attempts
- ✅ Require strong passwords (length, complexity)
- ✅ Implement proper session management
- ✅ Use secure, HTTPOnly cookies

**Don'ts:**
- ❌ Store passwords in plain text
- ❌ Use weak hashing (MD5, SHA1)
- ❌ Allow unlimited login attempts
- ❌ Use predictable session IDs

### 2. Data Protection

**Do's:**
- ✅ Use HTTPS everywhere
- ✅ Encrypt sensitive data at rest
- ✅ Use environment variables for secrets
- ✅ Implement proper key management
- ✅ Sanitize logs (no passwords/tokens)
- ✅ Use secure random number generation

**Don'ts:**
- ❌ Hardcode API keys or secrets
- ❌ Commit secrets to version control
- ❌ Log sensitive information
- ❌ Use weak encryption algorithms

### 3. Input Validation & Output Encoding

**Do's:**
- ✅ Validate all user input
- ✅ Use parameterized queries
- ✅ Sanitize output (prevent XSS)
- ✅ Validate file uploads
- ✅ Check file types and sizes
- ✅ Implement content security policy

**Don'ts:**
- ❌ Trust user input
- ❌ Use string concatenation for SQL
- ❌ Allow unrestricted file uploads
- ❌ Echo user input without sanitization

### 4. API Security

**Do's:**
- ✅ Implement rate limiting
- ✅ Use API versioning
- ✅ Validate request origins (CORS)
- ✅ Implement proper error handling
- ✅ Use request size limits
- ✅ Implement timeout for long operations

**Don'ts:**
- ❌ Expose internal errors to users
- ❌ Allow unlimited requests
- ❌ Use wildcard CORS in production
- ❌ Return detailed error messages

### 5. Database Security

**Do's:**
- ✅ Use parameterized queries
- ✅ Implement least privilege access
- ✅ Encrypt sensitive database fields
- ✅ Regular backups
- ✅ Use database firewalls
- ✅ Monitor database access

**Don'ts:**
- ❌ Use root/admin account for app
- ❌ Leave default credentials
- ❌ Expose database ports to internet
- ❌ Store sensitive data unencrypted

### 6. Infrastructure Security

**Do's:**
- ✅ Keep software updated
- ✅ Use firewalls
- ✅ Implement intrusion detection
- ✅ Regular security audits
- ✅ Monitor logs
- ✅ Use secure defaults

**Don'ts:**
- ❌ Use outdated software
- ❌ Leave unnecessary ports open
- ❌ Disable security features
- ❌ Ignore security updates

## Security Testing 🧪

### 1. Automated Security Scanning

**Tools:**
- **OWASP ZAP**: Web application security scanner
- **Bandit**: Python code security analyzer
- **npm audit**: Node.js dependency scanner
- **Safety**: Python dependency checker

**Example using Bandit:**
```bash
# Install
pip install bandit

# Scan Python code
bandit -r /path/to/your/code

# Example output shows security issues
```

### 2. Penetration Testing

**Manual tests:**
- Try SQL injection
- Attempt XSS attacks
- Test authentication bypass
- Check for exposed sensitive data
- Test rate limiting

### 3. Code Review

**Security-focused code review checklist:**
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Output encoding used
- [ ] Proper error handling
- [ ] Authentication checks
- [ ] Authorization checks
- [ ] Secure random generation
- [ ] HTTPS enforced

### 4. Dependency Scanning

**Check for vulnerable dependencies:**

```bash
# Python
pip install safety
safety check

# Node.js
npm audit
npm audit fix

# Update dependencies
pip install --upgrade package_name
npm update
```

## Secure Coding Practices 💻

### 1. Password Hashing

```python
import bcrypt

def hash_password(password):
    # Generate salt and hash password
    salt = bcrypt.gensalt(rounds=12)  # Higher = slower but more secure
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Usage
hashed = hash_password("user_password")
# Store hashed in database

# Later, verify
if verify_password("user_password", hashed):
    print("Password correct!")
```

### 2. Secure Random Generation

```python
import secrets

# Generate secure random token
token = secrets.token_urlsafe(32)  # 32 bytes = 256 bits

# Generate random API key
api_key = secrets.token_hex(16)

# Don't use random.random() for security!
```

### 3. Environment Variables

```python
import os

# .env file (never commit this!)
# API_KEY=your_secret_key
# DATABASE_URL=postgresql://...

# Load from environment
API_KEY = os.environ.get('API_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')

if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
```

### 4. Secure Headers

```python
from flask import Flask

app = Flask(__name__)

@app.after_request
def security_headers(response):
    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    
    # Prevent MIME sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Enable XSS filter
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Content Security Policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline';"
    )
    
    # Force HTTPS
    response.headers['Strict-Transport-Security'] = (
        'max-age=31536000; includeSubDomains'
    )
    
    # Referrer policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Permissions policy
    response.headers['Permissions-Policy'] = (
        'geolocation=(), microphone=(), camera=()'
    )
    
    return response
```

## Incident Response Plan 🚨

### 1. Preparation
- Maintain security contacts
- Document system architecture
- Keep backups updated
- Have rollback procedures ready

### 2. Detection
- Monitor logs
- Set up alerts
- Regular security scans
- User reports

### 3. Response
```
1. Identify the issue
2. Contain the threat
3. Eradicate the vulnerability
4. Recover systems
5. Post-incident review
```

### 4. Documentation
- Log all actions taken
- Document timeline
- Identify root cause
- Update procedures

## Security Standards & Compliance 📋

### OWASP Top 10 (2021)

1. **Broken Access Control**
2. **Cryptographic Failures**
3. **Injection**
4. **Insecure Design**
5. **Security Misconfiguration**
6. **Vulnerable and Outdated Components**
7. **Identification and Authentication Failures**
8. **Software and Data Integrity Failures**
9. **Security Logging and Monitoring Failures**
10. **Server-Side Request Forgery (SSRF)**

### Industry Standards

- **PCI DSS**: Payment card data security
- **GDPR**: EU data protection regulation
- **HIPAA**: Healthcare data protection (US)
- **SOC 2**: Security controls for service organizations

## Security Resources 📚

### Learning Resources
- OWASP Foundation (owasp.org)
- PortSwigger Web Security Academy
- NIST Cybersecurity Framework
- CWE/SANS Top 25

### Tools
- **Burp Suite**: Web security testing
- **Wireshark**: Network protocol analyzer
- **Metasploit**: Penetration testing
- **Nmap**: Network scanner

### Vulnerability Databases
- CVE (Common Vulnerabilities and Exposures)
- NVD (National Vulnerability Database)
- GitHub Security Advisories

## Final Security Checklist 🎯

Before deploying to production:

**Infrastructure:**
- [ ] HTTPS enabled everywhere
- [ ] Firewall configured
- [ ] Unnecessary ports closed
- [ ] Server hardened
- [ ] Monitoring set up

**Application:**
- [ ] All input validated
- [ ] Output encoded/escaped
- [ ] Authentication implemented
- [ ] Authorization checked
- [ ] Rate limiting enabled
- [ ] CORS configured properly
- [ ] Security headers set
- [ ] Error handling doesn't leak info

**Data:**
- [ ] Passwords hashed with bcrypt/argon2
- [ ] Sensitive data encrypted
- [ ] Secrets in environment variables
- [ ] Database access restricted
- [ ] Backups automated

**Code:**
- [ ] No hardcoded secrets
- [ ] Dependencies updated
- [ ] Security scan passed
- [ ] Code review completed
- [ ] Logging implemented (without sensitive data)

**Testing:**
- [ ] Penetration test performed
- [ ] Automated security scan run
- [ ] Dependency vulnerabilities checked
- [ ] Security headers verified

## Summary and Key Takeaways

✅ **Defense in depth**: Multiple layers of security  
✅ **Security is a process**, not a one-time task  
✅ **Assume breach**: Plan for security incidents  
✅ **Validate everything**: Never trust input  
✅ **Keep updated**: Patch vulnerabilities quickly  
✅ **Encrypt data**: In transit and at rest  
✅ **Monitor continuously**: Detect issues early  
✅ **Educate team**: Security is everyone's responsibility

## Congratulations! 🎉

You've completed the Network Fundamentals course! You now understand:
- How the internet and web work
- HTTP and API communication
- Authentication and authorization
- Database integration
- Security best practices
- Real-time communication
- Network protocols

**Next steps:**
- Build projects to practice
- Continue learning advanced topics
- Stay updated on security trends
- Contribute to open source

---

[← Back: HTTPS and TLS](../12-HTTPS-and-TLS/)

## Practice

Complete the exercises in [exercises.md](./exercises.md) to test your security knowledge!
