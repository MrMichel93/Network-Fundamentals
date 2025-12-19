# 📊 Module 01: Git and GitHub - Diagrams

Visual representations to help understand Git workflows, branching strategies, and collaboration patterns.

## 1. Git Workflow Visualization

The fundamental Git workflow showing how code moves through different stages:

```
Working Directory → Staging Area → Local Repository → Remote Repository
     (add)             (commit)          (push)


┌─────────────────┐
│    Working      │     Files you're editing
│    Directory    │     Your local filesystem
└────────┬────────┘
         │
         │ git add <file>
         │
         ▼
┌─────────────────┐
│    Staging      │     Files ready to commit
│      Area       │     (Index)
└────────┬────────┘
         │
         │ git commit -m "message"
         │
         ▼
┌─────────────────┐
│     Local       │     Committed snapshots
│   Repository    │     (.git directory)
└────────┬────────┘
         │
         │ git push origin main
         │
         ▼
┌─────────────────┐
│     Remote      │     Shared repository
│   Repository    │     (GitHub)
└─────────────────┘
```

**Reverse Flow (Getting Updates):**
```
Remote Repository → Local Repository → Working Directory
     (fetch)              (merge/pull)

git fetch origin     ─→  Updates local tracking branches
git merge origin/main ─→  Integrates changes
git pull origin main  ─→  Fetch + Merge in one command
```

**File States:**
```
Untracked → Unmodified → Modified → Staged → Committed
    │           │           │          │         │
    └───────────┴───────────┴──────────┴─────────┘
           Lifecycle of File States
```

---

## 2. Branching Strategy

Understanding branch creation, usage, and merging:

```
main     ─────●─────●─────●─────●─────●─────
               \                /       \
                \              /         \
feature/login    ●───●───●───●            \
                                           \
                                            \
feature/dashboard                            ●───●───●
```

**Detailed Branch Workflow:**
```
Timeline:

main          ●────●────●────●────●────●────●────●
              │    │    │    │    │    │    │    │
              A    │    D    │    G    │    J    K
                   │         │         │
feature/A          └●───●───●┘         │
                    B   C   (merge)    │
                                       │
feature/B                              └●───●───●┘
                                        H   I  (merge)

Legend:
● = Commit
─ = Time progression
\ / = Branch and merge points
```

**Branch Types:**
```
main (or master)
├── Long-lived branch
├── Production-ready code
└── Protected from direct commits

develop
├── Integration branch
├── Latest development changes
└── Base for feature branches

feature/*
├── Short-lived branches
├── Specific features or fixes
└── Merged back to develop

hotfix/*
├── Emergency fixes
├── Branch from main
└── Merge to main and develop

release/*
├── Release preparation
├── Branch from develop
└── Merge to main and develop
```

---

## 3. Pull Request Flow

The complete lifecycle of a pull request:

```
┌─────────────────────────────────────────────────┐
│           Pull Request Lifecycle                │
└──────────────────┬──────────────────────────────┘
                   │
            ┌──────▼──────┐
            │ Developer   │
            │ Creates PR  │
            └──────┬──────┘
                   │
                   ▼
         ┌──────────────────┐
         │ Automated Checks │
         │ - CI/CD Tests    │
         │ - Linting        │
         │ - Build          │
         └────────┬─────────┘
                  │
          ┌───────┴────────┐
         Pass            Fail
          │                │
          ▼                ▼
    ┌─────────┐     ┌──────────┐
    │ Ready   │     │ Fix      │
    │ for     │     │ Issues   │
    │ Review  │     └────┬─────┘
    └────┬────┘          │
         │               │
         │◄──────────────┘
         │
         ▼
   ┌──────────┐
   │ Code     │
   │ Review   │
   └────┬─────┘
        │
   ┌────┴────────────────┐
   │                     │
   ▼                     ▼
Approved           Changes Requested
   │                     │
   │              ┌──────▼──────┐
   │              │ Developer   │
   │              │ Updates PR  │
   │              └──────┬──────┘
   │                     │
   │◄────────────────────┘
   │
   ▼
┌──────────┐
│ Merge PR │
└────┬─────┘
     │
     ▼
┌────────────────┐
│ Branch Deleted │
│ (optional)     │
└────────────────┘
```

**PR Review Comments:**
```
Pull Request: Add user authentication
├── Files Changed: 15
├── +245 additions
├── -87 deletions
│
├── Reviewer 1: @alice
│   ├── ✅ Approved
│   └── Comment: "LGTM! Great work on the tests."
│
├── Reviewer 2: @bob
│   ├── 💬 Changes Requested
│   ├── Comment on auth.js:45: "Consider adding rate limiting"
│   └── Comment on login.html:12: "Missing CSRF token"
│
└── Status Checks
    ├── ✅ Tests (15/15 passed)
    ├── ✅ Build (success)
    ├── ✅ Linting (0 issues)
    └── ⏳ Security Scan (in progress)
```

---

## 4. Merge Conflict Resolution Process

Visual decision tree for handling merge conflicts:

```
                 Merge/Pull Operation
                         │
                         ▼
                 ┌───────────────┐
                 │  Conflicts?   │
                 └───────┬───────┘
                         │
                  ┌──────┴──────┐
                 No             Yes
                  │              │
                  ▼              ▼
         ┌──────────────┐  ┌──────────────┐
         │ Auto-merged  │  │ Git marks    │
         │ Successfully │  │ conflicts    │
         └──────────────┘  └──────┬───────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Open conflicted │
                         │ files in editor │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Examine markers │
                         │ <<<<<<< HEAD    │
                         │ your changes    │
                         │ =======         │
                         │ their changes   │
                         │ >>>>>>>         │
                         └────────┬────────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │   Resolution Strategy    │
                    └─────┬──────────┬─────────┘
                          │          │
                  ┌───────┴──┐   ┌───┴────────┐
                  ▼          ▼   ▼            ▼
            ┌─────────┐ ┌─────┐ ┌──────┐ ┌────────┐
            │ Keep    │ │Keep │ │Combine│ │Rewrite │
            │ yours   │ │theirs│ │ both │ │ fully  │
            └────┬────┘ └──┬──┘ └───┬──┘ └───┬────┘
                 │         │        │        │
                 └─────────┴────────┴────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ Remove conflict│
                  │ markers        │
                  └────────┬───────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ git add <file> │
                  └────────┬───────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ Test changes   │
                  └────────┬───────┘
                           │
                    ┌──────┴──────┐
                   Pass          Fail
                    │              │
                    ▼              ▼
           ┌────────────┐   ┌──────────┐
           │git commit  │   │ Fix and  │
           │           │   │ retest   │
           └────────────┘   └────┬─────┘
                                 │
                                 │
                    ◄────────────┘
```

**Conflict Example:**
```
File: app.js

<<<<<<< HEAD (Your changes)
function login(username, password) {
    return authenticateUser(username, password);
}
=======
function login(user, pass) {
    return authenticate(user, pass);
}
>>>>>>> feature-branch (Their changes)

Resolution Options:
1. Keep HEAD: Use your version
2. Keep feature-branch: Use their version
3. Combine: Use both (if they don't conflict logically)
4. Rewrite: Create a new version incorporating both
```

---

## 5. Git Rebase vs Merge

Understanding different integration strategies:

```
Initial State:
main     ●───●───●
          \
feature    ●───●

─────────────────────────────────────────

MERGE Strategy:
main     ●───●───●───────●
          \             /
feature    ●───●───────●
                  (merge commit)

Result: History preserved, merge commit created

─────────────────────────────────────────

REBASE Strategy:
main     ●───●───●───●───●
                    (feature commits 
                     replayed here)

Result: Linear history, no merge commit
```

---

## 6. Collaborative Workflows

Different team collaboration patterns:

```
Centralized Workflow:
─────────────────────
    ┌─────────┐
    │ GitHub  │
    │  main   │
    └────┬────┘
         │
    ┌────┴────┐
    │         │
┌───▼──┐  ┌──▼───┐
│Dev 1 │  │Dev 2 │
└──────┘  └──────┘

Feature Branch Workflow:
────────────────────────
        ┌─────────┐
        │ GitHub  │
        │  main   │
        └────┬────┘
             │
    ┌────────┼────────┐
    │        │        │
┌───▼────┐ ┌─▼─────┐ ┌▼──────┐
│feature1│ │feature2│ │feature3│
└───┬────┘ └───┬────┘ └┬──────┘
    │          │       │
┌───▼──┐   ┌───▼──┐ ┌─▼───┐
│Dev 1 │   │Dev 2 │ │Dev 3│
└──────┘   └──────┘ └─────┘

Forking Workflow:
─────────────────
    ┌─────────────┐
    │   Upstream  │
    │   (original)│
    └──────┬──────┘
           │
    ┌──────┼──────┐
    │      │      │
┌───▼──┐ ┌─▼───┐ ┌▼────┐
│Fork 1│ │Fork 2│ │Fork 3│
└───┬──┘ └──┬──┘ └┬────┘
    │       │     │
Pull Request │ Pull Request
    │        │
    └────────┴─────┘
```

---

## 7. Git States and Commands

Complete command reference with state transitions:

```
┌──────────────────────────────────────────────────┐
│              File State Transitions              │
└──────────────────────────────────────────────────┘

Untracked              Modified              Staged              Committed
  Files                 Files                Files               Snapshots
    │                    │                    │                     │
    │ git add            │ git add            │ git commit         │
    └───────────────────►└───────────────────►└────────────────────┘
                              │                     │
                              │ git restore --staged│
                              │◄────────────────────┘
                              │
                              │ git restore <file>
                              └◄─────── Working Dir ────┘


Common Commands by Category:
────────────────────────────

Setup & Config:
  git init              - Initialize repository
  git clone <url>       - Clone repository
  git config            - Configure Git

Basic Snapshotting:
  git add <file>        - Stage changes
  git commit -m "msg"   - Commit changes
  git status            - Check status
  git diff              - View changes

Branching & Merging:
  git branch            - List branches
  git branch <name>     - Create branch
  git checkout <branch> - Switch branch
  git merge <branch>    - Merge branch

Sharing & Updating:
  git push              - Push to remote
  git pull              - Fetch and merge
  git fetch             - Download objects

Inspection:
  git log               - View commit history
  git show <commit>     - Show commit details
  git diff <branch>     - Compare branches
```

---

## 8. GitHub Collaboration Features

GitHub-specific collaboration tools:

```
┌─────────────────────────────────────────────┐
│         GitHub Collaboration Tools          │
└──────────────────┬──────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
   ┌────▼───┐ ┌────▼───┐ ┌───▼────┐
   │Issues  │ │  PRs   │ │Actions │
   └────┬───┘ └────┬───┘ └───┬────┘
        │          │         │
        │          │         │
   Track bugs  Code review  Automation
   Features    Discussions  CI/CD
   Tasks       Approval     Testing

Additional Features:
├── Projects (Kanban boards)
├── Wiki (Documentation)
├── Discussions (Q&A)
├── Security (Dependabot, scanning)
└── Insights (Analytics)
```

---

## Summary

These diagrams illustrate:
- ✅ Git workflow and file state transitions
- ✅ Branching strategies and merge patterns
- ✅ Pull request lifecycle and review process
- ✅ Merge conflict resolution approaches
- ✅ Collaborative workflows for teams
- ✅ Git commands and their effects

**Key Takeaways:**
1. Always pull before starting new work
2. Create feature branches for new work
3. Commit often with clear messages
4. Use pull requests for code review
5. Resolve conflicts carefully
6. Keep branches up to date

**Next Steps:**
- Practice basic Git commands
- Create a feature branch
- Make a pull request
- Resolve a merge conflict
- Review the [exercises](./exercises.md)
