# Deployment Guide

Complete guide to deploying Compliance Monitor to GitHub and Vercel.

---

## Prerequisites

- GitHub account
- Vercel account (free tier works)
- Anthropic API key (from https://console.anthropic.com/)
- Git installed locally

---

## Part 1: Push to GitHub

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in details:
   - **Repository name:** `compliance-monitor`
   - **Description:** "🚨 AI-powered compliance monitoring for payment businesses"
   - **Visibility:** Public
   - **Do NOT** initialize with README, .gitignore, or license (we already have these)
3. Click "Create repository"

### Step 2: Push Code to GitHub

Open terminal in the `compliance-monitor` directory and run:

```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit: Production-ready compliance monitor with enhanced dashboard"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/compliance-monitor.git

# Push to GitHub
git branch -M main
git push -u origin main
```

✅ **Your code is now on GitHub!**

### Step 3: Configure Repository

1. Go to your repository on GitHub
2. Click **Settings**
3. In **About** section (right sidebar), add:
   - Description: "🚨 Get 6-12 months warning on payment compliance changes. AI-powered monitoring of Visa, Mastercard, PSPs & regulators."
   - Website: (will add after Vercel deployment)
   - Topics: `fintech`, `payments`, `compliance`, `ai`, `claude`, `visa`, `mastercard`, `crypto`, `gambling`, `opensource`

---

## Part 2: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard (Easiest)

1. Go to https://vercel.com/
2. Sign in with GitHub
3. Click **"Add New..."** → **"Project"**
4. Import your `compliance-monitor` repository
5. Configure:
   - **Framework Preset:** Other
   - **Root Directory:** `./` (leave as default)
   - **Build Command:** Leave empty
   - **Output Directory:** `dashboard`
6. Click **"Deploy"**

Your dashboard will be live at: `https://compliance-monitor-xxx.vercel.app`

### Option B: Deploy via Vercel CLI (Advanced)

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod

# Follow prompts:
# - Setup and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? compliance-monitor
# - In which directory? ./
# - Want to override settings? No
```

✅ **Dashboard is now live on Vercel!**

### Step 4: Add Environment Variables (Optional for Auto-Scans)

If you want GitHub Actions to run automated scans:

1. Go to GitHub repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Add:
   - **Name:** `ANTHROPIC_API_KEY`
   - **Value:** Your API key from https://console.anthropic.com/
4. Click **"Add secret"**

Now the GitHub Action workflow will run weekly scans automatically!

---

## Part 3: Enable GitHub Pages (Alternative to Vercel)

If you prefer GitHub Pages over Vercel:

1. Go to repository **Settings** → **Pages**
2. **Source:** Deploy from a branch
3. **Branch:** `main`
4. **Folder:** `/dashboard`
5. Click **Save**

Dashboard will be live at: `https://YOUR_USERNAME.github.io/compliance-monitor/`

**Note:** With GitHub Pages, you'll need GitHub Actions to update the dashboard data.

---

## Part 4: Update URLs

### Update README

1. Edit `README.md`
2. Replace `https://compliance-monitor.vercel.app` with your actual Vercel URL
3. Replace `https://github.com/ganeshgunti/compliance-monitor` with your GitHub URL
4. Commit and push:

```bash
git add README.md
git commit -m "Update deployment URLs"
git push
```

### Update Vercel URL in GitHub

1. Go to GitHub repository page
2. Click gear icon next to **About**
3. Add your Vercel URL to **Website**
4. Save

---

## For Others Forking Your Repository

Anyone can fork and deploy their own version:

### For Forkersmd:

1. **Fork the repository** on GitHub
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/compliance-monitor.git
   cd compliance-monitor
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

5. **Customize your setup:**
   - Edit `config/company_profile.yaml` with your MCCs, regions
   - Edit `config/sources.yaml` to add your monitoring sources

6. **Initialize and test:**
   ```bash
   python run.py init
   python run.py demo
   python run.py dashboard
   ```

7. **Deploy to Vercel:**
   - Push your changes to GitHub
   - Go to https://vercel.com
   - Import your fork
   - Deploy!

---

## Maintenance

### Update Dashboard Data

```bash
# Run scan (requires API credits)
python run.py scan

# Generate dashboard
python run.py dashboard

# Commit and push
git add dashboard/data.json
git commit -m "Update compliance data"
git push
```

Vercel will auto-deploy the update!

### Manual Trigger via GitHub Actions

1. Go to **Actions** tab
2. Click **"Compliance Scan"**
3. Click **"Run workflow"**
4. Click **"Run workflow"** button

---

## Troubleshooting

### Vercel deployment fails

- Check `vercel.json` is present
- Ensure `dashboard/` folder exists
- Check build logs in Vercel dashboard

### GitHub Pages not updating

- Check Actions tab for workflow errors
- Ensure GitHub Pages is enabled in Settings
- Clear browser cache

### API key not working

- Verify key is correct in repository secrets
- Check you have credits at https://console.anthropic.com/
- Ensure secret name is exactly `ANTHROPIC_API_KEY`

---

## Cost Estimates

### Hosting
- **Vercel:** Free tier (100GB bandwidth, unlimited requests)
- **GitHub Pages:** Free (1GB storage, 100GB bandwidth/month)

### API Costs
- **Sonnet 4:** ~$0.50-$1 per scan
- **Opus 4.5:** ~$2-$4 per scan
- **Weekly scans:** ~$8-16/month with Opus
- **Recommendation:** Start with demo data, add credits when ready

---

## Support

Questions? Open an issue on GitHub or check the documentation.

Happy monitoring! 🚀
