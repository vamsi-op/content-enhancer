import requests
from bs4 import BeautifulSoup
import re

class SERPScraper:
    """Scrape SERP results to analyze competition"""
    
    def scrape_google_results(self, keyword, num_results=10):
        """
        Scrape top Google results for a keyword
        Returns list of URLs and their basic info
        """
        try:
            # For hackathon: Using a simple scraping approach
            # In production, use proper SERP API (Serper, SerpAPI, etc.)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            query = keyword.replace(' ', '+')
            url = f"https://www.google.com/search?q={query}&num={num_results}"
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            
            # Find search result divs
            search_results = soup.find_all('div', class_='g')
            
            for result in search_results[:num_results]:
                try:
                    # Extract URL
                    link_tag = result.find('a')
                    if not link_tag or not link_tag.get('href'):
                        continue
                    
                    result_url = link_tag.get('href')
                    
                    # Skip non-http URLs
                    if not result_url.startswith('http'):
                        continue
                    
                    # Extract title
                    title_tag = result.find('h3')
                    title = title_tag.get_text() if title_tag else ""
                    
                    # Extract snippet
                    snippet_tag = result.find('div', class_='VwiC3b')
                    snippet = snippet_tag.get_text() if snippet_tag else ""
                    
                    results.append({
                        'url': result_url,
                        'title': title,
                        'snippet': snippet
                    })
                    
                except Exception as e:
                    continue
            
            return results
            
        except Exception as e:
            # If scraping fails, return empty list
            # In real scenario, would use SERP API
            return []
    
    def fetch_page_content(self, url):
        """Fetch and extract content from a URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "footer", "aside"]):
                element.decompose()
            
            # Get main content
            main = soup.find('main') or soup.find('article') or soup.find('body')
            text = main.get_text(separator=' ', strip=True) if main else ""
            
            # Extract headers
            headers_list = [h.get_text().strip() for level in ['h1', 'h2', 'h3'] 
                           for h in soup.find_all(level)]
            
            # Clean text
            text = re.sub(r'\s+', ' ', text).strip()
            
            return {
                'text': text,
                'word_count': len(text.split()),
                'headers': headers_list,
                'header_count': len(headers_list)
            }
            
        except Exception as e:
            return {
                'text': '',
                'word_count': 0,
                'headers': [],
                'header_count': 0
            }
