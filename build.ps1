# Production Build Script for Content Audit Tool (Windows)

Write-Host "🚀 Building Content Audit Tool for Production..." -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "vercel.json")) {
    Write-Host "❌ Error: vercel.json not found. Please run from project root." -ForegroundColor Red
    exit 1
}

# Install frontend dependencies
Write-Host "`n📦 Installing frontend dependencies..." -ForegroundColor Cyan
Set-Location frontend
npm install

# Build frontend
Write-Host "`n🔨 Building frontend..." -ForegroundColor Cyan
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Frontend build failed!" -ForegroundColor Red
    Set-Location ..
    exit 1
}

Write-Host "✅ Frontend build successful!" -ForegroundColor Green

# Check if dist folder exists
if (-not (Test-Path "dist")) {
    Write-Host "❌ Error: dist folder not created!" -ForegroundColor Red
    Set-Location ..
    exit 1
}

Set-Location ..

# Verify Python dependencies
Write-Host "`n🐍 Verifying Python dependencies..." -ForegroundColor Cyan
if (-not (Test-Path "requirements.txt")) {
    Write-Host "❌ Error: requirements.txt not found!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ All checks passed!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Build Summary:" -ForegroundColor Yellow
Write-Host "   - Frontend built to: frontend/dist/"
Write-Host "   - API entry point: api/index.py"
Write-Host "   - Configuration: vercel.json"
Write-Host ""
Write-Host "🎯 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Push to Git: git push origin main"
Write-Host "   2. Deploy: vercel --prod"
Write-Host "   3. Set OPENAI_API_KEY in Vercel dashboard"
Write-Host ""
Write-Host "✨ Ready for deployment!" -ForegroundColor Magenta
