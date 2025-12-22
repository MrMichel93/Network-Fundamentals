# Lab 3: Broken Authentication

## Overview

Broken authentication is a critical security vulnerability that occurs when authentication mechanisms are implemented incorrectly, allowing attackers to compromise passwords, keys, session tokens, or exploit other implementation flaws to assume users' identities.

## Learning Objectives

By the end of this lab, you will:
- Understand common authentication weaknesses
- Identify broken authentication patterns
- Exploit authentication vulnerabilities safely
- Implement secure authentication systems
- Learn about session management best practices

## Prerequisites

- Basic understanding of HTTP and sessions
- Python 3.7+
- Flask installed (`pip install flask pyjwt bcrypt`)

## Lab Structure

```
lab3-broken-authentication/
├── README.md (this file)
├── vulnerable_app.py (weak authentication)
├── fixed_app.py (secure authentication)
├── attack_demonstrations.sh (exploitation examples)
└── test_security.py (validation tests)
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install flask pyjwt bcrypt
   ```

2. **Start the vulnerable application:**
   ```bash
   python3 vulnerable_app.py
   ```

   Server runs on `http://localhost:5004`

## Part 1: Common Authentication Vulnerabilities

### Vulnerability 1: Weak Password Storage

**Problem:**
- Passwords stored in plaintext
- Using weak hashing (MD5, SHA1)
- No salting

**Attack:**
```bash
# If database is compromised, passwords are exposed
# Rainbow tables can crack unsalted hashes
```

**Fix:**
```python
import bcrypt

# Hash password with salt
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Verify password
if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
    # Password correct
```

### Vulnerability 2: Predictable Session Tokens

**Problem:**
- Sequential session IDs (session1, session2, ...)
- Weak random number generation
- No expiration

**Attack:**
```bash
# Try sequential session IDs
curl -H "Cookie: session_id=session123" http://localhost:5004/api/profile
curl -H "Cookie: session_id=session124" http://localhost:5004/api/profile
curl -H "Cookie: session_id=session125" http://localhost:5004/api/profile
```

**Fix:**
```python
import secrets

# Generate cryptographically secure token
session_id = secrets.token_urlsafe(32)

# Set expiration
session_data = {
    'user_id': user_id,
    'created_at': time.time(),
    'expires_at': time.time() + 3600  # 1 hour
}
```

### Vulnerability 3: No Multi-Factor Authentication (MFA)

**Problem:**
- Only password required
- No second factor
- Easy account takeover

**Fix:**
```python
# Implement TOTP (Time-based One-Time Password)
import pyotp

# Generate secret for user
secret = pyotp.random_base32()

# User scans QR code with authenticator app
totp = pyotp.TOTP(secret)

# Verify code
if totp.verify(user_code):
    # Code valid
```

### Vulnerability 4: No Account Lockout

**Problem:**
- Unlimited login attempts
- Enables brute force attacks
- No rate limiting

**Attack:**
```bash
# Brute force attack
for password in password_list:
    curl -X POST http://localhost:5004/api/login \
      -d '{"username":"admin","password":"'$password'"}'
done
```

**Fix:**
```python
# Track failed attempts
failed_attempts = {}

def check_login_attempts(username):
    if username in failed_attempts:
        attempts, last_attempt = failed_attempts[username]
        
        # Lock account after 5 failed attempts
        if attempts >= 5:
            time_since_last = time.time() - last_attempt
            # 15 minute lockout
            if time_since_last < 900:
                return False, f"Account locked. Try again in {900 - int(time_since_last)} seconds"
            else:
                # Reset after lockout period
                del failed_attempts[username]
    
    return True, None
```

### Vulnerability 5: Insecure JWT Implementation

**Problem:**
- Algorithm confusion (none, HS256 vs RS256)
- Weak secret keys
- No expiration
- Sensitive data in payload

**Attack:**
```bash
# Change algorithm to 'none'
# Modify payload and remove signature
# Use leaked secret key
```

**Fix:**
```python
import jwt
from datetime import datetime, timedelta

# Strong secret key (should be in environment variable)
SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

def create_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow()
    }
    
    # Use strong algorithm
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        # Explicitly specify allowed algorithms
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
```

### Vulnerability 6: Session Fixation

**Problem:**
- Session ID not regenerated after login
- Attacker can set victim's session ID

**Attack:**
```
1. Attacker gets session ID: SESS123
2. Attacker sends victim link with SESS123
3. Victim logs in (session not regenerated)
4. Attacker uses SESS123 to access victim's account
```

**Fix:**
```python
@app.route('/login', methods=['POST'])
def login():
    # ... authenticate user ...
    
    # IMPORTANT: Generate new session ID after login
    old_session_id = session.get('id')
    session.clear()
    
    # Generate new session ID
    new_session_id = secrets.token_urlsafe(32)
    session['id'] = new_session_id
    session['user_id'] = user.id
    
    return jsonify({'success': True})
```

## Part 2: Attack Demonstrations

### Demo 1: Credential Stuffing

```bash
# Using leaked credentials from other breaches
./attack_demonstrations.sh credential_stuffing
```

### Demo 2: Session Hijacking

```bash
# Stealing session tokens
./attack_demonstrations.sh session_hijack
```

### Demo 3: Password Reset Poisoning

```bash
# Manipulating password reset flow
./attack_demonstrations.sh password_reset
```

## Part 3: Secure Implementation

Key security measures in `fixed_app.py`:

1. **Password Hashing:** bcrypt with salt
2. **Secure Sessions:** Cryptographically random tokens
3. **Rate Limiting:** Account lockout after failed attempts
4. **JWT Security:** Proper algorithm, expiration, validation
5. **Session Regeneration:** New ID after authentication
6. **HTTPOnly Cookies:** Prevents XSS cookie theft
7. **HTTPS Only:** Secure flag on cookies
8. **Password Requirements:** Complexity enforcement

## Part 4: Testing Your Fix

```bash
# Run security tests
python3 test_security.py
```

Tests verify:
- ✅ Passwords properly hashed
- ✅ Sessions are secure and expire
- ✅ Brute force protection active
- ✅ JWT properly validated
- ✅ Session fixation prevented
- ✅ Security headers present

## Best Practices Summary

### ✅ DO:
- Use bcrypt, scrypt, or Argon2 for password hashing
- Generate cryptographically secure session tokens
- Implement session expiration and renewal
- Use HTTPS for all authenticated pages
- Set HTTPOnly and Secure flags on cookies
- Implement rate limiting and account lockout
- Regenerate session ID after login
- Use strong JWT secrets and proper algorithms
- Implement MFA for sensitive operations
- Log authentication events

### ❌ DON'T:
- Store passwords in plaintext or with weak hashing
- Use predictable session IDs
- Allow unlimited login attempts
- Expose authentication tokens in URLs
- Use weak JWT secrets
- Allow 'none' algorithm for JWT
- Include sensitive data in JWT payload
- Forget to expire sessions
- Rely on client-side authentication checks

## Additional Resources

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)

## Challenge Exercises

1. Implement password reset functionality securely
2. Add two-factor authentication (TOTP)
3. Create an OAuth 2.0 login flow
4. Implement remember me functionality safely
5. Add biometric authentication simulation

## Next Steps

- Move to [Lab 4: API Security Testing](../lab4-api-security-testing/)
- Review [Authentication Module](../../06-Authentication-and-Authorization/)
- Study OAuth 2.0 and OpenID Connect

---

**⚠️ Warning:** The vulnerable code is for educational purposes only. Never use in production!
