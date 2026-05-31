# Security and Deployment Guide

This document outlines security best practices, free/low-cost deployment options, scalability considerations, and credential management for the FastAPI backend.

---

## 1. Security Best Practices

### Authentication & Authorization

- **API Keys**: Implement simple API key validation for endpoints that need protection
- **JWT Tokens**: Use JSON Web Tokens for stateless authentication
  - Short-lived access tokens (15-60 minutes)
  - Refresh tokens for obtaining new access tokens
  - Proper token expiration and validation
- **Password Hashing**: Use `bcrypt` or `argon2` for password hashing (never store plain text)
- **Rate Limiting**: Implement rate limiting to prevent brute force attacks and DDoS
  - Use `slowapi` library for FastAPI rate limiting
  - Limit by IP address or API key

### Input Validation & Protection

- **Pydantic Models**: Always validate input using Pydantic schemas (already in place)
- **SQL Injection Prevention**: Use parameterized queries or ORM (when database is added)
- **CORS Configuration**: Restrict allowed origins in production (currently set to `["*"]`)
  - Should be changed to specific domain(s): `["https://yourdomain.com"]`
- **HTTPS Only**: Always use HTTPS in production
  - Redirect HTTP to HTTPS
  - Use secure cookies with `secure=True` and `httponly=True`

### Dependency Management

- **Keep Dependencies Updated**: Regularly update FastAPI, Pydantic, Uvicorn
  - Use `uv pip install --upgrade -r requirements.txt` periodically
- **Security Scanning**: Use tools to scan for vulnerabilities
  - `pip audit` - Check for known vulnerabilities in dependencies
  - `safety` - Scan requirements for security issues

### Environment & Configuration

- **Never Commit Secrets**: Keep `.env` file in `.gitignore` (already configured)
- **Environment Variables**: Store all sensitive data in environment variables
  - API keys, database URLs, secrets
  - Use `.env.example` as template (already in place)
- **Disable Debug in Production**: Set `DEBUG=False` for production
- **HTTPS Certificates**: Use Let's Encrypt (free SSL certificates)

### Additional Security Headers

- **Content Security Policy (CSP)**: Prevent XSS attacks
- **X-Frame-Options**: Prevent clickjacking
- **X-Content-Type-Options**: Prevent MIME type sniffing
- **Strict-Transport-Security (HSTS)**: Force HTTPS

### Logging & Monitoring

- **Structured Logging**: Log security events (failed auth attempts, errors)
- **Don't Log Secrets**: Never log API keys, tokens, or passwords
- **Monitor for Suspicious Activity**: Set up alerts for unusual patterns

---

## 2. Free Hosting Options for Friends to Access

### Option A: Replit (Recommended for Easy Sharing)

**Pros:**
- Free tier available
- Easy to share link with team
- No credit card needed
- Built-in environment variables support
- Simple deployment

**Cons:**
- Limited computational resources
- Slower than other options
- Limited uptime guarantees

**Cost:** Free tier available

**Steps:**
1. Push code to GitHub
2. Import repository into Replit
3. Set up environment variables in Replit secrets
4. Deploy and share link

### Option B: Railway.app (Best Free Tier)

**Pros:**
- Generous free tier ($5/month credit)
- Good performance
- Easy GitHub integration
- Simple environment variable management
- Good for development/testing

**Cons:**
- Limited free tier after credit runs out
- Needs monitoring to avoid overages

**Cost:** $5/month free credit (usually enough for testing)

**Steps:**
1. Push code to GitHub
2. Connect GitHub to Railway
3. Set environment variables
4. Auto-deploy on push

### Option C: Render.com (Good Balance)

**Pros:**
- Free tier with some limitations
- Good performance for tier
- Auto-deployment from GitHub
- 750 free tier hours per month (roughly 24/7 for 25 days)

**Cons:**
- Instance spins down after 15 minutes of inactivity (free tier)
- Slower startup time

**Cost:** Free tier with limitations

### Option D: Fly.io (Scalable)

**Pros:**
- Good free tier
- Global deployment
- Good performance
- Docker-ready

**Cons:**
- Slightly more complex setup
- Requires learning their CLI

**Cost:** Free tier available

### Option E: PythonAnywhere (Python Specific)

**Pros:**
- Python-specific hosting
- Beginner-friendly
- Good documentation

**Cons:**
- Limited free tier
- Slower performance

**Cost:** Free tier with limitations

### Recommendation for Your Use Case

**Best for free + team access: Railway.app or Render.com**
- Easy to set up
- Good performance
- Free tier sufficient for testing
- Team members can access public URL

---

## 3. Scalability Considerations

### Application Level

- **Stateless Design**: Ensure the app is stateless (already done with health checks)
  - Each instance can handle any request
  - No session data stored locally
  - Use external session store if needed

- **Async/Await**: Use async endpoints for I/O operations
  - Already supported by FastAPI
  - Better resource utilization

- **Caching Strategy**:
  - Cache frequently accessed data (Redis)
  - Cache external API responses (OpenAI API calls)
  - Implement cache invalidation logic

### Database Considerations

- **Choose appropriate database**:
  - PostgreSQL: Good for relational data, open source
  - MongoDB: Good for flexible schemas (free tier: MongoDB Atlas)
  - Firebase: Easy to scale, pay-per-use model

- **Database Connection Pooling**:
  - Reuse database connections
  - Avoid creating new connection per request

### API Rate Limiting & Throttling

- **Per-user limits**: Prevent single user from overloading
- **Per-endpoint limits**: Different endpoints may have different limits
- **Throttling**: Queue requests during peak times

### Load Balancing & Horizontal Scaling

- **Multiple Instances**: Run multiple app instances
  - Tools: Docker + Kubernetes, Docker Swarm
  - Or use managed services (Railway, Render auto-handle this)

- **API Gateway**: Route requests to multiple instances
  - Nginx, AWS API Gateway, etc.

### Monitoring & Observability

- **Health Checks**: Endpoints to monitor app health (already have `/health`)
- **Metrics Collection**:
  - Request count, response time, error rate
  - Tools: Prometheus, Datadog (free tier)

- **Logging Aggregation**:
  - Centralized logging (ELK stack, CloudWatch)
  - Easy debugging in production

### Free/Low-Cost Scalability Stack

1. **Development**: Local testing with FastAPI + SQLite
2. **Testing**: Railway/Render free tier with PostgreSQL (free tier available)
3. **Production**: Scale based on actual traffic
   - Start with single instance on Railway/Render
   - Move to Docker + Kubernetes when needed
   - Or use Vercel Functions / AWS Lambda for serverless

### When to Scale

- Monitor current metrics first
- Scale when: >80% CPU, high response times, error rate increases
- Vertical scaling first (bigger instance), then horizontal

---

## 4. Credential Management (API Keys, Secrets)

### Where to Store Credentials

#### Development Environment

**`.env` File (Local Only)**
- Store locally, never commit to git
- Use `.env.example` as template
- Include in `.gitignore` (already configured)

```
OPENAI_API_KEY=sk_test_your_key_here
DATABASE_URL=postgresql://user:pass@localhost/dbname
JWT_SECRET=your_secret_key_here
```

**Load via `python-dotenv`** (already in requirements.txt)
```python
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

#### Production Environment

**Option 1: Platform Environment Variables (Recommended for Free Tier)**

Railway, Render, Replit all support:
- Web UI to set environment variables
- Secrets are never logged
- Automatically injected into app
- Best for free hosting

**Option 2: AWS Secrets Manager**
- Encrypt secrets at rest
- Rotate secrets easily
- Audit access logs
- Cost: $0.40 per secret per month

**Option 3: HashiCorp Vault**
- Open source secret management
- Enterprise-grade
- Complex setup
- Better for teams

**Option 4: GitOps with Sealed Secrets (Kubernetes)**
- Encrypt secrets in git
- Decrypt at runtime
- Good for CI/CD pipelines

### Best Practices for Credentials

1. **Never hardcode secrets**
   ```python
   # ❌ DON'T DO THIS
   api_key = "sk_test_123456789"
   
   # ✅ DO THIS
   api_key = os.getenv("OPENAI_API_KEY")
   ```

2. **Use strong, random secrets**
   - Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
   - Different secret for each environment (dev, staging, prod)

3. **Rotate secrets regularly**
   - Especially if suspected leak
   - Update all instances immediately

4. **Limit secret scope**
   - API keys with specific permissions
   - Read-only credentials for non-critical operations
   - Separate keys per service

5. **Audit secret access**
   - Log who accessed which secret
   - Alert on suspicious access

### Managing OpenAI API Key Safely

1. **Create dedicated API key in OpenAI dashboard**
   - Not your primary account key
   - Can be revoked independently

2. **Store in environment variable**
   ```python
   import os
   from openai import OpenAI
   
   api_key = os.getenv("OPENAI_API_KEY")
   if not api_key:
       raise ValueError("OPENAI_API_KEY not set")
   
   client = OpenAI(api_key=api_key)
   ```

3. **Set usage limits in OpenAI dashboard**
   - Monthly budget limit
   - Per-minute rate limit
   - Prevents accidental overages

4. **Never log the full key**
   ```python
   # ❌ DON'T DO THIS
   logger.info(f"Using key: {api_key}")
   
   # ✅ DO THIS
   logger.info(f"Using key: {api_key[:20]}...")
   ```

5. **For team sharing**
   - Each team member creates their own OpenAI API key
   - Each sets it in their local `.env`
   - Production uses separate key with budget limits

### Recommended Approach for This Project

**Development:**
- Store in local `.env` file (never commit)
- Load with `python-dotenv`

**Free Hosting (Railway/Render):**
- Set environment variables in platform UI
- No `.env` file needed in production

**Example Structure:**
```
Local Development:
├── .env (local, NOT in git)
├── .env.example (in git, shows structure)
└── config.py (reads from env)

Production (Railway/Render):
├── Web UI sets environment variables
├── App starts with injected variables
└── No .env file needed
```

---

## Implementation Roadmap

### Phase 1: Current State (Done)
- ✅ Basic structure in place
- ✅ `.env.example` created
- ✅ `.gitignore` configured
- ✅ Health check endpoints

### Phase 2: Security Basics (Recommended Next)
- [ ] Add rate limiting
- [ ] Add input validation middleware
- [ ] Add security headers middleware
- [ ] Update CORS for production

### Phase 3: Authentication (When Needed)
- [ ] Add API key validation
- [ ] Add JWT token support
- [ ] Add user authentication

### Phase 4: Deployment (When Ready)
- [ ] Deploy to Railway/Render
- [ ] Set up environment variables
- [ ] Enable HTTPS
- [ ] Add monitoring

### Phase 5: Database (When Needed)
- [ ] Add PostgreSQL/MongoDB
- [ ] Implement connection pooling
- [ ] Add migrations

### Phase 6: Advanced Security (Production)
- [ ] Add encryption for sensitive data
- [ ] Implement audit logging
- [ ] Add request signing
- [ ] Set up WAF (Web Application Firewall)

---

## Summary: Free & Low-Cost Stack

| Component | Solution | Cost |
|-----------|----------|------|
| **Hosting** | Railway/Render | Free tier |
| **Database** | PostgreSQL (Railway/Render) or MongoDB Atlas | Free tier |
| **Credentials** | Environment variables (Railway/Render UI) | Free |
| **SSL/TLS** | Provided by platform | Free |
| **Monitoring** | Datadog free tier or built-in | Free |
| **DNS** | Cloudflare | Free tier |
| **Storage** | AWS S3 (free tier) or Cloudflare R2 | ~$5/month or free tier |
| **Total Monthly Cost** | **$0-5** | Very affordable |

---

## Next Steps

1. Choose hosting platform (Railway.app recommended)
2. Test locally with all security headers
3. Deploy to free tier
4. Get feedback from team
5. Scale based on actual usage

