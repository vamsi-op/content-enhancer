# Content Quality Audit Tool

> AI-powered content analysis tool that scores content across 5 critical dimensions with real-time SERP analysis and intelligent recommendations.

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://content-enhancer.vercel.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

![Content Audit Tool](https://img.shields.io/badge/Made%20with-React%20%2B%20Flask-61DAFB?style=flat&logo=react)

---

## Features

### Comprehensive Content Analysis

- **SEO Score** - Keyword density, readability, meta tags, and header structure
- **SERP Performance** - Real-time comparison with top 10 Google results
- **AEO Score** - AI-friendly content structure and citation quality
- **Humanization Score** - Detects AI-generated patterns with visual heatmap
- **Differentiation Score** - Measures uniqueness against competitors

### Unique Capabilities

- **AI Rank Simulator** - Predicts ranking improvement (e.g., Rank #27 → #9)
- **Competitor Intelligence** - Analyzes top 10 SERP patterns and content strategies
- **Humanization Heatmap** - Color-coded visualization of AI vs human-like text
- **One-Click AI Rewrite** - Fix content issues with OpenAI-powered suggestions
- **History Tracking** - Save and revisit past analyses with localStorage
- **Export Options** - Download as JSON or formatted HTML report

---

## Demo

**Live Site:** [https://content-enhancer.vercel.app](https://content-enhancer.vercel.app)

### Quick Start
1. Paste content or enter a URL
2. Add target keyword (optional)
3. Click "Analyze Content"
4. Get instant scores across 5 dimensions

---

## Tech Stack

**Frontend**
- React 18 + Vite
- Modern CSS with responsive design
- Local Storage for history

**Backend**
- Python 3.9+ with Flask
- BeautifulSoup4 for SERP scraping
- TextStat for readability analysis
- OpenAI API for content improvements

**Deployment**
- Vercel (Serverless)
- Auto-scaling, CDN, HTTPS


---

## Local Development

### Prerequisites
- Python 3.9+
- Node.js 16+
- OpenAI API key (optional, for AI features)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env

python app.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

---

## Usage Examples

### Analyze a Blog Post

```
Input: Paste your blog content
Keyword: "best budget laptops"
Result: Overall Score 68.4/100
- SEO: 72/100 ✓ Good structure
- SERP: 58/100 ⚠️ 42% shorter than competitors
- AEO: 65/100 ⚠️ Missing FAQ section
- Humanization: 58/100 ⚠️ Repetitive sentence patterns
- Differentiation: 51/100 ⚠️ 70% content overlap
```

### Analyze a URL

```
Input: https://example.com/article
Result: Full analysis with SERP comparison
- Current estimated rank: #22
- With improvements: #8 potential
```

---

## Key Features Explained

### AI Rank Simulator
Visual prediction showing how fixing identified issues could improve search rankings.

### SERP Intelligence
- Scrapes top 10 Google results
- Analyzes word count, topics, content patterns
- Shows competitor strategies (e.g., "80% use case studies")

### Humanization Heatmap
Color-coded sentences:
- Green = Natural, human-like
- Red = AI-generated patterns detected

### AI Content Rewriter
Multiple rewrite modes:
- Full rewrite (fix all issues)
- SEO optimize
- Humanize content
- Improve readability
- Boost engagement
- Generate meta description

---

## Scoring Methodology

Each dimension scored 0-100:
- **SEO**: Keywords, readability (Flesch-Kincaid), headers, meta tags
- **SERP**: Content length, topic coverage vs top 10 results
- **AEO**: Structured data, citations, AI-friendly formatting
- **Humanization**: Sentence variety, transition words, AI patterns
- **Differentiation**: Unique examples, voice, content originality

**Overall Score**: Average of all 5 dimensions

---

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Built for Buildathon - AI for Vizag
- Powered by OpenAI API
- Deployed on Vercel

---

## Contact

**Project Link:** [https://github.com/vamsi-op/content-enhancer](https://github.com/vamsi-op/content-enhancer)

**Live Demo:** [https://content-enhancer.vercel.app](https://content-enhancer.vercel.app)

---

<p align="center">Made with care for content creators</p>
