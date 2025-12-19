# 📊 Prerequisites - Diagrams

Visual representations to help understand prerequisite concepts and development environment setup.

## 1. Python Development Environment Structure

This diagram shows how Python, pip, and virtual environments relate to each other:

```
┌─────────────────────────────────────────────────────────┐
│                    Your Computer                        │
│                                                         │
│  ┌────────────────────────────────────────────────┐   │
│  │           System Python Installation            │   │
│  │                                                 │   │
│  │  ┌─────────────┐      ┌──────────────┐        │   │
│  │  │   Python    │      │     pip      │        │   │
│  │  │  (3.9.7)    │◄────►│  (package    │        │   │
│  │  │ Interpreter │      │   manager)   │        │   │
│  │  └─────────────┘      └──────────────┘        │   │
│  │         │                                      │   │
│  │         │ creates                              │   │
│  │         ▼                                      │   │
│  │  ┌────────────────────────────────────┐       │   │
│  │  │   Project Virtual Environments     │       │   │
│  │  │                                    │       │   │
│  │  │  ┌──────────┐    ┌──────────┐    │       │   │
│  │  │  │ venv1/   │    │ venv2/   │    │       │   │
│  │  │  ├──────────┤    ├──────────┤    │       │   │
│  │  │  │ python   │    │ python   │    │       │   │
│  │  │  │ pip      │    │ pip      │    │       │   │
│  │  │  │ requests │    │ flask    │    │       │   │
│  │  │  │ numpy    │    │ django   │    │       │   │
│  │  │  └──────────┘    └──────────┘    │       │   │
│  │  │                                    │       │   │
│  │  │  Each project has isolated deps   │       │   │
│  │  └────────────────────────────────────┘       │   │
│  └────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Key Points:**
- System Python is the base installation
- Each project gets its own virtual environment
- Virtual environments are isolated from each other
- Same package can have different versions in different environments

---

## 2. Virtual Environment Workflow

The step-by-step process of setting up and using a virtual environment:

```
Start
  │
  ├─► 1. Create Virtual Environment
  │      $ python3 -m venv venv
  │
  │      ┌─────────────┐
  │      │  venv/      │
  │      │  ├── bin/   │  ← Contains activate script
  │      │  ├── lib/   │  ← Contains packages
  │      │  └── ...    │
  │      └─────────────┘
  │
  ├─► 2. Activate Environment
  │      $ source venv/bin/activate
  │      (venv) $  ← Notice the prompt change!
  │
  ├─► 3. Install Packages
  │      (venv) $ pip install requests
  │
  │      Packages install to venv/lib/
  │      not system Python!
  │
  ├─► 4. Work on Project
  │      (venv) $ python script.py
  │
  │      Uses packages from venv/
  │
  └─► 5. Deactivate When Done
         (venv) $ deactivate
         $  ← Back to normal prompt
```

---

## 3. Package Installation Flow

Understanding where packages go when you install them:

```
┌──────────────────────────────────────────────────────────┐
│                  pip install requests                    │
└────────────────────┬─────────────────────────────────────┘
                     │
        ┌────────────▼────────────┐
        │  Is virtual env active? │
        └────────┬────────┬───────┘
                 │        │
            YES  │        │  NO
                 │        │
        ┌────────▼──┐  ┌──▼─────────┐
        │ Install   │  │  Install   │
        │ to venv/  │  │  to system │
        │ lib/      │  │  Python    │
        └───────────┘  └────────────┘
             │              │
             │              │
        ✅ Good!       ⚠️  Risky!
        Isolated      May conflict
        Per-project   System-wide
```

**Best Practice:** Always activate virtual environment before `pip install`

---

## 4. Command Line Directory Navigation

Visual representation of directory structure and navigation:

```
/home/user/
    │
    ├── projects/
    │   │
    │   ├── networking-course/        ← You are here (pwd)
    │   │   │
    │   │   ├── venv/                 │ cd venv
    │   │   │   └── bin/              │ cd ..
    │   │   │                         ▼
    │   │   ├── 00-Prerequisites/     ← cd 00-Prerequisites
    │   │   │   ├── README.md
    │   │   │   └── exercises.md
    │   │   │
    │   │   ├── 01-How-The-Internet-Works/
    │   │   └── requirements.txt
    │   │
    │   └── another-project/          │ cd ../another-project
    │
    └── documents/                    │ cd ~/documents

Commands:
- pwd                    → /home/user/projects/networking-course
- cd 00-Prerequisites    → Move into subdirectory
- cd ..                  → Move up one level
- cd ~                   → Go to home directory
- cd /                   → Go to root directory
```

---

## 5. Git + Virtual Environment Best Practices

What to commit to Git and what to ignore:

```
my-project/
├── .git/                     ← Git metadata (automatic)
├── .gitignore               ← Tells Git what to ignore
│   Contents:
│   venv/                    ← Don't commit virtual env
│   __pycache__/             ← Don't commit Python cache
│   *.pyc                    ← Don't commit compiled files
│
├── venv/                     ❌ NOT in Git (too large, system-specific)
│   └── ...                     
│
├── requirements.txt         ✅ IN Git (others can recreate venv)
│   requests==2.26.0
│   flask==2.0.1
│
├── src/                     ✅ IN Git (your actual code)
│   └── app.py
│
└── README.md                ✅ IN Git (documentation)


Workflow for others:
1. git clone <repo>
2. python3 -m venv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. Ready to work!
```

---

## 6. Python Import System

How Python finds and loads modules:

```
When you write: import requests

Python searches in order:
1. Current directory
2. Standard library     (/usr/lib/python3.9/)
3. Site packages       (system: /usr/lib/python3.9/site-packages/)
                       (venv: venv/lib/python3.9/site-packages/)

┌─────────────────────────────────────────┐
│  import requests                        │
└────────┬────────────────────────────────┘
         │
         ├─► Look in current dir/         ✗ Not found
         │
         ├─► Look in standard library/    ✗ Not found
         │
         └─► Look in site-packages/       ✓ Found!
             │
             └─► Load and use the module

If virtual env is active:
  - Checks venv/lib/.../site-packages/ FIRST
  - Falls back to system site-packages

If NOT active:
  - Only checks system site-packages
  - Won't find packages installed in venv
```

---

## 7. Development Environment Setup Flow

Complete setup process for a new project:

```
┌─────────────────────────────────────────────────────────┐
│                  New Project Setup                      │
└───┬─────────────────────────────────────────────────────┘
    │
    ├─► Step 1: Create project directory
    │   $ mkdir my-networking-project
    │   $ cd my-networking-project
    │
    ├─► Step 2: Initialize Git (optional)
    │   $ git init
    │   $ touch .gitignore
    │
    ├─► Step 3: Create virtual environment
    │   $ python3 -m venv venv
    │
    ├─► Step 4: Activate virtual environment
    │   $ source venv/bin/activate
    │   (venv) $ ← Confirm activation
    │
    ├─► Step 5: Install dependencies
    │   (venv) $ pip install requests flask
    │
    ├─► Step 6: Save dependencies
    │   (venv) $ pip freeze > requirements.txt
    │
    ├─► Step 7: Create project files
    │   (venv) $ touch app.py
    │   (venv) $ touch README.md
    │
    └─► Step 8: Start coding!
        (venv) $ code .  # Open in VS Code
        
Ready to develop! ✅
```

---

## 8. Troubleshooting Decision Tree

When things go wrong:

```
                    Problem Occurred
                          │
                          ▼
            ┌─────────────────────────┐
            │ What's the error type?  │
            └──┬────────┬─────────┬───┘
               │        │         │
    ┌──────────▼──┐  ┌──▼────┐  ┌▼────────────────┐
    │ Command not │  │Module │  │ Permission      │
    │ found       │  │not    │  │ denied          │
    └──┬──────────┘  │found  │  └┬────────────────┘
       │             └──┬────┘   │
       ▼                ▼        ▼
    Check PATH     Activate    Check if using
    Check spelling  venv and    sudo (don't!)
    Install tool    pip install Use venv instead
```

---

## 9. Cross-Platform Considerations

Differences between operating systems:

```
┌────────────────┬──────────────────┬───────────────────┐
│    Action      │   Mac/Linux      │     Windows       │
├────────────────┼──────────────────┼───────────────────┤
│ Create venv    │ python3 -m venv  │ python -m venv    │
│                │ venv             │ venv              │
├────────────────┼──────────────────┼───────────────────┤
│ Activate venv  │ source venv/     │ venv\Scripts\     │
│                │ bin/activate     │ activate          │
├────────────────┼──────────────────┼───────────────────┤
│ Python command │ python3          │ python            │
├────────────────┼──────────────────┼───────────────────┤
│ Pip command    │ pip3             │ pip               │
├────────────────┼──────────────────┼───────────────────┤
│ Path separator │ / (forward)      │ \ (backslash)     │
│                │                  │ or / (both work)  │
├────────────────┼──────────────────┼───────────────────┤
│ List files     │ ls               │ dir               │
├────────────────┼──────────────────┼───────────────────┤
│ Clear screen   │ clear            │ cls               │
└────────────────┴──────────────────┴───────────────────┘

Tip: In Python code, always use / for paths (works everywhere)
```

---

## 10. Good vs Bad Setup

Compare correct and incorrect setups:

```
❌ Bad Setup                          ✅ Good Setup
────────────────────────────          ────────────────────────────

$ sudo pip install requests           $ python3 -m venv venv
   (system-wide, needs root)          $ source venv/bin/activate
                                      (venv) $ pip install requests
                                         (isolated, no root)

$ python2 script.py                   $ python3 --version
   (outdated Python version)             (confirm Python 3.7+)
                                      $ python3 script.py

$ pip install everything              $ pip install -r requirements.txt
   (no version control)                  (specific versions)

projects/                             projects/
├── venv/  ← commits to Git          ├── venv/  ← in .gitignore
└── app.py   (huge repo!)            ├── requirements.txt ← in Git
                                      └── app.py
```

---

## Summary

These diagrams illustrate:
- ✅ Virtual environment isolation
- ✅ Proper package installation workflow
- ✅ Directory navigation concepts
- ✅ Git and Python integration
- ✅ Platform differences
- ✅ Troubleshooting approaches

**Next:** Apply these concepts in the [exercises](./exercises.md) and verify understanding with the [checkpoint](./checkpoint.md).
