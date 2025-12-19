# 📊 Module 02: Command-Line Mastery - Diagrams

Visual representations to help understand the Linux file system, processes, and shell operations.

## 1. Linux File System Hierarchy

Tree diagram showing the standard Linux directory structure:

```
/  (root)
├── home/
│   ├── user1/
│   │   ├── Documents/
│   │   ├── Downloads/
│   │   ├── Projects/
│   │   └── .bashrc
│   └── user2/
│       └── ...
│
├── var/
│   ├── log/         ← System and application logs
│   │   ├── syslog
│   │   ├── auth.log
│   │   └── nginx/
│   ├── www/         ← Web server files
│   │   └── html/
│   └── tmp/         ← Temporary files
│
├── etc/             ← Configuration files
│   ├── nginx/
│   │   └── nginx.conf
│   ├── ssh/
│   │   └── sshd_config
│   ├── hosts
│   ├── passwd
│   └── fstab
│
├── usr/             ← User programs and data
│   ├── bin/         ← User commands
│   ├── lib/         ← Libraries
│   ├── local/       ← Locally installed software
│   └── share/       ← Shared data
│
├── bin/             ← Essential command binaries
│   ├── ls
│   ├── cp
│   ├── mv
│   └── bash
│
├── sbin/            ← System binaries (admin)
│   ├── shutdown
│   ├── reboot
│   └── iptables
│
├── tmp/             ← Temporary files (cleared on boot)
│   └── ...
│
├── opt/             ← Optional software packages
│   └── ...
│
├── dev/             ← Device files
│   ├── sda          ← Hard disk
│   ├── tty          ← Terminal
│   └── null         ← Null device
│
├── proc/            ← Process information (virtual)
│   ├── cpuinfo
│   ├── meminfo
│   └── [pid]/
│
├── sys/             ← System information (virtual)
│   └── ...
│
├── boot/            ← Boot loader files
│   ├── vmlinuz      ← Kernel
│   └── grub/
│
├── lib/             ← Essential shared libraries
│   └── ...
│
├── media/           ← Removable media mount points
│   ├── cdrom/
│   └── usb/
│
├── mnt/             ← Temporary mount points
│   └── ...
│
└── root/            ← Root user's home directory
    └── ...
```

**Key Directory Purposes:**

| Directory | Purpose | Example Contents |
|-----------|---------|-----------------|
| `/home` | User personal files | Documents, projects, configs |
| `/etc` | System configuration | nginx.conf, hosts, passwd |
| `/var` | Variable data | Logs, caches, databases |
| `/usr` | User programs | Applications, libraries |
| `/tmp` | Temporary files | Session data, temp files |
| `/bin` | Essential binaries | ls, cp, bash |
| `/dev` | Device files | Hard drives, terminals |

---

## 2. Process Hierarchy

Parent-child process relationships in Linux:

```
init (PID 1)  ← First process, parent of all
│
├── systemd   ← System and service manager
│   │
│   ├── sshd  ← SSH daemon
│   │   │
│   │   ├── sshd (session 1)  ← User connection
│   │   │   └── bash          ← User shell
│   │   │       ├── vim       ← Editor
│   │   │       └── ls        ← Command
│   │   │
│   │   └── sshd (session 2)
│   │       └── bash
│   │
│   ├── nginx ← Web server
│   │   ├── nginx (worker 1)
│   │   ├── nginx (worker 2)
│   │   └── nginx (worker 3)
│   │
│   └── docker ← Container runtime
│       ├── containerd
│       └── container processes
│
├── getty     ← Terminal login
│   └── login
│       └── bash
│
└── cron      ← Scheduled tasks
    └── backup.sh
```

**Process States:**
```
┌──────────┐
│  Created │
└────┬─────┘
     │
     ▼
┌──────────┐     ┌──────────┐
│  Ready   │────▶│ Running  │
└────▲─────┘     └────┬─────┘
     │                │
     │                ▼
     │           ┌──────────┐
     └───────────│ Waiting  │
                 └────┬─────┘
                      │
                      ▼
                 ┌──────────┐
                 │ Zombie   │
                 └────┬─────┘
                      │
                      ▼
                 ┌──────────┐
                 │Terminated│
                 └──────────┘

States:
- Ready: Waiting for CPU
- Running: Executing on CPU
- Waiting: Waiting for I/O
- Zombie: Completed but not cleaned up
- Terminated: Removed from system
```

**Process Information:**
```
$ ps aux
USER  PID  %CPU %MEM    VSZ   RSS TTY   STAT START   TIME COMMAND
root    1   0.0  0.1  19896  1234 ?     Ss   10:00   0:01 /sbin/init
root  123   0.5  2.0  98765  4321 ?     Sl   10:01   0:30 /usr/bin/nginx
user  456   1.2  3.5 123456  7890 pts/0 S+   10:05   1:15 python app.py

Fields:
PID  = Process ID
PPID = Parent Process ID
TTY  = Terminal
STAT = Process state (S=sleeping, R=running, Z=zombie)
TIME = CPU time used
```

---

## 3. Pipe and Redirect Flow

How data flows between commands and files:

```
Standard Streams:
─────────────────
stdin  (0)  ← Input  (keyboard)
stdout (1)  ← Output (screen)
stderr (2)  ← Errors (screen)


Basic Redirection:
──────────────────

command > file        Redirect stdout to file (overwrite)
command >> file       Redirect stdout to file (append)
command 2> file       Redirect stderr to file
command &> file       Redirect both stdout and stderr
command < file        Redirect file to stdin


Pipe Flow:
──────────

command1 → stdout ─┬─→ command2 → stdout → file
                   └─→ stderr → file


Example 1: Simple Pipe
──────────────────────

$ cat file.txt | grep "error" | wc -l

┌─────────┐       ┌──────────┐       ┌──────┐
│ cat     │stdout │ grep     │stdout │ wc   │
│file.txt │──────▶│ "error"  │──────▶│ -l   │
└─────────┘       └──────────┘       └──┬───┘
                                         │
                                         ▼
                                     terminal


Example 2: Complex Redirection
───────────────────────────────

$ command 2>&1 | tee output.log

┌─────────┐
│ command │
└────┬────┘
     │
     ├──stdout(1)──┐
     │             │
     └──stderr(2)──┤ (2>&1 redirects stderr to stdout)
                   │
                   ▼
              ┌────────┐
              │  tee   │
              └───┬────┘
                  │
          ┌───────┴────────┐
          │                │
          ▼                ▼
      terminal        output.log


Example 3: Multiple Redirections
─────────────────────────────────

$ ./script.sh > output.log 2> error.log < input.txt

    input.txt
        │
        │ stdin
        ▼
    ┌─────────┐
    │script.sh│
    └────┬────┘
         │
    ┌────┴─────┐
    │          │
stdout(1)   stderr(2)
    │          │
    ▼          ▼
output.log  error.log


Common Patterns:
────────────────

Discard output:
  command > /dev/null       # Discard stdout
  command 2> /dev/null      # Discard stderr
  command &> /dev/null      # Discard both

Save and display:
  command | tee file.txt    # Save to file and show on screen

Combine and redirect:
  command 2>&1 > file.txt   # Redirect both to file

Chain multiple commands:
  cmd1 | cmd2 | cmd3 | cmd4 # Pipeline
```

---

## 4. Shell Script Execution Flow

Flowchart showing script parsing and execution:

```
┌─────────────────────────────────────────┐
│     Script Execution Process            │
└────────────────┬────────────────────────┘
                 │
          ┌──────▼──────┐
          │ Run command │
          │ $ ./script.sh│
          └──────┬──────┘
                 │
          ┌──────▼──────────┐
          │ Check execute   │
          │ permission      │
          └──────┬──────────┘
                 │
          ┌──────┴──────┐
         Yes            No
          │              │
          │       ┌──────▼────────┐
          │       │ chmod +x      │
          │       │ script.sh     │
          │       └──────┬────────┘
          │              │
          │◄─────────────┘
          │
          ▼
   ┌──────────────┐
   │ Read shebang │
   │ #!/bin/bash  │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │ Launch shell │
   │ interpreter  │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │ Parse script │
   │ line by line │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │ Execute      │
   │ commands     │
   └──────┬───────┘
          │
          ▼
   ┌──────────────────┐
   │ Command type?    │
   └──┬───────────┬───┘
      │           │
  ┌───▼────┐  ┌───▼────┐
  │Built-in│  │External│
  │command │  │program │
  └───┬────┘  └───┬────┘
      │           │
      │           ▼
      │    ┌──────────────┐
      │    │ Fork process │
      │    └──────┬───────┘
      │           │
      │           ▼
      │    ┌──────────────┐
      │    │ Execute in   │
      │    │ child process│
      │    └──────┬───────┘
      │           │
      └───────────┴────────┐
                           │
                           ▼
                    ┌──────────────┐
                    │ Check exit   │
                    │ status       │
                    └──────┬───────┘
                           │
                    ┌──────┴──────┐
                   0 (success)  ≠0 (error)
                    │              │
                    ▼              ▼
             ┌──────────┐   ┌──────────┐
             │ Continue │   │ Handle   │
             │ script   │   │ error    │
             └────┬─────┘   └────┬─────┘
                  │              │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ More lines?  │
                  └──────┬───────┘
                         │
                  ┌──────┴──────┐
                 Yes            No
                  │              │
                  │              ▼
                  │       ┌──────────┐
                  └──────▶│  Exit    │
                          └──────────┘


Script Components:
──────────────────

#!/bin/bash              ← Shebang (interpreter)

# Variables
name="World"             ← Variable assignment
echo "Hello $name"       ← Variable expansion

# Control Flow
if [ condition ]; then   ← Conditional
    command
fi

for item in list; do     ← Loop
    command
done

# Functions
function_name() {        ← Function definition
    commands
    return 0
}

# Exit Status
exit 0                   ← Script exit code
```

---

## 5. Command Execution Search Path

How the shell finds commands:

```
$ command_name

Shell searches in order:
├── 1. Aliases
│   └── alias ll='ls -la'
│
├── 2. Shell Functions
│   └── function mycommand() { ... }
│
├── 3. Built-in Commands
│   └── cd, echo, exit, etc.
│
└── 4. External Programs (via $PATH)
    └── Search directories in order:
        ├── /usr/local/bin/
        ├── /usr/bin/
        ├── /bin/
        └── /usr/sbin/

Example PATH:
$ echo $PATH
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

Search order for 'python':
1. Check aliases: No
2. Check functions: No
3. Check built-ins: No
4. Check /usr/local/bin/python: No
5. Check /usr/bin/python: Found! ✓

Use 'which' to find command location:
$ which python
/usr/bin/python
```

---

## 6. File Permissions and Ownership

Understanding Linux file permissions:

```
File Permission Structure:
─────────────────────────

$ ls -l file.txt
-rwxr-xr--  1  user  group  1234  Dec 19 10:00  file.txt
│││││││││  │   │     │      │     │            │
│││││││││  │   │     │      │     └─ Filename
│││││││││  │   │     │      └─ Modification date
│││││││││  │   │     └─ Size in bytes
│││││││││  │   └─ Group
│││││││││  └─ Owner
││││││││└─ Other permissions (read)
│││││└──── Other permissions (no write)
││││└───── Other permissions (no execute)
│││└────── Group permissions (read)
││└─────── Group permissions (no write)
│└──────── Group permissions (execute)
└───────── Owner permissions (read, write, execute)


Permission Types:
─────────────────

r (read)    = 4   ─┐
w (write)   = 2   ─┼─ Octal notation
x (execute) = 1   ─┘

Examples:
rwx = 4+2+1 = 7
rw- = 4+2+0 = 6
r-x = 4+0+1 = 5
r-- = 4+0+0 = 4


Permission Diagram:
───────────────────

┌────────────────────────────────────┐
│            File Access             │
└────────────────┬───────────────────┘
                 │
        ┌────────┼────────┐
        │        │        │
   ┌────▼───┐ ┌──▼───┐ ┌─▼────┐
   │ Owner  │ │Group │ │Others│
   │  rwx   │ │ r-x  │ │ r--  │
   └────────┘ └──────┘ └──────┘
        7        5        4

$ chmod 754 file.txt


Permission Check Flow:
──────────────────────

User tries to access file
         │
         ▼
   Is user owner? ──Yes──▶ Check owner permissions
         │                      │
         No                     ▼
         │                  Apply owner rwx
         ▼
   Is user in group? ──Yes──▶ Check group permissions
         │                        │
         No                       ▼
         │                   Apply group rwx
         ▼
   Check other permissions
         │
         ▼
   Apply other rwx


Directory Permissions:
──────────────────────

For directories, permissions mean:
r (read)    = List directory contents (ls)
w (write)   = Create/delete files in directory
x (execute) = Access directory (cd)

Example:
drwxr-xr-x  2  user  group  4096  Dec 19  dirname/
│
└─ 'd' means directory
```

---

## 7. Environment Variables

Understanding shell environment:

```
Environment Variable Hierarchy:
───────────────────────────────

┌─────────────────────────────────┐
│     System-Wide Variables       │
│     /etc/environment            │
│     /etc/profile                │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│     User Variables              │
│     ~/.bashrc                   │
│     ~/.bash_profile             │
│     ~/.profile                  │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│     Session Variables           │
│     export VAR=value            │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│     Process Variables           │
│     VAR=value command           │
└─────────────────────────────────┘


Common Environment Variables:
──────────────────────────────

$PATH      Command search path
$HOME      User's home directory
$USER      Current username
$SHELL     Current shell
$PWD       Present working directory
$OLDPWD    Previous directory
$LANG      System language
$EDITOR    Default text editor
$TERM      Terminal type


Variable Scope:
───────────────

┌──────────────┐
│ Parent Shell │
│ VAR=value    │
└──────┬───────┘
       │
       │ export VAR
       │
       ▼
┌──────────────┐
│ Child Process│
│ Can see VAR  │
└──────────────┘

Without export:
┌──────────────┐
│ Parent Shell │
│ VAR=value    │
└──────┬───────┘
       │
       │ (no export)
       │
       ▼
┌──────────────┐
│ Child Process│
│ Cannot see   │
│ VAR          │
└──────────────┘


Usage Examples:
───────────────

# Set variable (current shell only)
$ MY_VAR="hello"
$ echo $MY_VAR
hello

# Export to child processes
$ export MY_VAR="hello"
$ bash -c 'echo $MY_VAR'
hello

# Temporary variable for single command
$ MY_VAR="hello" ./script.sh

# Add to PATH
$ export PATH="$PATH:/new/directory"
```

---

## Summary

These diagrams illustrate:
- ✅ Linux file system hierarchy and standard directories
- ✅ Process relationships and lifecycle
- ✅ Input/output redirection and pipes
- ✅ Shell script execution flow
- ✅ File permissions and ownership model
- ✅ Environment variables and scope

**Key Command Categories:**
- **Navigation**: cd, ls, pwd
- **File Operations**: cp, mv, rm, mkdir, touch
- **Text Processing**: cat, grep, sed, awk
- **Process Management**: ps, top, kill, jobs
- **Permissions**: chmod, chown, chgrp
- **System Info**: df, du, free, uname

**Next Steps:**
- Practice navigating the file system
- Experiment with pipes and redirection
- Write simple shell scripts
- Master file permissions
- Complete the [exercises](./exercises.md)
