#!/usr/bin/env python3
"""
Unit tests for the web crawler
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from crawler import WebCrawler
import queue


class TestWebCrawler(unittest.TestCase):
    """Test cases for WebCrawler class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_url = "http://example.com"
        
    @patch('crawler.RobotFileParser')
    def test_crawler_initialization(self, mock_robot_parser):
        """Test crawler initialization"""
        crawler = WebCrawler(
            start_url=self.test_url,
            max_depth=2,
            max_pages=10,
            respect_robots=False
        )
        
        self.assertEqual(crawler.start_url, self.test_url)
        self.assertEqual(crawler.max_depth, 2)
        self.assertEqual(crawler.max_pages, 10)
        self.assertEqual(crawler.start_domain, "example.com")
        self.assertIsInstance(crawler.visited_urls, set)
        self.assertIsInstance(crawler.url_queue, queue.Queue)
        self.assertIsInstance(crawler.results, list)
        
    def test_is_valid_url_scheme(self):
        """Test URL validation for different schemes"""
        crawler = WebCrawler(
            start_url=self.test_url,
            respect_robots=False
        )
        
        # Valid URLs
        self.assertTrue(crawler._is_valid_url("http://example.com/page"))
        self.assertTrue(crawler._is_valid_url("https://example.com/page"))
        
        # Invalid schemes
        self.assertFalse(crawler._is_valid_url("ftp://example.com/page"))
        self.assertFalse(crawler._is_valid_url("javascript:alert(1)"))
        
    def test_is_valid_url_same_domain(self):
        """Test URL validation for same domain restriction"""
        crawler = WebCrawler(
            start_url=self.test_url,
            same_domain_only=True,
            respect_robots=False
        )
        
        # Same domain
        self.assertTrue(crawler._is_valid_url("http://example.com/page"))
        
        # Different domain
        self.assertFalse(crawler._is_valid_url("http://other.com/page"))
        
    def test_is_valid_url_visited(self):
        """Test URL validation for already visited URLs"""
        crawler = WebCrawler(
            start_url=self.test_url,
            respect_robots=False
        )
        
        test_page_url = "http://example.com/page"
        
        # First time should be valid
        self.assertTrue(crawler._is_valid_url(test_page_url))
        
        # Add to visited
        crawler.visited_urls.add(test_page_url)
        
        # Second time should be invalid
        self.assertFalse(crawler._is_valid_url(test_page_url))
        
    def test_extract_links(self):
        """Test link extraction from HTML"""
        crawler = WebCrawler(
            start_url=self.test_url,
            respect_robots=False
        )
        
        html = '''
        <html>
            <body>
                <a href="http://example.com/page1">Page 1</a>
                <a href="/page2">Page 2</a>
                <a href="http://other.com/page">Other</a>
                <a href="#fragment">Fragment</a>
                <a href="javascript:void(0)">JS</a>
            </body>
        </html>
        '''
        
        links = crawler._extract_links(html, "http://example.com")
        
        # Should extract valid links
        self.assertIn("http://example.com/page1", links)
        self.assertIn("http://example.com/page2", links)
        
        # Should not extract javascript or fragments
        self.assertNotIn("javascript:void(0)", links)
        
    def test_get_statistics(self):
        """Test statistics generation"""
        crawler = WebCrawler(
            start_url=self.test_url,
            max_depth=3,
            max_pages=50,
            respect_robots=False
        )
        
        # Add some visited URLs
        crawler.visited_urls.add("http://example.com/page1")
        crawler.visited_urls.add("http://example.com/page2")
        
        # Add some results
        crawler.results.append({'url': 'http://example.com/page1'})
        
        stats = crawler.get_statistics()
        
        self.assertEqual(stats['total_urls_crawled'], 2)
        self.assertEqual(stats['successful_fetches'], 1)
        self.assertEqual(stats['start_url'], self.test_url)
        self.assertEqual(stats['max_depth'], 3)
        self.assertEqual(stats['max_pages'], 50)
        
    @patch('crawler.requests.get')
    def test_fetch_url_success(self, mock_get):
        """Test successful URL fetching"""
        crawler = WebCrawler(
            start_url=self.test_url,
            respect_robots=False
        )
        
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html>Test</html>"
        mock_response.content = b"<html>Test</html>"
        mock_response.headers = {'content-type': 'text/html'}
        mock_get.return_value = mock_response
        
        result = crawler._fetch_url("http://example.com/page")
        
        self.assertIsNotNone(result)
        self.assertEqual(result['status_code'], 200)
        self.assertEqual(result['content'], "<html>Test</html>")
        self.assertEqual(result['content_type'], 'text/html')
        
    @patch('crawler.requests.get')
    def test_fetch_url_failure(self, mock_get):
        """Test URL fetching failure"""
        crawler = WebCrawler(
            start_url=self.test_url,
            respect_robots=False
        )
        
        # Mock exception
        from requests.exceptions import RequestException
        mock_get.side_effect = RequestException("Network error")
        
        result = crawler._fetch_url("http://example.com/page")
        
        self.assertIsNone(result)
        

class TestWebCrawlerIntegration(unittest.TestCase):
    """Integration tests for WebCrawler"""
    
    @patch('crawler.requests.get')
    def test_crawl_with_mocked_requests(self, mock_get):
        """Test crawling with mocked HTTP requests"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '''
        <html>
            <body>
                <a href="http://example.com/page1">Page 1</a>
            </body>
        </html>
        '''
        mock_response.content = mock_response.text.encode()
        mock_response.headers = {'content-type': 'text/html'}
        mock_get.return_value = mock_response
        
        crawler = WebCrawler(
            start_url="http://example.com",
            max_depth=1,
            max_pages=5,
            max_workers=2,
            delay=0.1,
            respect_robots=False
        )
        
        results = crawler.crawl()
        
        # Should have crawled at least the start URL
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]['status_code'], 200)


if __name__ == '__main__':
    unittest.main()
