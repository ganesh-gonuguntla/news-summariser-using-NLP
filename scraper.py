import requests
from bs4 import BeautifulSoup
import re

def fetch_article_text(url):
    """
    Fetches the main text content from a given news article URL.
    Returns the extracted text or an error message.
    """
    # A user-agent header is often needed to bypass basic bot protection on news sites.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}"

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Remove script, style, header, footer, and nav elements to clean up noise
    for script in soup(["script", "style", "header", "footer", "nav", "aside", "form"]):
        script.extract()
        
    paragraphs = soup.find_all('p')
    # Use strip=True to remove leading/trailing whitespaces from each paragraph
    article_text = ' '.join([p.get_text(strip=True) for p in paragraphs])
    
    # Clean up excessive whitespaces
    article_text = re.sub(r'\s+', ' ', article_text).strip()
    
    if not article_text:
        return "Error: Could not extract useful text from the URL. Please provide raw text instead."
        
    return article_text
