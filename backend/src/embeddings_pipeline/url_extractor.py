"""
Module for extracting and managing URLs from the AI Robotics textbook sitemap.
"""
import requests
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET
from src.config import settings
import logging


def get_all_urls(sitemap_url: str = None) -> List[str]:
    """
    Fetch all URLs from the sitemap.

    Args:
        sitemap_url: URL of the sitemap to parse. If None, uses the default from settings.

    Returns:
        List of URLs extracted from the sitemap.
    """
    if sitemap_url is None:
        sitemap_url = settings.SITEMAP_URL

    try:
        response = requests.get(sitemap_url, timeout=settings.REQUEST_TIMEOUT)
        response.raise_for_status()

        # Parse the sitemap XML
        root = ET.fromstring(response.content)

        # Find all URL elements in the sitemap
        urls = []
        for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url',
                                   {'http://www.sitemaps.org/schemas/sitemap/0.9': 'http://www.sitemaps.org/schemas/sitemap/0.9'}):
            loc_elem = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc',
                                   {'http://www.sitemaps.org/schemas/sitemap/0.9': 'http://www.sitemaps.org/schemas/sitemap/0.9'})
            if loc_elem is not None and loc_elem.text:
                urls.append(loc_elem.text)

        # If no namespaced elements found, try without namespace
        if not urls:
            for url_elem in root.findall('.//url'):
                loc_elem = url_elem.find('loc')
                if loc_elem is not None and loc_elem.text:
                    urls.append(loc_elem.text)

        # Replace placeholder domain with actual domain if needed
        book_base_url = settings.BOOK_BASE_URL.rstrip('/')
        parsed_base = urlparse(book_base_url)
        actual_domain = parsed_base.netloc

        processed_urls = []
        for url in urls:
            # Replace placeholder domains with actual domain
            processed_url = url.replace("your-docusaurus-site.example.com", actual_domain)
            processed_url = processed_url.replace("ai-robotics-textbook-ten.vercel.app", actual_domain)  # In case there are inconsistencies

            # Only include URLs that belong to the book domain
            parsed_url = urlparse(processed_url)
            if parsed_url.netloc == actual_domain:
                processed_urls.append(processed_url)

        return processed_urls
    except requests.RequestException as e:
        print(f"Error fetching sitemap: {e}")
        return []
    except ET.ParseError as e:
        print(f"Error parsing sitemap XML: {e}")
        return []


def is_valid_url(url: str) -> bool:
    """
    Check if a URL is valid and properly formatted.

    Args:
        url: The URL to validate.

    Returns:
        True if the URL is valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_url_accessibility(url: str, timeout: int = None, max_retries: int = 3) -> Dict[str, Any]:
    """
    Validate that a URL is accessible and returns valid content with retry logic.

    Args:
        url: The URL to validate
        timeout: Request timeout in seconds (default from settings)
        max_retries: Maximum number of retry attempts

    Returns:
        Dictionary with validation results
    """
    if timeout is None:
        timeout = settings.REQUEST_TIMEOUT

    last_error = None
    for attempt in range(max_retries):
        try:
            # Try HEAD request first (lightweight)
            response = requests.head(url, timeout=timeout, allow_redirects=True)
            status_code = response.status_code

            # If HEAD request doesn't give us the info we need, try GET
            if status_code == 405 or status_code >= 400:
                response = requests.get(url, timeout=timeout, headers={'Range': 'bytes=0-1023'})
                status_code = response.status_code

            has_content = status_code < 400  # If we got a good status, assume there's content

            # For definitive content check, do a small GET request if needed
            if status_code >= 200 and status_code < 300 and not has_content:
                try:
                    get_response = requests.get(url, timeout=timeout, headers={'Range': 'bytes=0-1023'})
                    has_content = len(get_response.content) > 0
                except:
                    # If range request fails, try a normal request with short timeout
                    try:
                        get_response = requests.get(url, timeout=min(5, timeout))
                        has_content = len(get_response.content) > 0
                    except:
                        has_content = False

            return {
                'url': url,
                'accessible': 200 <= status_code < 400,
                'status_code': status_code,
                'has_content': has_content,
                'valid': 200 <= status_code < 400 and has_content,
                'error': None,
                'attempt': attempt + 1,
                'retry_needed': attempt > 0
            }
        except requests.RequestException as e:
            last_error = str(e)
            if attempt < max_retries - 1:
                # Wait before retrying (exponential backoff)
                import time
                time.sleep(2 ** attempt)
            else:
                # All retries exhausted
                return {
                    'url': url,
                    'accessible': False,
                    'status_code': None,
                    'has_content': False,
                    'valid': False,
                    'error': last_error,
                    'attempt': attempt + 1
                }
        except Exception as e:
            last_error = str(e)
            if attempt < max_retries - 1:
                import time
                time.sleep(2 ** attempt)
            else:
                return {
                    'url': url,
                    'accessible': False,
                    'status_code': None,
                    'has_content': False,
                    'valid': False,
                    'error': last_error,
                    'attempt': attempt + 1
                }


def validate_urls_batch(urls: List[str], max_workers: int = 10) -> List[Dict[str, Any]]:
    """
    Validate multiple URLs in parallel for better performance.

    Args:
        urls: List of URLs to validate
        max_workers: Maximum number of parallel workers

    Returns:
        List of validation results for each URL
    """
    import concurrent.futures

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_url = {
            executor.submit(validate_url_accessibility, url): url
            for url in urls
        }

        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_url):
            result = future.result()
            results.append(result)

    # Sort results to match original order
    url_to_result = {result['url']: result for result in results}
    ordered_results = [url_to_result[url] for url in urls if url in url_to_result]

    return ordered_results


def filter_book_urls(urls: List[str], base_url: str = None) -> List[str]:
    """
    Filter URLs to only include those from the textbook domain.

    Args:
        urls: List of URLs to filter.
        base_url: Base URL to filter by. If None, uses the default from settings.

    Returns:
        List of URLs that belong to the textbook domain.
    """
    if base_url is None:
        base_url = settings.BOOK_BASE_URL

    filtered_urls = []
    base_domain = urlparse(base_url).netloc

    for url in urls:
        if is_valid_url(url):
            url_domain = urlparse(url).netloc
            if url_domain == base_domain:
                filtered_urls.append(url)

    return filtered_urls


def validate_book_content_entity(content_data: Dict[str, str]) -> bool:
    """
    Validate BookContent entity according to data-model.md specifications.

    Args:
        content_data: Dictionary with content data to validate

    Returns:
        True if valid, False otherwise
    """
    # Check required fields
    if not content_data.get('url'):
        print("Validation failed: URL is required")
        return False

    if not content_data.get('content'):
        print("Validation failed: Content is required")
        return False

    # Check that URL is valid
    if not is_valid_url(content_data['url']):
        print(f"Validation failed: Invalid URL format - {content_data['url']}")
        return False

    # Additional checks can be added based on the data model
    return True


def handle_inaccessible_urls(
    validation_results: List[Dict[str, Any]],
    log_level: str = "ERROR"
) -> List[Dict[str, Any]]:
    """
    Handle inaccessible URLs with proper logging and error handling.

    Args:
        validation_results: List of validation results from validate_urls_batch
        log_level: Logging level for error messages

    Returns:
        List of inaccessible URLs with error details
    """
    logger = logging.getLogger('embeddings_pipeline.url_extractor')

    # Set up logging if not already configured
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, log_level.upper()))

    inaccessible_urls = []

    for result in validation_results:
        if not result.get('valid', False):
            inaccessible_urls.append(result)

            # Log the error with appropriate level
            error_msg = f"URL {result['url']} is inaccessible"
            if result.get('error'):
                error_msg += f": {result['error']}"

            if result.get('status_code'):
                error_msg += f" (Status: {result['status_code']})"

            if result.get('attempt', 1) > 1:
                error_msg += f" (after {result['attempt']} attempts)"

            logger.log(getattr(logging, log_level.upper()), error_msg)

    return inaccessible_urls


if __name__ == "__main__":
    # Example usage
    print("Fetching URLs from sitemap...")
    all_urls = get_all_urls()
    book_urls = filter_book_urls(all_urls)

    print(f"Found {len(book_urls)} book URLs:")
    for url in book_urls[:10]:  # Print first 10 URLs
        print(f"  - {url}")

    if len(book_urls) > 10:
        print(f"  ... and {len(book_urls) - 10} more")

    # Example of validating a URL
    if book_urls:
        validation_result = validate_url_accessibility(book_urls[0])
        print(f"\nValidation result for {book_urls[0]}:")
        print(f"  Accessible: {validation_result['accessible']}")
        print(f"  Status code: {validation_result['status_code']}")
        print(f"  Has content: {validation_result['has_content']}")