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
    
    try:
        # Handle GitHub URLs specifically
        if 'github.com' in docs_url:
            base_html = fetch_url(docs_url)
            md_links = get_links(base_html, '.md')
            
            # Filter for valid docs links and remove duplicates (GitHub specific)
            valid_links = []
            for link in md_links:
                if 'blob/main/docs/' in link or 'blob/master/docs/' in link:
                    raw_url = 'https://raw.githubusercontent.com' + link.replace('/blob', '')
                    valid_links.append(raw_url)
            valid_links = list(set(valid_links))
            
        else:
            # Handle generic URLs
            base_url = docs_url.rstrip('/')
            base_html = fetch_url(docs_url)
            md_links = get_links(base_html, '.md')
            valid_links = [urljoin(base_url, link) for link in md_links]

        # Download files
        for link in valid_links:
            try:
                filename = os.path.basename(link.split('#')[0])  # Remove anchors
                if filename.endswith('.md'):
                    save_path = os.path.join(RAW_DOCS_PATH, filename)
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    print(f'Downloading: {filename} from {link}')
                    download_file(link, save_path)
                    print(f'Downloaded: {filename}')
            except Exception as e:
                print(f'Error downloading {link}: {e}')

    except Exception as e:
        print(f"Error processing URL {docs_url}: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch documentation from specified URL')
    parser.add_argument('--url', help='URL to fetch documentation from')
    args = parser.parse_args()
    
    fetch_docs(args.url)
