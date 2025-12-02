# 🚀 Vercel Deployment Checklist

Use this checklist before deploying to ensure everything is configured correctly.

## Pre-Deployment Checklist

### 📁 Files & Configuration
- [x] `vercel.json` exists in root
- [x] `api/index.py` properly configured
- [x] `requirements.txt` in root directory
- [x] Frontend `package.json` has `build` script
- [x] `.vercelignore` configured
- [x] `.env.example` created (don't commit actual `.env`)

### 🔧 Code Configuration
- [x] API URLs use relative paths in production (`/api`)
- [x] CORS configured in `api/index.py`
- [x] Flask app exports `handler` for Vercel
- [x] Frontend builds successfully (`npm run build`)

### 🔑 Environment Variables
- [ ] `OPENAI_API_KEY` - Get from https://platform.openai.com/api-keys
- [ ] Add to Vercel dashboard after deployment

### 📦 Dependencies
- [x] All Python packages in `requirements.txt`
- [x] All npm packages in `frontend/package.json`
- [x] No missing imports in code

### 🧪 Testing
- [ ] Test build locally: `npm run build` (in frontend/)
- [ ] Test API locally: `python api/index.py` (if possible)
- [ ] Verify frontend connects to backend locally
- [ ] Test all features work (analyze, AI rewrite, history, export)

## Deployment Steps

### 1. Push to Git
```bash
git add .
git commit -m "Ready for production deployment"
git push origin main
```

### 2. Vercel Dashboard Deployment
1. Go to https://vercel.com/new
2. Import your Git repository
3. Vercel auto-detects settings from `vercel.json`
4. Click **Deploy**

### 3. Add Environment Variables
**After first deployment:**
1. Go to Project Settings → Environment Variables
2. Add `OPENAI_API_KEY`:
   - Name: `OPENAI_API_KEY`
   - Value: `sk-...` (your OpenAI key)
   - Environments: Production, Preview, Development
3. Click **Save**
4. **Redeploy** the project

### 4. Verify Deployment
Test these URLs (replace with your deployment URL):

- [ ] Frontend loads: `https://your-project.vercel.app`
- [ ] API health check: `https://your-project.vercel.app/api/health`
- [ ] Analyze content feature works
- [ ] AI rewrite feature works (requires API key)
- [ ] History saves and loads
- [ ] Export features work

## Post-Deployment

### Custom Domain (Optional)
1. Go to Settings → Domains
2. Add your domain
3. Configure DNS records
4. Wait for SSL (automatic)

### Monitoring
- Check **Deployments** tab for build logs
- View **Functions** tab for API logs
- Monitor usage in **Analytics**

### Continuous Deployment
Every push to `main` auto-deploys:
```bash
git add .
git commit -m "New feature"
git push
# Auto-deploys to Vercel!
```

## Troubleshooting Guide

### Build Fails
- [ ] Check **Deployment Logs** in Vercel dashboard
- [ ] Verify all dependencies are in `package.json` and `requirements.txt`
- [ ] Test build locally first

### API Errors
- [ ] Check if `OPENAI_API_KEY` is set
- [ ] View **Function Logs** in Vercel dashboard
- [ ] Test `/api/health` endpoint
- [ ] Verify CORS headers in `api/index.py`

### Frontend 404
- [ ] Check if `frontend/dist` was created during build
- [ ] Verify `vercel.json` routes configuration
- [ ] Check build logs for npm errors

### AI Features Not Working
- [ ] Confirm `OPENAI_API_KEY` is valid
- [ ] Check OpenAI API quotas/billing
- [ ] View function logs for specific errors
- [ ] Test API key with curl/Postman

## Performance Tips

### Optimize Frontend
- Images: Use WebP format
- Code splitting: Already configured in Vite
- Lazy loading: Consider for large components

### Optimize Backend
- Cache SERP results (add Redis if needed)
- Reduce OpenAI token usage
- Optimize text processing

### Vercel Limits (Free Tier)
- 100 GB bandwidth/month
- 100 function invocations/day
- 10s function timeout
- 12 MB function size

**Upgrade to Pro if needed ($20/month):**
- Unlimited bandwidth
- Unlimited invocations
- 60s timeout

## Quick Commands

```bash
# View deployment logs
vercel logs

# List environment variables
vercel env ls

# Deploy to production
vercel --prod

# Rollback deployment
vercel rollback

# Open project in browser
vercel open
```

## Success Criteria

Your deployment is successful when:
- ✅ Frontend loads without errors
- ✅ API responds to health check
- ✅ Content analysis works
- ✅ AI features functional (if API key set)
- ✅ History persists across sessions
- ✅ Export features work
- ✅ Mobile responsive
- ✅ Fast loading (<3s)

## Need Help?

- **Vercel Docs:** https://vercel.com/docs
- **Vercel Support:** https://vercel.com/support
- **OpenAI API Docs:** https://platform.openai.com/docs

---

**Ready to deploy? Let's go! 🚀**

```bash
vercel --prod
```
