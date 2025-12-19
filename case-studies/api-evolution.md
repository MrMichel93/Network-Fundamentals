# Case Study: API Evolution at Scale

## Background

**Company:** TechStartup (fictional)
**Challenge:** Evolving a REST API from V1 to V2 without breaking existing clients
**Timeline:** 6 months
**Team:** 5 backend engineers, 1 DevOps engineer

## Initial Situation

TechStartup launched their mobile app 2 years ago with a REST API (V1). The API had:
- 20,000+ daily active users
- 50 endpoints
- 3 mobile app versions in the wild (users don't always update)
- Several third-party integrations

### The Problem

V1 API had several issues:
- Inconsistent naming conventions (mix of snake_case and camelCase)
- No pagination on list endpoints (performance problems)
- Overly nested JSON responses
- Missing important fields
- No versioning strategy

## The Challenge

**Requirements:**
1. Redesign API with better structure
2. Fix performance issues
3. Maintain backwards compatibility
4. Migrate users gradually
5. Minimize development overhead

**Constraints:**
- Can't break existing mobile apps
- Limited engineering resources
- Need to ship new features alongside migration
- Can't have extended downtime

## Solution Approach

### Phase 1: Planning and Design (Month 1)

**1. API Audit**
```bash
# Analyzed API usage
- Most used endpoints: /users, /posts, /comments
- Least used: <10% endpoints, candidates for deprecation
- Performance bottlenecks: /posts (no pagination, returns all data)
```

**2. Design V2 API**
```
Decisions made:
- Consistent naming: camelCase throughout
- All list endpoints: mandatory pagination
- Flatter JSON structure
- Add HATEOAS links for discoverability
- Include meta information in responses
```

**3. Versioning Strategy**
```
Chose: URL versioning
https://api.techstartup.com/v1/users  ← Old
https://api.techstartup.com/v2/users  ← New

Alternatives considered:
- Header versioning: Accept: application/vnd.techstartup.v2+json
- Query parameter: ?version=2

Why URL versioning:
+ Clear and explicit
+ Easy to test/debug
+ Industry standard
- Takes more URL space
```

### Phase 2: Implementation (Months 2-4)

**1. Built V2 alongside V1**
```python
# Both versions coexist
@app.route('/v1/users', methods=['GET'])
def get_users_v1():
    users = User.query.all()  # No pagination!
    return jsonify([u.to_dict_v1() for u in users])

@app.route('/v2/users', methods=['GET'])
def get_users_v2():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    users = User.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'data': [u.to_dict_v2() for u in users.items],
        'meta': {
            'page': page,
            'perPage': per_page,
            'total': users.total,
            'pages': users.pages
        },
        'links': {
            'self': url_for('get_users_v2', page=page),
            'next': url_for('get_users_v2', page=page+1) if users.has_next else None,
            'prev': url_for('get_users_v2', page=page-1) if users.has_prev else None
        }
    })
```

**2. Shared business logic**
```python
# Avoid duplication
class UserService:
    @staticmethod
    def get_user(user_id):
        # Shared logic
        return User.query.get_or_404(user_id)

# V1 endpoint
@app.route('/v1/users/<user_id>')
def get_user_v1(user_id):
    user = UserService.get_user(user_id)
    return jsonify(user.to_dict_v1())

# V2 endpoint
@app.route('/v2/users/<user_id>')
def get_user_v2(user_id):
    user = UserService.get_user(user_id)
    return jsonify({
        'data': user.to_dict_v2(),
        'links': {
            'self': url_for('get_user_v2', user_id=user_id),
            'posts': url_for('get_user_posts_v2', user_id=user_id)
        }
    })
```

### Phase 3: Migration (Months 4-5)

**1. Communication**
```markdown
Migration Plan Email to Clients:

Subject: API V2 Launch - Better Performance & Features

We're excited to announce API V2!

**What's New:**
- Paginated responses (faster!)
- Consistent data format
- Better documentation
- New features: filtering, sorting

**Timeline:**
- Now: V2 available
- Month 1-3: Both V1 and V2 supported
- Month 4+: V1 deprecated (warning headers)
- Month 6: V1 sunset

**Migration Guide:**
https://docs.techstartup.com/api/v2/migration

**Need Help?**
Email: api-support@techstartup.com
```

**2. Gradual Migration**
```python
# Add deprecation headers to V1
@app.route('/v1/<path:path>')
def v1_handler(path):
    response = handle_v1_request(path)
    
    # Warn about deprecation
    response.headers['X-API-Warn'] = 'V1 is deprecated. Migrate to V2 by June 1.'
    response.headers['X-API-Deprecation'] = 'true'
    response.headers['Link'] = '<https://docs.techstartup.com/api/v2/migration>; rel="migration-guide"'
    
    return response
```

**3. Monitor Usage**
```python
# Track V1 vs V2 usage
@app.before_request
def log_api_version():
    if request.path.startswith('/v1'):
        metrics.increment('api.v1.requests')
    elif request.path.startswith('/v2'):
        metrics.increment('api.v2.requests')
```

### Phase 4: Deprecation and Sunset (Month 6)

**1. Monitored Migration Progress**
```
Week 0: V1: 95%, V2: 5%
Week 4: V1: 80%, V2: 20%
Week 8: V1: 50%, V2: 50%
Week 12: V1: 20%, V2: 80%
```

**2. Reached Out to Stragglers**
```
Identified clients still on V1:
- 5 mobile app versions
- 2 third-party integrations

Direct outreach:
- Email reminders
- Phone calls to partners
- Offered migration assistance
```

**3. Final Cutover**
```python
# Sunset V1
@app.route('/v1/<path:path>')
def v1_sunset(path):
    return jsonify({
        'error': 'API V1 has been sunset',
        'message': 'Please migrate to V2',
        'migration_guide': 'https://docs.techstartup.com/api/v2/migration',
        'v2_endpoint': request.path.replace('/v1/', '/v2/')
    }), 410  # 410 Gone
```

## Results

### Successes
✅ Smooth migration with minimal complaints
✅ V2 adoption: 95% after 4 months
✅ API response times improved 60% (pagination)
✅ Consistent data format praised by developers
✅ Only 2 support tickets related to migration

### Challenges Faced
⚠️ Two partners delayed migration (extended support by 1 month)
⚠️ Internal dashboard briefly broke (forgot to update)
⚠️ Initial V2 had bugs (fixed within 1 week)

### Metrics
- **Performance:** Average response time: 450ms → 180ms
- **Adoption:** 95% on V2 after 4 months
- **Satisfaction:** Developer survey score: 7.5/10 → 9/10

## Lessons Learned

### 1. Communication is Critical
- **Early** announcement (3 months notice)
- **Multiple channels** (email, docs, in-app messages)
- **Clear timeline** with milestones

### 2. Support Both Versions Longer Than Expected
- Originally planned 3 months overlap
- Extended to 6 months
- Some clients need more time

### 3. Make Migration Easy
- Detailed migration guide
- Code examples in multiple languages
- Offer support/office hours

### 4. Monitor Everything
- Track V1 vs V2 usage
- Identify slow adopters early
- Celebrate milestones

### 5. Plan for Failure
- Keep V1 code even after sunset (just in case)
- Have rollback plan
- Gradual cutover

## Key Takeaways

**For API Design:**
- ✅ Version from day 1
- ✅ Design for evolution
- ✅ Keep backwards compatibility in mind
- ✅ Pagination is not optional

**For Migration:**
- ✅ Communicate early and often
- ✅ Provide migration tools/guides
- ✅ Support overlap period
- ✅ Monitor adoption metrics

**For Teams:**
- ✅ Involve stakeholders early
- ✅ Don't rush the sunset
- ✅ Learn from each iteration

## Discussion Questions

1. What versioning strategy would you choose and why?
2. How would you handle a critical bug found in V1 during migration?
3. What if a major partner refuses to migrate?
4. How long should you support old API versions?
5. What metrics would you track?

---

**Related Case Studies:**
- [Scalability Challenges](./scalability-challenges.md)
- [Real-time Architecture](./realtime-architecture.md)
- [Security Incidents](./security-incidents.md)
