# ❓ Frequently Asked Questions

Common questions about the Networking Fundamentals course.

## General Questions

### Who is this course for?

This course is designed for:
- High school students with basic programming knowledge
- Self-learners who want to understand networking
- Developers who want to build networked applications
- Anyone curious about how the internet works

You should have basic familiarity with:
- Python or JavaScript
- Command line/terminal
- Programming concepts (variables, functions, loops)

### How long does the course take?

**Estimated time:** 4-6 weeks (2-3 hours per week)

- Some students complete it faster
- Take your time - learning is not a race!
- Each module can be completed in 2-4 hours
- Projects take additional time

### Do I need to complete modules in order?

**Yes, strongly recommended!** Each module builds on previous knowledge:
1. Prerequisites → 2. Internet Basics → 3. HTTP → 4. REST APIs → 5. WebSockets → 6. Protocols → 7. Security → 8. Projects

Skipping ahead may leave knowledge gaps.

### Is this course free?

**Yes, completely free!** All materials are open source and freely available.

### Do I get a certificate?

Currently, no certificate is provided. However, the hands-on projects serve as portfolio pieces to demonstrate your skills.

## Technical Questions

### What software do I need?

**Required:**
- Python 3.7 or higher
- Text editor or IDE (VS Code recommended)
- Terminal/command prompt
- Web browser (Chrome, Firefox, or Edge)

**Optional:**
- curl (for testing APIs)
- Postman (for API testing)
- Git (for version control)

### Which operating system should I use?

The course works on:
- ✅ Windows 10/11
- ✅ macOS
- ✅ Linux (Ubuntu, Debian, Fedora, etc.)

Most examples work identically across all platforms.

### Python or JavaScript?

**Primary language: Python**
- Most code examples are in Python
- Python is beginner-friendly
- Excellent networking libraries

**JavaScript is used for:**
- WebSocket client examples (browser-based)
- Front-end web interfaces

### I'm getting "ModuleNotFoundError"

This usually means a Python package isn't installed.

**Solution:**
```bash
# Make sure virtualenv is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Or install individual package
pip install requests
```

### I'm getting "Permission denied" errors

**On Mac/Linux:**
```bash
# Scripts need execute permission
chmod +x script.py

# Don't use sudo with pip in virtual environment
```

**On Windows:**
- Run terminal as Administrator (if needed)
- Check firewall settings if ports are blocked

### Ports are already in use

**Error:** `Address already in use` or `Port 5000 is already in use`

**Solution:**
```bash
# Find what's using the port
# Mac/Linux
lsof -i :5000

# Windows
netstat -ano | findstr :5000

# Kill the process or use a different port
python app.py --port 5001
```

### Can't connect to localhost

**Check these:**
1. Is the server running?
2. Using correct port number?
3. Firewall blocking connections?
4. Using `localhost`, `127.0.0.1`, or `0.0.0.0`?

**Try:**
```bash
# Test if port is open
curl http://localhost:5000
# or
telnet localhost 5000
```

## Content Questions

### What's the difference between HTTP and HTTPS?

**HTTP** (Port 80):
- Unencrypted
- Data sent in plain text
- Anyone can read it
- Use for: Development only

**HTTPS** (Port 443):
- Encrypted with TLS/SSL
- Data is secure
- Verifies server identity
- Use for: Production, always!

### When should I use WebSockets vs HTTP?

**Use HTTP when:**
- Simple request/response pattern
- Client initiates all communication
- CRUD operations
- RESTful APIs

**Use WebSockets when:**
- Real-time updates needed
- Server needs to push data to client
- Bidirectional communication
- Examples: chat, live dashboards, gaming

### What's the difference between TCP and UDP?

| Feature | TCP | UDP |
|---------|-----|-----|
| Reliability | Guaranteed delivery | No guarantee |
| Speed | Slower | Faster |
| Order | In-order | May be out of order |
| Use case | Web, email, files | Video, gaming, voice |

**TCP:** Like certified mail (reliable, tracked)  
**UDP:** Like throwing postcards (fast, might lose some)

### How do I secure my API?

**Essential security measures:**
1. ✅ Use HTTPS (always!)
2. ✅ Implement authentication (API keys, JWT)
3. ✅ Validate all input
4. ✅ Use parameterized queries (prevent SQL injection)
5. ✅ Escape HTML output (prevent XSS)
6. ✅ Implement CORS correctly
7. ✅ Rate limit requests
8. ✅ Hash passwords (never store plain text)

See [Module 6: Security Basics](./06-Security-Basics/) for details.

### What API should I use for learning?

**Great free APIs for practice:**
- [GitHub API](https://api.github.com) - No key required for many endpoints
- [OpenWeatherMap](https://openweathermap.org/api) - Free tier available
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - Fake API for testing
- [httpbin.org](https://httpbin.org/) - Test HTTP requests

## Course-Specific Questions

### Where are the solutions to exercises?

Solutions are in the `solutions/` folder. Try exercises yourself first before checking solutions!

### Can I skip the exercises?

**Not recommended!** Exercises are where real learning happens. You can:
- Try on your own first
- Check hints if stuck
- Look at solutions after attempting
- Build your own variations

### I'm stuck on a project. What should I do?

1. **Review related modules** - refresh concepts
2. **Read error messages carefully** - they often tell you what's wrong
3. **Use print/console.log** for debugging
4. **Break down the problem** into smaller pieces
5. **Check the hints** in the project file
6. **Search for similar examples** online
7. **Ask for help** - open a GitHub issue

### How do I run the examples?

```bash
# Python examples
python example_file.py

# Make sure dependencies are installed
pip install -r requirements.txt

# For HTML files
# Open in browser or use:
python -m http.server 8000
# Then visit http://localhost:8000
```

### The code examples don't work

**Check:**
1. ✅ Dependencies installed? (`pip install -r requirements.txt`)
2. ✅ Virtual environment activated?
3. ✅ Using Python 3.7+? (check with `python --version`)
4. ✅ Correct working directory?
5. ✅ Server running (for client examples)?
6. ✅ Port available (not already in use)?

If still stuck, open an issue with:
- Error message (full text)
- Python version
- Operating system
- What you tried

## Project Questions

### Can I use these projects in my portfolio?

**Absolutely!** That's encouraged. You can:
- Complete the projects as-is
- Add your own features
- Modify for your use case
- Share on GitHub

Just mention that you learned from this course.

### Can I use different technologies?

**Yes!** The concepts are language-agnostic. Feel free to:
- Use Node.js instead of Python
- Try different frameworks (Express, FastAPI, Django)
- Build mobile apps
- Use different databases

The learning objectives remain the same.

### How do I deploy my projects?

Popular options:
- **Heroku** - Easy, free tier available
- **Railway** - Modern alternative to Heroku
- **Vercel/Netlify** - Great for front-end
- **DigitalOcean** - VPS for more control
- **AWS/GCP/Azure** - Enterprise solutions

See deployment guides for each platform.

## Getting Help

### Still have questions?

1. **Check the module README** - detailed explanations
2. **Review exercises** - practical examples
3. **Search this FAQ** - Ctrl+F to find keywords
4. **Check GitHub issues** - maybe already answered
5. **Open a new issue** - we're happy to help!

### How to ask good questions

**Include:**
- What you're trying to do
- What you expected to happen
- What actually happened
- Error messages (full text)
- Code snippet (minimal example)
- What you've already tried

**Example:**
> "I'm trying to run the WebSocket server from Module 4, but I get this error:
> `ModuleNotFoundError: No module named 'websockets'`
> 
> I'm on Windows 10, Python 3.9. I tried `pip install websockets` but it says 'already installed'. My virtual environment is activated."

This helps us help you faster!

## Contributing

### Can I contribute to this course?

**Yes!** We welcome:
- Bug fixes
- Improved explanations
- New examples
- Additional exercises
- Translations
- Corrections

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

---

**Didn't find your answer?** [Open an issue](https://github.com/MrMichel93/Network-Fundamentals/issues/new) and ask!

[Back to Home](./README.md)
