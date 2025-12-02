import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

class TextExtractor:
    """Extract text content from URL or raw text input"""
    
    def extract(self, input_data):
        """
        Extract text from input (URL or raw text)
        Returns dict with: text, url, headers, meta_description, title
        """
        # Check if input is a URL
        if self._is_url(input_data):
            return self._extract_from_url(input_data)
        else:
            return self._extract_from_text(input_data)
    
    def _is_url(self, text):
        """Check if input is a valid URL"""
        try:
            result = urlparse(text.strip())
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _extract_from_url(self, url):
        """Scrape content from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "aside"]):
                script.decompose()
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ""
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            meta_description = meta_desc.get('content', '').strip() if meta_desc else ""
            
            # Extract headers
            headers_list = []
            for level in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                for header in soup.find_all(level):
                    headers_list.append({
                        'level': level,
                        'text': header.get_text().strip()
                    })
            
            # Extract main content text
            # Try to find main content area
            main_content = soup.find('main') or soup.find('article') or soup.find('body')
            
            if main_content:
                text = main_content.get_text(separator=' ', strip=True)
            else:
                text = soup.get_text(separator=' ', strip=True)
            
            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            return {
                'text': text,
                'url': url,
                'title': title_text,
                'headers': headers_list,
                'meta_description': meta_description,
                'source_type': 'url'
            }
            
        except Exception as e:
            raise Exception(f"Failed to extract content from URL: {str(e)}")
    
    def _extract_from_text(self, text):
        """Process raw text input"""
        return {
            'text': text.strip(),
            'url': None,
            'title': '',
            'headers': [],
            'meta_description': '',
            'source_type': 'text'
        }
