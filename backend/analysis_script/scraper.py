import sys
import os
import re
import argparse
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


def get_page(url, headers=None):
    """Fetch a webpage and return the BeautifulSoup object."""
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser'), response.url
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        return None, None


def find_investors_section(base_url, soup):
    """Find and navigate to the investors section."""
    # Common patterns for investor section links
    investor_keywords = [
        'investor', 'investors', 'investor-relations', 'ir', 
        'shareholder', 'shareholders', 'financial', 'corporate'
    ]
    
    # Search for links containing investor keywords
    links = soup.find_all('a', href=True)
    
    for link in links:
        href = link.get('href', '')
        text = link.get_text().lower()
        
        # Check if link text or href contains investor keywords
        for keyword in investor_keywords:
            if keyword in href.lower() or keyword in text:
                full_url = urljoin(base_url, href)
                logger.info(f"Found investors section: {link.get_text().strip()} -> {full_url}")
                return full_url
    
    logger.warning("Could not find investors section link. Trying common paths...")
    # Try common investor section paths
    common_paths = [
        '/investors', '/investor-relations', '/ir', '/investors/',
        '/shareholders', '/corporate/investors'
    ]
    
    parsed_url = urlparse(base_url)
    base = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    for path in common_paths:
        test_url = urljoin(base, path)
        soup_test, final_url = get_page(test_url)
        if soup_test:
            logger.info(f"Found investors section at: {final_url}")
            return final_url
    
    return None


def find_financial_results_page(investors_url, soup):
    """Find the financial results or annual filings page."""
    financial_keywords = [
        'financial results', 'financial reports', 'quarterly', 'annual',
        'filings', 'reports', 'earnings', 'sec filings', 'financial statements',
        'quarterly results', 'annual report'
    ]
    
    links = soup.find_all('a', href=True)
    
    for link in links:
        href = link.get('href', '')
        text = link.get_text().lower()
        
        for keyword in financial_keywords:
            if keyword in href.lower() or keyword in text:
                full_url = urljoin(investors_url, href)
                logger.info(f"Found financial results page: {link.get_text().strip()} -> {full_url}")
                return full_url
    
    logger.warning("Could not find financial results link. Trying common paths...")
    # Try common financial results paths
    common_paths = [
        '/financial-results', '/reports', '/filings', '/quarterly-results',
        '/annual-reports', '/financial-reports', '/earnings'
    ]
    
    parsed_url = urlparse(investors_url)
    base = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    for path in common_paths:
        test_url = urljoin(base, path)
        soup_test, final_url = get_page(test_url)
        if soup_test:
            logger.info(f"Found financial results page at: {final_url}")
            return final_url
    
    return investors_url  # Return investors URL as fallback


def extract_date_from_text(text):
    """Extract date from text, prioritizing quarter/year patterns."""
    # Patterns for dates: Q1 2024, Q2 2024, 2024 Q1, etc.
    quarter_patterns = [
        r'Q([1-4])\s+(\d{4})',  # Q1 2024
        r'(\d{4})\s+Q([1-4])',  # 2024 Q1
        r'(\d{1,2})/(\d{4})',   # 3/2024 (month/year)
        r'(\d{4})-(\d{2})-(\d{2})',  # 2024-03-31
        r'(\d{1,2})/(\d{1,2})/(\d{4})',  # 03/31/2024
    ]
    
    for pattern in quarter_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                if 'Q' in pattern:
                    # Quarter pattern
                    if pattern.startswith('Q'):
                        quarter, year = match.groups()
                        return (int(year), int(quarter))
                    else:
                        year, quarter = match.groups()
                        return (int(year), int(quarter))
                else:
                    # Date pattern - extract year and try to determine quarter
                    groups = match.groups()
                    year = int(groups[-1]) if len(groups) > 1 else int(groups[0])
                    if len(groups) >= 2:
                        month = int(groups[0]) if len(groups) == 3 else int(groups[-2])
                        quarter = (month - 1) // 3 + 1
                        return (year, quarter)
            except (ValueError, IndexError):
                continue
    
    # Try to extract just year
    year_match = re.search(r'(\d{4})', text)
    if year_match:
        try:
            year = int(year_match.group(1))
            return (year, 0)  # Unknown quarter
        except ValueError:
            pass
    
    return None


def find_quarterly_pdfs(financial_url, soup):
    """Find all PDF links that appear to be quarterly reports."""
    pdf_links = []
    
    # Find all links
    links = soup.find_all('a', href=True)
    
    for link in links:
        href = link.get('href', '')
        text = link.get_text().strip()
        
        # Check if it's a PDF
        if href.lower().endswith('.pdf') or '.pdf' in href.lower():
            full_url = urljoin(financial_url, href)
            
            # Check if it looks like a quarterly report
            text_lower = text.lower()
            href_lower = href.lower()
            
            quarterly_indicators = [
                'quarter', 'q1', 'q2', 'q3', 'q4', '10-q', 'quarterly',
                'earnings', 'results', 'financial'
            ]
            
            is_quarterly = any(indicator in text_lower or indicator in href_lower 
                             for indicator in quarterly_indicators)
            
            if is_quarterly or not pdf_links:  # Include all PDFs if no quarterly found
                date_info = extract_date_from_text(text + ' ' + href)
                pdf_links.append({
                    'url': full_url,
                    'text': text,
                    'date_info': date_info,
                    'filename': os.path.basename(urlparse(full_url).path) or f"report_{len(pdf_links)}.pdf"
                })
    
    # Also check for PDF links in iframes or embedded content
    iframes = soup.find_all('iframe', src=True)
    for iframe in iframes:
        iframe_url = urljoin(financial_url, iframe['src'])
        iframe_soup, _ = get_page(iframe_url)
        if iframe_soup:
            iframe_links = iframe_soup.find_all('a', href=True)
            for link in iframe_links:
                href = link.get('href', '')
                if href.lower().endswith('.pdf'):
                    full_url = urljoin(iframe_url, href)
                    text = link.get_text().strip()
                    date_info = extract_date_from_text(text + ' ' + href)
                    pdf_links.append({
                        'url': full_url,
                        'text': text,
                        'date_info': date_info,
                        'filename': os.path.basename(urlparse(full_url).path) or f"report_{len(pdf_links)}.pdf"
                    })
    
    return pdf_links


def get_latest_quarterly_report(pdf_links):
    """Get the most recent quarterly report based on date information."""
    if not pdf_links:
        return None
    
    # Filter out None date_info and sort by (year, quarter)
    valid_links = [link for link in pdf_links if link['date_info']]
    
    if not valid_links:
        # If no date info, return the first one
        logger.warning("No date information found in PDFs. Returning first PDF.")
        return pdf_links[0]
    
    # Sort by year (descending), then quarter (descending)
    valid_links.sort(key=lambda x: x['date_info'], reverse=True)
    return valid_links[0]


def download_pdf(url, filename, cwd=None):
    """Download a PDF file to the current working directory."""
    if cwd is None:
        cwd = os.getcwd()
    
    filepath = os.path.join(cwd, filename)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        logger.info(f"Downloading PDF from: {url}")
        response = requests.get(url, headers=headers, timeout=30, stream=True)
        response.raise_for_status()
        
        # Ensure filename ends with .pdf
        if not filename.lower().endswith('.pdf'):
            filename = filename + '.pdf'
            filepath = os.path.join(cwd, filename)
        
        # Write the PDF file
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = os.path.getsize(filepath)
        logger.info(f"Successfully downloaded: {filename}")
        logger.info(f"File size: {file_size:,} bytes")
        logger.info(f"Saved to: {filepath}")
        return filepath
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading PDF: {e}")
        return None
    except Exception as e:
        logger.error(f"Error saving PDF: {e}")
        return None

def download_quarterly_report(base_url, download_path=None):
    """Main function to navigate and download the latest quarterly report."""
    logger.info("Starting Quarterly Report Download Process")
    
    # Step 1: Get the base page
    logger.info("[Step 1] Fetching base website...")
    soup, final_url = get_page(base_url)
    if not soup:
        logger.error("Failed to fetch base website.")
        return None
    
    # Step 2: Find investors section
    logger.info("[Step 2] Looking for investors section...")
    investors_url = find_investors_section(final_url, soup)
    if not investors_url:
        logger.error("Could not find investors section.")
        return None
    
    # Step 3: Navigate to investors section
    logger.info("[Step 3] Navigating to investors section...")
    investors_soup, investors_final_url = get_page(investors_url)
    if not investors_soup:
        logger.error("Could not load investors section.")
        return None
    
    # Step 4: Find financial results page
    logger.info("[Step 4] Looking for financial results/annual filings page...")
    financial_url = find_financial_results_page(investors_final_url, investors_soup)
    if not financial_url:
        logger.error("Could not find financial results page.")
        return None
    
    # Step 5: Navigate to financial results page
    logger.info("[Step 5] Navigating to financial results page...")
    financial_soup, financial_final_url = get_page(financial_url)
    if not financial_soup:
        logger.error("Could not load financial results page.")
        return None
    
    # Step 6: Find all quarterly PDFs
    logger.info("[Step 6] Searching for quarterly report PDFs...")
    pdf_links = find_quarterly_pdfs(financial_final_url, financial_soup)
    
    if not pdf_links:
        logger.error("No PDF files found on the financial results page.")
        return None
    
    logger.info(f"Found {len(pdf_links)} PDF file(s):")
    for i, pdf in enumerate(pdf_links, 1):
        date_str = f"{pdf['date_info'][0]} Q{pdf['date_info'][1]}" if pdf['date_info'] else "Unknown date"
        logger.debug(f"  {i}. {pdf['text']} ({date_str})")
    
    # Step 7: Get the latest quarterly report
    logger.info("[Step 7] Identifying latest quarterly report...")
    latest_pdf = get_latest_quarterly_report(pdf_links)
    if not latest_pdf:
        logger.error("Could not determine latest quarterly report.")
        return None
    
    date_str = f"{latest_pdf['date_info'][0]} Q{latest_pdf['date_info'][1]}" if latest_pdf['date_info'] else "Unknown date"
    logger.debug(f"Latest quarterly report: {latest_pdf['text']} ({date_str})")
    
    # Step 8: Download the PDF
    logger.info("[Step 8] Downloading PDF...")
    filepath = download_pdf(latest_pdf['url'], latest_pdf['filename'], download_path)
    
    if filepath:
        logger.info("=" * 60)
        logger.info("Download completed successfully!")
        logger.info("=" * 60)
        return filepath
    else:
        logger.error("=" * 60)
        logger.error("Download failed!")
        logger.error("=" * 60)
        return None


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Scrape a website and download financial reports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Examples:
  python scraper.py --uri https://example.com --download-report t
  python scraper.py --uri https://example.com --download-report true
  python scraper.py --download-report t --uri https://example.com
        '''
    )
    parser.add_argument(
        '--uri',
        required=True,
        help='Website URI to scrape'
    )
    parser.add_argument(
        '--download-report',
        required=False,
        help='Directory path where the PDF report should be downloaded'
    )
    return parser.parse_args()


def validate_args(args):
    """
    Validate and process parsed arguments.
    
    Args:
        args: Parsed arguments from ArgumentParser
    
    Returns:
        Validated and processed arguments
    """
    # Validate required arguments (uri is required by argparse)
    if not args.uri:
        logger.error("Error: --uri argument is required")
        sys.exit(1)
    
    # Validate and normalize URI
    if not args.uri.startswith(('http://', 'https://')):
        logger.info(f"URI missing protocol, adding https:// prefix")
        args.uri = 'https://' + args.uri
    
    # Validate download_report path if provided
    if args.download_report:
        download_path = args.download_report
        # Create directory if it doesn't exist
        if not os.path.exists(download_path):
            try:
                os.makedirs(download_path, exist_ok=True)
                logger.info(f"Created download directory: {download_path}")
            except Exception as e:
                logger.error(f"Error creating download directory {download_path}: {e}")
                sys.exit(1)

        if not os.path.isdir(download_path):
            logger.error(f"Error: {download_path} is not a directory")
            sys.exit(1)
    else:
        # Default to current working directory if not specified
        args.download_report = os.getcwd()
        logger.info(f"No download path specified, using current directory: {args.download_report}")
    
    return args


def main():
    args = parse_arguments()
    args = validate_args(args)

    download_quarterly_report(args.uri, args.download_report)


if __name__ == '__main__':
    main()
