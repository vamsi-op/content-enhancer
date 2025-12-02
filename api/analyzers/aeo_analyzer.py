import re

class AEOAnalyzer:
    """Analyze Answer Engine Optimization - how AI-friendly is the content"""
    
    def analyze(self, text, headers=None):
        """
        Analyze AEO factors for AI discoverability
        Returns score with issues and recommendations
        """
        score = 100
        issues = []
        recommendations = []
        details = {}
        
        # 1. Citation/Source Analysis
        citations = self._detect_citations(text)
        details['citations'] = citations
        
        if citations['count'] == 0:
            score -= 25
            issues.append("No citations or sources found")
            recommendations.append("Add 3-5 authoritative sources with links")
        elif citations['count'] < 3:
            score -= 15
            issues.append(f"Only {citations['count']} citation(s) found")
            recommendations.append("Add more authoritative sources (aim for 3-5)")
        else:
            details['good_points'] = [f"{citations['count']} citations with sources"]
        
        # 2. Structured Data / Formatting
        structured = self._analyze_structured_content(text, headers)
        details['structured_content'] = structured
        
        if not structured['has_faq_pattern']:
            score -= 15
            issues.append("No FAQ section detected")
            recommendations.append("Add FAQ section with schema markup (great for featured snippets)")
        
        if not structured['has_lists']:
            score -= 10
            issues.append("No bulleted or numbered lists found")
            recommendations.append("Use lists for better scannability and AI parsing")
        
        if not structured['has_how_to_pattern']:
            score -= 10
            issues.append("No step-by-step instructions detected")
            recommendations.append("Add clear step-by-step format (enhances AI understanding)")
        
        # 3. AI-Friendly Patterns
        ai_patterns = self._analyze_ai_patterns(text)
        details['ai_patterns'] = ai_patterns
        
        if ai_patterns['definition_count'] < 2:
            score -= 10
            issues.append("Few clear definitions found")
            recommendations.append("Define key terms clearly (helps AI understand context)")
        
        if not ai_patterns['has_summary']:
            score -= 10
            issues.append("No summary or conclusion section")
            recommendations.append("Add a clear summary or key takeaways section")
        
        # 4. Answer-Style Content
        answer_style = self._analyze_answer_style(text)
        details['answer_style'] = answer_style
        
        if answer_style['direct_answers'] < 3:
            score -= 10
            issues.append("Content lacks direct, quotable answers")
            recommendations.append("Include direct answers to common questions")
        
        score = max(0, score)
        
        return {
            'score': score,
            'issues': issues,
            'recommendations': recommendations[:3],
            'details': details
        }
    
    def _detect_citations(self, text):
        """Detect citations and sources in content"""
        # Look for citation patterns
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        source_keywords = r'(according to|source:|via|study by|research by|data from|reported by)'
        
        urls = re.findall(url_pattern, text)
        source_mentions = len(re.findall(source_keywords, text, re.IGNORECASE))
        
        return {
            'count': len(urls) + source_mentions,
            'urls': len(urls),
            'source_mentions': source_mentions
        }
    
    def _analyze_structured_content(self, text, headers):
        """Analyze structured content elements"""
        text_lower = text.lower()
        
        # Check for FAQ pattern
        faq_pattern = r'(frequently asked questions|faq|q:|question:|q\d+:)'
        has_faq = bool(re.search(faq_pattern, text_lower))
        
        # Check for lists
        has_lists = (text.count('•') > 2 or 
                    text.count('\n- ') > 2 or 
                    text.count('\n1.') > 1 or
                    text.count('\n2.') > 1)
        
        # Check for how-to/step pattern
        how_to_pattern = r'(step \d+|first,|second,|third,|finally,|\d+\.\s+\w+)'
        has_how_to = bool(re.search(how_to_pattern, text_lower))
        
        return {
            'has_faq_pattern': has_faq,
            'has_lists': has_lists,
            'has_how_to_pattern': has_how_to
        }
    
    def _analyze_ai_patterns(self, text):
        """Analyze AI-friendly content patterns"""
        text_lower = text.lower()
        
        # Look for definitions
        definition_patterns = r'(is defined as|refers to|means that|is a|are \w+ that)'
        definition_count = len(re.findall(definition_patterns, text_lower))
        
        # Look for summary/conclusion
        summary_pattern = r'(in summary|in conclusion|to summarize|key takeaways|bottom line)'
        has_summary = bool(re.search(summary_pattern, text_lower))
        
        # Look for comparisons (good for AI)
        comparison_pattern = r'(compared to|versus|vs\.|difference between|similar to)'
        has_comparisons = bool(re.search(comparison_pattern, text_lower))
        
        return {
            'definition_count': definition_count,
            'has_summary': has_summary,
            'has_comparisons': has_comparisons
        }
    
    def _analyze_answer_style(self, text):
        """Analyze if content provides direct, quotable answers"""
        sentences = re.split(r'[.!?]+', text)
        
        # Look for direct answer patterns
        direct_patterns = [
            r'^(yes|no),',
            r'^the (best|main|primary|key)',
            r'^\w+ (is|are|can|will|should)',
            r'^you (can|should|need|must)'
        ]
        
        direct_answers = 0
        for sentence in sentences:
            sentence_clean = sentence.strip().lower()
            if len(sentence_clean) < 10:
                continue
            for pattern in direct_patterns:
                if re.match(pattern, sentence_clean):
                    direct_answers += 1
                    break
        
        return {
            'direct_answers': direct_answers,
            'total_sentences': len([s for s in sentences if len(s.strip()) > 10])
        }
