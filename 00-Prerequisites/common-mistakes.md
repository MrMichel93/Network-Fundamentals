# ⚠️ Common Mistakes - Prerequisites

Learn from these common pitfalls to save time and frustration during setup.

## Setup and Installation Mistakes

### 1. Not Using Virtual Environments

**Mistake:**
```bash
# Installing packages globally
pip install requests
pip install flask
```

**Why it's a problem:**
- Packages conflict with system Python
- Different projects may need different versions
- Hard to reproduce environment on another machine
- Can break system tools that depend on Python

**Correct approach:**
```bash
# Create and activate virtual environment first
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# or venv\Scripts\activate  # Windows

# Then install packages
pip install requests
```

**Lesson:** Always use virtual environments for Python projects to isolate dependencies.

---

### 2. Using `sudo` with pip

**Mistake:**
```bash
sudo pip install requests  # Don't do this!
```

**Why it's a problem:**
- Installs packages system-wide with elevated privileges
- Can break your system Python installation
- Security risk - running package installations as root
- Makes it impossible to have different versions per project

**Correct approach:**
```bash
# Use virtual environment (no sudo needed)
python3 -m venv venv
source venv/bin/activate
pip install requests
```

**Lesson:** Never use `sudo` with pip. Virtual environments eliminate the need for system-wide installations.

---

### 3. Mixing Python 2 and Python 3

**Mistake:**
```bash
python script.py  # Might be Python 2
pip install package  # Might install to Python 2
```

**Why it's a problem:**
- Python 2 is deprecated and no longer supported
- Syntax and behavior differ between Python 2 and 3
- Packages installed to wrong Python version

**Correct approach:**
```bash
# Be explicit about Python version
python3 --version  # Check version first
python3 script.py  # Use Python 3 explicitly
pip3 install package  # Install to Python 3

# Or use virtual environment which locks to specific version
python3 -m venv venv
source venv/bin/activate
python script.py  # Now always uses Python 3
```

**Lesson:** Be explicit about Python versions. Use `python3` and `pip3` or rely on virtual environments.

---

### 4. Forgetting to Activate Virtual Environment

**Mistake:**
```bash
# Created virtual environment but forgot to activate
python3 -m venv venv
pip install requests  # Installs to system, not venv!
python script.py  # Might not find the package
```

**Why it's a problem:**
- Packages get installed to wrong location
- Scripts can't find dependencies
- Defeats the purpose of virtual environments

**Correct approach:**
```bash
python3 -m venv venv
source venv/bin/activate  # Don't forget this step!
# Now you'll see (venv) in your prompt
pip install requests
python script.py
```

**Tip:** Your terminal prompt should show `(venv)` when the environment is active.

**Lesson:** Always activate your virtual environment before installing packages or running scripts.

---

### 5. Wrong Python Path or Multiple Python Installations

**Mistake:**
```bash
# Installed Python but terminal doesn't find it
python3 --version
# bash: python3: command not found
```

**Why it's a problem:**
- Python not added to system PATH
- Multiple Python installations causing confusion
- Using wrong Python version without realizing it

**Correct approach:**
```bash
# Find where Python is installed
which python3  # Mac/Linux
where python3  # Windows

# Check all Python installations
which -a python python3  # Mac/Linux
where python*  # Windows

# Add to PATH if needed (varies by OS)
# Or reinstall Python with PATH option checked
```

**Lesson:** Ensure Python is properly installed and in your system PATH. Use `which` or `where` to verify.

---

## Command Line Mistakes

### 6. Not Understanding Current Directory

**Mistake:**
```bash
# Trying to run script from wrong directory
python script.py
# FileNotFoundError: [Errno 2] No such file or directory: 'script.py'
```

**Why it's a problem:**
- Commands run relative to current directory
- Files can't be found if you're in the wrong place

**Correct approach:**
```bash
# Always check where you are
pwd  # Print working directory

# Navigate to the right place
cd /path/to/your/project

# Or use full path
python /path/to/your/project/script.py
```

**Lesson:** Always be aware of your current directory. Use `pwd` to check and `cd` to navigate.

---

### 7. Incorrect File Paths

**Mistake:**
```python
# Using wrong path separators
file = open("C:\Users\name\file.txt")  # Windows backslash issue
```

**Why it's a problem:**
- Backslashes are escape characters in Python strings
- Code isn't portable between operating systems

**Correct approach:**
```python
# Use forward slashes (works on all platforms)
file = open("C:/Users/name/file.txt")

# Or use raw strings for Windows paths
file = open(r"C:\Users\name\file.txt")

# Or use pathlib (best practice)
from pathlib import Path
file_path = Path("C:/Users/name/file.txt")
file = open(file_path)

# Or use os.path.join for cross-platform
import os
file_path = os.path.join("C:", "Users", "name", "file.txt")
```

**Lesson:** Use forward slashes in paths or Python's path libraries for cross-platform compatibility.

---

## Package and Dependency Mistakes

### 8. Not Installing Requirements

**Mistake:**
```bash
# Cloning a repo and running code immediately
git clone https://github.com/user/project.git
cd project
python app.py  # Missing dependencies!
```

**Why it's a problem:**
- Code depends on external packages
- ImportError for missing packages

**Correct approach:**
```bash
git clone https://github.com/user/project.git
cd project

# Look for requirements.txt
ls requirements.txt

# Install dependencies
pip install -r requirements.txt

# Now run the code
python app.py
```

**Lesson:** Always check for and install `requirements.txt` before running project code.

---

### 9. Version Mismatch Issues

**Mistake:**
```bash
# Installing without specifying versions
pip install flask
# Gets latest version, might be incompatible
```

**Why it's a problem:**
- Latest version might have breaking changes
- Code written for older version might not work
- Hard to reproduce exact environment

**Correct approach:**
```bash
# Use requirements.txt with versions
# requirements.txt:
# flask==2.0.1
# requests==2.26.0

pip install -r requirements.txt
```

**Lesson:** Pin dependency versions in `requirements.txt` for reproducible environments.

---

## Learning Mistakes

### 10. Skipping the Basics

**Mistake:**
- Jumping straight to advanced topics
- Not understanding command line or Python fundamentals
- Copying code without understanding it

**Why it's a problem:**
- Builds on shaky foundation
- Hard to debug when things go wrong
- Missing context makes learning harder

**Correct approach:**
- Complete prerequisite exercises thoroughly
- Understand each concept before moving forward
- Type code yourself rather than copy-pasting
- Experiment and break things to learn

**Lesson:** Take time to build solid fundamentals. They'll save you time in the long run.

---

### 11. Not Reading Error Messages

**Mistake:**
```bash
python script.py
# Traceback (most recent call last):
#   File "script.py", line 5, in <module>
#     import requests
# ModuleNotFoundError: No module named 'requests'

# Response: "It's broken! What do I do?"
```

**Why it's a problem:**
- Error messages contain valuable debugging information
- Skipping them leads to random trial-and-error

**Correct approach:**
1. **Read the error message completely**
2. **Identify the error type** (ModuleNotFoundError)
3. **Find the cause** (module 'requests' not found)
4. **Apply the solution** (install requests: `pip install requests`)

**Lesson:** Error messages are your friends. Read them carefully—they tell you exactly what's wrong.

---

### 12. Not Testing Changes

**Mistake:**
```bash
# Making multiple changes without testing
# Edit file 1
# Edit file 2
# Edit file 3
python script.py  # Now there's an error - which change broke it?
```

**Why it's a problem:**
- Hard to identify which change caused an issue
- Wastes time debugging multiple changes at once

**Correct approach:**
```bash
# Make one small change
# Test it
python script.py

# Make next change
# Test again
python script.py
```

**Lesson:** Test after each change. Small iterations make debugging easier.

---

## Best Practices to Avoid Mistakes

### ✅ Do's

1. **Always use virtual environments**
2. **Keep dependencies in requirements.txt**
3. **Read error messages carefully**
4. **Test incrementally**
5. **Use version control (Git)**
6. **Comment your code**
7. **Keep learning resources open**
8. **Ask for help when stuck**

### ❌ Don'ts

1. **Don't use sudo with pip**
2. **Don't install packages globally**
3. **Don't skip error messages**
4. **Don't copy-paste without understanding**
5. **Don't ignore warnings**
6. **Don't forget to activate virtual environment**
7. **Don't mix Python 2 and 3**
8. **Don't commit virtual environment to Git**

---

## Quick Reference: Problem-Solution Matrix

| Problem | Symptom | Solution |
|---------|---------|----------|
| Module not found | `ModuleNotFoundError` | Install with pip |
| Wrong Python version | Code doesn't work | Use python3 explicitly |
| Permission denied | Can't install packages | Use virtual environment |
| Virtual env not active | Packages in wrong place | `source venv/bin/activate` |
| Path not found | `FileNotFoundError` | Check current directory with `pwd` |
| Command not found | `bash: python: command not found` | Check PATH or use full path |

---

## Next Steps

Now that you know what to avoid:
1. Review your current setup
2. Fix any issues you might have
3. Set up your environment correctly
4. Move on to [Module 01: How The Internet Works](../01-How-The-Internet-Works/)

**Remember:** Everyone makes these mistakes when learning. The key is to learn from them and establish good habits early!
