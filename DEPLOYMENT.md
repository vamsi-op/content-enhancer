# 🚀 Vercel Deployment Guide

## Prerequisites
- Vercel account (free tier works)
- Git repository (GitHub, GitLab, or Bitbucket)
- OpenAI API key (for AI features)

## Quick Deploy Steps

### 1. Prepare Your Repository
```bash
# Make sure all changes are committed
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

### 2. Deploy to Vercel

#### Option A: Using Vercel Dashboard (Recommended)
1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New Project"**
3. Import your Git repository
4. Vercel will auto-detect the configuration from `vercel.json`
5. **Add Environment Variable:**
   - Key: `OPENAI_API_KEY`
   - Value: Your OpenAI API key
6. Click **"Deploy"**

#### Option B: Using Vercel CLI
```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from project root
vercel

# Follow the prompts:
# - Link to existing project? No
# - Project name: content-audit-tool
# - Directory: ./
# - Override settings? No

# Add environment variable
vercel env add OPENAI_API_KEY

# Deploy to production
vercel --prod
```

### 3. Configure Environment Variables
After deployment, add your OpenAI API key:

1. Go to your project dashboard on Vercel
2. Navigate to **Settings** → **Environment Variables**
3. Add the following:
   - **Name:** `OPENAI_API_KEY`
   - **Value:** Your OpenAI API key (starts with `sk-...`)
   - **Environment:** Production, Preview, Development (select all)
4. Click **Save**
5. **Redeploy** the project for changes to take effect

### 4. Verify Deployment
Once deployed, test these endpoints:

1. **Frontend:** `https://your-project.vercel.app`
2. **API Health:** `https://your-project.vercel.app/api/health`
3. **Test Analysis:** Use the web interface to analyze some content

## Project Structure
```
Content_Audit_Tool/
├── api/
│   └── index.py          # Serverless API entry point
├── backend/
│   ├── analyzers/        # Analysis modules
│   ├── utils/            # Helper utilities
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/              # React source code
│   ├── dist/             # Build output (generated)
│   └── package.json      # Node dependencies
├── vercel.json           # Vercel configuration
└── requirements.txt      # Root Python dependencies
```

## Configuration Files Explained

### `vercel.json`
- Routes API requests to Python serverless functions
- Serves React frontend as static files
- Handles SPA routing

### API Routes
- `/api/*` → Python Flask backend
- `/*` → React frontend (static files)

## Troubleshooting

### Issue: API requests fail with CORS errors
**Solution:** The `api/index.py` already has CORS configured. Make sure the frontend is using relative URLs (`/api`) in production.

### Issue: AI features not working
**Solution:** 
1. Check if `OPENAI_API_KEY` is set in Vercel environment variables
2. Verify the API key is valid
3. Check function logs in Vercel dashboard

### Issue: Frontend shows 404
**Solution:** 
1. Check if frontend build succeeded in deployment logs
2. Verify `vercel.json` routes configuration
3. Make sure `frontend/dist` folder contains built files

### Issue: Python dependencies not installing
**Solution:** 
1. Check `requirements.txt` has all dependencies
2. Ensure Python version is compatible (3.9+)
3. Check Vercel build logs for specific errors

### Issue: Function timeout
**Solution:** 
1. Vercel free tier has 10s timeout
2. Optimize SERP scraping (reduce requests)
3. Consider upgrading to Pro for 60s timeout

## Performance Optimization

### 1. Reduce Bundle Size
```bash
cd frontend
npm run build
```
Check bundle size in `frontend/dist`

### 2. Cache Static Assets
Already configured in `vercel.json` routes

### 3. Optimize Images
Use WebP format for images in `frontend/public`

## Monitoring

### View Logs
```bash
vercel logs [deployment-url]
```

Or check the Vercel dashboard:
1. Go to your project
2. Click **Deployments**
3. Select a deployment
4. View **Function Logs** and **Build Logs**

## Custom Domain (Optional)

1. Go to **Settings** → **Domains**
2. Add your custom domain
3. Update DNS records as instructed
4. Wait for SSL certificate (automatic)

## Continuous Deployment

Vercel automatically deploys when you push to your main branch:
```bash
git add .
git commit -m "Update feature"
git push origin main
# Vercel auto-deploys!
```

## Environment-Specific URLs

- **Production:** `https://your-project.vercel.app`
- **Preview:** `https://your-project-git-branch.vercel.app` (for each branch)
- **Development:** `http://localhost:5173` (local)

## Security Best Practices

1. ✅ Never commit `.env` files
2. ✅ Use Vercel environment variables
3. ✅ Keep `OPENAI_API_KEY` secret
4. ✅ Enable Vercel Authentication for sensitive features (optional)
5. ✅ Use `.vercelignore` to exclude unnecessary files

## Cost Considerations

**Free Tier Includes:**
- 100 GB bandwidth/month
- 100 serverless function executions/day
- 6000 build minutes/month
- Automatic HTTPS

**Pro Tier ($20/month):**
- Unlimited bandwidth
- Unlimited function executions
- 60s function timeout (vs 10s free)

## Support

- **Vercel Docs:** https://vercel.com/docs
- **GitHub Issues:** Report bugs in your repository
- **Vercel Support:** support@vercel.com

---

## Quick Commands Cheat Sheet

```bash
# Local development
npm run dev                    # Start frontend (port 5173)
python backend/app.py          # Start backend (port 5000)

# Build locally
cd frontend && npm run build   # Build frontend

# Deploy
vercel                         # Deploy preview
vercel --prod                  # Deploy production

# Logs
vercel logs                    # View deployment logs
vercel env ls                  # List environment variables

# Rollback
vercel rollback               # Rollback to previous deployment
```

## Success Checklist

- [ ] Repository pushed to Git
- [ ] Project imported to Vercel
- [ ] `OPENAI_API_KEY` environment variable set
- [ ] Deployment successful (check logs)
- [ ] Frontend loads correctly
- [ ] API health endpoint responds
- [ ] Test content analysis works
- [ ] AI rewrite features functional
- [ ] History saves and loads
- [ ] Export features work

**Your app is now live! 🎉**
