# Lab 4: API Security Testing with OWASP ZAP

## Overview

Learn how to use OWASP ZAP (Zed Attack Proxy), an industry-standard security testing tool, to scan APIs for vulnerabilities. This lab teaches you practical penetration testing skills used by security professionals.

## Learning Objectives

By the end of this lab, you will:
- Install and configure OWASP ZAP
- Perform automated security scans on APIs
- Interpret scan results and prioritize findings
- Manually test for specific vulnerabilities
- Generate professional security reports
- Fix discovered vulnerabilities

## Prerequisites

- Basic understanding of HTTP and APIs
- Python 3.7+
- OWASP ZAP installed (free download)
- Java Runtime Environment (for ZAP)

## Lab Structure

```
lab4-api-security-testing/
├── README.md (this file)
├── practice_api.py (API to test)
├── zap_scan_guide.md (detailed ZAP instructions)
├── scan_results/ (sample scan outputs)
└── fixes/ (vulnerability fixes)
```

## Setup

### Step 1: Install OWASP ZAP

**Option A: Download Installer**
```bash
# Visit https://www.zaproxy.org/download/
# Download ZAP for your platform
# Follow installation wizard
```

**Option B: Using Package Manager**
```bash
# macOS
brew install --cask owasp-zap

# Linux (Debian/Ubuntu)
sudo snap install zaproxy --classic

# Windows
choco install zap
```

### Step 2: Start the Practice API

```bash
# Install dependencies
pip install flask flask-cors

# Run the API
python3 practice_api.py
```

API runs on `http://localhost:5005`

### Step 3: Launch OWASP ZAP

```bash
# Start ZAP GUI
zap.sh  # Linux/Mac
zap.bat # Windows
```

## Part 1: Understanding OWASP ZAP

### What is OWASP ZAP?

OWASP ZAP is a free, open-source web application security scanner that helps find vulnerabilities in web applications and APIs.

**Key Features:**
- Automated scanner
- Manual testing tools (intercepting proxy)
- Spider/crawler for discovering endpoints
- Active and passive scanning
- API testing support
- Report generation

### ZAP Interface Components

1. **Sites Tree:** Shows discovered URLs
2. **Request/Response:** View HTTP traffic
3. **Active Scan:** Automated vulnerability testing
4. **Alerts:** Discovered vulnerabilities
5. **Spider:** Crawls application to find URLs
6. **Fuzzer:** Tests inputs with various payloads

## Part 2: Automated Scanning

### Quick Scan

1. **Open ZAP**
2. **Select "Automated Scan"**
3. **Enter URL:** `http://localhost:5005`
4. **Click "Attack"**
5. **Wait for scan to complete**
6. **Review Alerts**

### Manual Scan Configuration

#### Step 1: Configure Proxy

```
ZAP → Tools → Options → Local Proxies
- Address: localhost
- Port: 8080
```

#### Step 2: Spider the API

```
Right-click on http://localhost:5005 in Sites tree
→ Attack → Spider
→ Start Scan
```

**What it does:**
- Discovers all endpoints
- Maps API structure
- Identifies parameters

#### Step 3: Active Scan

```
Right-click on http://localhost:5005
→ Attack → Active Scan
→ Configure scan:
  ✓ SQL Injection
  ✓ Cross Site Scripting (XSS)
  ✓ Path Traversal
  ✓ Remote File Inclusion
  ✓ Server Side Include
  ✓ Script Active Scan Rules
→ Start Scan
```

**What it does:**
- Tests each endpoint with attack payloads
- Identifies vulnerabilities
- Rates severity (High, Medium, Low, Info)

## Part 3: Interpreting Results

### Understanding Alert Levels

| Risk Level | Color | Meaning | Action Required |
|-----------|-------|---------|-----------------|
| High | Red | Critical vulnerability | Fix immediately |
| Medium | Orange | Significant risk | Fix soon |
| Low | Yellow | Minor issue | Fix when possible |
| Informational | Blue | Best practice | Consider improving |

### Common Findings

#### 1. SQL Injection (High)

**Alert Details:**
```
Risk: High
Confidence: Medium
URL: http://localhost:5005/api/user?id=1
Parameter: id
Attack: 1' OR '1'='1
Evidence: SQL error message or unexpected data
```

**Fix:**
```python
# Use parameterized queries
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

#### 2. Cross-Site Scripting (High)

**Alert Details:**
```
Risk: High
Confidence: Medium
URL: http://localhost:5005/api/search?q=test
Parameter: q
Attack: <script>alert(1)</script>
Evidence: Script reflected unescaped
```

**Fix:**
```python
from markupsafe import escape
output = escape(user_input)
```

#### 3. Missing Security Headers (Medium)

**Alert Details:**
```
Risk: Medium
URL: http://localhost:5005
Missing Headers:
- Content-Security-Policy
- X-Frame-Options
- X-Content-Type-Options
```

**Fix:**
```python
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response
```

#### 4. Sensitive Data Exposure (High)

**Alert Details:**
```
Risk: High
URL: http://localhost:5005/api/users
Evidence: Password field in JSON response
```

**Fix:**
```python
# Never return passwords in API responses
user_data = {
    'id': user.id,
    'username': user.username,
    'email': user.email
    # DON'T include: 'password': user.password
}
```

## Part 4: Manual Testing

### Using ZAP Proxy for Manual Tests

#### 1. Configure Browser Proxy

**Firefox:**
```
Settings → Network Settings → Manual proxy configuration
HTTP Proxy: localhost
Port: 8080
✓ Also use this proxy for HTTPS
```

#### 2. Intercept Requests

```
In ZAP:
- Click the green/red breakpoint button
- Make request in browser
- Request pauses in ZAP
- Modify parameters
- Forward request
- Observe response
```

#### 3. Test Authentication

```
1. Intercept login request
2. Try SQL injection in username
3. Modify response to bypass checks
4. Test session token manipulation
```

### Using Manual Request Editor

```
Right-click any request in history
→ Open/Resend with Request Editor
→ Modify method, headers, body
→ Send
→ View response
```

### Fuzzing

```
Right-click on parameter
→ Fuzz
→ Add payloads:
  - SQL injection strings
  - XSS payloads
  - Path traversal strings
→ Start Fuzzer
→ Review responses for anomalies
```

## Part 5: API-Specific Testing

### Testing REST APIs

#### 1. Import OpenAPI/Swagger Spec

```
Import → Import an OpenAPI definition
→ Select swagger.json file
→ ZAP creates requests for all endpoints
```

#### 2. Test Each HTTP Method

```
GET /api/users/1     → Access control
POST /api/users      → Input validation
PUT /api/users/1     → Authorization
DELETE /api/users/1  → Authentication
```

#### 3. Test Authentication

```
# Test with no token
# Test with invalid token
# Test with expired token
# Test with another user's token
```

### GraphQL Testing

```
POST /graphql
Content-Type: application/json

{
  "query": "{ users { id password } }"
}

# Test for:
- Introspection enabled (info disclosure)
- Query depth limits
- Authorization on fields
```

## Part 6: Generating Reports

### HTML Report

```
Report → Generate HTML Report
→ Choose template: Traditional HTML
→ Select alerts to include
→ Save report
```

### JSON Report

```
Report → Export Messages to File
→ Format: JSON
→ Useful for automation/CI/CD
```

### PDF Report (with extension)

```
Marketplace → Install "Report Generation"
→ Report → Generate Report
→ Format: PDF
```

## Part 7: Fixing Vulnerabilities

After scanning, create a remediation plan:

### Priority Matrix

| Finding | Severity | Effort | Priority |
|---------|----------|--------|----------|
| SQL Injection | High | Medium | 1 |
| XSS | High | Low | 2 |
| Missing Auth | High | High | 3 |
| CSRF | Medium | Medium | 4 |
| Info Disclosure | Low | Low | 5 |

### Re-scan After Fixes

```
1. Apply fixes
2. Restart application
3. Run ZAP scan again
4. Verify alerts are resolved
5. Check for new issues introduced
```

## Part 8: Automation & CI/CD

### ZAP Baseline Scan (Command Line)

```bash
# Basic scan
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t http://localhost:5005

# Generate report
docker run -v $(pwd):/zap/wrk:rw -t owasp/zap2docker-stable \
  zap-baseline.py -t http://localhost:5005 \
  -r report.html
```

### ZAP API Scan

```bash
# More thorough API testing
docker run -t owasp/zap2docker-stable zap-api-scan.py \
  -t http://localhost:5005/openapi.json \
  -f openapi
```

### Integrate with CI/CD

```yaml
# .github/workflows/security-scan.yml
name: Security Scan
on: [push]
jobs:
  zap_scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: ZAP Scan
        uses: zaproxy/action-baseline@v0.7.0
        with:
          target: 'http://localhost:5005'
```

## Best Practices Summary

### ✅ DO:
- Run scans regularly (not just once)
- Test in staging, not production
- Review all findings manually
- Prioritize by risk and impact
- Re-scan after fixes
- Keep ZAP updated
- Use authenticated scans for protected endpoints
- Combine automated and manual testing

### ❌ DON'T:
- Scan production without permission
- Trust automated scans 100%
- Ignore low-severity findings
- Skip manual verification
- Forget to test authentication/authorization
- Scan third-party sites without permission
- Use aggressive scans on production

## Additional Resources

- [OWASP ZAP Documentation](https://www.zaproxy.org/docs/)
- [ZAP Getting Started Guide](https://www.zaproxy.org/getting-started/)
- [API Security Top 10](https://owasp.org/www-project-api-security/)
- [ZAP Automation Framework](https://www.zaproxy.org/docs/automate/)

## Challenge Exercises

1. Scan the main vulnerable_api.py from security-labs
2. Create an OpenAPI spec for practice_api.py
3. Write a ZAP automation script
4. Integrate ZAP into a CI/CD pipeline
5. Perform authenticated scanning

## Next Steps

- Move to [Lab 5: Rate Limiting](../lab5-rate-limiting/)
- Review [API Security Module](../../09-API-Security/)
- Study OWASP API Security Top 10

---

**⚠️ Warning:** Only scan applications you own or have permission to test!
