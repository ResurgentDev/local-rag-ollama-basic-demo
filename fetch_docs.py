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
        # Parse the URL properly
        parsed_url = urlparse(docs_url)
        if not parsed_url.scheme:
            raise ValueError("URL must include scheme (e.g., https://)")
        
        # Handle different URL types
        if 'github.com' in parsed_url.netloc:
            # GitHub specific handling
            parts = docs_url.split('github.com/')[1].split('/tree/')
            if len(parts) == 2:
                org_repo = parts[0]
                path = parts[1]
                base_url = f'https://raw.githubusercontent.com/{org_repo}/{path}'
            else:
                raise ValueError("Invalid GitHub URL format. Expected: github.com/owner/repo/tree/branch/path")
        else:
            # Generic URL handling
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{os.path.dirname(parsed_url.path)}"
        
        base_html = fetch_url(docs_url)
        md_links = get_links(base_html, '.md')
        
        if not md_links:
            print("Warning: No markdown files found at the specified URL")
            return
        
        # Convert relative links to absolute URLs
        valid_links = []
        for link in md_links:
            if link.startswith('http'):
                valid_links.append(link)
            elif 'github.com' in docs_url:
                # GitHub specific link handling
                if link.startswith('/'):
                    link = link.lstrip('/')
                if '#' in link:
                    link = link.split('#')[0]
                if 'blob/main' in link:
                    link = link.replace('blob/main/', '')
                elif 'blob/master' in link:
                    link = link.replace('blob/master/', '')
                raw_url = f"{base_url}/{link}"
                valid_links.append(raw_url)
            else:
                # Generic URL handling
                if link.startswith('//'):
                    link = parsed_url.scheme + ':' + link
                elif link.startswith('/'):
                    link = f"{parsed_url.scheme}://{parsed_url.netloc}{link}"
                else:
                    link = urljoin(base_url + '/', link)
                valid_links.append(link)
        
        # Remove duplicates while preserving order
        valid_links = list(dict.fromkeys(valid_links))
        
        if not valid_links:
            print("Warning: No valid markdown links found after processing")
            return
            
        # Download files
        success_count = 0
        for link in valid_links:
            try:
                filename = os.path.basename(link.split('#')[0])
                if filename.endswith('.md'):
                    save_path = os.path.join(RAW_DOCS_PATH, filename)
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    print(f'Downloading: {filename} from {link}')
                    download_file(link, save_path)
                    print(f'Downloaded: {filename}')
                    success_count += 1
            except Exception as e:
                print(f'Error downloading {link}: {e}')
        
        if success_count == 0:
            print("Warning: No files were successfully downloaded")
        else:
            print(f"Successfully downloaded {success_count} files")
            
    except Exception as e:
        print(f"Error processing URL {docs_url}: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch documentation from specified URL')
    parser.add_argument('--url', help='URL to fetch documentation from')
    args = parser.parse_args()
    
    fetch_docs(args.url)
