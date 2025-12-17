# 🛠️ Setup Guide

Detailed setup instructions for different operating systems.

## Table of Contents
- [Windows Setup](#windows-setup)
- [macOS Setup](#macos-setup)
- [Linux Setup](#linux-setup)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Windows Setup

### 1. Install Python

1. Visit [python.org](https://www.python.org/downloads/)
2. Download Python 3.7 or higher
3. **Important:** Check "Add Python to PATH" during installation
4. Complete the installation

**Verify:**
```cmd
python --version
pip --version
```

### 2. Install Git (Optional)

1. Visit [git-scm.com](https://git-scm.com/download/win)
2. Download and install
3. Use default settings

**Verify:**
```cmd
git --version
```

### 3. Install Text Editor

**Recommended: VS Code**
1. Visit [code.visualstudio.com](https://code.visualstudio.com/)
2. Download and install
3. Install Python extension

**Alternatives:**
- PyCharm Community Edition
- Sublime Text
- Notepad++

### 4. Set Up Project

```cmd
REM Clone repository
git clone https://github.com/MrMichel93/Network-Fundamentals.git
cd Network-Fundamentals

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt
```

### 5. Enable Script Execution (if needed)

If you get execution policy errors:

```powershell
# Open PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Common Windows Issues

**Issue: "python not recognized"**
```cmd
# Add Python to PATH manually:
# 1. Search "Environment Variables" in Start menu
# 2. Edit system PATH
# 3. Add: C:\Users\YourName\AppData\Local\Programs\Python\Python39
# 4. Restart command prompt
```

**Issue: "pip not found"**
```cmd
# Use python -m pip instead
python -m pip install requests
```

---

## macOS Setup

### 1. Install Homebrew (Package Manager)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Python

```bash
# Install Python 3
brew install python3

# Verify
python3 --version
pip3 --version
```

### 3. Install Git

```bash
# Git usually pre-installed, but to update:
brew install git

# Verify
git --version
```

### 4. Install Text Editor

**Recommended: VS Code**
```bash
brew install --cask visual-studio-code
```

**Or download from:** [code.visualstudio.com](https://code.visualstudio.com/)

### 5. Set Up Project

```bash
# Clone repository
git clone https://github.com/MrMichel93/Network-Fundamentals.git
cd Network-Fundamentals

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 6. Install Additional Tools

```bash
# curl (usually pre-installed)
brew install curl

# jq (JSON processor)
brew install jq
```

### Common macOS Issues

**Issue: "command not found: python"**
```bash
# Use python3 instead
python3 script.py

# Or create an alias
echo "alias python=python3" >> ~/.zshrc
source ~/.zshrc
```

**Issue: Permission errors**
```bash
# Never use sudo with pip in virtual environment!
# Make sure virtual environment is activated first
```

---

## Linux Setup

### Ubuntu / Debian

```bash
# Update package list
sudo apt update

# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv

# Install Git
sudo apt install git

# Install curl
sudo apt install curl

# Install jq (optional)
sudo apt install jq

# Verify installations
python3 --version
pip3 --version
git --version
```

### Fedora / CentOS / RHEL

```bash
# Install Python 3
sudo dnf install python3 python3-pip

# Install Git
sudo dnf install git

# Install curl
sudo dnf install curl
```

### Arch Linux

```bash
# Install Python
sudo pacman -S python python-pip

# Install Git
sudo pacman -S git

# Install curl
sudo pacman -S curl
```

### Set Up Project (All Linux Distributions)

```bash
# Clone repository
git clone https://github.com/MrMichel93/Network-Fundamentals.git
cd Network-Fundamentals

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Text Editor Options for Linux

```bash
# VS Code
sudo snap install code --classic

# Or download from: code.visualstudio.com
```

**Alternatives:**
- vim / neovim
- Sublime Text
- PyCharm
- Atom

### Common Linux Issues

**Issue: "python not found"**
```bash
# Use python3
python3 script.py

# Or create symlink
sudo ln -s /usr/bin/python3 /usr/bin/python
```

**Issue: "pip: command not found"**
```bash
# Use python3 -m pip
python3 -m pip install requests
```

---

## Verification

After setup, verify everything works:

### 1. Test Python

```bash
# Check Python version (should be 3.7+)
python --version    # or python3 --version

# Check pip
pip --version       # or pip3 --version
```

### 2. Test Virtual Environment

```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# You should see (venv) in your prompt
(venv) $

# Deactivate when done
deactivate
```

### 3. Test Dependencies

```bash
# Activate virtual environment first
source venv/bin/activate  # Mac/Linux

# Create test file
cat > test_setup.py << 'EOF'
import sys
import requests

print(f"Python version: {sys.version}")
print(f"Requests version: {requests.__version__}")
print("\n✅ Setup successful! You're ready to start learning!")
EOF

# Run test
python test_setup.py
```

### 4. Test Network Tools

```bash
# Test curl
curl -I https://github.com

# Test ping
ping -c 4 google.com  # Mac/Linux
ping -n 4 google.com  # Windows

# Test nslookup
nslookup github.com
```

---

## Troubleshooting

### Virtual Environment Issues

**Problem:** Can't activate virtual environment

**Windows:**
```cmd
# Try different activation scripts
venv\Scripts\activate.bat  # Command Prompt
venv\Scripts\Activate.ps1  # PowerShell
```

**Mac/Linux:**
```bash
# Make sure you're in the right directory
cd Network-Fundamentals
source venv/bin/activate
```

### Package Installation Issues

**Problem:** pip install fails

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Try installing with --user flag
pip install --user requests

# Clear pip cache
pip cache purge
pip install -r requirements.txt
```

### Port Already in Use

```bash
# Find what's using port 5000
# Mac/Linux
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or use a different port
python app.py --port 5001
```

### Firewall Issues

**Windows:**
1. Search "Firewall" in Start menu
2. Allow Python through firewall
3. Allow the specific port (5000, 8000, etc.)

**Mac:**
1. System Preferences → Security & Privacy → Firewall
2. Click Firewall Options
3. Allow Python

**Linux:**
```bash
# Ubuntu/Debian (UFW)
sudo ufw allow 5000

# CentOS/RHEL (firewalld)
sudo firewall-cmd --add-port=5000/tcp --permanent
sudo firewall-cmd --reload
```

### SSL Certificate Errors

```bash
# Update certificates
pip install --upgrade certifi

# Or temporarily disable SSL verification (development only!)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org package_name
```

---

## Next Steps

✅ **Setup complete!** You're ready to start learning.

Head over to [00-Prerequisites](./00-Prerequisites/) to begin the course!

---

## Need More Help?

- Check the [FAQ](./FAQ.md)
- Review module-specific README files
- Open a GitHub issue
- Search online for platform-specific issues

[Back to Home](./README.md)
