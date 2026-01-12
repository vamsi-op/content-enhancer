import os
from dotenv import load_dotenv

load_dotenv()

class AIContentImprover:
    """Use AI providers (Groq, Gemini, or OpenAI) to generate content improvements"""
    
    def __init__(self):
        self.client = None
        self.provider = None
        self.init_errors = []
        
        # Try Groq first (FREE - fastest)
        groq_key = os.getenv('GROQ_API_KEY')
        if groq_key:
            groq_key = groq_key.strip()  # Remove whitespace
            if groq_key:
                try:
                    from groq import Groq
                    # Validate key format
                    if not groq_key.startswith('gsk_'):
                        self.init_errors.append(f"Groq key format invalid (should start with 'gsk_'). Current: {groq_key[:10]}...")
                    else:
                        self.client = Groq(api_key=groq_key)
                        # Test with a simple call
                        try:
                            test = self.client.chat.completions.create(
                                model="llama-3.1-70b-versatile",
                                messages=[{"role": "user", "content": "hi"}],
                                max_tokens=5
                            )
                            self.provider = 'groq'
                            print("✓ Using Groq AI (Free & Fast)")
                            return
                        except Exception as test_err:
                            self.init_errors.append(f"Groq API test failed: {str(test_err)[:150]}")
                except ImportError:
                    self.init_errors.append("Groq library not installed. Run: pip install groq")
                except Exception as e:
                    self.init_errors.append(f"Groq failed: {str(e)[:150]}")
        
        # Try Google Gemini (FREE tier available)
        gemini_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        if gemini_key:
            gemini_key = gemini_key.strip()  # Remove whitespace
            if gemini_key:
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=gemini_key)
                    self.client = genai.GenerativeModel('gemini-pro')
                    self.provider = 'gemini'
                    print("✓ Using Google Gemini (Free tier)")
                    return
                except ImportError:
                    self.init_errors.append("Gemini library not installed. Run: pip install google-generativeai")
                except Exception as e:
                    self.init_errors.append(f"Gemini failed: {str(e)[:150]}")
        
        # Fallback to OpenAI (Paid)
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            openai_key = openai_key.strip()  # Remove whitespace
            if openai_key:
                try:
                    from openai import OpenAI
                    self.client = OpenAI(api_key=openai_key)
                    self.provider = 'openai'
                    print("✓ Using OpenAI (Paid)")
                    return
                except ImportError:
                    self.init_errors.append("OpenAI library not installed. Run: pip install openai")
                except Exception as e:
                    self.init_errors.append(f"OpenAI failed: {str(e)[:150]}")
        
        print("⚠ No AI provider configured")
        if self.init_errors:
            print("Errors encountered:")
            for error in self.init_errors:
                print(f"  - {error}")
    
    def _call_ai(self, prompt, system_message="You are an expert content writer.", temperature=0.7, max_tokens=2500):
        """Universal AI caller that works with all providers"""
        if not self.client:
            return None
        
        try:
            if self.provider == 'groq':
                response = self.client.chat.completions.create(
                    model="llama-3.1-70b-versatile",  # Free, fast, high-quality
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content
                
            elif self.provider == 'gemini':
                full_prompt = f"{system_message}\n\n{prompt}"
                response = self.client.generate_content(
                    full_prompt,
                    generation_config={
                        'temperature': temperature,
                        'max_output_tokens': max_tokens
                    }
                )
                return response.text
                
            elif self.provider == 'openai':
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content
                
        except Exception as e:
            error_msg = str(e)
            provider_name = self.provider.upper() if self.provider else "AI"
            
            if '401' in error_msg or 'not_authorized' in error_msg or 'invalid' in error_msg.lower():
                raise Exception(f'Invalid {provider_name} API key. Get a FREE key: https://console.groq.com (Groq) or https://makersuite.google.com/app/apikey (Gemini)')
            elif 'quota' in error_msg.lower():
                raise Exception(f'{provider_name} quota exceeded. Switch to FREE Groq: https://console.groq.com')
            elif 'rate_limit' in error_msg.lower():
                raise Exception(f'{provider_name} rate limit reached. Try again in a moment or use FREE Groq.')
            elif 'api_key' in error_msg.lower():
                raise Exception(f'{provider_name} API key issue. Get FREE key: https://console.groq.com')
            raise e
        
        return None
    
    def generate_fixes(self, text, analysis_results):
        """
        Generate AI-powered content improvements
        Returns rewritten/improved content
        """
        if not self.client:
            return {
                'success': False,
                'error': 'AI features require an API key. Get FREE keys from: https://console.groq.com or https://makersuite.google.com/app/apikey'
            }
        
        try:
            prompt = self._build_improvement_prompt(text, analysis_results)
            improved_content = self._call_ai(
                prompt,
                "You are an expert SEO and content strategist. Improve content based on specific feedback.",
                0.7,
                2000
            )
            
            if not improved_content:
                raise Exception("AI provider returned no content")
            
            return {
                'success': True,
                'improved_content': improved_content,
                'changes_made': self._summarize_changes(analysis_results)
            }
            
        except Exception as e:
            error_msg = str(e)
            if '401' in error_msg or 'not_authorized' in error_msg or 'archived' in error_msg.lower():
                error_msg = f'Invalid API key. Get a FREE key from: https://console.groq.com (Groq) or https://makersuite.google.com/app/apikey (Gemini)'
            elif 'quota' in error_msg.lower():
                error_msg = 'API quota exceeded. Try switching to a different provider or wait a moment.'
            elif 'rate_limit' in error_msg.lower():
                error_msg = 'Rate limit reached. Please try again in a moment.'
            
            return {
                'success': False,
                'error': error_msg
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
            return {'success': False, 'error': 'Get a FREE API key from: https://console.groq.com or https://makersuite.google.com/app/apikey'}
        
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

            improved = self._call_ai(
                prompt,
                "You are an expert SEO content writer. Optimize content for search engines while keeping it natural and engaging.",
                0.7,
                2500
            )
            
            if not improved:
                raise Exception("AI returned no content")
            
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
            error_msg = str(e)
            if '401' in error_msg or 'not_authorized' in error_msg or 'archived' in error_msg.lower():
                error_msg = 'Invalid API key. Get FREE key: https://console.groq.com'
            return {'success': False, 'error': error_msg}
    
    def humanize_content(self, text):
        """Make content sound more human and natural"""
        if not self.client:
            return {'success': False, 'error': 'Get a FREE API key from: https://console.groq.com'}
        
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

            improved = self._call_ai(
                prompt,
                "You are an expert content writer who excels at making text sound natural and human. Avoid AI-like patterns.",
                0.8,
                2500
            )
            
            if not improved:
                raise Exception("AI returned no content")
            
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
            return {'success': False, 'error': 'Get a FREE API key from: https://console.groq.com'}
        
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

            improved = self._call_ai(
                prompt,
                "You are an expert at simplifying complex content. Make text clear, concise, and easy to understand.",
                0.6,
                2500
            )
            
            if not improved:
                raise Exception("AI returned no content")
            
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
            return {'success': False, 'error': 'Get a FREE API key from: https://console.groq.com'}
        
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

            improved = self._call_ai(
                prompt,
                "You are an expert copywriter who creates compelling, engaging content that captures attention and drives action.",
                0.8,
                2500
            )
            
            if not improved:
                raise Exception("AI returned no content")
            
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
