# 📋 Prerequisites

Welcome to the Networking Fundamentals course! Before we dive into networking concepts, let's make sure you're ready to get the most out of this course.

## 🎯 Learning Objectives

By the end of this module, you will:
- Understand what knowledge is expected for this course
- Set up your development environment
- Verify that all required tools are installed and working
- Be ready to start learning networking fundamentals

## What You Should Already Know

This course assumes you have basic programming knowledge. Specifically, you should be comfortable with:

### 1. **Basic Programming Concepts**
- Variables and data types (strings, numbers, lists/arrays, dictionaries/objects)
- Control flow (if/else statements, loops)
- Functions (defining and calling them)
- Basic error handling (try/catch or try/except)

**Example in Python:**
```python
def greet(name):
    if name:
        return f"Hello, {name}!"
    else:
        return "Hello, stranger!"

print(greet("Alice"))
```

**Example in JavaScript:**
```javascript
function greet(name) {
    if (name) {
        return `Hello, ${name}!`;
    } else {
        return "Hello, stranger!";
    }
}

console.log(greet("Alice"));
```

### 2. **Command Line Basics**
You should know how to:
- Open a terminal or command prompt
- Navigate directories (`cd`, `ls` or `dir`)
- Run programs from the command line
- Install packages using package managers

**Basic commands you should know:**
```bash
# Navigate to a directory
cd my-project

# List files
ls              # Mac/Linux
dir             # Windows

# Create a directory
mkdir new-folder

# Run a Python script
python script.py

# Check Python version
python --version
```

### 3. **Text Editor or IDE**
You should be comfortable:
- Creating and editing files
- Saving files
- Understanding file paths

**Popular options:**
- Visual Studio Code (recommended for beginners)
- PyCharm
- Sublime Text
- Atom
- Notepad++ (Windows)

## Required Software

### 1. **Python 3.7 or Higher**

**Why Python?** Python is beginner-friendly, has excellent networking libraries, and is widely used in real-world applications.

**Check if you have Python installed:**
```bash
python --version
# or
python3 --version
```

**If you see something like `Python 3.9.7`, you're good to go!**

**Don't have Python?** Download it from [python.org](https://www.python.org/downloads/)

### 2. **pip (Python Package Manager)**

pip usually comes with Python. Verify it's installed:
```bash
pip --version
# or
pip3 --version
```

### 3. **Git (Optional but Recommended)**

Git helps you clone this repository and track your changes.

```bash
git --version
```

Don't have Git? Download from [git-scm.com](https://git-scm.com/downloads)

### 4. **A Web Browser**

You'll need a modern web browser with developer tools:
- Chrome (recommended)
- Firefox
- Edge
- Safari

## Setting Up Your Environment

### Step 1: Clone or Download This Repository

**Option A: Using Git (Recommended)**
```bash
git clone https://github.com/MrMichel93/Network-Fundamentals.git
cd Network-Fundamentals
```

**Option B: Download ZIP**
1. Click the green "Code" button on GitHub
2. Select "Download ZIP"
3. Extract the ZIP file
4. Open terminal and navigate to the extracted folder

### Step 2: Create a Virtual Environment

A virtual environment keeps this course's dependencies separate from other Python projects.

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**You'll know it's activated** when you see `(venv)` at the start of your command prompt.

### Step 3: Install Required Packages

```bash
pip install -r requirements.txt
```

This installs all the Python packages we'll use throughout the course.

### Step 4: Test Your Setup

Create a test file to verify everything works:

**test_setup.py:**
```python
import sys
import requests

print(f"Python version: {sys.version}")
print(f"Requests library version: {requests.__version__}")
print("\n✅ Setup successful! You're ready to start learning!")
```

Run it:
```bash
python test_setup.py
```

If you see the success message, you're all set!

## Helpful Tools to Install (Optional)

These tools will enhance your learning experience:

### 1. **curl**
A command-line tool for making HTTP requests.

**Check if installed:**
```bash
curl --version
```

**Install:**
- Mac: Usually pre-installed
- Windows: Download from [curl.se](https://curl.se/windows/)
- Linux: `sudo apt-get install curl`

### 2. **Postman**
A graphical tool for testing APIs (we'll introduce this later).

Download from [postman.com](https://www.postman.com/downloads/)

### 3. **Browser Extensions**
- **JSONView** (Chrome/Firefox) - Makes JSON responses readable

## Common Setup Issues

### Issue 1: "python: command not found"
**Solution:** Try `python3` instead of `python`, or reinstall Python.

### Issue 2: "pip: command not found"
**Solution:** Try `pip3` instead of `pip`, or reinstall Python with pip included.

### Issue 3: Virtual environment won't activate
**Solution:** 
- On Windows, you might need to run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Make sure you're in the correct directory

### Issue 4: Permission errors when installing packages
**Solution:** 
- Make sure your virtual environment is activated
- On Mac/Linux, don't use `sudo` with pip inside a virtual environment

## What's Next?

Now that your environment is set up, you're ready to learn about how the internet works!

### Quick Self-Check Quiz

Before moving on, make sure you can answer "yes" to these questions:

- [ ] I can open a terminal and navigate between directories
- [ ] I have Python 3.7+ installed and can run Python scripts
- [ ] I understand basic programming concepts (variables, functions, loops)
- [ ] I have a text editor or IDE installed
- [ ] I've created and activated a virtual environment for this course
- [ ] I've installed the required packages using pip

**All checked?** Great! Head over to [01-How-The-Internet-Works](../01-How-The-Internet-Works/) to begin your networking journey!

**Need help?** Check our [FAQ](../FAQ.md) or open an issue on GitHub.

## Summary

✅ You should know basic programming (Python or JavaScript)  
✅ You should be comfortable with the command line  
✅ You need Python 3.7+, pip, and a text editor  
✅ Create a virtual environment to keep dependencies organized  
✅ Install required packages with `pip install -r requirements.txt`  
✅ Test your setup before proceeding

**Remember:** Don't worry if you're not an expert in all these areas. The most important thing is a willingness to learn and experiment. You can always revisit this section or ask questions as you go!

---

[Next: How The Internet Works →](../01-How-The-Internet-Works/)
