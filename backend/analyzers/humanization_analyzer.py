import re
from collections import Counter
import math

class HumanizationAnalyzer:
    """Analyze how human vs AI-generated the content sounds"""
    
    def analyze(self, text):
        """
        Analyze humanization factors
        Returns score with heatmap data for AI patterns
        """
        score = 100
        issues = []
        recommendations = []
        details = {}
        
        sentences = self._split_sentences(text)
        
        if len(sentences) < 3:
            return {
                'score': 50,
                'issues': ['Content too short for humanization analysis'],
                'recommendations': ['Add more content'],
                'details': {}
            }
        
        # 1. Sentence Starter Variety with example patterns
        starters = self._analyze_sentence_starters(sentences)
        details['sentence_starters'] = starters
        
        if starters['repetition_rate'] > 40:
            score -= 20
            common_pattern = starters.get('most_common', 'same way')
            issues.append(f"{starters['repetition_rate']}% sentences start same way (\"{common_pattern}\"...)")
            recommendations.append("Vary sentence starters and lengths")
        elif starters['repetition_rate'] > 25:
            score -= 10
            issues.append(f"{starters['repetition_rate']}% sentences have repetitive starts")
            recommendations.append("Mix up sentence beginnings more")
        
        # 2. Sentence Length Variation with detailed metrics
        length_analysis = self._analyze_sentence_lengths(sentences)
        details['sentence_lengths'] = length_analysis
        
        if length_analysis['std_dev'] < 3:
            score -= 20
            issues.append(f"Low sentence length variation (avg {length_analysis['avg']:.0f} words, std dev {length_analysis['std_dev']:.1f})")
            recommendations.append("Vary sentence lengths - mix short punchy sentences with longer detailed ones")
        elif length_analysis['std_dev'] < 5:
            score -= 10
            issues.append(f"Moderate sentence length variation (avg {length_analysis['avg']:.0f} words, std dev {length_analysis['std_dev']:.1f})")
        
        # 3. AI Pattern Detection
        ai_patterns = self._detect_ai_patterns(text, sentences)
        details['ai_patterns'] = ai_patterns
        
        if ai_patterns['ai_score'] > 60:
            score -= 25
            issues.append(f"High AI pattern score: {ai_patterns['ai_score']}%")
            issues.append(f"Detected: {', '.join(ai_patterns['detected_patterns'])}")
            recommendations.append("Rewrite to sound more conversational and less formulaic")
        elif ai_patterns['ai_score'] > 40:
            score -= 15
            issues.append(f"Moderate AI patterns detected: {ai_patterns['ai_score']}%")
        
        # 4. Transition Word Overuse
        transitions = self._analyze_transitions(text)
        details['transitions'] = transitions
        
        if transitions['overuse_rate'] > 30:
            score -= 10
            issues.append("Overuse of transition words (very AI-like)")
            recommendations.append("Reduce formulaic transitions like 'moreover', 'furthermore', 'additionally'")
        
        # 5. Natural Flow Indicators
        flow = self._analyze_natural_flow(text, sentences)
        details['natural_flow'] = flow
        
        if not flow['has_contractions']:
            score -= 10
            issues.append("No contractions used (sounds stiff)")
            recommendations.append("Use contractions (don't, can't, it's) for natural tone")
        
        if not flow['has_questions']:
            score -= 5
            issues.append("No questions to engage reader")
            recommendations.append("Add rhetorical questions to engage readers")
        
        # 6. Generate Heatmap Data
        heatmap = self._generate_heatmap(text, sentences, ai_patterns)
        details['heatmap'] = heatmap
        
        score = max(0, score)
        
        return {
            'score': score,
            'issues': issues,
            'recommendations': recommendations[:3],
            'details': details
        }
    
    def _split_sentences(self, text):
        """Split text into sentences"""
        # Simple sentence splitter
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    def _analyze_sentence_starters(self, sentences):
        """Analyze how sentences start"""
        starters = []
        
        for sentence in sentences:
            # Get first 1-2 words
            words = sentence.split()
            if len(words) > 0:
                starter = words[0].lower()
                starters.append(starter)
        
        # Count repetitions
        starter_counts = Counter(starters)
        most_common = starter_counts.most_common(3)
        
        # Calculate repetition rate
        total = len(starters)
        top_repetitions = sum(count for _, count in most_common[:1])
        repetition_rate = int((top_repetitions / total) * 100) if total > 0 else 0
        
        # Get the actual most common starter word for reporting
        most_common_word = most_common[0][0] if most_common else 'same way'
        
        return {
            'total_sentences': total,
            'unique_starters': len(set(starters)),
            'repetition_rate': repetition_rate,
            'most_common': most_common_word,
            'top_starters': most_common
        }
    
    def _analyze_sentence_lengths(self, sentences):
        """Analyze sentence length variation"""
        lengths = [len(s.split()) for s in sentences]
        
        avg_length = sum(lengths) / len(lengths) if lengths else 0
        
        # Calculate standard deviation
        if len(lengths) > 1:
            variance = sum((x - avg_length) ** 2 for x in lengths) / len(lengths)
            std_dev = math.sqrt(variance)
        else:
            std_dev = 0
        
        return {
            'avg': round(avg_length, 1),
            'avg_length': round(avg_length, 1),
            'std_dev': round(std_dev, 1),
            'min_length': min(lengths) if lengths else 0,
            'max_length': max(lengths) if lengths else 0
        }
    
    def _detect_ai_patterns(self, text, sentences):
        """Detect AI-specific writing patterns"""
        text_lower = text.lower()
        ai_score = 0
        detected = []
        
        # Pattern 1: Overuse of "delve"
        if 'delve' in text_lower:
            ai_score += 15
            detected.append("uses 'delve' (rare in human writing)")
        
        # Pattern 2: Formulaic phrases
        formulaic_phrases = [
            'it is important to note',
            'it is worth noting',
            'in today\'s world',
            'in today\'s digital age',
            'in conclusion',
            'to sum up',
            'as we\'ve seen'
        ]
        
        formulaic_count = sum(1 for phrase in formulaic_phrases if phrase in text_lower)
        if formulaic_count > 2:
            ai_score += 20
            detected.append(f"{formulaic_count} formulaic phrases")
        
        # Pattern 3: Excessive use of adverbs
        adverb_pattern = r'\b(very|really|quite|extremely|incredibly|absolutely|definitely)\b'
        adverb_count = len(re.findall(adverb_pattern, text_lower))
        word_count = len(text.split())
        adverb_rate = (adverb_count / word_count) * 100 if word_count > 0 else 0
        
        if adverb_rate > 2:
            ai_score += 15
            detected.append("excessive adverbs")
        
        # Pattern 4: Perfect grammar (too perfect)
        # AI rarely makes grammar mistakes
        has_fragments = bool(re.search(r'\b(but|and|so)\s+[A-Z]', text))
        has_informal = bool(re.search(r'\b(gonna|wanna|gotta|yeah|nah)\b', text_lower))
        
        if not has_fragments and not has_informal and len(sentences) > 10:
            ai_score += 10
            detected.append("overly perfect grammar")
        
        # Pattern 5: Uniform sentence structure
        sentence_patterns = []
        for s in sentences[:10]:  # Check first 10
            words = s.split()
            if len(words) > 0:
                # Simple pattern: first word + sentence length category
                pattern = f"{words[0].lower()}_{len(words)//5}"
                sentence_patterns.append(pattern)
        
        unique_patterns = len(set(sentence_patterns))
        if unique_patterns < len(sentence_patterns) * 0.6:
            ai_score += 15
            detected.append("repetitive sentence structure")
        
        return {
            'ai_score': min(ai_score, 100),
            'detected_patterns': detected if detected else ['none detected']
        }
    
    def _analyze_transitions(self, text):
        """Analyze transition word usage"""
        text_lower = text.lower()
        
        # AI loves these transitions
        ai_transitions = [
            'moreover', 'furthermore', 'additionally', 'consequently',
            'nevertheless', 'nonetheless', 'thus', 'hence', 'therefore'
        ]
        
        transition_count = sum(text_lower.count(word) for word in ai_transitions)
        sentence_count = len(self._split_sentences(text))
        
        overuse_rate = int((transition_count / sentence_count) * 100) if sentence_count > 0 else 0
        
        return {
            'transition_count': transition_count,
            'overuse_rate': overuse_rate
        }
    
    def _analyze_natural_flow(self, text, sentences):
        """Analyze natural, conversational indicators"""
        text_lower = text.lower()
        
        # Look for contractions (human indicator)
        contractions = ['don\'t', 'can\'t', 'won\'t', 'isn\'t', 'aren\'t', 
                       'hasn\'t', 'haven\'t', 'it\'s', 'that\'s', 'what\'s']
        has_contractions = any(c in text_lower for c in contractions)
        
        # Look for questions
        has_questions = '?' in text
        question_count = text.count('?')
        
        # Look for first-person
        has_first_person = bool(re.search(r'\b(i|we|my|our|me|us)\b', text_lower))
        
        return {
            'has_contractions': has_contractions,
            'has_questions': has_questions,
            'question_count': question_count,
            'has_first_person': has_first_person
        }
    
    def _generate_heatmap(self, text, sentences, ai_patterns):
        """Generate heatmap data for highlighting AI patterns"""
        # Return sentence-level scores for frontend highlighting
        sentence_scores = []
        
        for i, sentence in enumerate(sentences):
            score = 0  # 0 = human, 100 = AI
            
            sentence_lower = sentence.lower()
            
            # Check for AI indicators
            if 'delve' in sentence_lower:
                score += 30
            
            if any(phrase in sentence_lower for phrase in [
                'it is important to note', 'it is worth noting', 'in today\'s',
                'as we\'ve seen', 'to sum up'
            ]):
                score += 25
            
            if re.search(r'\b(moreover|furthermore|additionally|consequently|nevertheless)\b', sentence_lower):
                score += 20
            
            # Check sentence length uniformity
            word_count = len(sentence.split())
            if 15 <= word_count <= 20:  # AI loves this range
                score += 10
            
            sentence_scores.append({
                'sentence': sentence[:100] + '...' if len(sentence) > 100 else sentence,
                'score': min(score, 100),
                'index': i
            })
        
        return sentence_scores
