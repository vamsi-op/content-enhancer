from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import sys
import os

load_dotenv()

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analyzers.seo_analyzer import SEOAnalyzer
from analyzers.serp_analyzer import SERPAnalyzer
from analyzers.aeo_analyzer import AEOAnalyzer
from analyzers.humanization_analyzer import HumanizationAnalyzer
from analyzers.differentiation_analyzer import DifferentiationAnalyzer
from utils.text_extractor import TextExtractor
from utils.ai_improver import AIContentImprover

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Content Audit API is running"})

@app.route('/api/analyze', methods=['POST'])
def analyze_content():
    """Main endpoint to analyze content"""
    try:
        data = request.json
        input_data = data.get('input', '')
        target_keyword = data.get('target_keyword', '')
        is_url = data.get('is_url', False)
        
        if not input_data:
            return jsonify({"error": "No input provided"}), 400
        
        # 1. Extract text and metadata
        extractor = TextExtractor()
        
        # If URL mode, fetch the content
        if is_url:
            try:
                import requests
                from bs4 import BeautifulSoup
                
                response = requests.get(input_data, timeout=10, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract title
                title = soup.find('title')
                title = title.get_text() if title else ''
                
                # Extract meta description
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                meta_description = meta_desc['content'] if meta_desc and meta_desc.get('content') else ''
                
                # Extract headers
                headers = []
                for tag in ['h1', 'h2', 'h3']:
                    headers.extend([h.get_text().strip() for h in soup.find_all(tag)])
                
                # Extract main content
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
        
        # Safety check - ensure content_data is a dictionary
        if not isinstance(content_data, dict):
            return jsonify({"error": "Failed to extract content properly"}), 400
            
        if not content_data.get('text'):
            return jsonify({"error": "Could not extract text from input"}), 400
        
        text = content_data['text']
        url = content_data.get('url')
        
        # Headers should remain in dict format [{'level': 'h1', 'text': 'Title'}]
        headers = content_data.get('headers', [])
        if not isinstance(headers, list):
            headers = []
        
        # DEBUG: Print headers to see what we're working with
        print(f"\n=== DEBUG HEADERS ===")
        print(f"Type: {type(headers)}")
        print(f"Length: {len(headers)}")
        if headers:
            print(f"First item type: {type(headers[0])}")
            print(f"First item: {headers[0]}")
        print(f"====================\n")
            
        meta_description = content_data.get('meta_description', '')
        title = content_data.get('title', '')
        
        # 2. Run all analyzers
        seo_analyzer = SEOAnalyzer()
        serp_analyzer = SERPAnalyzer()
        aeo_analyzer = AEOAnalyzer()
        humanization_analyzer = HumanizationAnalyzer()
        differentiation_analyzer = DifferentiationAnalyzer()
        
        # SEO Analysis
        seo_results = seo_analyzer.analyze(
            text=text,
            headers=headers,
            meta_description=meta_description,
            target_keyword=target_keyword
        )
        
        # SERP Performance Analysis
        serp_results = serp_analyzer.analyze(
            text=text,
            target_keyword=target_keyword,
            headers=headers
        )
        
        # AEO Analysis
        aeo_results = aeo_analyzer.analyze(
            text=text,
            headers=headers
        )
        
        # Humanization Analysis
        humanization_results = humanization_analyzer.analyze(text)
        
        # Differentiation Analysis
        differentiation_results = differentiation_analyzer.analyze(
            text=text,
            serp_data=serp_results.get('details', {})
        )
        
        # 3. Calculate overall score
        scores = [
            seo_results['score'],
            serp_results['score'],
            aeo_results['score'],
            humanization_results['score'],
            differentiation_results['score']
        ]
        overall_score = sum(scores) / len(scores)
        
        # 4. Generate rank improvement prediction
        current_rank = serp_results['details'].get('ranking_prediction', {}).get('current_position', 20)
        improved_rank = max(3, int(current_rank * 0.4)) if overall_score < 70 else max(3, int(current_rank * 0.6))
        
        rank_prediction = {
            'current_estimated_rank': current_rank,
            'improved_estimated_rank': improved_rank,
            'improvement': current_rank - improved_rank,
            'message': f"Fix these issues to potentially move from Rank {current_rank} → Rank {improved_rank}"
        }
        
        # 5. Compile results
        response = {
            'overall_score': round(overall_score, 1),
            'original_text': text[:5000],  # Store first 5000 chars for AI rewriting
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
        
        return jsonify(response)
        
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print("="*50)
        print("ERROR IN /api/analyze:")
        print(error_traceback)
        print("="*50)
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
        custom_prompt = data.get('custom_prompt', None)
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        improver = AIContentImprover()
        
        if improvement_type == 'meta':
            # Generate meta description
            title = data.get('title', '')
            result = improver.fix_meta_description(title, text, target_keyword)
            
            return jsonify({
                'success': True,
                'improved_meta': result,
                'changes_made': ['Generated SEO-optimized meta description']
            })
        
        elif improvement_type == 'seo':
            # SEO-focused rewrite
            result = improver.rewrite_for_seo(text, target_keyword, analysis)
            return jsonify(result)
        
        elif improvement_type == 'humanize':
            # Humanization rewrite
            result = improver.humanize_content(text)
            return jsonify(result)
        
        elif improvement_type == 'readability':
            # Readability improvement
            result = improver.improve_readability(text)
            return jsonify(result)
        
        elif improvement_type == 'engagement':
            # Engagement optimization
            result = improver.boost_engagement(text)
            return jsonify(result)
        
        elif improvement_type == 'paragraph':
            # Rewrite specific paragraph
            paragraph = data.get('paragraph', text[:500])
            issue_type = data.get('issue_type', 'humanization')
            result = improver.rewrite_paragraph(paragraph, issue_type)
            
            return jsonify({
                'success': True,
                'improved_paragraph': result
            })
        
        else:
            # Full content improvement (default)
            result = improver.generate_fixes(text, analysis)
            return jsonify(result)
            
    except Exception as e:
        import traceback
        print("Error in improve_content:", traceback.format_exc())
        return jsonify({"error": str(e), "success": False}), 500

@app.route('/api/subtopics', methods=['POST'])
def suggest_subtopics():
    """Suggest missing subtopics"""
    try:
        data = request.json
        keyword = data.get('keyword', '')
        serp_data = data.get('serp_data', {})
        
        if not keyword:
            return jsonify({"error": "No keyword provided"}), 400
        
        improver = AIContentImprover()
        subtopics = improver.suggest_subtopics(keyword, serp_data)
        
        return jsonify({
            'success': True,
            'subtopics': subtopics
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def _get_top_recommendations(all_results):
    """Extract top 5 recommendations across all analyzers"""
    all_recommendations = []
    
    for result in all_results:
        if 'recommendations' in result:
            all_recommendations.extend(result['recommendations'][:2])
    
    # Return top 5 unique recommendations
    unique_recs = []
    for rec in all_recommendations:
        if rec not in unique_recs:
            unique_recs.append(rec)
    
    return unique_recs[:5]

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Content Quality Audit Tool - Backend Starting")
    print("="*50)
    print("\nAPI will be available at: http://localhost:5000")
    print("\nEndpoints:")
    print("  POST /api/analyze - Analyze content")
    print("  POST /api/improve - AI-powered improvements")
    print("  POST /api/subtopics - Suggest missing topics")
    print("\n" + "="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
