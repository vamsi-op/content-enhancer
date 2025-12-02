import re
import textstat
import math
from collections import Counter

class SEOAnalyzer:
    """Analyze content for SEO optimization"""
    
    def analyze(self, text, headers=None, meta_description="", target_keyword=""):
        """
        Analyze SEO factors
        Returns score (0-100) with issues and recommendations
        """
        score = 100
        issues = []
        recommendations = []
        details = {}
        
        # 0. Content Metrics
        word_count = len(text.split())
        reading_time = math.ceil(word_count / 200)  # 200 words per minute
        details['content_metrics'] = {
            'word_count': word_count,
            'reading_time_minutes': reading_time,
            'character_count': len(text),
            'paragraph_count': len([p for p in text.split('\n\n') if p.strip()])
        }
        
        # Word count assessment
        if word_count < 300:
            score -= 20
            issues.append(f"Content is too short ({word_count} words). Aim for 800-2000 words")
            recommendations.append("Expand content with more details, examples, and value")
        elif word_count < 600:
            score -= 10
            issues.append(f"Content is short ({word_count} words). Consider adding more depth")
            recommendations.append("Add more comprehensive information (aim for 1000+ words)")
        elif word_count > 3000:
            issues.append(f"Very long content ({word_count} words) - ensure it stays engaging")
            recommendations.append("Consider breaking into multiple articles or adding clear navigation")
        
        # 1. Keyword Density Analysis (if target keyword provided)
        if target_keyword:
            keyword_data = self._analyze_keyword_density(text, target_keyword)
            details['keyword_density'] = keyword_data
            
            if keyword_data['density'] < 0.5:
                score -= 15
                issues.append(f"Keyword \"{target_keyword}\" appears only {keyword_data['count']} times ({keyword_data['density']:.1f}% density)")
                recommendations.append(f"Increase keyword to 5-7 mentions (1.5% density)")
            elif keyword_data['density'] > 3:
                score -= 10
                issues.append(f"Keyword density too high: {keyword_data['density']:.1f}% - may look spammy")
                recommendations.append("Reduce keyword usage to maintain natural flow (aim for 1-2% density)")
            else:
                details['good_points'] = details.get('good_points', [])
                details['good_points'].append(f"Good keyword density: {keyword_data['density']:.1f}%")
        
        # 2. Readability Analysis
        readability = self._analyze_readability(text)
        details['readability'] = readability
        
        if readability['flesch_reading_ease'] < 30:
            score -= 15
            issues.append(f"Content is very difficult to read (Flesch score: {readability['flesch_reading_ease']:.1f})")
            recommendations.append("Simplify sentences and use shorter words to improve readability")
        elif readability['flesch_reading_ease'] < 50:
            score -= 8
            issues.append(f"Content is somewhat difficult to read (Flesch score: {readability['flesch_reading_ease']:.1f})")
            recommendations.append("Consider breaking complex sentences into simpler ones")
        else:
            details['good_points'] = details.get('good_points', [])
            details['good_points'].append(f"Good readability (Flesch score: {readability['flesch_reading_ease']:.1f})")
        
        # 3. Header Structure Analysis
        if headers:
            header_analysis = self._analyze_headers(headers, target_keyword)
            details['headers'] = header_analysis
            
            if not header_analysis['has_h1']:
                score -= 20
                issues.append("No H1 header found")
                recommendations.append("Add a clear H1 header as the main title")
            
            if not header_analysis['has_hierarchy']:
                score -= 10
                issues.append("Header hierarchy is incomplete (missing H2 or H3)")
                recommendations.append("Use proper header hierarchy: H1 → H2 → H3")
            else:
                details['good_points'] = details.get('good_points', [])
                details['good_points'].append("Header structure present (H1, H2, H3)")
            
            if target_keyword and not header_analysis['keyword_in_headers']:
                score -= 10
                issues.append(f"Target keyword '{target_keyword}' not found in any headers")
                recommendations.append(f"Include '{target_keyword}' in at least one header")
        else:
            score -= 15
            issues.append("No header structure detected")
            recommendations.append("Add clear headers (H1, H2, H3) to organize content")
        
        # 4. Meta Description
        if not meta_description:
            score -= 15
            issues.append("No meta description detected")
            recommendations.append("Add meta description (150-160 characters)")
        elif len(meta_description) < 120:
            score -= 8
            issues.append(f"Meta description too short: {len(meta_description)} characters")
            recommendations.append("Expand meta description to 150-160 characters")
        elif len(meta_description) > 160:
            score -= 5
            issues.append(f"Meta description too long: {len(meta_description)} characters")
            recommendations.append("Shorten meta description to 150-160 characters")
        else:
            details['good_points'] = details.get('good_points', [])
            details['good_points'].append(f"Good meta description length: {len(meta_description)} characters")
        
        # 5. Content Length
        word_count = len(text.split())
        details['word_count'] = word_count
        
        if word_count < 300:
            score -= 20
            issues.append(f"Content too short: {word_count} words")
            recommendations.append("Expand content to at least 1,000 words for better SEO")
        elif word_count < 800:
            score -= 10
            issues.append(f"Content length moderate: {word_count} words")
            recommendations.append("Consider expanding to 1,500-2,500 words for competitive keywords")
        
        # Ensure score doesn't go below 0
        score = max(0, score)
        
        return {
            'score': score,
            'issues': issues,
            'recommendations': recommendations[:3],  # Top 3
            'details': details
        }
    
    def _analyze_keyword_density(self, text, keyword):
        """Calculate keyword density"""
        text_lower = text.lower()
        keyword_lower = keyword.lower()
        
        # Count occurrences
        count = text_lower.count(keyword_lower)
        
        # Calculate density
        total_words = len(text.split())
        keyword_words = len(keyword.split())
        
        # Density as percentage
        if total_words > 0:
            density = (count * keyword_words / total_words) * 100
        else:
            density = 0
        
        return {
            'count': count,
            'density': density,
            'total_words': total_words
        }
    
    def _analyze_readability(self, text):
        """Analyze readability scores"""
        try:
            flesch = textstat.flesch_reading_ease(text)
            fk_grade = textstat.flesch_kincaid_grade(text)
            
            return {
                'flesch_reading_ease': flesch,
                'flesch_kincaid_grade': fk_grade,
                'reading_level': self._get_reading_level(flesch)
            }
        except:
            return {
                'flesch_reading_ease': 0,
                'flesch_kincaid_grade': 0,
                'reading_level': 'Unknown'
            }
    
    def _get_reading_level(self, flesch_score):
        """Convert Flesch score to reading level"""
        if flesch_score >= 90:
            return "Very Easy (5th grade)"
        elif flesch_score >= 80:
            return "Easy (6th grade)"
        elif flesch_score >= 70:
            return "Fairly Easy (7th grade)"
        elif flesch_score >= 60:
            return "Standard (8th-9th grade)"
        elif flesch_score >= 50:
            return "Fairly Difficult (10th-12th grade)"
        elif flesch_score >= 30:
            return "Difficult (College)"
        else:
            return "Very Difficult (College graduate)"
    
    def _analyze_headers(self, headers, target_keyword=""):
        """Analyze header structure"""
        # Safety check: ensure headers is a list
        if not isinstance(headers, list):
            headers = []
        
        # Normalize headers to dict format if they're strings
        normalized_headers = []
        for h in headers:
            if isinstance(h, dict) and 'level' in h and 'text' in h:
                normalized_headers.append(h)
            elif isinstance(h, str):
                # If it's a string, skip it (shouldn't happen but be defensive)
                continue
        
        has_h1 = any(h['level'] == 'h1' for h in normalized_headers)
        has_h2 = any(h['level'] == 'h2' for h in normalized_headers)
        has_h3 = any(h['level'] == 'h3' for h in normalized_headers)
        
        keyword_in_headers = False
        if target_keyword:
            keyword_lower = target_keyword.lower()
            keyword_in_headers = any(keyword_lower in h['text'].lower() for h in normalized_headers)
        
        return {
            'has_h1': has_h1,
            'has_h2': has_h2,
            'has_h3': has_h3,
            'has_hierarchy': has_h1 and has_h2,
            'total_headers': len(normalized_headers),
            'keyword_in_headers': keyword_in_headers
        }
