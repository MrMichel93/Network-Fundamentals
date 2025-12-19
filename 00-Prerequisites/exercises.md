# 📝 Prerequisites - Exercises

These exercises will help you verify your setup and ensure you're ready for the networking fundamentals course.

## Exercise 1: Environment Verification

**Goal:** Confirm your development environment is properly configured.

**Tasks:**
1. Open your terminal/command prompt
2. Check your Python version:
   ```bash
   python --version
   ```
   or
   ```bash
   python3 --version
   ```
3. Verify pip is installed:
   ```bash
   pip --version
   ```

**Expected Output:**
- Python version should be 3.7 or higher
- pip version should be displayed

**Troubleshooting:**
If you see errors, refer to the [Prerequisites README](./README.md#common-setup-issues).

---

## Exercise 2: Create and Activate Virtual Environment

**Goal:** Practice creating isolated Python environments.

**Tasks:**
1. Navigate to a practice directory:
   ```bash
   mkdir ~/networking-practice
   cd ~/networking-practice
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv my-test-env
   ```

3. Activate it:
   - **Mac/Linux:**
     ```bash
     source my-test-env/bin/activate
     ```
   - **Windows:**
     ```bash
     my-test-env\Scripts\activate
     ```

4. Verify activation by checking if `(my-test-env)` appears in your prompt

5. Deactivate when done:
   ```bash
   deactivate
   ```

**Success Criteria:**
- Virtual environment created without errors
- Prompt shows environment name when activated
- Can activate and deactivate successfully

---

## Exercise 3: Install and Test a Package

**Goal:** Practice using pip to install Python packages.

**Tasks:**
1. Make sure your virtual environment is activated
2. Install the `requests` library:
   ```bash
   pip install requests
   ```

3. Create a test script `test_requests.py`:
   ```python
   import requests
   
   response = requests.get('https://api.github.com')
   print(f"Status Code: {response.status_code}")
   print(f"Requests library is working!")
   ```

4. Run the script:
   ```bash
   python test_requests.py
   ```

**Expected Output:**
```
Status Code: 200
Requests library is working!
```

---

## Exercise 4: Basic Python Review

**Goal:** Refresh your Python skills before diving into networking.

**Tasks:**
Create a script `review.py` with the following:

```python
# 1. Create a function that takes a URL and prints its components
def analyze_url(url):
    """
    Extract and print parts of a URL
    Example: https://api.example.com/users?limit=10
    """
    # Your code here
    # Hint: You can use string methods like split(), find(), etc.
    pass

# 2. Create a dictionary representing an HTTP request
http_request = {
    "method": "GET",
    "url": "https://api.example.com/users",
    "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer token123"
    }
}

# 3. Write a function to pretty-print the request
def print_request(request):
    """Print HTTP request in a readable format"""
    # Your code here
    pass

# Test your functions
if __name__ == "__main__":
    analyze_url("https://api.example.com/users?limit=10")
    print_request(http_request)
```

**Success Criteria:**
- Functions execute without errors
- Output is readable and informative
- You understand each line of code you wrote

<details>
<summary>💡 Hint for analyze_url</summary>

```python
def analyze_url(url):
    print(f"Full URL: {url}")
    
    # Find protocol
    if "://" in url:
        protocol, rest = url.split("://", 1)
        print(f"Protocol: {protocol}")
        url = rest
    
    # Check for query parameters
    if "?" in url:
        path, query = url.split("?", 1)
        print(f"Path: {path}")
        print(f"Query: {query}")
    else:
        print(f"Path: {url}")
```
</details>

<details>
<summary>💡 Hint for print_request</summary>

```python
def print_request(request):
    print(f"{request['method']} {request['url']}")
    print("\nHeaders:")
    for key, value in request['headers'].items():
        print(f"  {key}: {value}")
```
</details>

---

## Exercise 5: Command Line Navigation

**Goal:** Ensure comfort with basic terminal operations.

**Tasks:**
Complete these command line operations and document what each command does:

1. Create a directory structure:
   ```bash
   mkdir -p networking-course/module-01/exercises
   ```

2. Navigate into it:
   ```bash
   cd networking-course/module-01/exercises
   ```

3. Create a file:
   ```bash
   touch notes.txt
   ```
   (Windows: `type nul > notes.txt`)

4. List files:
   ```bash
   ls -la
   ```
   (Windows: `dir`)

5. Go back to parent directory:
   ```bash
   cd ../..
   ```

6. Show current directory:
   ```bash
   pwd
   ```
   (Windows: `cd`)

7. Remove the test directory:
   ```bash
   rm -rf networking-course
   ```
   (Windows: `rmdir /s networking-course`)

**Document:** Write down what each command does in your own words.

---

## Exercise 6: Text Editor Familiarity

**Goal:** Ensure you can efficiently work with code files.

**Tasks:**
1. Open your text editor (VS Code, PyCharm, etc.)
2. Create a new file called `hello_network.py`
3. Write a simple program:
   ```python
   def main():
       print("Hello, Network Fundamentals!")
       print("I'm ready to learn about:")
       topics = ["HTTP", "REST APIs", "WebSockets", "Security"]
       for i, topic in enumerate(topics, 1):
           print(f"  {i}. {topic}")
   
   if __name__ == "__main__":
       main()
   ```
4. Save the file
5. Run it from terminal:
   ```bash
   python hello_network.py
   ```

**Success Criteria:**
- Can create and save files quickly
- Comfortable with syntax highlighting
- Can run code from terminal

---

## Exercise 7: Git Basics (Optional)

**Goal:** Practice basic Git operations.

**Tasks:**
1. Check Git version:
   ```bash
   git --version
   ```

2. Configure Git (if not done already):
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

3. Initialize a test repository:
   ```bash
   mkdir git-test
   cd git-test
   git init
   ```

4. Create a file and commit:
   ```bash
   echo "# Test Repository" > README.md
   git add README.md
   git commit -m "Initial commit"
   ```

5. View commit history:
   ```bash
   git log
   ```

**Success Criteria:**
- Git commands execute successfully
- Understand basic Git workflow (init, add, commit)
- Can view repository history

---

## Challenge Exercise: Setup Verification Script

**Goal:** Create a comprehensive setup checker.

**Tasks:**
Create a script `verify_setup.py` that checks:
1. Python version (must be 3.7+)
2. pip is installed
3. requests library is installed
4. Can make a simple HTTP request
5. Prints a success message if all checks pass

**Starter Code:**
```python
import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.7 or higher"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 7:
        print("✅ Python version is sufficient")
        return True
    else:
        print("❌ Python version must be 3.7 or higher")
        return False

def check_pip():
    """Check if pip is installed"""
    try:
        result = subprocess.run(['pip', '--version'], 
                              capture_output=True, text=True)
        print(f"✅ pip is installed: {result.stdout.strip()}")
        return True
    except:
        print("❌ pip is not installed")
        return False

# Add more checks here...

def main():
    print("=== Setup Verification ===\n")
    checks = [
        check_python_version(),
        check_pip(),
        # Add more checks...
    ]
    
    if all(checks):
        print("\n🎉 All checks passed! You're ready to start!")
    else:
        print("\n⚠️ Some checks failed. Please review the setup instructions.")

if __name__ == "__main__":
    main()
```

**Complete the script** by adding checks for:
- requests library
- Making a test HTTP request
- Any other verification you think is useful

---

## Reflection Questions

After completing these exercises, answer these questions:

1. What command do you use to activate a virtual environment on your system?
2. Why is it important to use virtual environments?
3. What's the difference between `python` and `python3` commands?
4. How do you install a Python package using pip?
5. What's your preferred text editor and why?

---

## Next Steps

Once you've completed these exercises:
- ✅ You're comfortable with the command line
- ✅ You can create and activate virtual environments
- ✅ You can install and use Python packages
- ✅ Your text editor is set up and ready
- ✅ You understand basic Python and Git

**Ready to move forward?** Head to [Module 01: How The Internet Works](../01-How-The-Internet-Works/) to start learning networking fundamentals!

---

**Having trouble with any exercises?** Check the [Troubleshooting Guide](../troubleshooting-guides/module-00-setup-issues.md) or reach out for help.
