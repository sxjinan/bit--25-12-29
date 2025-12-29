"""
示例：使用高性能Web爬虫爬取新闻网站
Example: Using the high-performance web crawler to scrape a news website

这个示例展示了如何使用爬虫框架来爬取和提取数据。
This example demonstrates how to use the crawler framework to crawl and extract data.
"""

import asyncio
from crawler import WebCrawler, CrawlerConfig
from bs4 import BeautifulSoup
from typing import Dict


class CustomNewsCrawler(WebCrawler):
    """自定义新闻爬虫 (Custom news crawler)"""
    
    def extract_data(self, html: str, url: str) -> Dict:
        """
        重写数据提取方法以提取新闻特定的数据
        Override data extraction method to extract news-specific data
        """
        soup = BeautifulSoup(html, 'lxml')
        
        # 提取标题 (Extract title)
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No title"
        
        # 提取主要内容 (Extract main content)
        # 这里使用常见的新闻文章选择器 (Using common news article selectors)
        article_selectors = ['article', '.article', '#article', '.post', '.content']
        article_content = ""
        
        for selector in article_selectors:
            if '.' in selector:
                article = soup.find(class_=selector[1:])
            elif '#' in selector:
                article = soup.find(id=selector[1:])
            else:
                article = soup.find(selector)
            
            if article:
                article_content = article.get_text(separator=' ', strip=True)
                break
        
        # 提取发布日期 (Extract publish date)
        date_meta = soup.find('meta', attrs={'property': 'article:published_time'})
        publish_date = date_meta.get('content', '') if date_meta else ''
        
        # 提取作者 (Extract author)
        author_meta = soup.find('meta', attrs={'name': 'author'})
        author = author_meta.get('content', '') if author_meta else ''
        
        return {
            'url': url,
            'title': title_text,
            'author': author,
            'publish_date': publish_date,
            'content_length': len(article_content),
            'has_article': bool(article_content)
        }


async def crawl_example_site():
    """爬取示例网站 (Crawl example website)"""
    
    # 配置爬虫参数 (Configure crawler parameters)
    config = CrawlerConfig(
        max_concurrent_requests=3,  # 并发请求数 (Concurrent requests)
        request_timeout=30,           # 请求超时时间（秒）(Request timeout in seconds)
        max_retries=3,                # 最大重试次数 (Max retries)
        delay_between_requests=1.0,   # 请求间隔（秒）(Delay between requests in seconds)
        max_depth=1,                  # 最大爬取深度 (Max crawl depth)
        allowed_domains=['example.com']  # 只爬取这些域名 (Only crawl these domains)
    )
    
    start_urls = [
        'https://example.com'
    ]
    
    print("开始爬取... (Starting crawl...)")
    print(f"起始URL (Starting URLs): {start_urls}")
    print(f"最大并发数 (Max concurrent): {config.max_concurrent_requests}")
    print(f"最大深度 (Max depth): {config.max_depth}")
    print("-" * 50)
    
    async with CustomNewsCrawler(config) as crawler:
        await crawler.crawl(start_urls)
        await crawler.save_results('example_results.json')
        
        # 打印详细统计 (Print detailed statistics)
        print("\n" + "=" * 50)
        print("爬取完成！(Crawling completed!)")
        print("=" * 50)
        print(f"成功爬取的页面数 (Successfully crawled pages): {len(crawler.results)}")
        print(f"访问过的URL总数 (Total visited URLs): {len(crawler.url_queue.visited)}")
        
        if crawler.results:
            print("\n前5个爬取结果示例 (First 5 crawl results):")
            for i, result in enumerate(crawler.results[:5], 1):
                print(f"\n{i}. {result.get('title', 'No title')}")
                print(f"   URL: {result.get('url', '')}")
                print(f"   内容长度 (Content length): {result.get('content_length', 0)} 字符 (characters)")


async def crawl_multiple_sites():
    """爬取多个网站示例 (Example of crawling multiple websites)"""
    
    config = CrawlerConfig(
        max_concurrent_requests=10,
        request_timeout=30,
        max_retries=2,
        delay_between_requests=0.5,
        max_depth=2,
        allowed_domains=['example.com', 'example.org']
    )
    
    start_urls = [
        'https://example.com',
        'https://example.org'
    ]
    
    async with WebCrawler(config) as crawler:
        await crawler.crawl(start_urls)
        await crawler.save_results('multiple_sites_results.json')
        
        print(f"爬取完成！共处理 (Completed! Processed): {len(crawler.results)} 个页面 (pages)")


if __name__ == '__main__':
    print("高性能Web爬虫示例 (High-Performance Web Crawler Example)")
    print("=" * 50)
    
    # 运行示例1：爬取单个网站 (Run example 1: Crawl single website)
    asyncio.run(crawl_example_site())
    
    # 取消注释以运行示例2：爬取多个网站 (Uncomment to run example 2: Crawl multiple websites)
    # asyncio.run(crawl_multiple_sites())
