# Module 00 - Setup Issues Troubleshooting

Common setup problems and solutions.

## Python Installation Issues

### Problem: "python: command not found"

**Symptoms:**
```bash
$ python --version
bash: python: command not found
```

**Solutions:**
1. Try `python3` instead:
   ```bash
   python3 --version
   ```

2. Check if Python is installed:
   ```bash
   which python3  # Mac/Linux
   where python   # Windows
   ```

3. Install Python from [python.org](https://python.org)

4. Add Python to PATH (Windows):
   - Reinstall Python
   - Check "Add Python to PATH" during installation

---

### Problem: pip not found

**Symptoms:**
```bash
$ pip --version
bash: pip: command not found
```

**Solutions:**
1. Try `pip3`:
   ```bash
   pip3 --version
   ```

2. Install pip:
   ```bash
   python3 -m ensurepip
   ```

3. Use python -m pip:
   ```bash
   python3 -m pip --version
   python3 -m pip install package_name
   ```

---

## Virtual Environment Issues

### Problem: Cannot activate virtual environment (Windows)

**Symptoms:**
```powershell
PS> venv\Scripts\activate
cannot be loaded because running scripts is disabled
```

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

---

### Problem: Virtual environment not activating

**Symptoms:**
```bash
$ source venv/bin/activate
# Nothing happens, no (venv) in prompt
```

**Solutions:**
1. Check you're in the correct directory:
   ```bash
   pwd
   ls venv/
   ```

2. Recreate virtual environment:
   ```bash
   rm -rf venv
   python3 -m venv venv
   ```

3. Try full path:
   ```bash
   source /full/path/to/venv/bin/activate
   ```

---

## Package Installation Issues

### Problem: Permission denied when installing packages

**Symptoms:**
```bash
$ pip install requests
ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied
```

**Solutions:**
1. **Best:** Use virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install requests
   ```

2. **If you must** install globally (not recommended):
   ```bash
   pip install --user requests
   ```

3. **Never use sudo** with pip inside a virtual environment

---

### Problem: Package version conflicts

**Symptoms:**
```bash
$ pip install package_a package_b
ERROR: package_a requires package_c<2.0, but you have package_c 2.1
```

**Solutions:**
1. Install from requirements.txt with exact versions:
   ```bash
   pip install -r requirements.txt
   ```

2. Create fresh virtual environment:
   ```bash
   deactivate
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

---

## IDE/Editor Issues

### Problem: VS Code not finding Python interpreter

**Solution:**
1. Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
2. Type "Python: Select Interpreter"
3. Choose your Python installation or virtual environment

---

### Problem: Import errors in IDE but code runs

**Solution:**
1. IDE might not be using the virtual environment
2. Set interpreter to venv:
   - VS Code: Select interpreter
   - PyCharm: Settings → Project → Python Interpreter

---

## Git Issues

### Problem: Git not found

**Symptoms:**
```bash
$ git --version
bash: git: command not found
```

**Solutions:**
- Mac: Install with `brew install git` or download from git-scm.com
- Linux: `sudo apt-get install git` or `sudo yum install git`
- Windows: Download from git-scm.com

---

## General Troubleshooting Steps

1. **Read the error message carefully** - it usually tells you what's wrong
2. **Check you're in the right directory** - `pwd` to confirm
3. **Verify virtual environment is active** - look for `(venv)` in prompt
4. **Try restarting** - terminal, IDE, or computer
5. **Search the error message** - others have likely encountered it
6. **Check versions** - ensure Python 3.7+ and latest pip

---

## Getting Help

If stuck:
1. Review the [Prerequisites README](../00-Prerequisites/README.md)
2. Check [Common Mistakes](../00-Prerequisites/common-mistakes.md)
3. Search online with specific error message
4. Ask for help with:
   - Exact error message
   - What you tried
   - Your OS and Python version
   - Steps to reproduce

---

**Remember:** Everyone encounters setup issues. Take your time, read error messages carefully, and don't hesitate to ask for help!
