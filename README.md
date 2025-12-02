# 🎯 Content Quality Audit Tool

**Hackathon 2025 Submission**

A comprehensive content analysis tool that scores content across 5 critical dimensions with AI-powered insights and predictions.

## 🚀 Features

### Core Analysis Modules
1. **SEO Score** (0-100)
   - Keyword density analysis
   - Flesch-Kincaid readability
   - Header structure validation
   - Meta description check

2. **SERP Performance Score** (0-100)
   - Scrapes top 10 Google results
   - Compares word count, topics, content elements
   - **AI Rank Predictor**: Shows current vs improved ranking (e.g., Rank 27 → Rank 9)
   - Competitor fingerprinting (patterns analysis)

3. **AEO Score** (0-100)
   - Citation quality detection
   - Structured formatting check
   - AI-friendly patterns analysis

4. **Humanization Score** (0-100)
   - Sentence variety analysis
   - AI pattern detection
   - **Humanization Heatmap**: Color-coded AI vs human sentences

5. **Differentiation Score** (0-100)
   - Content uniqueness vs SERP top 3
   - Unique examples detection
   - Voice differentiation

### Signature Features (Competitive Advantage)
- **📈 AI Rank Simulator**: Visual before/after ranking prediction
- **🌡️ Humanization Heatmap**: Highlights AI-patterned sentences
- **🔄 AI-Powered Rewrites**: Fix content issues with OpenAI (one-click improvements)
- **⚡ Lightning Fast**: Instant analysis (URL → Full audit in 5 seconds)
- **🎨 Clean Dashboard**: Notion-style UI with color-coded scores

## 🛠️ Tech Stack

**Backend:**
- Python 3.11+
- Flask + Flask-CORS
- BeautifulSoup4 (SERP scraping)
- NLTK + TextStat (NLP analysis)
- Scikit-learn (text similarity)
- OpenAI API (content improvements)

**Frontend:**
- React 18 (Vite)
- Modern CSS (responsive, gradient design)
- Local Storage (history feature)

**Deployment:**
- Vercel (Serverless deployment)
- Auto-scaling, CDN, HTTPS included

## 📦 Installation

### Quick Deploy to Vercel (Recommended)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/content-audit-tool)

**OR follow the detailed guide:** [DEPLOYMENT.md](DEPLOYMENT.md)

**Quick steps:**
1. Push to GitHub
2. Import to Vercel
3. Add `OPENAI_API_KEY` environment variable
4. Deploy! ✨

### Local Development

#### Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Mac/Linux
pip install -r requirements.txt

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .env

python app.py
```

Backend runs on: http://localhost:5000

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: http://localhost:5173

### Build for Production
```bash
# Windows
.\build.ps1

# Mac/Linux
./build.sh
```

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide.

**Environment Variables Required:**
- `OPENAI_API_KEY` - Your OpenAI API key (required for AI features)

## 🎮 Usage

1. **Enter Content**: Paste text OR enter a URL
2. **Add Keyword** (optional): Target keyword for SEO analysis
3. **Click Analyze**: Get instant results across all 5 dimensions
4. **View Insights**:
   - Overall content quality score
   - AI rank prediction (current vs improved)
   - Detailed breakdown for each dimension
   - Humanization heatmap
   - Top recommendations

## 📊 What Makes This Special

### 1. Real SERP Analysis (Not Hand-Wavy)
- Actually scrapes top 10 Google results
- Compares word count, headers, content elements
- Shows competitor patterns: "80% include case studies, 70% use comparison tables"

### 2. AI Rank Simulator
```
Current Estimate: Rank #27
With Improvements: Rank #9
↑ Improvement: +18 positions
```

### 3. Humanization Heatmap
Visually highlights AI-like sentences:
- 🟢 Green = Human-like
- 🔴 Red = AI patterns detected

### 4. One-Click AI Improvements
- Fix meta description
- Rewrite AI-sounding paragraphs
- Suggest missing subtopics

## 🏆 Competitive Edge

**vs Other Teams:**
- ✅ Working prototype (not slideware)
- ✅ Real SERP data (not mocked)
- ✅ Unique visualizations (rank simulator + heatmap)
- ✅ Clean, fast UI (Notion-style)
- ✅ AI-powered fixes (OpenAI integration)

**Judge-Friendly:**
- Visible, impressive results
- Solves universal pain point
- Live demo ready
- Works on any content/URL

## 📝 Example Output

```
CONTENT AUDIT RESULTS

Overall Score: 68.4/100

📈 AI Rank Prediction:
Current Estimate: Rank #22
With Improvements: Rank #8
Message: Fix these issues to potentially move from Rank 22 → Rank 8

🔍 SEO Score: 72/100
✓ Good: Header structure present (H1, H2, H3)
✗ Issue: Keyword "budget laptops" appears only 2 times (0.4% density)
→ Rec: Increase keyword to 5-7 mentions (aim for 1.5% density)

📊 SERP Performance: 58/100
✗ Issue: Content 58% shorter than SERP average
→ Rec: Expand to 2,500+ words covering missing subtopics

🤖 AEO Score: 65/100
✗ Issue: No FAQ section detected
→ Rec: Add FAQ section with schema markup

👤 Humanization: 58/100
✗ Issue: 40% sentences start the same way
→ Rec: Vary sentence starters and lengths

💎 Differentiation: 51/100
✗ Issue: 70% content overlap with top 3 SERP results
→ Rec: Add original data points or unique examples
```

## 🎯 Built For

**Hackathon Success Criteria:**
- ✅ Accepts text OR URL inputs
- ✅ Generates meaningful scores (0-100)
- ✅ SERP analysis with real data
- ✅ Specific, actionable recommendations
- ✅ Clean dashboard presentation
- ✅ Working prototype

## 🎨 UI Highlights

- Gradient header (purple → pink)
- Color-coded score badges (green/yellow/red)
- Rank simulator with visual comparison
- Heatmap for AI patterns
- Responsive design
- Fast, smooth interactions

## 📄 License

MIT License - Built for Hackathon 2025

---

**Made with ❤️ and lots of ☕**
