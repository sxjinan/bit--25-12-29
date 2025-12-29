"""
单元测试 (Unit Tests)

测试爬虫的核心功能
Test the core functionality of the crawler
"""

import asyncio
import unittest
from unittest.mock import Mock, patch, AsyncMock
from crawler import WebCrawler, CrawlerConfig, URLQueue, RateLimiter
import time


class TestURLQueue(unittest.TestCase):
    """测试URL队列管理 (Test URL queue management)"""
    
    def setUp(self):
        self.queue = URLQueue()
    
    def test_add_and_get_url(self):
        """测试添加和获取URL (Test adding and getting URLs)"""
        self.queue.add_url('https://example.com', 0)
        url, depth = self.queue.get_url()
        
        self.assertEqual(url, 'https://example.com')
        self.assertEqual(depth, 0)
    
    def test_url_deduplication(self):
        """测试URL去重 (Test URL deduplication)"""
        self.queue.add_url('https://example.com', 0)
        self.queue.add_url('https://example.com', 0)  # 重复URL (Duplicate URL)
        
        # 应该只有一个URL (Should only have one URL)
        url1, depth1 = self.queue.get_url()
        url2 = self.queue.get_url()
        
        self.assertIsNotNone(url1)
        self.assertIsNone(url2)
    
    def test_mark_visited(self):
        """测试标记已访问 (Test marking as visited)"""
        self.queue.add_url('https://example.com', 0)
        url, depth = self.queue.get_url()
        self.queue.mark_visited(url)
        
        self.assertIn(url, self.queue.visited)
        self.assertNotIn(url, self.queue.in_progress)
    
    def test_is_empty(self):
        """测试队列是否为空 (Test if queue is empty)"""
        self.assertTrue(self.queue.is_empty())
        
        self.queue.add_url('https://example.com', 0)
        self.assertFalse(self.queue.is_empty())


class TestRateLimiter(unittest.TestCase):
    """测试速率限制器 (Test rate limiter)"""
    
    def test_rate_limiting(self):
        """测试速率限制 (Test rate limiting)"""
        async def run_test():
            limiter = RateLimiter(delay=0.5)
            
            start_time = time.time()
            await limiter.wait()
            await limiter.wait()
            end_time = time.time()
            
            # 两次请求应该至少间隔0.5秒 (Two requests should be at least 0.5s apart)
            elapsed = end_time - start_time
            self.assertGreaterEqual(elapsed, 0.5)
        
        asyncio.run(run_test())


class TestCrawlerConfig(unittest.TestCase):
    """测试爬虫配置 (Test crawler configuration)"""
    
    def test_default_config(self):
        """测试默认配置 (Test default configuration)"""
        config = CrawlerConfig()
        
        self.assertEqual(config.max_concurrent_requests, 10)
        self.assertEqual(config.request_timeout, 30)
        self.assertEqual(config.max_retries, 3)
        self.assertEqual(config.delay_between_requests, 1.0)
    
    def test_custom_config(self):
        """测试自定义配置 (Test custom configuration)"""
        config = CrawlerConfig(
            max_concurrent_requests=5,
            request_timeout=20,
            max_retries=2,
            delay_between_requests=0.5
        )
        
        self.assertEqual(config.max_concurrent_requests, 5)
        self.assertEqual(config.request_timeout, 20)
        self.assertEqual(config.max_retries, 2)
        self.assertEqual(config.delay_between_requests, 0.5)


class TestWebCrawler(unittest.TestCase):
    """测试Web爬虫 (Test web crawler)"""
    
    def test_is_allowed_domain(self):
        """测试域名过滤 (Test domain filtering)"""
        async def run_test():
            config = CrawlerConfig(allowed_domains=['example.com'])
            async with WebCrawler(config) as crawler:
                # 应该允许的 (Should be allowed)
                self.assertTrue(crawler.is_allowed_domain('https://example.com/page'))
                self.assertTrue(crawler.is_allowed_domain('https://www.example.com/page'))
                self.assertTrue(crawler.is_allowed_domain('https://sub.example.com/page'))
                
                # 不应该允许的 (Should not be allowed)
                self.assertFalse(crawler.is_allowed_domain('https://other.com/page'))
                self.assertFalse(crawler.is_allowed_domain('https://malicious-example.com/page'))
                self.assertFalse(crawler.is_allowed_domain('https://examplecom.net/page'))
        
        asyncio.run(run_test())
    
    def test_extract_links(self):
        """测试链接提取 (Test link extraction)"""
        async def run_test():
            config = CrawlerConfig()
            async with WebCrawler(config) as crawler:
                html = '''
                <html>
                    <body>
                        <a href="https://example.com/page1">Link 1</a>
                        <a href="/page2">Link 2</a>
                        <a href="javascript:void(0)">Not a link</a>
                    </body>
                </html>
                '''
                
                links = crawler.extract_links(html, 'https://example.com')
                
                # 应该提取两个HTTP(S)链接 (Should extract two HTTP(S) links)
                self.assertEqual(len(links), 2)
                self.assertIn('https://example.com/page1', links)
                self.assertIn('https://example.com/page2', links)
        
        asyncio.run(run_test())
    
    def test_extract_data(self):
        """测试数据提取 (Test data extraction)"""
        async def run_test():
            config = CrawlerConfig()
            async with WebCrawler(config) as crawler:
                html = '''
                <html>
                    <head>
                        <title>Test Page</title>
                        <meta name="description" content="Test description">
                    </head>
                    <body>
                        <h1>Main Content</h1>
                        <p>This is a test page.</p>
                    </body>
                </html>
                '''
                
                data = crawler.extract_data(html, 'https://example.com')
                
                self.assertEqual(data['url'], 'https://example.com')
                self.assertEqual(data['title'], 'Test Page')
                self.assertEqual(data['description'], 'Test description')
                self.assertGreater(data['text_length'], 0)
        
        asyncio.run(run_test())


def run_tests():
    """运行所有测试 (Run all tests)"""
    print("运行单元测试... (Running unit tests...)")
    print("=" * 60)
    
    # 创建测试套件 (Create test suite)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类 (Add test classes)
    suite.addTests(loader.loadTestsFromTestCase(TestURLQueue))
    suite.addTests(loader.loadTestsFromTestCase(TestRateLimiter))
    suite.addTests(loader.loadTestsFromTestCase(TestCrawlerConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestWebCrawler))
    
    # 运行测试 (Run tests)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 打印结果 (Print results)
    print("\n" + "=" * 60)
    print(f"测试完成 (Tests completed)")
    print(f"运行测试数 (Tests run): {result.testsRun}")
    print(f"成功 (Successes): {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败 (Failures): {len(result.failures)}")
    print(f"错误 (Errors): {len(result.errors)}")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
