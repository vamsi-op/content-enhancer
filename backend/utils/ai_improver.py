import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AIContentImprover:
    """Use OpenAI to generate content improvements"""
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        try:
            self.client = OpenAI(api_key=api_key) if api_key else None
        except TypeError as e:
            # Handle version incompatibility
            print(f"OpenAI client initialization error: {e}")
            print("Try: pip install --upgrade openai")
            self.client = None
    
    def generate_fixes(self, text, analysis_results):
        """
        Generate AI-powered content improvements
        Returns rewritten/improved content
        """
        if not self.client:
            return {
                'success': False,
                'error': 'OpenAI API key not configured'
            }
        
        try:
            # Build improvement prompt from analysis
            prompt = self._build_improvement_prompt(text, analysis_results)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert SEO and content strategist. Improve content based on specific feedback."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            improved_content = response.choices[0].message.content
            
            return {
                'success': True,
                'improved_content': improved_content,
                'changes_made': self._summarize_changes(analysis_results)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def fix_meta_description(self, title, text, target_keyword=""):
        """Generate optimized meta description"""
        if not self.client:
            return None
        
        try:
            prompt = f"""Write a compelling meta description (150-160 characters) for this content:

Title: {title}
Target Keyword: {target_keyword}
Content Preview: {text[:500]}

Requirements:
- Exactly 150-160 characters
- Include target keyword naturally
- Compelling and click-worthy
- Accurate summary of content"""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip('"')
            
        except:
            return None
    
    def suggest_subtopics(self, keyword, serp_data):
        """Suggest missing subtopics based on SERP analysis"""
        if not self.client:
            return []
        
        try:
            competitor_info = ""
            if serp_data and 'patterns' in serp_data:
                competitor_info = f"""
Competitor patterns:
- {serp_data['patterns'].get('has_stats', 0)}% include statistics
- {serp_data['patterns'].get('has_examples', 0)}% use case studies
- {serp_data['patterns'].get('has_comparisons', 0)}% have comparisons
"""
            
            prompt = f"""For the keyword "{keyword}", suggest 5-7 subtopics that top-ranking content should cover.

{competitor_info}

Return as a numbered list of subtopics, each 3-6 words."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200
            )
            
            subtopics = response.choices[0].message.content.strip().split('\n')
            return [s.strip() for s in subtopics if s.strip()]
            
        except:
            return []
    
    def rewrite_paragraph(self, paragraph, issue_type):
        """Rewrite a specific paragraph to fix issues"""
        if not self.client:
            return paragraph
        
        try:
            instructions = {
                'humanization': 'Make this sound more natural and conversational. Vary sentence structure and length. Remove AI-like patterns.',
                'readability': 'Simplify this paragraph. Use shorter sentences and simpler words. Improve readability.',
                'keyword': 'Rewrite this to naturally include the target keyword 2-3 times without keyword stuffing.',
                'engagement': 'Make this more engaging. Add a question or hook. Make it more compelling.'
            }
            
            instruction = instructions.get(issue_type, 'Improve this paragraph')
            
            prompt = f"""{instruction}

Original: {paragraph}

Rewritten (same meaning, improved style):"""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except:
            return paragraph
    
    def _build_improvement_prompt(self, text, analysis):
        """Build comprehensive improvement prompt"""
        issues = []
        
        # Collect top issues from all analyzers
        if 'seo' in analysis and analysis['seo'].get('issues'):
            issues.extend([f"SEO: {issue}" for issue in analysis['seo']['issues'][:2]])
        
        if 'humanization' in analysis and analysis['humanization'].get('issues'):
            issues.extend([f"Humanization: {issue}" for issue in analysis['humanization']['issues'][:2]])
        
        if 'differentiation' in analysis and analysis['differentiation'].get('issues'):
            issues.extend([f"Uniqueness: {issue}" for issue in analysis['differentiation']['issues'][:1]])
        
        prompt = f"""Improve this content based on these specific issues:

{chr(10).join(f'- {issue}' for issue in issues[:5])}

Original Content:
{text[:1500]}

Please rewrite focusing on fixing these issues while maintaining the core message. Make it more engaging, SEO-friendly, and unique."""

        return prompt
    
    def _summarize_changes(self, analysis):
        """Summarize what changes were made"""
        changes = []
        
        if 'seo' in analysis and analysis['seo']['score'] < 75:
            changes.append("Improved keyword usage and readability")
        
        if 'humanization' in analysis and analysis['humanization']['score'] < 70:
            changes.append("Made content sound more natural and conversational")
        
        if 'differentiation' in analysis and analysis['differentiation']['score'] < 70:
            changes.append("Added unique perspective and examples")
        
        return changes if changes else ["General content improvements"]

    def rewrite_for_seo(self, text, target_keyword, analysis):
        """SEO-focused content rewrite"""
        if not self.client:
            return {'success': False, 'error': 'OpenAI API key not configured'}
        
        try:
            prompt = f"""Rewrite this content to be SEO-optimized for the keyword: "{target_keyword}"

Requirements:
- Include the target keyword naturally 3-5 times
- Use semantic keywords and related terms
- Improve heading structure with keywords
- Add relevant examples and data
- Maintain readability and natural flow

Original Content:
{text[:2000]}

SEO-Optimized Version:"""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert SEO content writer. Optimize content for search engines while keeping it natural and engaging."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2500
            )
            
            improved = response.choices[0].message.content
            
            return {
                'success': True,
                'improved_content': improved,
                'changes_made': [
                    f'Optimized for target keyword: {target_keyword}',
                    'Improved keyword density and placement',
                    'Enhanced heading structure',
                    'Added semantic keywords'
                ]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def humanize_content(self, text):
        """Make content sound more human and natural"""
        if not self.client:
            return {'success': False, 'error': 'OpenAI API key not configured'}
        
        try:
            prompt = f"""Rewrite this content to sound more human, natural, and conversational.

Requirements:
- Vary sentence structure and length
- Use contractions naturally (e.g., "you're" instead of "you are")
- Add personality and warmth
- Remove robotic or AI-like patterns
- Include transitional phrases
- Make it engaging and relatable

Original Content:
{text[:2000]}

Humanized Version:"""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert content writer who excels at making text sound natural and human. Avoid AI-like patterns."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=2500
            )
            
            improved = response.choices[0].message.content
            
            return {
                'success': True,
                'improved_content': improved,
                'changes_made': [
                    'Added natural conversational tone',
                    'Varied sentence structure',
                    'Removed AI-like patterns',
                    'Increased readability and warmth'
                ]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def improve_readability(self, text):
        """Simplify content for better readability"""
        if not self.client:
            return {'success': False, 'error': 'OpenAI API key not configured'}
        
        try:
            prompt = f"""Rewrite this content to be easier to read and understand.

Requirements:
- Use simpler words (8th-grade reading level)
- Shorter sentences (15-20 words average)
- Clear and direct language
- Break complex ideas into smaller parts
- Use bullet points where appropriate
- Add examples to clarify concepts

Original Content:
{text[:2000]}

Simplified Version:"""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at simplifying complex content. Make text clear, concise, and easy to understand."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=2500
            )
            
            improved = response.choices[0].message.content
            
            return {
                'success': True,
                'improved_content': improved,
                'changes_made': [
                    'Simplified language and vocabulary',
                    'Shortened sentences',
                    'Improved clarity and flow',
                    'Added helpful examples'
                ]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def boost_engagement(self, text):
        """Make content more engaging and compelling"""
        if not self.client:
            return {'success': False, 'error': 'OpenAI API key not configured'}
        
        try:
            prompt = f"""Rewrite this content to be more engaging, compelling, and captivating.

Requirements:
- Start with a strong hook
- Use power words and emotional triggers
- Add questions to engage readers
- Include storytelling elements
- Create urgency or curiosity
- Use active voice
- Add specific examples and data points

Original Content:
{text[:2000]}

Engaging Version:"""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert copywriter who creates compelling, engaging content that captures attention and drives action."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=2500
            )
            
            improved = response.choices[0].message.content
            
            return {
                'success': True,
                'improved_content': improved,
                'changes_made': [
                    'Added engaging hooks and questions',
                    'Incorporated storytelling elements',
                    'Used power words and emotional triggers',
                    'Improved overall compelling nature'
                ]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
