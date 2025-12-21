# 🔒 HTTPS and TLS

Learn how encryption works to keep your data safe on the internet.

## 🎯 Learning Objectives

By the end of this module, you will:
- Understand how HTTPS encryption works
- Learn about TLS/SSL protocols
- Understand certificates and certificate authorities
- Know about man-in-the-middle attacks
- Learn how to set up HTTPS for your applications

## HTTP vs HTTPS 🔓 vs 🔒

### HTTP (Insecure)
```
Client → [Hello, password123] → Server
         ↑
    Anyone can read this!
```

### HTTPS (Secure)
```
Client → [Encrypted gibberish] → Server
         ↑
    Can't read without the key!
```

## How Encryption Works 🔐

### Symmetric Encryption
Same key for encryption and decryption.

```
Message: "Hello"
Key: "secret123"
Encrypted: "X$@9k"

To decrypt: Use same key "secret123"
```

**Problem**: How do you share the key securely?

### Asymmetric Encryption
Two keys: public (encrypt) and private (decrypt).

```
Server has:
- Public key (anyone can use to encrypt)
- Private key (only server can decrypt)

Client encrypts with public key → Server decrypts with private key
```

## TLS/SSL Protocol 🤝

**TLS (Transport Layer Security)** is the modern protocol for encrypting internet traffic. SSL is the older version.

### TLS Handshake

```
1. Client → Server: "Hello, I want HTTPS"
2. Server → Client: "Here's my certificate and public key"
3. Client verifies certificate
4. Client → Server: Encrypted session key (using server's public key)
5. Both use session key for symmetric encryption (faster!)
```

### The Process in Detail

```
Step 1: ClientHello
Client: "I support TLS 1.3, these ciphers: [list]"

Step 2: ServerHello
Server: "Let's use TLS 1.3, cipher AES-256-GCM"
Server: "Here's my certificate"

Step 3: Certificate Verification
Client checks:
- Is certificate signed by trusted CA?
- Is it for the correct domain?
- Is it still valid (not expired)?

Step 4: Key Exchange
Client generates session key
Client encrypts it with server's public key
Server decrypts with private key

Step 5: Encrypted Communication
Both use session key for fast symmetric encryption
```

## Certificates 📜

A **certificate** proves a server's identity.

### What's in a Certificate?

```
Certificate Contents:
- Domain name: example.com
- Organization: Example Inc.
- Public key: [long key...]
- Issuer: Let's Encrypt
- Valid from: 2024-01-01
- Valid until: 2025-01-01
- Signature: [cryptographic signature]
```

### Certificate Authorities (CAs)

**Trusted organizations** that verify and sign certificates:
- Let's Encrypt (free!)
- DigiCert
- GlobalSign
- Comodo

### Certificate Chain

```
Root CA (trusted by browser)
    ↓ signs
Intermediate CA
    ↓ signs
Your Certificate (example.com)
```

Browser trusts the root, so it trusts your certificate!

## Man-in-the-Middle (MITM) Attacks 🕵️

### The Attack

```
Without HTTPS:
You → [password: secret123] → Attacker → [password: secret123] → Bank
      ↑                          ↓
   Attacker sees everything!
```

### How HTTPS Prevents MITM

```
With HTTPS:
You → [encrypted] → Attacker → [encrypted] → Bank
      ↑                ↓
   Attacker sees gibberish, can't decrypt!
```

Even if attacker intercepts, they can't:
- Read the data (it's encrypted)
- Modify it (would break signature)
- Impersonate server (don't have private key)

## Setting Up HTTPS 🛠️

### Option 1: Let's Encrypt (Free!)

**Prerequisites**: You need a domain name.

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d example.com -d www.example.com

# Certbot automatically:
# 1. Verifies you own the domain
# 2. Gets certificate
# 3. Configures web server
# 4. Sets up auto-renewal
```

### Option 2: Self-Signed Certificate (Development)

**Warning**: Browsers will show security warning!

```bash
# Generate private key and certificate
openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout key.pem -out cert.pem -days 365

# Use with Python Flask
from flask import Flask
app = Flask(__name__)

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))
```

### Flask with HTTPS

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Secure connection!'

if __name__ == '__main__':
    # Production: Use actual certificates
    app.run(
        ssl_context=('cert.pem', 'key.pem'),
        host='0.0.0.0',
        port=443
    )
```

### Nginx Configuration

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://localhost:5000;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

## HTTPS Best Practices ✅

### 1. Always Use HTTPS
```python
# Force HTTPS in Flask
@app.before_request
def force_https():
    if not request.is_secure:
        return redirect(request.url.replace('http://', 'https://'))
```

### 2. Use HSTS Header
```python
@app.after_request
def set_hsts(response):
    # Tell browser to always use HTTPS
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

### 3. Keep Certificates Updated
```bash
# Let's Encrypt auto-renews
sudo certbot renew --dry-run  # Test renewal
```

### 4. Use Strong Ciphers
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
```

### 5. Monitor Certificate Expiration
Use services like:
- SSL Labs (https://www.ssllabs.com/ssltest/)
- Certificate monitoring tools

## Testing HTTPS 🧪

### Check Certificate Details

```bash
# Using OpenSSL
openssl s_client -connect example.com:443 -servername example.com

# Check expiration
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
```

### Test with Browser
1. Visit https://yourdomain.com
2. Click padlock icon
3. View certificate details
4. Verify:
   - Certificate is valid
   - Issued to correct domain
   - Not expired

### SSL Labs Test
Visit https://www.ssllabs.com/ssltest/ and enter your domain to get a security rating.

## Common Issues 🔧

### "Your connection is not private"
**Cause**: Certificate issue (expired, self-signed, wrong domain)
**Fix**: Get valid certificate from CA

### Mixed Content Warning
**Cause**: HTTPS page loading HTTP resources
**Fix**: Change all resources to HTTPS

```html
<!-- Bad -->
<script src="http://example.com/script.js"></script>

<!-- Good -->
<script src="https://example.com/script.js"></script>
```

### Certificate Expired
**Cause**: Certificate validity period ended
**Fix**: Renew certificate

## Summary and Key Takeaways

✅ **HTTPS encrypts data** in transit, preventing eavesdropping  
✅ **TLS/SSL** protocols establish secure connections  
✅ **Certificates** prove server identity and enable encryption  
✅ **Certificate Authorities** verify and sign certificates  
✅ **Let's Encrypt** provides free, automated certificates  
✅ **Always use HTTPS** in production for sensitive data  
✅ **HSTS** forces browsers to use HTTPS  
✅ **Monitor certificates** to prevent expiration

## What's Next?

Learn comprehensive **Network Security Best Practices** to secure your entire application stack!

---

[← Back: Other Protocols](../11-Other-Protocols/) | [Next: Network Security Best Practices →](../13-Network-Security-Best-Practices/)

## Practice

Complete the exercises in [exercises.md](./exercises.md) to set up HTTPS!
