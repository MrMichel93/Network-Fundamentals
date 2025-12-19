# 📊 Module 05: Infrastructure-as-Code-Lite - Diagrams

Visual representations to help understand Infrastructure as Code concepts, Docker Compose, and configuration management.

## 1. IaC Concept: Manual vs Automated

Comparing traditional manual infrastructure management with IaC automation:

```
MANUAL PROCESS (Traditional):
──────────────────────────────

Developer needs server
         │
         ▼
┌────────────────┐
│ Create ticket  │
│ Wait for ops   │
└────────┬───────┘
         │ Days/Weeks
         ▼
┌────────────────┐
│ Ops team       │
│ provisions     │
│ server         │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│ Manual config  │
│ SSH, commands  │
│ Install deps   │
└────────┬───────┘
         │ Hours
         ▼
┌────────────────┐
│ Test & verify  │
│ Fix issues     │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│ Document steps │
│ (maybe)        │
└────────┬───────┘
         │
         ▼
   Server ready
   (Days later)

Problems:
❌ Slow (days/weeks)
❌ Error-prone
❌ Not reproducible
❌ Hard to scale
❌ Inconsistent
❌ Poor documentation


AUTOMATED IaC PROCESS:
──────────────────────

Developer needs server
         │
         ▼
┌────────────────────┐
│ Write config file  │
│ docker-compose.yml │
└────────┬───────────┘
         │ Minutes
         ▼
┌────────────────────┐
│ $ docker-compose   │
│   up -d            │
└────────┬───────────┘
         │ Seconds
         ▼
┌────────────────────┐
│ Infrastructure     │
│ auto-provisioned   │
│ - Servers          │
│ - Networks         │
│ - Volumes          │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│ Auto-configured    │
│ - Dependencies     │
│ - Environment      │
│ - Services         │
└────────┬───────────┘
         │
         ▼
   Server ready
   (Minutes later)

Benefits:
✅ Fast (minutes)
✅ Reproducible
✅ Version controlled
✅ Easy to scale
✅ Consistent
✅ Self-documenting


COMPARISON DIAGRAM:
───────────────────

Manual Infrastructure:          IaC Infrastructure:
─────────────────────          ──────────────────

┌──────────────────┐           ┌──────────────────┐
│  Documentation   │           │   Code Files     │
│  (outdated?)     │           │  (version ctrl)  │
└──────────────────┘           └────────┬─────────┘
         │                              │
         ↓                              ↓
  (Ops interprets)              (Tool executes)
         │                              │
         ↓                              ↓
┌──────────────────┐           ┌──────────────────┐
│  Manual Steps    │           │   Automation     │
│  (error-prone)   │           │  (consistent)    │
└────────┬─────────┘           └────────┬─────────┘
         │                              │
         ↓                              ↓
┌──────────────────┐           ┌──────────────────┐
│  Infrastructure  │           │  Infrastructure  │
│  (snowflake)     │           │  (reproducible)  │
└──────────────────┘           └──────────────────┘


INFRASTRUCTURE LIFECYCLE:
─────────────────────────

Traditional:                    IaC:

Create → Configure → Use        Code → Apply → Use
   ↓                               ↓
Manual updates                  Update code
   ↓                               ↓
Drift & inconsistency          Re-apply
   ↓                               ↓
Manual rebuild                 Automated rebuild
   ↓                               ↓
Different setup!               Same setup ✓


IaC BENEFITS VISUALIZATION:
───────────────────────────

┌────────────────────────────────────────────┐
│         Version Control (Git)              │
│                                            │
│  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ Version  │  │ Version  │  │ Version │ │
│  │   1.0    │→ │   2.0    │→ │   3.0   │ │
│  └──────────┘  └──────────┘  └─────────┘ │
│       │             │              │       │
│       ↓             ↓              ↓       │
└───────┼─────────────┼──────────────┼───────┘
        │             │              │
        ↓             ↓              ↓
   ┌────────┐   ┌────────┐    ┌────────┐
   │  Dev   │   │Staging │    │  Prod  │
   │  Env   │   │  Env   │    │  Env   │
   └────────┘   └────────┘    └────────┘
   
   All environments identical!
   Reproducible at any version!
```

---

## 2. Docker Compose Stack

Detailed view of service relationships and dependencies:

```
docker-compose.yml Structure:
─────────────────────────────

version: '3.8'

services:
  nginx:       ← Web Server / Reverse Proxy
  api:         ← Application Backend
  worker:      ← Background Jobs
  db:          ← Database
  redis:       ← Cache
  
networks:
  frontend:    ← Public-facing
  backend:     ← Internal services
  
volumes:
  db-data:     ← Persistent storage
  uploads:     ← File storage


Service Dependency Graph:
─────────────────────────

                    Internet
                        │
                        ▼
            ┌───────────────────┐
            │                   │
        :80 │      nginx        │ :443
            │  (Reverse Proxy)  │
            │                   │
            └─────────┬─────────┘
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
    ┌──────────┐          ┌──────────┐
    │   api    │          │  static  │
    │(Node.js) │          │  files   │
    │  :3000   │          │          │
    └─────┬────┘          └──────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌────────┐  ┌────────┐
│  db    │  │ redis  │
│(Postgres│  │(Cache) │
│ :5432  │  │ :6379  │
└───┬────┘  └────────┘
    │
    ▼
┌─────────┐
│ Volume  │
│db-data  │
└─────────┘


Network Segmentation:
─────────────────────

┌─────────────────────────────────────────────┐
│          frontend network                   │
│                                             │
│  ┌─────────┐              ┌──────────┐     │
│  │ nginx   │──────────────│  static  │     │
│  └────┬────┘              └──────────┘     │
│       │                                     │
└───────┼─────────────────────────────────────┘
        │
        │ Bridge between networks
        │
┌───────▼─────────────────────────────────────┐
│          backend network                    │
│                                             │
│  ┌─────────┐    ┌──────────┐  ┌─────────┐ │
│  │   api   │────│    db    │  │  redis  │ │
│  └─────────┘    └──────────┘  └─────────┘ │
│                                             │
└─────────────────────────────────────────────┘

Security Benefits:
- nginx can access both networks
- api can only access backend
- db and redis isolated from internet
- Static files separated from logic


Complete Stack Example:
───────────────────────

┌────────────────────────────────────────────────┐
│                                                │
│           Production-Like Stack                │
│                                                │
│  ┌──────────────────────────────────────┐     │
│  │          Load Balancer               │     │
│  │             nginx                    │     │
│  │         Ports: 80, 443               │     │
│  └──────────┬───────────────────────────┘     │
│             │                                  │
│      ┌──────┴──────┐                          │
│      │             │                          │
│  ┌───▼────┐   ┌────▼───┐                     │
│  │  api-1 │   │  api-2 │    ← Scaled         │
│  │(replica)│   │(replica)│    ← services      │
│  └───┬────┘   └────┬───┘                     │
│      │             │                          │
│      └──────┬──────┘                          │
│             │                                  │
│      ┌──────┴──────┐                          │
│      │             │                          │
│  ┌───▼────┐   ┌────▼────┐                    │
│  │  db    │   │  redis  │                    │
│  │(primary)│   │ (cache) │                    │
│  └───┬────┘   └─────────┘                    │
│      │                                        │
│  ┌───▼──────────┐                            │
│  │   db-replica │   ← Read replicas          │
│  │   (readonly) │                            │
│  └──────────────┘                            │
│                                               │
│  Volumes:                                     │
│  ├─ db-data (persistent)                     │
│  ├─ redis-data (persistent)                  │
│  └─ app-uploads (shared)                     │
│                                               │
└────────────────────────────────────────────────┘


Health Checks:
──────────────

Each service has health check:

┌─────────────────────────┐
│  Service: api           │
├─────────────────────────┤
│  healthcheck:           │
│    test: curl -f        │
│          localhost:3000/│
│    interval: 30s        │
│    timeout: 10s         │
│    retries: 3           │
└─────────────────────────┘
         │
         ▼
   ┌─────────┐
   │ Healthy?│
   └────┬────┘
        │
  ┌─────┴──────┐
 Yes          No
  │            │
  ▼            ▼
Ready     Unhealthy
          (restart)


Service Restart Policy:
───────────────────────

restart: unless-stopped

Service starts
      │
      ▼
   Running ──────┐
      │          │
      │  Crash   │
      ▼          │
   Restart ◄─────┘
      │
      │  Manual stop
      ▼
   Stopped
   (don't restart)


Scaling Services:
─────────────────

$ docker-compose up --scale api=3

Before:                After:
┌──────┐              ┌──────┐
│ api  │              │api-1 │
└──────┘              ├──────┤
                      │api-2 │
                      ├──────┤
                      │api-3 │
                      └──────┘
                          ▲
                          │
                    Load balanced
```

---

## 3. Configuration Management Flow

How configuration flows from environment variables to containers:

```
CONFIGURATION SOURCES:
──────────────────────

1. Environment Files (.env)
2. docker-compose.yml
3. Dockerfile ENV
4. Runtime overrides


Configuration Hierarchy:
────────────────────────

┌─────────────────────────────────────┐
│      Priority (Highest First)       │
├─────────────────────────────────────┤
│  1. Runtime: docker run -e VAR=val  │ ← Override everything
├─────────────────────────────────────┤
│  2. Compose: environment section    │ ← Compose file
├─────────────────────────────────────┤
│  3. Compose: env_file directive     │ ← .env file
├─────────────────────────────────────┤
│  4. Dockerfile: ENV instruction     │ ← Image defaults
├─────────────────────────────────────┤
│  5. Application: default values     │ ← Code defaults
└─────────────────────────────────────┘


Configuration Flow:
───────────────────

Development:
┌──────────────┐
│  .env.dev    │
│  DB_HOST=    │
│  localhost   │
│  DEBUG=true  │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ docker-compose   │
│    .yml          │
│  env_file:       │
│   - .env.dev     │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│   Container      │
│   Environment    │
│  Variables       │
└──────────────────┘


Production:
┌──────────────┐
│ .env.prod    │
│ DB_HOST=     │
│ db.prod.com  │
│ DEBUG=false  │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ CI/CD Pipeline   │
│ (adds secrets)   │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│   Container      │
│   Environment    │
│  Variables       │
└──────────────────┘


Configuration Pattern Example:
──────────────────────────────

File: .env
─────────

# Database
DB_HOST=postgres
DB_PORT=5432
DB_NAME=myapp
DB_USER=postgres

# Application
APP_PORT=3000
NODE_ENV=development
LOG_LEVEL=debug

# Redis
REDIS_HOST=redis
REDIS_PORT=6379


File: docker-compose.yml
────────────────────────

services:
  api:
    environment:
      - DB_HOST=${DB_HOST}         ← From .env
      - DB_PORT=${DB_PORT}         ← From .env
      - DB_NAME=${DB_NAME}         ← From .env
      - DB_USER=${DB_USER}         ← From .env
      - SECRET_KEY=${SECRET_KEY}   ← From secure vault
    env_file:
      - .env                       ← Load file


Variable Substitution:
──────────────────────

.env file:
  DB_HOST=postgres
      │
      ▼
docker-compose.yml:
  environment:
    - DB_HOST=${DB_HOST}    ← Substituted
      │
      ▼
Container sees:
  DB_HOST=postgres         ← Final value


Multi-Environment Setup:
─────────────────────────

Project Structure:
├── docker-compose.yml          ← Base config
├── docker-compose.dev.yml      ← Dev overrides
├── docker-compose.prod.yml     ← Prod overrides
├── .env.dev                    ← Dev vars
├── .env.prod                   ← Prod vars
└── .env.example                ← Template

Usage:
Development:
$ docker-compose \
  -f docker-compose.yml \
  -f docker-compose.dev.yml \
  --env-file .env.dev \
  up

Production:
$ docker-compose \
  -f docker-compose.yml \
  -f docker-compose.prod.yml \
  --env-file .env.prod \
  up -d


Configuration Merging:
──────────────────────

docker-compose.yml (base):
services:
  api:
    image: myapp:latest
    environment:
      - NODE_ENV=production
      │
      ▼
      
docker-compose.dev.yml (override):
services:
  api:
    build: .              ← Override image
    environment:
      - NODE_ENV=development  ← Override env
      - DEBUG=true            ← Add new env
      │
      ▼

Merged result:
services:
  api:
    build: .              ← From dev
    environment:
      - NODE_ENV=development  ← From dev (overridden)
      - DEBUG=true            ← From dev (added)


Secrets Management:
───────────────────

❌ Bad (committed to git):
.env:
  DB_PASSWORD=mysecretpass123
  API_KEY=sk_live_abc123xyz

✅ Good (not in git):
.env.example:
  DB_PASSWORD=changeme
  API_KEY=your_key_here

.gitignore:
  .env
  .env.prod
  .env.dev

Production (CI/CD):
  Environment Variables set in:
  ├─ GitHub Secrets
  ├─ AWS Parameter Store
  ├─ HashiCorp Vault
  └─ Azure Key Vault


Configuration Validation:
─────────────────────────

┌─────────────────┐
│ Start container │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Load config     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Validate        │
│ required vars   │
└────────┬────────┘
         │
    ┌────┴────┐
   OK       Missing
    │          │
    ▼          ▼
┌───────┐  ┌───────┐
│Start  │  │ Fail  │
│app    │  │ with  │
│       │  │ error │
└───────┘  └───────┘


Config by Environment:
──────────────────────

┌─────────────────────────────────────────┐
│           Configuration Matrix          │
├────────────┬──────────┬─────────────────┤
│  Variable  │   Dev    │   Production    │
├────────────┼──────────┼─────────────────┤
│ DB_HOST    │localhost │db.prod.com:5432 │
│ DEBUG      │  true    │     false       │
│ LOG_LEVEL  │  debug   │     warn        │
│ REPLICAS   │    1     │      3          │
│ CACHE      │  false   │     true        │
└────────────┴──────────┴─────────────────┘
```

---

## Summary

These diagrams illustrate:
- ✅ Benefits of Infrastructure as Code vs manual processes
- ✅ Docker Compose service architecture and relationships
- ✅ Configuration management patterns and best practices
- ✅ Environment-specific configurations
- ✅ Secrets management approaches
- ✅ Service scaling and orchestration

**IaC Key Benefits:**
- **Reproducibility**: Same config = same infrastructure
- **Version Control**: Track changes over time
- **Speed**: Minutes vs days/weeks
- **Consistency**: Eliminates configuration drift
- **Documentation**: Code is the documentation

**Docker Compose Features:**
- **Multi-container**: Define entire stack in one file
- **Networking**: Automatic service discovery
- **Volumes**: Persistent data management
- **Scaling**: Easy horizontal scaling
- **Environment**: Configuration management

**Best Practices:**
- Use .env files for configuration
- Never commit secrets to git
- Separate concerns (dev/staging/prod)
- Validate configurations
- Document your setup
- Use health checks
- Implement proper logging

**Next Steps:**
- Create a docker-compose.yml for a multi-service app
- Practice environment-specific configurations
- Implement proper secrets management
- Add health checks to services
- Complete the [exercises](./exercises.md)
