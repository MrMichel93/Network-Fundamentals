# Lab 1: SQL Injection

## Overview

SQL Injection is a critical web security vulnerability that allows attackers to interfere with database queries. This lab will teach you how to identify, exploit, and fix SQL injection vulnerabilities.

## Learning Objectives

By the end of this lab, you will:
- Understand how SQL injection works
- Identify vulnerable code patterns
- Exploit SQL injection vulnerabilities safely
- Implement proper defenses using parameterized queries
- Test your fixes to ensure security

## Prerequisites

- Basic understanding of SQL
- Python 3.7+
- Flask installed (`pip install flask`)

## Lab Structure

```
lab1-sql-injection/
├── README.md (this file)
├── vulnerable_app.py (intentionally vulnerable)
├── fixed_app.py (secure implementation)
├── exploit_examples.sh (demonstration attacks)
└── test_security.py (validation tests)
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install flask requests
   ```

2. **Start the vulnerable application:**
   ```bash
   python3 vulnerable_app.py
   ```

   The server will run on `http://localhost:5001`

## Part 1: Understanding the Vulnerability

### What is SQL Injection?

SQL injection occurs when user input is directly concatenated into SQL queries without proper sanitization. Attackers can manipulate the query logic to:
- Bypass authentication
- Extract sensitive data
- Modify or delete data
- Execute administrative operations

### Vulnerable Code Pattern

```python
# VULNERABLE - DO NOT USE IN PRODUCTION
username = request.form['username']
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```

**Why is this dangerous?**

If an attacker enters `admin' --` as the username, the query becomes:
```sql
SELECT * FROM users WHERE username = 'admin' --'
```

The `--` comments out the rest of the query, bypassing any password check!

## Part 2: Exploitation Examples

### Attack 1: Authentication Bypass

**Objective:** Login without knowing the password

**Payload:**
```bash
curl -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin'\'' --", "password": "anything"}'
```

**What happens:**
- The SQL query becomes: `SELECT * FROM users WHERE username = 'admin' --' AND password = '...'`
- Everything after `--` is a comment
- The password check is bypassed!

### Attack 2: Data Extraction

**Objective:** Retrieve all users from the database

**Payload:**
```bash
curl "http://localhost:5001/api/user/admin'%20OR%20'1'='1"
```

**What happens:**
- The query becomes: `SELECT * FROM users WHERE username = 'admin' OR '1'='1'`
- `'1'='1'` is always true
- All users are returned!

### Attack 3: UNION-based Injection

**Objective:** Extract data from other tables

**Payload:**
```bash
curl "http://localhost:5001/api/user/admin'%20UNION%20SELECT%201,2,3,4,5--"
```

**What happens:**
- UNION allows combining results from multiple SELECT statements
- Attackers can extract data from any table they can query

## Part 3: Running the Exploits

Run the provided exploit script:

```bash
chmod +x exploit_examples.sh
./exploit_examples.sh
```

Observe:
1. The server logs showing the malicious SQL queries
2. Successful authentication bypass
3. Unauthorized data access
4. Error messages that reveal database structure

## Part 4: Implementing the Fix

### Secure Code Pattern

```python
# SECURE - Use parameterized queries
username = request.form['username']
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

**Why is this safe?**

- The `?` placeholder is treated as a parameter, not part of the SQL syntax
- User input is properly escaped by the database driver
- Special characters like quotes don't affect query structure
- The query structure is fixed and cannot be modified by user input

### Key Security Principles

1. **Never concatenate user input into SQL queries**
2. **Always use parameterized queries (prepared statements)**
3. **Use ORM libraries when possible** (SQLAlchemy, Django ORM)
4. **Validate and sanitize input** (defense in depth)
5. **Use least privilege** (database user should have minimal permissions)
6. **Never expose SQL errors to users** (information disclosure)

### Compare the Code

Look at `vulnerable_app.py` vs `fixed_app.py`:

| Aspect | Vulnerable | Fixed |
|--------|-----------|-------|
| Query building | String concatenation | Parameterized queries |
| Error handling | Exposes SQL errors | Generic error messages |
| Input validation | None | Type checking + sanitization |
| Logging | Logs full queries | Logs sanitized info only |

## Part 5: Testing Your Fix

1. **Start the fixed application:**
   ```bash
   python3 fixed_app.py
   ```

2. **Run the security tests:**
   ```bash
   python3 test_security.py
   ```

The tests will verify:
- ✅ SQL injection attacks fail
- ✅ Legitimate queries still work
- ✅ Error messages don't leak information
- ✅ All authentication is properly validated

3. **Try the exploits manually:**
   ```bash
   # This should now fail gracefully
   curl -X POST http://localhost:5002/api/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin'\'' --", "password": "anything"}'
   ```

   Expected response: `{"error": "Invalid credentials"}` (401 Unauthorized)

## Part 6: Best Practices Summary

### ✅ DO:
- Use parameterized queries/prepared statements
- Use ORM libraries (SQLAlchemy, Django ORM)
- Validate input types and formats
- Use allowlists for expected input
- Implement proper error handling
- Use least privilege for database connections
- Keep software and libraries updated

### ❌ DON'T:
- Concatenate user input into SQL strings
- Trust any user input without validation
- Expose database errors to users
- Use dynamic table/column names from user input
- Grant excessive database permissions
- Rely solely on client-side validation

## Additional Resources

- [OWASP SQL Injection Guide](https://owasp.org/www-community/attacks/SQL_Injection)
- [SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
- [Bobby Tables Comic](https://xkcd.com/327/)
- [Python sqlite3 Security](https://docs.python.org/3/library/sqlite3.html)

## Challenge Exercises

1. **Identify vulnerability:** Review `vulnerable_app.py` and list all vulnerable endpoints
2. **Create new attack:** Develop a SQL injection that extracts email addresses
3. **Defense in depth:** Add input validation layer before the parameterized query
4. **Audit code:** Check if the course's other Python files have SQL injection risks

## Next Steps

After completing this lab:
- Move to [Lab 2: XSS Attacks](../lab2-xss-attacks/)
- Review the [API Security Module](../../09-API-Security/)
- Apply these principles to your own projects

---

**⚠️ Warning:** The vulnerable code in this lab is for educational purposes only. Never use it in production or expose it to the internet!
