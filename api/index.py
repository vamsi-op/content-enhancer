from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Initialize Flask app first
app = Flask(__name__)

# Enable CORS for Vercel deployment
CORS(app, resources={
    r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Try to import and initialize NLTK
try:
    import nltk
    nltk.data.path.append('/tmp/nltk_data')
    # Download required NLTK data
    try:
        nltk.download('punkt', download_dir='/tmp/nltk_data', quiet=True)
        nltk.download('stopwords', download_dir='/tmp/nltk_data', quiet=True)
    except:
        pass
except Exception as e:
    print(f"NLTK initialization warning: {e}")

# Import analyzers and utilities with error handling
IMPORT_ERROR = None
try:
    # Use relative imports for Vercel serverless
    import sys
    import os
    # Add current directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from analyzers.seo_analyzer import SEOAnalyzer
    from analyzers.serp_analyzer import SERPAnalyzer
    from analyzers.aeo_analyzer import AEOAnalyzer
    from analyzers.humanization_analyzer import HumanizationAnalyzer
    from analyzers.differentiation_analyzer import DifferentiationAnalyzer
    from utils.text_extractor import TextExtractor
    from utils.ai_improver import AIContentImprover
    MODULES_LOADED = True
except Exception as e:
    IMPORT_ERROR = str(e)
    print(f"Module import error: {e}")
    import traceback
    traceback.print_exc()
    MODULES_LOADED = False

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "message": "Content Audit API is running",
        "modules_loaded": MODULES_LOADED,
        "error": IMPORT_ERROR if not MODULES_LOADED else None
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_content():
    """Main endpoint to analyze content"""
    if not MODULES_LOADED:
        return jsonify({"error": "Server initialization failed. Please check logs."}), 500
    
    try:
        data = request.json
        input_data = data.get('input', '')
        target_keyword = data.get('target_keyword', '')
        is_url = data.get('is_url', False)
        
        if not input_data:
            return jsonify({"error": "No input provided"}), 400
        
        # Extract text and metadata
        extractor = TextExtractor()
        
        if is_url:
            try:
                import requests
                from bs4 import BeautifulSoup
                
                response = requests.get(input_data, timeout=10, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                soup = BeautifulSoup(response.content, 'html.parser')
                
                title = soup.find('title')
                title = title.get_text() if title else ''
                
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                meta_description = meta_desc['content'] if meta_desc and meta_desc.get('content') else ''
                
                headers = []
                for tag in ['h1', 'h2', 'h3']:
                    headers.extend([h.get_text().strip() for h in soup.find_all(tag)])
                
                for script in soup(['script', 'style', 'nav', 'footer', 'header']):
                    script.decompose()
                text = soup.get_text(separator=' ', strip=True)
                
                content_data = {
                    'text': text,
                    'url': input_data,
                    'headers': headers,
                    'meta_description': meta_description,
                    'title': title
                }
            except Exception as e:
                return jsonify({"error": f"Failed to fetch URL: {str(e)}"}), 400
        else:
            content_data = extractor.extract(input_data)
        
        if not isinstance(content_data, dict):
            return jsonify({"error": "Failed to extract content properly"}), 400
            
        if not content_data.get('text'):
            return jsonify({"error": "Could not extract text from input"}), 400
        
        text = content_data['text']
        url = content_data.get('url')
        headers = content_data.get('headers', [])
        if not isinstance(headers, list):
            headers = []
            
        meta_description = content_data.get('meta_description', '')
        title = content_data.get('title', '')
        
        # Run all analyzers
        seo_analyzer = SEOAnalyzer()
        serp_analyzer = SERPAnalyzer()
        aeo_analyzer = AEOAnalyzer()
        humanization_analyzer = HumanizationAnalyzer()
        differentiation_analyzer = DifferentiationAnalyzer()
        
        seo_results = seo_analyzer.analyze(
            text=text,
            headers=headers,
            meta_description=meta_description,
            target_keyword=target_keyword
        )
        
        serp_results = serp_analyzer.analyze(
            text=text,
            target_keyword=target_keyword,
            headers=headers
        )
        
        aeo_results = aeo_analyzer.analyze(
            text=text,
            headers=headers
        )
        
        humanization_results = humanization_analyzer.analyze(text)
        
        differentiation_results = differentiation_analyzer.analyze(
            text=text,
            serp_data=serp_results.get('details', {})
        )
        
        scores = [
            seo_results['score'],
            serp_results['score'],
            aeo_results['score'],
            humanization_results['score'],
            differentiation_results['score']
        ]
        overall_score = sum(scores) / len(scores)
        
        current_rank = serp_results['details'].get('ranking_prediction', {}).get('current_position', 20)
        improved_rank = max(3, int(current_rank * 0.4)) if overall_score < 70 else max(3, int(current_rank * 0.6))
        
        rank_prediction = {
            'current_estimated_rank': current_rank,
            'improved_estimated_rank': improved_rank,
            'improvement': current_rank - improved_rank,
            'message': f"Fix these issues to potentially move from Rank {current_rank} → Rank {improved_rank}"
        }
        
        response_data = {
            'overall_score': round(overall_score, 1),
            'original_text': text[:5000],
            'content_info': {
                'word_count': len(text.split()),
                'source_type': content_data.get('source_type', 'text'),
                'url': url,
                'title': title,
                'target_keyword': target_keyword
            },
            'scores': {
                'seo': seo_results,
                'serp': serp_results,
                'aeo': aeo_results,
                'humanization': humanization_results,
                'differentiation': differentiation_results
            },
            'rank_prediction': rank_prediction,
            'top_recommendations': _get_top_recommendations([
                seo_results, serp_results, aeo_results, 
                humanization_results, differentiation_results
            ])
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        return jsonify({"error": str(e), "traceback": error_traceback}), 500

@app.route('/api/improve', methods=['POST'])
def improve_content():
    """AI-powered content improvement endpoint with multiple modes"""
    try:
        data = request.json
        text = data.get('text', '')
        analysis = data.get('analysis', {})
        improvement_type = data.get('improvement_type', 'full')
        target_keyword = data.get('target_keyword', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        improver = AIContentImprover()
        
        if improvement_type == 'meta':
            title = data.get('title', '')
            result = improver.fix_meta_description(title, text, target_keyword)
            
            return jsonify({
                'success': True,
                'improved_meta': result,
                'changes_made': ['Generated SEO-optimized meta description']
            })
        
        elif improvement_type == 'seo':
            result = improver.rewrite_for_seo(text, target_keyword, analysis)
            return jsonify(result)
        
        elif improvement_type == 'humanize':
            result = improver.humanize_content(text)
            return jsonify(result)
        
        elif improvement_type == 'readability':
            result = improver.improve_readability(text)
            return jsonify(result)
        
        elif improvement_type == 'engagement':
            result = improver.boost_engagement(text)
            return jsonify(result)
        
        else:
            result = improver.generate_fixes(text, analysis)
            return jsonify(result)
            
    except Exception as e:
        import traceback
        return jsonify({"error": str(e), "success": False}), 500

def _get_top_recommendations(all_results):
    """Extract top 5 recommendations across all analyzers"""
    all_recommendations = []
    
    for result in all_results:
        if 'recommendations' in result:
            all_recommendations.extend(result['recommendations'][:2])
    
    unique_recs = []
    for rec in all_recommendations:
        if rec not in unique_recs:
            unique_recs.append(rec)
    
    return unique_recs[:5]

# Vercel looks for 'app' or 'application' variable
# This exports the Flask app for Vercel's Python runtime
if __name__ == '__main__':
    app.run(debug=True, port=5000)
