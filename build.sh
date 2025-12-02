#!/bin/bash

# Production Build Script for Content Audit Tool

echo "🚀 Building Content Audit Tool for Production..."

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: vercel.json not found. Please run from project root."
    exit 1
fi

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install

# Build frontend
echo "🔨 Building frontend..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Frontend build failed!"
    exit 1
fi

echo "✅ Frontend build successful!"

# Check if dist folder exists
if [ ! -d "dist" ]; then
    echo "❌ Error: dist folder not created!"
    exit 1
fi

cd ..

# Verify Python dependencies
echo "🐍 Verifying Python dependencies..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found!"
    exit 1
fi

echo "✅ All checks passed!"
echo ""
echo "📋 Build Summary:"
echo "   - Frontend built to: frontend/dist/"
echo "   - API entry point: api/index.py"
echo "   - Configuration: vercel.json"
echo ""
echo "🎯 Next Steps:"
echo "   1. Push to Git: git push origin main"
echo "   2. Deploy: vercel --prod"
echo "   3. Set OPENAI_API_KEY in Vercel dashboard"
echo ""
echo "✨ Ready for deployment!"
