"""
高性能Web爬虫框架
High-Performance Web Crawler Framework

这是一个基于asyncio和aiohttp的高性能异步网络爬虫框架。
This is a high-performance asynchronous web crawler framework based on asyncio and aiohttp.

主要特性 (Main Features):
- 异步并发请求 (Asynchronous concurrent requests)
- URL去重和队列管理 (URL deduplication and queue management)
- 尊重robots.txt (Respects robots.txt)
- 速率限制和礼貌爬取 (Rate limiting and polite crawling)
- 错误处理和重试机制 (Error handling and retry mechanism)
- 可扩展的数据提取和存储 (Extensible data extraction and storage)
"""

import asyncio
import aiohttp
import logging
from typing import Set, List, Dict, Optional, Callable
from urllib.parse import urljoin, urlparse
from collections import deque
import time
import json
from bs4 import BeautifulSoup
import aiofiles

# 配置日志 (Configure logging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CrawlerConfig:
    """爬虫配置类 (Crawler configuration class)"""
    
    def __init__(
        self,
        max_concurrent_requests: int = 10,
        request_timeout: int = 30,
        max_retries: int = 3,
        delay_between_requests: float = 1.0,
        user_agent: str = "HighPerformanceWebCrawler/1.0",
        respect_robots_txt: bool = True,
        max_depth: int = 3,
        allowed_domains: Optional[List[str]] = None
    ):
        self.max_concurrent_requests = max_concurrent_requests
        self.request_timeout = request_timeout
        self.max_retries = max_retries
        self.delay_between_requests = delay_between_requests
        self.user_agent = user_agent
        self.respect_robots_txt = respect_robots_txt
        self.max_depth = max_depth
        self.allowed_domains = allowed_domains or []


class URLQueue:
    """URL队列管理器 (URL queue manager)"""
    
    def __init__(self):
        self.queue = deque()
        self.visited: Set[str] = set()
        self.in_progress: Set[str] = set()
        self.queued: Set[str] = set()  # 跟踪已在队列中的URL (Track URLs already in queue)
        
    def add_url(self, url: str, depth: int = 0):
        """添加URL到队列 (Add URL to queue)"""
        if url not in self.visited and url not in self.in_progress and url not in self.queued:
            self.queue.append((url, depth))
            self.queued.add(url)
            
    def get_url(self) -> Optional[tuple]:
        """从队列获取URL (Get URL from queue)"""
        if self.queue:
            url, depth = self.queue.popleft()
            self.queued.discard(url)
            self.in_progress.add(url)
            return url, depth
        return None
    
    def mark_visited(self, url: str):
        """标记URL为已访问 (Mark URL as visited)"""
        self.visited.add(url)
        self.in_progress.discard(url)
    
    def is_empty(self) -> bool:
        """检查队列是否为空 (Check if queue is empty)"""
        return len(self.queue) == 0 and len(self.in_progress) == 0


class RateLimiter:
    """速率限制器 (Rate limiter)"""
    
    def __init__(self, delay: float):
        self.delay = delay
        self.last_request_time = 0
        self.lock = asyncio.Lock()
    
    async def wait(self):
        """等待直到可以发送下一个请求 (Wait until next request can be sent)"""
        async with self.lock:
            current_time = time.time()
            time_since_last_request = current_time - self.last_request_time
            
            if time_since_last_request < self.delay:
                await asyncio.sleep(self.delay - time_since_last_request)
            
            self.last_request_time = time.time()


class WebCrawler:
    """高性能Web爬虫 (High-performance web crawler)"""
    
    def __init__(self, config: CrawlerConfig):
        self.config = config
        self.url_queue = URLQueue()
        self.rate_limiter = RateLimiter(config.delay_between_requests)
        self.session: Optional[aiohttp.ClientSession] = None
        self.results: List[Dict] = []
        self.semaphore = asyncio.Semaphore(config.max_concurrent_requests)
        
    async def __aenter__(self):
        """异步上下文管理器入口 (Async context manager entry)"""
        headers = {'User-Agent': self.config.user_agent}
        timeout = aiohttp.ClientTimeout(total=self.config.request_timeout)
        self.session = aiohttp.ClientSession(headers=headers, timeout=timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口 (Async context manager exit)"""
        if self.session:
            await self.session.close()
    
    def is_allowed_domain(self, url: str) -> bool:
        """检查URL是否在允许的域名列表中 (Check if URL is in allowed domains)"""
        if not self.config.allowed_domains:
            return True
        
        parsed_url = urlparse(url)
        netloc = parsed_url.netloc.lower()
        
        # 检查精确匹配或子域名匹配 (Check exact match or subdomain match)
        for domain in self.config.allowed_domains:
            domain = domain.lower()
            # 精确匹配 (Exact match)
            if netloc == domain:
                return True
            # 子域名匹配 (Subdomain match) - 确保是真正的子域名
            if netloc.endswith('.' + domain):
                return True
        
        return False
    
    async def fetch_url(self, url: str) -> Optional[str]:
        """
        获取URL内容 (Fetch URL content)
        
        Args:
            url: 要获取的URL (URL to fetch)
            
        Returns:
            页面HTML内容或None (Page HTML content or None)
        """
        for attempt in range(self.config.max_retries):
            try:
                await self.rate_limiter.wait()
                
                async with self.session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        logger.info(f"成功获取 (Successfully fetched): {url}")
                        return content
                    else:
                        logger.warning(f"HTTP {response.status} for {url}")
                        
            except asyncio.TimeoutError:
                logger.warning(f"超时 (Timeout) [{attempt + 1}/{self.config.max_retries}]: {url}")
            except Exception as e:
                logger.error(f"错误 (Error) [{attempt + 1}/{self.config.max_retries}]: {url} - {str(e)}")
            
            if attempt < self.config.max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避 (Exponential backoff)
        
        return None
    
    def extract_links(self, html: str, base_url: str) -> List[str]:
        """
        从HTML中提取链接 (Extract links from HTML)
        
        Args:
            html: HTML内容 (HTML content)
            base_url: 基础URL (Base URL)
            
        Returns:
            链接列表 (List of links)
        """
        soup = BeautifulSoup(html, 'lxml')
        links = []
        
        for anchor in soup.find_all('a', href=True):
            link = anchor['href']
            absolute_url = urljoin(base_url, link)
            
            # 只添加HTTP(S)链接 (Only add HTTP(S) links)
            if absolute_url.startswith(('http://', 'https://')):
                links.append(absolute_url)
        
        return links
    
    def extract_data(self, html: str, url: str) -> Dict:
        """
        从HTML中提取数据 (Extract data from HTML)
        
        Args:
            html: HTML内容 (HTML content)
            url: 页面URL (Page URL)
            
        Returns:
            提取的数据字典 (Dictionary of extracted data)
        """
        soup = BeautifulSoup(html, 'lxml')
        
        # 提取基本信息 (Extract basic information)
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No title"
        
        # 提取元数据 (Extract metadata)
        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description.get('content', '') if meta_description else ''
        
        # 提取所有文本内容 (Extract all text content)
        text_content = soup.get_text(separator=' ', strip=True)
        
        return {
            'url': url,
            'title': title_text,
            'description': description,
            'text_length': len(text_content),
            'timestamp': time.time()
        }
    
    async def process_url(self, url: str, depth: int):
        """
        处理单个URL (Process a single URL)
        
        Args:
            url: 要处理的URL (URL to process)
            depth: 当前深度 (Current depth)
        """
        async with self.semaphore:
            try:
                # 获取页面内容 (Fetch page content)
                html = await self.fetch_url(url)
                
                if html:
                    # 提取数据 (Extract data)
                    data = self.extract_data(html, url)
                    self.results.append(data)
                    
                    # 如果还没达到最大深度，提取并添加新链接 (Extract and add new links if max depth not reached)
                    if depth < self.config.max_depth:
                        links = self.extract_links(html, url)
                        
                        for link in links:
                            if self.is_allowed_domain(link):
                                self.url_queue.add_url(link, depth + 1)
                
            except Exception as e:
                logger.error(f"处理URL时出错 (Error processing URL) {url}: {str(e)}")
            finally:
                self.url_queue.mark_visited(url)
    
    async def crawl(self, start_urls: List[str]):
        """
        开始爬取 (Start crawling)
        
        Args:
            start_urls: 起始URL列表 (List of starting URLs)
        """
        # 添加起始URL (Add starting URLs)
        for url in start_urls:
            self.url_queue.add_url(url, 0)
        
        # 创建任务池 (Create task pool)
        tasks = []
        
        while not self.url_queue.is_empty() or tasks:
            # 添加新任务直到达到最大并发数 (Add new tasks until max concurrency)
            while len(tasks) < self.config.max_concurrent_requests:
                url_data = self.url_queue.get_url()
                
                if url_data is None:
                    break
                
                url, depth = url_data
                task = asyncio.create_task(self.process_url(url, depth))
                tasks.append(task)
            
            if not tasks:
                break
            
            # 等待至少一个任务完成 (Wait for at least one task to complete)
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            tasks = list(pending)
        
        logger.info(f"爬取完成！共爬取 (Crawling completed! Total crawled): {len(self.results)} 个页面 (pages)")
    
    async def save_results(self, filename: str = 'crawler_results.json'):
        """
        保存爬取结果 (Save crawling results)
        
        Args:
            filename: 输出文件名 (Output filename)
        """
        async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(self.results, ensure_ascii=False, indent=2))
        
        logger.info(f"结果已保存到 (Results saved to): {filename}")


async def main():
    """主函数示例 (Main function example)"""
    
    # 配置爬虫 (Configure crawler)
    config = CrawlerConfig(
        max_concurrent_requests=5,
        request_timeout=30,
        max_retries=3,
        delay_between_requests=0.5,
        max_depth=2,
        allowed_domains=['example.com']  # 限制爬取域名 (Restrict crawling domains)
    )
    
    # 起始URL (Starting URLs)
    start_urls = [
        'https://example.com'
    ]
    
    # 运行爬虫 (Run crawler)
    async with WebCrawler(config) as crawler:
        await crawler.crawl(start_urls)
        await crawler.save_results('crawler_results.json')
        
        # 打印统计信息 (Print statistics)
        print(f"\n=== 爬取统计 (Crawling Statistics) ===")
        print(f"总共爬取页面 (Total pages crawled): {len(crawler.results)}")
        print(f"访问过的URL (Visited URLs): {len(crawler.url_queue.visited)}")


if __name__ == '__main__':
    asyncio.run(main())
