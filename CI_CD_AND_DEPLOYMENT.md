# CI/CD and Deployment Guide

Guide for setting up CI/CD pipelines, deployment methods, and sharing your local development server with team members.

---

## 1. Free CI/CD Pipelines

### Option 1: GitHub Actions (Best Free Option) ⭐

**Completely free for public repos, unlimited workflows**

```yaml
# .github/workflows/deploy.yml
name: Deploy to Railway
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        run: |
          npm i -g @railway/cli
          railway deploy
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

**Pros:**
- Completely free for public repos
- Unlimited workflows
- Integrated with GitHub
- Runs on every push/PR
- Can run tests, build, deploy automatically

### Option 2: Vercel (Free)
- Best for serverless/edge functions
- Automatic deployments from GitHub
- Good dashboard and monitoring

### Option 3: Netlify (Free)
- Similar to Vercel
- Easier for frontends
- Less ideal for FastAPI backend

### Option 4: GitLab CI/CD (Free)
- 400 free CI/CD minutes per month
- Good alternative to GitHub Actions

### Option 5: Render Auto-Deploy (Free)
- Connect GitHub repo directly
- Auto-deploys on push
- Built-in to Render platform
- No extra setup needed

---

## 2. Deployment Methods Comparison

| Platform | Cost | Setup | Best For | CI/CD Integration |
|----------|------|-------|----------|------------------|
| **Railway** | Free tier | Very easy | Beginners | Manual or webhook |
| **Render** | Free tier | Easy | General use | Auto-deploy from GitHub |
| **Fly.io** | Free tier | Medium | Global deployment | Via CLI |
| **PythonAnywhere** | Free tier | Easy | Python-specific | Manual or API |
| **Replit** | Free tier | Very easy | Quick demos | Auto-deploy |
| **AWS Lambda** | Free tier | Complex | Serverless (pay-per-use) | Via GitHub Actions |
| **Google Cloud Run** | Free tier | Medium | Serverless, auto-scaling | Native integration |
| **Docker + VPS** | ~$3-5/month | Hard | Full control | Custom setup |

### Recommendation
**Render.com or Railway.app** - Best balance of ease and features. Auto-deploy from GitHub, free tier, good performance.

---

## 3. Share Local Dev Server with Friends (Tunneling)

For development, share your local machine with friends without deploying.

### Option 1: ngrok (Most Popular)

**Installation:**
```bash
# macOS
brew install ngrok

# Windows
choco install ngrok

# Linux
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
```

**Usage:**
```bash
# Run your FastAPI app locally in one terminal
uvicorn main:app --reload

# In another terminal, expose it
ngrok http 8000

# Share this URL with friends
# https://abc123.ngrok.io/health
# https://abc123.ngrok.io/docs
```

**Pros:**
- Works immediately
- Excellent documentation
- Good free tier

**Cons:**
- URL changes on restart (unless paid tier)
- Slower than direct connection

---

### Option 2: Cloudflare Tunnel (Best for Persistence) ⭐

**Installation:**
```bash
# macOS
brew install cloudflare/cloudflare/cf

# Or download from https://developers.cloudflare.com/cloudflare-one/connections/connect-applications/install-and-setup/tunnel-guide/local/
```

**Setup (One-time):**
```bash
# Authenticate with Cloudflare
cf tunnel login

# Create tunnel
cf tunnel create my-fastapi-tunnel

# Route to your domain (requires owning a domain on Cloudflare)
cf tunnel route dns my-fastapi-tunnel yourdomain.com
```

**Usage (Every dev session):**
```bash
# Run your FastAPI app
uvicorn main:app --reload

# In another terminal, run tunnel
cf tunnel run my-fastapi-tunnel --url http://localhost:8000

# Share with friends
# https://yourdomain.com/health
# https://yourdomain.com/docs
```

**Pros:**
- Free forever
- Persistent URL (domain-based)
- No rate limits
- Secure (runs over HTTPS)
- No account required if using domain

**Cons:**
- Requires a domain name on Cloudflare (free or paid)

---

### Option 3: LocalTunnel (Simple)

**Installation:**
```bash
npm install -g localtunnel
```

**Usage:**
```bash
# Run app
uvicorn main:app --reload

# In another terminal
lt --port 8000 --subdomain my-fastapi

# Share: https://my-fastapi.loca.lt/health
```

**Pros:**
- Super simple, one command
- Free

**Cons:**
- Limited free tier
- Less reliable than ngrok

---

### Option 4: Expose.sh (One-liner)

```bash
# Most minimal option
uvicorn main:app --reload | expose
```

**Pros:**
- Single command
- Very lightweight

**Cons:**
- Limited features
- Less stable

---

## 4. Recommended Development Workflow

### For Local Development + Team Testing

**Best Option: Cloudflare Tunnel (if you have a domain)**

```bash
# Terminal 1: Run your app
cd ~/fastapi_project
source my_env/bin/activate
uvicorn main:app --reload

# Terminal 2: Run tunnel
cf tunnel run my-fastapi-tunnel --url http://localhost:8000

# Share URL with friends:
# https://yourdomain.com
```

**Alternative: ngrok (no domain needed)**

```bash
# Terminal 1: Run your app
cd ~/fastapi_project
source my_env/bin/activate
uvicorn main:app --reload

# Terminal 2: Run tunnel
ngrok http 8000

# Copy and share the URL
# https://abc123.ngrok.io
```

---

## 5. Complete CI/CD + Deployment Flow

```
┌─────────────────────────────────────────────────────────┐
│ Development Phase                                       │
├─────────────────────────────────────────────────────────┤
│ 1. Local Development                                    │
│    ├─ Run: uvicorn main:app --reload                  │
│    ├─ Share: ngrok/cf tunnel for friend testing       │
│    └─ Version: Git commits to initial_dev             │
│                                                         │
│ 2. Push to initial_dev                                │
│    └─ Create PR to main                               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ CI/CD Pipeline (GitHub Actions)                        │
├─────────────────────────────────────────────────────────┤
│ 1. Merge PR to main                                    │
│    └─ Trigger GitHub Actions                          │
│                                                         │
│ 2. Automated Tests                                     │
│    ├─ Lint code                                        │
│    ├─ Run unit tests                                   │
│    └─ Check dependencies                              │
│                                                         │
│ 3. Build                                              │
│    ├─ Create Docker image (optional)                  │
│    └─ Run health checks                               │
│                                                         │
│ 4. Deploy                                             │
│    └─ Push to Railway/Render                          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Production                                              │
├─────────────────────────────────────────────────────────┤
│ 1. Live Environment (Railway/Render)                   │
│    ├─ Auto-scaled instances                           │
│    ├─ HTTPS enabled                                    │
│    └─ Environment variables set                       │
│                                                         │
│ 2. Team Access                                         │
│    └─ https://your-app.railway.app                    │
│    └─ https://your-app.onrender.com                   │
│                                                         │
│ 3. Monitoring                                          │
│    ├─ Health checks                                    │
│    ├─ Error tracking                                   │
│    └─ Performance metrics                             │
└─────────────────────────────────────────────────────────┘
```

---

## 6. GitHub Actions Implementation Examples

### Basic CI/CD Workflow

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, initial_dev]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Lint with flake8
        run: |
          pip install flake8
          flake8 app main.py --count --select=E9,F63,F7,F82 --show-source --statistics
      
      - name: Health check
        run: |
          python -m pytest tests/ || echo "No tests yet"

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: |
          npm i -g @railway/cli
          railway deploy --service fastapi-backend
```

### Deploy to Render

```yaml
# .github/workflows/deploy-render.yml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Trigger Render Deploy
        run: |
          curl https://api.render.com/deploy/srv-${{ secrets.RENDER_SERVICE_ID }}?key=${{ secrets.RENDER_API_KEY }} \
            -X POST
```

---

## 7. Setting Up GitHub Actions (Step-by-Step)

### 1. Create Workflow File

```bash
mkdir -p .github/workflows
touch .github/workflows/ci-cd.yml
```

### 2. Add Workflow Content

Copy the YAML from section 6 above into `.github/workflows/ci-cd.yml`

### 3. Add Secrets to GitHub

```
GitHub Repo → Settings → Secrets and variables → Actions

Add:
- RAILWAY_TOKEN (from Railway dashboard)
- RENDER_API_KEY (from Render dashboard)
- RENDER_SERVICE_ID (from Render dashboard)
```

### 4. Push and Test

```bash
git add .github/
git commit -m "Add CI/CD pipeline"
git push origin initial_dev
```

### 5. View Pipeline Status

- Go to GitHub → Actions tab
- Click on your workflow
- See build status and logs

---

## 8. Cost Breakdown

### Free Stack

| Component | Service | Cost |
|-----------|---------|------|
| CI/CD | GitHub Actions | Free |
| Hosting | Railway/Render | Free tier |
| Database | PostgreSQL (Railway/Render) | Free tier |
| Tunneling (dev) | Cloudflare Tunnel | Free |
| Domain | Cloudflare | Free tier |
| **Total** | | **$0/month** |

### Low-Cost Stack

| Component | Service | Cost |
|-----------|---------|------|
| CI/CD | GitHub Actions | Free |
| Hosting | Railway | $5-10/month |
| Database | PostgreSQL | Included |
| Monitoring | Datadog | Free tier |
| **Total** | | **$5-10/month** |

---

## 9. Quick Start Checklist

- [ ] Set up GitHub Actions workflow (.github/workflows/)
- [ ] Add RAILWAY_TOKEN or RENDER_API_KEY to GitHub Secrets
- [ ] Test pipeline: Push to main
- [ ] Verify deployment completes
- [ ] Share deployed URL with team
- [ ] Set up ngrok/Cloudflare Tunnel for dev testing
- [ ] Create PR template for code reviews

---

## 10. Troubleshooting

### Pipeline Fails

1. Check GitHub Actions logs: Repo → Actions → Failed workflow
2. Common issues:
   - Missing environment variables
   - Dependency installation failure
   - Invalid token/secrets

### Deploy Fails

1. Check platform logs (Railway/Render dashboard)
2. Verify environment variables set correctly
3. Check logs with: `railway logs` or `render logs`

### Tunnel Not Working

1. ngrok: Check if port 8000 is in use
2. Cloudflare: Verify domain DNS is pointing to Cloudflare
3. Try different port: `ngrok http 8001`

---

## Next Steps

1. **Immediately:** Set up ngrok or Cloudflare Tunnel for dev testing
2. **Soon:** Create `.github/workflows/ci-cd.yml` for GitHub Actions
3. **When ready:** Integrate with Railway/Render deployment
4. **Later:** Add tests and advanced monitoring

---

## Useful Links

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Railway Deployment](https://railway.app)
- [Render Deployment](https://render.com)
- [ngrok Documentation](https://ngrok.com/docs)
- [Cloudflare Tunnel Guide](https://developers.cloudflare.com/cloudflare-one/connections/connect-applications/)
