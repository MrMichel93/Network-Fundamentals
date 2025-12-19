# ✓ Prerequisites - Checkpoint

Use this checkpoint to assess your readiness before moving to Module 01.

## Self-Assessment Quiz

Answer these questions honestly to gauge your understanding.

### Section 1: Environment Setup (5 questions)

**1. What command creates a Python virtual environment?**
- [ ] A) `python setup venv`
- [ ] B) `python3 -m venv venv`
- [ ] C) `pip install venv`
- [ ] D) `create-venv`

<details>
<summary>Answer</summary>
**B** - `python3 -m venv venv` creates a virtual environment named 'venv'
</details>

---

**2. How do you activate a virtual environment on Mac/Linux?**
- [ ] A) `activate venv`
- [ ] B) `venv/bin/activate`
- [ ] C) `source venv/bin/activate`
- [ ] D) `python activate`

<details>
<summary>Answer</summary>
**C** - `source venv/bin/activate` (Windows uses `venv\Scripts\activate`)
</details>

---

**3. What does `pip install -r requirements.txt` do?**
- [ ] A) Creates a requirements file
- [ ] B) Installs all packages listed in requirements.txt
- [ ] C) Removes all installed packages
- [ ] D) Updates pip to latest version

<details>
<summary>Answer</summary>
**B** - Installs all dependencies listed in requirements.txt
</details>

---

**4. Why should you use virtual environments?**
- [ ] A) They make Python run faster
- [ ] B) They're required by law
- [ ] C) They isolate project dependencies
- [ ] D) They backup your code automatically

<details>
<summary>Answer</summary>
**C** - Virtual environments isolate dependencies, preventing conflicts between projects
</details>

---

**5. What indicates a virtual environment is active in your terminal?**
- [ ] A) Terminal turns green
- [ ] B) You see `(venv)` in the prompt
- [ ] C) Python icon appears
- [ ] D) Terminal asks for confirmation

<details>
<summary>Answer</summary>
**B** - The environment name (e.g., `(venv)`) appears at the start of your prompt
</details>

---

### Section 2: Command Line Basics (5 questions)

**6. What command shows your current directory?**
- [ ] A) `ls`
- [ ] B) `cd`
- [ ] C) `pwd`
- [ ] D) `dir`

<details>
<summary>Answer</summary>
**C** - `pwd` (Print Working Directory) shows your current location
</details>

---

**7. How do you navigate to a parent directory?**
- [ ] A) `cd ..`
- [ ] B) `cd back`
- [ ] C) `cd parent`
- [ ] D) `cd ~`

<details>
<summary>Answer</summary>
**A** - `cd ..` moves up one directory level
</details>

---

**8. What does `ls -la` do? (Mac/Linux)**
- [ ] A) Lists only hidden files
- [ ] B) Lists files in alphabetical order
- [ ] C) Lists all files with detailed information
- [ ] D) Deletes all files

<details>
<summary>Answer</summary>
**C** - Lists all files (including hidden) with detailed info like permissions, size, and date
</details>

---

**9. How do you create a new directory?**
- [ ] A) `new-dir my-folder`
- [ ] B) `mkdir my-folder`
- [ ] C) `create my-folder`
- [ ] D) `folder my-folder`

<details>
<summary>Answer</summary>
**B** - `mkdir` (make directory) creates a new folder
</details>

---

**10. What's the safest way to delete a file?**
- [ ] A) `rm -rf *` (delete everything)
- [ ] B) `rm filename` (specific file)
- [ ] C) `delete all`
- [ ] D) Drag to trash in GUI

<details>
<summary>Answer</summary>
**B** or **D** - Delete specific files, not everything. When learning, GUI trash is reversible.
</details>

---

### Section 3: Python Basics (5 questions)

**11. Which Python version is required for this course?**
- [ ] A) Python 2.7+
- [ ] B) Python 3.5+
- [ ] C) Python 3.7+
- [ ] D) Any version

<details>
<summary>Answer</summary>
**C** - Python 3.7 or higher is required
</details>

---

**12. What's the output of this code?**
```python
def greet(name="World"):
    return f"Hello, {name}!"

print(greet())
```
- [ ] A) `Hello, !`
- [ ] B) `Hello, World!`
- [ ] C) `Hello, name!`
- [ ] D) Error

<details>
<summary>Answer</summary>
**B** - Default parameter value is used: `Hello, World!`
</details>

---

**13. What does this do?**
```python
import requests
```
- [ ] A) Creates a new module called requests
- [ ] B) Imports the requests library for use
- [ ] C) Requests data from the internet
- [ ] D) Checks if requests is installed

<details>
<summary>Answer</summary>
**B** - Imports the requests library so you can use its functions
</details>

---

**14. How do you check if a Python library is installed?**
- [ ] A) `python --check requests`
- [ ] B) `pip show requests`
- [ ] C) `is-installed requests`
- [ ] D) `library requests`

<details>
<summary>Answer</summary>
**B** - `pip show requests` displays info about an installed package
</details>

---

**15. What's wrong with this code?**
```python
import requests

response = requests.get('https://api.github.com')
print(response.status_code
```
- [ ] A) Missing closing parenthesis
- [ ] B) Wrong URL
- [ ] C) Should use POST not GET
- [ ] D) Nothing wrong

<details>
<summary>Answer</summary>
**A** - Missing closing parenthesis on the print statement
</details>

---

## Practical Skills Checklist

Check off each skill you can perform confidently:

### Environment Management
- [ ] I can create a Python virtual environment
- [ ] I can activate/deactivate a virtual environment
- [ ] I can install packages using pip
- [ ] I can create a requirements.txt file
- [ ] I know when my virtual environment is active

### Command Line Operations
- [ ] I can open a terminal/command prompt
- [ ] I can navigate between directories using cd
- [ ] I can list files in a directory
- [ ] I can create and delete files/directories
- [ ] I know how to check my current directory

### Python Skills
- [ ] I can write and run a Python script
- [ ] I understand variables and data types
- [ ] I can write functions with parameters
- [ ] I can use if/else statements and loops
- [ ] I can import and use libraries

### Tools
- [ ] I have a text editor/IDE installed and know how to use it
- [ ] I can run Python from the command line
- [ ] I have Git installed (optional but recommended)
- [ ] I have a modern web browser with DevTools

---

## Hands-On Challenge

Complete this mini-project to prove readiness:

### Challenge: Environment Setup Validator

**Task:** Create a script that validates your setup.

**Requirements:**
1. Create a new directory: `prerequisite-check`
2. Create a virtual environment in it
3. Create a script: `validate.py`
4. The script should:
   - Print Python version
   - Check if requests library is installed
   - Make a test HTTP request to https://httpbin.org/get
   - Print success message if everything works

**Starter code:**
```python
import sys

def check_python_version():
    print(f"Python version: {sys.version}")
    if sys.version_info >= (3, 7):
        return True
    return False

def check_requests():
    try:
        import requests
        print(f"✓ requests library is installed")
        return True
    except ImportError:
        print("✗ requests library not found")
        return False

def test_http_request():
    try:
        import requests
        response = requests.get('https://httpbin.org/get')
        if response.status_code == 200:
            print(f"✓ HTTP request successful (status: {response.status_code})")
            return True
        else:
            print(f"✗ HTTP request failed (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"✗ HTTP request error: {e}")
        return False

def main():
    print("=== Setup Validation ===\n")
    
    checks = [
        check_python_version(),
        check_requests(),
        test_http_request()
    ]
    
    print("\n" + "="*30)
    if all(checks):
        print("✅ All checks passed! You're ready to continue!")
    else:
        print("❌ Some checks failed. Review the setup instructions.")

if __name__ == "__main__":
    main()
```

**Expected output:**
```
=== Setup Validation ===

Python version: 3.9.7 (...)
✓ requests library is installed
✓ HTTP request successful (status: 200)

==============================
✅ All checks passed! You're ready to continue!
```

---

## Scoring Guide

Count your correct answers:

- **13-15 correct:** Excellent! You're well-prepared.
- **10-12 correct:** Good foundation. Review weak areas.
- **7-9 correct:** Need more practice. Revisit README and exercises.
- **Below 7:** Review the Prerequisites module thoroughly before continuing.

Count your checklist items:

- **All checked:** Ready to proceed!
- **3-5 unchecked:** Practice those specific skills.
- **6+ unchecked:** Spend more time with the exercises.

---

## Final Readiness Questions

Before moving to Module 01, answer YES to all:

1. **Can you create and activate a virtual environment without help?**
   - [ ] Yes, I'm confident
   - [ ] No, I need more practice

2. **Can you install a Python package and use it in a script?**
   - [ ] Yes, I've done it successfully
   - [ ] No, I'm still unsure

3. **Are you comfortable with basic command line navigation?**
   - [ ] Yes, I can navigate directories and run commands
   - [ ] No, I need more practice

4. **Do you understand basic Python syntax?**
   - [ ] Yes, I can write simple scripts
   - [ ] No, I need to review Python basics

5. **Have you successfully completed the hands-on challenge?**
   - [ ] Yes, my script runs correctly
   - [ ] No, I encountered issues

---

## What to Do Based on Results

### ✅ Ready to Continue (4-5 YES answers)
Great job! You have the foundation needed for networking fundamentals.

**Next step:** Proceed to [Module 01: How The Internet Works](../01-How-The-Internet-Works/)

### 🔄 Need More Practice (2-3 YES answers)
You're getting there but need to solidify some areas.

**Next steps:**
1. Review the [Prerequisites README](./README.md)
2. Complete the [exercises](./exercises.md) you skipped
3. Review [common mistakes](./common-mistakes.md)
4. Retake this checkpoint

### 📚 Need to Review (0-1 YES answers)
Take time to build your foundation properly.

**Next steps:**
1. Carefully read the [Prerequisites README](./README.md)
2. Complete all [exercises](./exercises.md)
3. Review Python basics (external resources if needed)
4. Practice command line basics
5. Retake this checkpoint in a few days

---

## Additional Resources

If you need more help:

- **Python Basics:** [Python.org Tutorial](https://docs.python.org/3/tutorial/)
- **Command Line:** [Command Line Crash Course](https://learnpythonthehardway.org/book/appendixa.html)
- **Virtual Environments:** [Python venv documentation](https://docs.python.org/3/library/venv.html)
- **pip Basics:** [pip User Guide](https://pip.pypa.io/en/stable/user_guide/)

---

## Remember

🎯 **The goal isn't perfection** - it's confidence in the basics.

🚀 **Learning is iterative** - you'll get better with practice.

💪 **Everyone starts somewhere** - take your time and build solid foundations.

When you're ready, move on to [Module 01: How The Internet Works](../01-How-The-Internet-Works/)!
