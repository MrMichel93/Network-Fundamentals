# ⚠️ Common Mistakes - Other Protocols

Learn from these common pitfalls when working with TCP, UDP, FTP, SMTP, SSH, and other protocols.

## TCP vs UDP Mistakes

### 1. Using UDP When Reliability is Needed

**Mistake:**
```python
# Sending critical financial transaction via UDP
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.sendto(b'TRANSFER $10000 FROM...', (host, port))
# What if the packet is lost? Money disappeared!
```

**Why it's wrong:**
- UDP doesn't guarantee delivery
- No confirmation of receipt
- Packets can be lost
- Order not guaranteed

**Correct:**
```python
# Use TCP for reliable data transfer
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
sock.connect((host, port))
sock.sendall(b'TRANSFER $10000 FROM...')
response = sock.recv(1024)  # Get confirmation
sock.close()
```

**Lesson:** Use TCP when reliability is critical. Use UDP only when speed matters more than reliability.

---

### 2. Using TCP When Low Latency is Critical

**Mistake:**
```python
# Sending game position updates via TCP
while gaming:
    position = get_player_position()
    tcp_socket.sendall(position)  # Too slow for real-time gaming!
```

**Why it's wrong:**
- TCP has overhead (acknowledgments, retransmissions)
- Head-of-line blocking
- Higher latency
- Old data delivered late is useless in games

**Correct:**
```python
# Use UDP for real-time, time-sensitive data
while gaming:
    position = get_player_position()
    udp_socket.sendto(position, (host, port))
    # Lost packets OK, next update coming soon anyway
```

**Lesson:** Use UDP for real-time applications where latest data matters more than every packet.

---

## FTP Mistakes

### 3. Using FTP Instead of SFTP/FTPS

**Mistake:**
```python
# Connecting to FTP server
ftp = FTP('ftp.example.com')
ftp.login('username', 'password')  # Transmitted in plain text!
```

**Why it's wrong:**
- Credentials sent unencrypted
- Data transmitted unencrypted
- Vulnerable to eavesdropping
- Security risk

**Correct:**
```python
# Use SFTP (SSH File Transfer Protocol)
import paramiko

transport = paramiko.Transport((host, 22))
transport.connect(username='user', password='pass')  # Encrypted!
sftp = paramiko.SFTPClient.from_transport(transport)

# Or use FTPS (FTP Secure)
from ftplib import FTP_TLS
ftps = FTP_TLS('ftp.example.com')
ftps.login('username', 'password')  # Encrypted connection
```

**Lesson:** Never use plain FTP for sensitive data. Use SFTP or FTPS instead.

---

### 4. Not Setting Binary Mode for File Transfers

**Mistake:**
```python
ftp = FTP('ftp.example.com')
ftp.login('user', 'pass')
# Transferring image in ASCII mode
with open('image.jpg', 'rb') as f:
    ftp.storlines('STOR image.jpg', f)  # Wrong! Corrupts binary data
```

**Why it's wrong:**
- ASCII mode modifies line endings
- Corrupts binary files (images, executables, etc.)
- Files become unusable

**Correct:**
```python
ftp = FTP('ftp.example.com')
ftp.login('user', 'pass')
# Binary mode for binary files
with open('image.jpg', 'rb') as f:
    ftp.storbinary('STOR image.jpg', f)  # Correct!

# ASCII mode only for text files
with open('document.txt', 'rb') as f:
    ftp.storlines('STOR document.txt', f)  # OK for text
```

**Lesson:** Use binary mode for all files unless you specifically need ASCII mode for text.

---

## SMTP/Email Mistakes

### 5. Not Using TLS for Email

**Mistake:**
```python
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.login('user@gmail.com', 'password')  # Before TLS!
```

**Why it's wrong:**
- Credentials sent unencrypted
- Email content exposed
- Vulnerable to interception

**Correct:**
```python
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()  # Enable TLS encryption
server.login('user@gmail.com', 'password')  # Now encrypted
```

**Lesson:** Always use TLS (STARTTLS) when sending email.

---

### 6. Not Validating Email Addresses

**Mistake:**
```python
# Sending to any input
email = input("Enter email: ")
send_email(email)  # What if it's not valid?
```

**Why it's wrong:**
- Invalid addresses cause failures
- Can be used for email injection
- Wastes resources

**Correct:**
```python
import re

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

email = input("Enter email: ")
if is_valid_email(email):
    send_email(email)
else:
    print("Invalid email address")
```

**Lesson:** Always validate email addresses before sending.

---

## SSH Mistakes

### 7. Accepting Unknown Host Keys Blindly

**Mistake:**
```python
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Dangerous!
ssh.connect('server.com', username='user', password='pass')
```

**Why it's wrong:**
- Vulnerable to man-in-the-middle attacks
- Can connect to imposter servers
- Security risk

**Correct:**
```python
import paramiko

ssh = paramiko.SSHClient()
# Option 1: Use known_hosts file
ssh.load_system_host_keys()

# Option 2: Load specific known_hosts
ssh.load_host_keys('/path/to/known_hosts')

# Option 3: Verify manually first time
ssh.set_missing_host_key_policy(paramiko.WarningPolicy())

try:
    ssh.connect('server.com', username='user', password='pass')
except paramiko.SSHException as e:
    print(f"Warning: {e}")
    # Manually verify host key before proceeding
```

**Lesson:** Always verify SSH host keys to prevent MITM attacks.

---

### 8. Using Password Authentication Instead of Keys

**Mistake:**
```python
# Using password for SSH
ssh.connect('server.com', username='user', password='mypassword')
```

**Why it's wrong:**
- Passwords can be guessed
- Vulnerable to brute force
- Less secure than key-based auth

**Correct:**
```python
# Use SSH key authentication
ssh.connect('server.com',
            username='user',
            key_filename='/path/to/private_key')

# Or use ssh-agent
ssh.connect('server.com',
            username='user',
            look_for_keys=True)
```

**Lesson:** Use SSH key-based authentication for better security.

---

## Protocol Selection Mistakes

### 9. Using Wrong Protocol for the Job

**Common mistakes:**
- Using HTTP polling instead of WebSockets for real-time updates
- Using TCP for live video streaming (use UDP with error correction)
- Using SMTP directly instead of email service APIs
- Using FTP for automated deployments (use SCP/rsync/CI/CD)

**Correct approach:**
```
Choose protocol based on requirements:

Real-time bidirectional: WebSockets
Real-time broadcast: UDP (with custom reliability if needed)
Reliable data transfer: TCP, HTTP
File transfer: SFTP, SCP, rsync
Email: SMTP with TLS (or email service API)
Remote command execution: SSH
Video streaming: RTMP, WebRTC (UDP-based)
```

**Lesson:** Understand protocol characteristics and choose appropriately.

---

### 10. Not Understanding Port Numbers

**Mistake:**
```python
# Using random high port for server
server_socket.bind(('0.0.0.0', 55555))  # What service is this?
```

**Why it's confusing:**
- Not following conventions
- Hard to remember
- Conflicts with other services

**Correct understanding:**
```
Well-known ports (0-1023):
- 21: FTP
- 22: SSH
- 25: SMTP
- 80: HTTP
- 443: HTTPS
- 587: SMTP with STARTTLS

Registered ports (1024-49151):
- Use for custom services
- Register if public service

Dynamic/Private (49152-65535):
- For temporary connections
- Client-side ports
```

**Lesson:** Use standard ports for standard protocols. Document custom ports clearly.

---

## Best Practices

### ✅ Do's
1. **Use appropriate protocol** for your needs
2. **Use encryption** (TLS, SSH) for sensitive data
3. **Validate input** before sending
4. **Handle errors** gracefully
5. **Use standard ports** when possible
6. **Implement timeouts**
7. **Close connections** properly
8. **Document protocol choices**

### ❌ Don'ts
1. **Don't use plain text protocols** for sensitive data
2. **Don't trust unvalidated input**
3. **Don't use TCP when UDP is better** (and vice versa)
4. **Don't ignore protocol security best practices**
5. **Don't hardcode credentials**
6. **Don't assume connections always work**
7. **Don't use deprecated protocols** (e.g., plain FTP, Telnet)

---

## Protocol Selection Guide

| Use Case | Recommended Protocol | Why |
|----------|---------------------|-----|
| File transfer | SFTP, SCP, rsync | Secure, reliable |
| Remote shell | SSH | Secure, standard |
| Email | SMTP with TLS | Standard, secure |
| Real-time chat | WebSockets | Bidirectional, low latency |
| Live streaming | WebRTC, UDP | Low latency |
| API calls | HTTPS/REST | Standard, scalable |
| Database | Protocol-specific | Optimized |
| Game updates | UDP | Speed over reliability |

---

## Quick Reference

| Mistake | Impact | Solution |
|---------|--------|----------|
| UDP for critical data | Data loss | Use TCP |
| TCP for real-time | High latency | Use UDP |
| Plain FTP | Security risk | Use SFTP/FTPS |
| No TLS for email | Exposed data | Use STARTTLS |
| Password SSH | Weak security | Use key-based auth |
| Wrong protocol | Poor performance | Choose appropriately |

**Next:** Review [Other Protocols README](./README.md) and complete [exercises](./exercises.md).
