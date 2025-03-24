import os
import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urljoin, urlparse
from config import DEFAULT_DOCS_URL, RAW_DOCS_PATH

def fetch_url(url):
    """Fetch content from URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def get_links(html, file_ext=''):
    """Extract links with specified extension from HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for link in soup.find_all('a', href=True):
        if file_ext in link['href']:
            links.append(link['href'])
    return links

def download_file(url, save_path):
    """Download file from URL to specified path."""
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, 'wb') as f:
        f.write(response.content)

def fetch_docs(url=None):
    """
    Fetch documentation from specified URL.
    
    Args:
        url: Optional URL to fetch docs from. Uses DEFAULT_DOCS_URL if not provided.
    """
    docs_url = url or DEFAULT_DOCS_URL
    print(f"Fetching documentation from: {docs_url}")
    
    base_html = fetch_url(docs_url)
    md_links = get_links(base_html, '.md')

    # Convert relative links to absolute URLs and filter for markdown files
    valid_links = []
    base_url = docs_url.rstrip('/')
    
    for link in md_links:
        # Handle both relative and absolute URLs
        if link.startswith('http'):
            valid_links.append(link)
        else:
            # For GitHub specifically, convert blob links to raw content
            if 'github.com' in base_url and '/blob/' in link:
                raw_link = link.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
                valid_links.append(raw_link)
            else:
                # For other sources, just join with base URL
                valid_links.append(urljoin(base_url, link))

    # Remove duplicates while preserving order
    valid_links = list(dict.fromkeys(valid_links))

    for link in valid_links:
        try:
            filename = os.path.basename(urlparse(link).path)
            if filename.endswith('.md'):
                save_path = os.path.join(RAW_DOCS_PATH, filename)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                download_file(link, save_path)
                print(f'Downloaded: {filename} from {link}')
        except Exception as e:
            print(f'Error downloading {link}: {e}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch documentation from specified URL')
    parser.add_argument('--url', help='URL to fetch documentation from')
    args = parser.parse_args()
    
    fetch_docs(args.url)
