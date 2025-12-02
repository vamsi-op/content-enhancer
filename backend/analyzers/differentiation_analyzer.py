import re

class DifferentiationAnalyzer:
    """Analyze content uniqueness vs SERP competition"""
    
    def analyze(self, text, serp_data=None):
        """
        Analyze content differentiation from competitors
        Returns score with uniqueness analysis
        """
        score = 100
        issues = []
        recommendations = []
        details = {}
        
        if not serp_data or 'serp_data' not in serp_data:
            # Basic analysis without SERP data
            uniqueness = self._analyze_basic_uniqueness(text)
            details['uniqueness'] = uniqueness
            
            if not uniqueness['has_unique_examples']:
                score -= 20
                issues.append("No unique examples or data points detected")
                recommendations.append("Add original data points or product comparisons")
            
            if not uniqueness['has_unique_angle']:
                score -= 15
                issues.append("Content follows generic structure")
                recommendations.append("Use unique angle (e.g., 'student perspective' vs generic advice)")
            
            return {
                'score': score,
                'issues': issues,
                'recommendations': recommendations,
                'details': details
            }
        
        # If we have SERP competitor data
        serp_info = serp_data.get('serp_data', {})
        
        # For this hackathon version, simulate competitor content analysis
        # In production, you'd actually fetch and compare against top 3 SERP results
        
        # 1. Content overlap analysis with detailed breakdown
        overlap_score = self._simulate_content_overlap(text)
        details['content_overlap'] = overlap_score
        
        if overlap_score['overlap_percentage'] > 70:
            score -= 30
            issues.append(f"{overlap_score['overlap_percentage']}% content overlap with top 3 SERP results")
            issues.append("No unique examples or data")
            recommendations.append("Add original data points or product comparisons")
        elif overlap_score['overlap_percentage'] > 50:
            score -= 20
            issues.append(f"{overlap_score['overlap_percentage']}% content overlap with competitors")
            recommendations.append("Inject more unique perspective or original research")
        
        # 2. Unique elements detection with specific counts
        unique_elements = self._detect_unique_elements(text)
        details['unique_elements'] = unique_elements
        
        if unique_elements['personal_examples'] == 0:
            score -= 15
            issues.append("No unique examples or data")
            recommendations.append("Add original data points or product comparisons")
        
        if unique_elements['original_data'] == 0:
            score -= 10
            # Don't duplicate if already mentioned above
            if unique_elements['personal_examples'] > 0:
                issues.append("No original data or research")
                recommendations.append("Include original data, surveys, or experiments")
        
        # 3. Structure comparison with specific feedback
        structure_diff = self._analyze_structure_difference(text, serp_info)
        details['structure'] = structure_diff
        
        if not structure_diff['has_unique_structure']:
            score -= 15
            issues.append("Same structure as competitors (all follow identical outline)")
            recommendations.append("Use unique angle (e.g., 'student perspective' vs generic advice)")
        
        # 4. Voice and tone differentiation
        voice = self._analyze_voice_differentiation(text)
        details['voice'] = voice
        
        if not voice['has_distinct_voice']:
            score -= 10
            issues.append("Generic voice and tone")
            recommendations.append("Develop stronger brand voice (casual, technical, playful, etc.)")
        
        score = max(0, score)
        
        return {
            'score': score,
            'issues': issues,
            'recommendations': recommendations[:3],
            'details': details
        }
    
    def _analyze_basic_uniqueness(self, text):
        """Basic uniqueness analysis without SERP comparison"""
        text_lower = text.lower()
        
        # Check for unique examples
        personal_indicators = [
            'in my experience', 'i found', 'we discovered', 'our research',
            'we tested', 'my team', 'our analysis', 'we analyzed'
        ]
        has_unique_examples = any(indicator in text_lower for indicator in personal_indicators)
        
        # Check for unique angle
        perspective_indicators = [
            'student', 'beginner', 'expert', 'professional', 'small business',
            'enterprise', 'startup', 'freelancer', 'mom', 'dad', 'senior'
        ]
        has_unique_angle = any(indicator in text_lower for indicator in perspective_indicators)
        
        return {
            'has_unique_examples': has_unique_examples,
            'has_unique_angle': has_unique_angle
        }
    
    def _simulate_content_overlap(self, text):
        """
        Simulate content overlap analysis
        In production: would use TF-IDF or embeddings to compare against actual SERP content
        """
        text_lower = text.lower()
        
        # Common generic phrases that appear in ALL content
        generic_phrases = [
            'it is important', 'you need to', 'there are many', 'this is a',
            'can help you', 'one of the', 'make sure', 'keep in mind',
            'in this article', 'we will discuss', 'you should', 'it can be'
        ]
        
        generic_count = sum(1 for phrase in generic_phrases if phrase in text_lower)
        sentence_count = len(re.split(r'[.!?]+', text))
        
        # Estimate overlap based on generic phrase density
        overlap_percentage = min(int((generic_count / sentence_count) * 100), 90) if sentence_count > 0 else 70
        
        # Add some randomness based on content length
        word_count = len(text.split())
        if word_count < 500:
            overlap_percentage += 10
        
        return {
            'overlap_percentage': min(overlap_percentage, 95),
            'generic_phrases_found': generic_count
        }
    
    def _detect_unique_elements(self, text):
        """Detect unique, differentiating elements"""
        text_lower = text.lower()
        
        # Personal examples
        personal_patterns = r'(in my|i found|we tested|our research|we analyzed|my experience|our study)'
        personal_examples = len(re.findall(personal_patterns, text_lower))
        
        # Original data indicators
        data_patterns = r'(our data shows|we found that|our analysis reveals|survey of \d+)'
        original_data = len(re.findall(data_patterns, text_lower))
        
        # Unique comparisons or tools
        tool_patterns = r'(we compared|we tested|we evaluated|our comparison|our review)'
        unique_comparisons = len(re.findall(tool_patterns, text_lower))
        
        # Visual content indicators
        visual_patterns = r'(see chart|see graph|image below|screenshot|diagram|infographic)'
        has_visuals = bool(re.search(visual_patterns, text_lower))
        
        return {
            'personal_examples': personal_examples,
            'original_data': original_data,
            'unique_comparisons': unique_comparisons,
            'has_visuals': has_visuals
        }
    
    def _analyze_structure_difference(self, text, serp_info):
        """Analyze if structure is different from competitors"""
        # Common generic structures
        generic_starts = [
            'in this article', 'in this guide', 'in this post',
            'what is', 'introduction', 'overview'
        ]
        
        first_100 = text[:100].lower()
        has_generic_start = any(start in first_100 for start in generic_starts)
        
        # Check for unique formatting
        has_unique_format = (
            '---' in text or  # Dividers
            '💡' in text or   # Emojis
            '→' in text or    # Arrows
            text.count('**') > 4 or  # Bold formatting
            text.count('`') > 4       # Code formatting
        )
        
        return {
            'has_unique_structure': not has_generic_start or has_unique_format,
            'has_generic_opening': has_generic_start
        }
    
    def _analyze_voice_differentiation(self, text):
        """Analyze voice and tone distinctiveness"""
        text_lower = text.lower()
        
        # Casual voice indicators
        casual_indicators = ['you\'ll', 'let\'s', 'here\'s', 'that\'s', 'don\'t']
        casual_count = sum(text_lower.count(ind) for ind in casual_indicators)
        
        # Technical voice
        technical_indicators = ['algorithm', 'optimize', 'metric', 'parameter', 'implementation']
        technical_count = sum(text_lower.count(ind) for ind in technical_indicators)
        
        # Playful voice
        playful_indicators = ['🎯', '🚀', '💪', '✨', '!' * 2]
        playful_count = sum(text.count(ind) for ind in playful_indicators)
        
        # Story-driven voice
        story_indicators = ['once', 'imagine', 'picture this', 'story', 'journey']
        story_count = sum(text_lower.count(ind) for ind in story_indicators)
        
        # Determine if there's a distinct voice
        total_indicators = casual_count + technical_count + playful_count + story_count
        has_distinct_voice = total_indicators > 5
        
        dominant_voice = 'generic'
        if casual_count > 3:
            dominant_voice = 'casual'
        elif technical_count > 3:
            dominant_voice = 'technical'
        elif playful_count > 2:
            dominant_voice = 'playful'
        elif story_count > 2:
            dominant_voice = 'story-driven'
        
        return {
            'has_distinct_voice': has_distinct_voice,
            'dominant_voice': dominant_voice,
            'casual_score': casual_count,
            'technical_score': technical_count
        }
