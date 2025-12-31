"""
High-Performance Web Crawler
北京理工大学小学期高性能web爬虫实战

A concurrent web crawler with configurable depth and URL filtering.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import threading
import queue
import time
import logging
from typing import Set, List, Optional
from collections import deque


class WebCrawler:
    """
    A high-performance web crawler with concurrent fetching capabilities.
    
    Features:
    - Concurrent URL fetching using threading
    - URL deduplication
    - Configurable crawling depth
    - Robots.txt compliance
    - Domain filtering
    - Custom request headers
    """
    
    def __init__(
        self,
        start_url: str,
        max_depth: int = 2,
        max_pages: int = 100,
        max_workers: int = 5,
        delay: float = 0.5,
        respect_robots: bool = True,
        same_domain_only: bool = True,
        timeout: int = 10
    ):
        """
        Initialize the web crawler.
        
        Args:
            start_url: The starting URL for crawling
            max_depth: Maximum depth to crawl
            max_pages: Maximum number of pages to crawl
            max_workers: Number of concurrent workers
            delay: Delay between requests (in seconds)
            respect_robots: Whether to respect robots.txt
            same_domain_only: Only crawl URLs from the same domain
            timeout: Request timeout in seconds
        """
        self.start_url = start_url
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.max_workers = max_workers
        self.delay = delay
        self.respect_robots = respect_robots
        self.same_domain_only = same_domain_only
        self.timeout = timeout
        
        # Logging (setup first so it can be used by other methods)
        self._setup_logging()
        
        # URL tracking
        self.visited_urls: Set[str] = set()
        self.url_queue: queue.Queue = queue.Queue()
        self.results: List[dict] = []
        
        # Domain info
        parsed_url = urlparse(start_url)
        self.start_domain = parsed_url.netloc
        
        # Robots.txt parser
        self.robot_parser = None
        if respect_robots:
            self._init_robot_parser(start_url)
        
        # Threading
        self.lock = threading.Lock()
        self.workers: List[threading.Thread] = []
        
    def _setup_logging(self):
        """Configure logging for the crawler."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('crawler.log')
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _init_robot_parser(self, url: str):
        """Initialize robots.txt parser for the domain."""
        try:
            parsed_url = urlparse(url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            self.robot_parser = RobotFileParser()
            self.robot_parser.set_url(robots_url)
            self.robot_parser.read()
            self.logger.info(f"Loaded robots.txt from {robots_url}")
        except Exception as e:
            self.logger.warning(f"Could not load robots.txt: {e}")
            self.robot_parser = None
            
    def _can_fetch(self, url: str) -> bool:
        """Check if URL can be fetched according to robots.txt."""
        if not self.respect_robots or not self.robot_parser:
            return True
        try:
            return self.robot_parser.can_fetch("*", url)
        except Exception:
            return True
            
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid for crawling."""
        if not url or url in self.visited_urls:
            return False
            
        parsed = urlparse(url)
        
        # Check scheme
        if parsed.scheme not in ('http', 'https'):
            return False
            
        # Check domain if same_domain_only is enabled
        if self.same_domain_only and parsed.netloc != self.start_domain:
            return False
            
        # Check robots.txt
        if not self._can_fetch(url):
            return False
            
        return True
        
    def _extract_links(self, html: str, base_url: str) -> List[str]:
        """Extract all links from HTML content."""
        links = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Convert relative URLs to absolute
                absolute_url = urljoin(base_url, href)
                # Remove fragment
                absolute_url = absolute_url.split('#')[0]
                if self._is_valid_url(absolute_url):
                    links.append(absolute_url)
        except Exception as e:
            self.logger.error(f"Error extracting links from {base_url}: {e}")
        return links
        
    def _fetch_url(self, url: str) -> Optional[dict]:
        """Fetch content from a URL."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; WebCrawler/1.0)'
            }
            response = requests.get(
                url,
                headers=headers,
                timeout=self.timeout,
                allow_redirects=True
            )
            response.raise_for_status()
            
            return {
                'url': url,
                'status_code': response.status_code,
                'content': response.text,
                'content_type': response.headers.get('content-type', ''),
                'size': len(response.content)
            }
        except requests.RequestException as e:
            self.logger.warning(f"Failed to fetch {url}: {e}")
            return None
            
    def _worker(self):
        """Worker thread function to process URLs from the queue."""
        while True:
            try:
                # Get URL from queue with timeout
                try:
                    url, depth = self.url_queue.get(timeout=1)
                except queue.Empty:
                    break
                    
                # Check if we've reached max pages
                with self.lock:
                    if len(self.visited_urls) >= self.max_pages:
                        self.url_queue.task_done()
                        break
                        
                    # Mark as visited
                    if url in self.visited_urls:
                        self.url_queue.task_done()
                        continue
                    self.visited_urls.add(url)
                    
                # Fetch the page
                self.logger.info(f"Crawling (depth {depth}): {url}")
                result = self._fetch_url(url)
                
                if result:
                    # Store result
                    with self.lock:
                        self.results.append({
                            **result,
                            'depth': depth
                        })
                    
                    # Extract links if not at max depth
                    if depth < self.max_depth:
                        links = self._extract_links(result['content'], url)
                        for link in links:
                            if link not in self.visited_urls:
                                self.url_queue.put((link, depth + 1))
                
                # Rate limiting
                time.sleep(self.delay)
                
                self.url_queue.task_done()
                
            except Exception as e:
                self.logger.error(f"Worker error: {e}")
                self.url_queue.task_done()
                
    def crawl(self) -> List[dict]:
        """
        Start the crawling process.
        
        Returns:
            List of crawled page results
        """
        self.logger.info(f"Starting crawler from {self.start_url}")
        self.logger.info(f"Configuration: max_depth={self.max_depth}, "
                        f"max_pages={self.max_pages}, max_workers={self.max_workers}")
        
        # Add start URL to queue
        self.url_queue.put((self.start_url, 0))
        
        # Start worker threads
        for i in range(self.max_workers):
            worker = threading.Thread(target=self._worker, daemon=True)
            worker.start()
            self.workers.append(worker)
            
        # Wait for all tasks to complete
        self.url_queue.join()
        
        # Wait for workers to finish
        for worker in self.workers:
            worker.join(timeout=1)
            
        self.logger.info(f"Crawling completed. Visited {len(self.visited_urls)} URLs.")
        return self.results
        
    def get_statistics(self) -> dict:
        """Get crawling statistics."""
        return {
            'total_urls_crawled': len(self.visited_urls),
            'successful_fetches': len(self.results),
            'start_url': self.start_url,
            'max_depth': self.max_depth,
            'max_pages': self.max_pages
        }


def main():
    """Example usage of the web crawler."""
    # Example: Crawl a website
    crawler = WebCrawler(
        start_url="http://example.com",
        max_depth=2,
        max_pages=50,
        max_workers=5,
        delay=0.5,
        respect_robots=True,
        same_domain_only=True
    )
    
    results = crawler.crawl()
    
    # Print statistics
    print("\n" + "="*50)
    print("Crawling Statistics")
    print("="*50)
    stats = crawler.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Print first few results
    print("\n" + "="*50)
    print("Sample Results")
    print("="*50)
    for i, result in enumerate(results[:5], 1):
        print(f"\n{i}. URL: {result['url']}")
        print(f"   Status: {result['status_code']}")
        print(f"   Size: {result['size']} bytes")
        print(f"   Depth: {result['depth']}")


if __name__ == "__main__":
    main()
