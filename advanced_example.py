"""
高级示例：带有更多功能的爬虫
Advanced Example: Crawler with More Features

包括：
- CSV导出
- 统计分析
- 自定义过滤器
- 进度显示

Includes:
- CSV export
- Statistical analysis
- Custom filters
- Progress display
"""

import asyncio
import csv
from datetime import datetime
from typing import Dict, List
from crawler import WebCrawler, CrawlerConfig
from bs4 import BeautifulSoup


class AdvancedCrawler(WebCrawler):
    """高级爬虫，包含更多功能 (Advanced crawler with more features)"""
    
    def __init__(self, config: CrawlerConfig):
        super().__init__(config)
        self.stats = {
            'total_pages': 0,
            'successful_pages': 0,
            'failed_pages': 0,
            'total_links_found': 0
        }
    
    def extract_data(self, html: str, url: str) -> Dict:
        """增强的数据提取 (Enhanced data extraction)"""
        soup = BeautifulSoup(html, 'lxml')
        
        # 提取标题 (Extract title)
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No title"
        
        # 提取所有标题 (Extract all headings)
        headings = {
            'h1': [h.get_text().strip() for h in soup.find_all('h1')],
            'h2': [h.get_text().strip() for h in soup.find_all('h2')],
            'h3': [h.get_text().strip() for h in soup.find_all('h3')]
        }
        
        # 提取图片 (Extract images)
        images = [img.get('src', '') for img in soup.find_all('img')]
        
        # 提取链接数量 (Extract link count)
        links = soup.find_all('a', href=True)
        
        # 提取元数据 (Extract metadata)
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        keywords = meta_keywords.get('content', '') if meta_keywords else ''
        
        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description.get('content', '') if meta_description else ''
        
        # 提取文本内容 (Extract text content)
        text_content = soup.get_text(separator=' ', strip=True)
        
        # 更新统计 (Update statistics)
        self.stats['successful_pages'] += 1
        self.stats['total_links_found'] += len(links)
        
        return {
            'url': url,
            'title': title_text,
            'description': description,
            'keywords': keywords,
            'h1_count': len(headings['h1']),
            'h2_count': len(headings['h2']),
            'h3_count': len(headings['h3']),
            'h1_text': ', '.join(headings['h1'][:3]),  # 前3个h1标题
            'image_count': len(images),
            'link_count': len(links),
            'text_length': len(text_content),
            'crawled_at': datetime.now().isoformat()
        }
    
    def export_to_csv(self, filename: str = 'crawler_results.csv'):
        """导出结果到CSV (Export results to CSV)"""
        if not self.results:
            print("没有结果可导出 (No results to export)")
            return
        
        # 获取所有字段 (Get all fields)
        fieldnames = list(self.results[0].keys())
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)
        
        print(f"结果已导出到 (Results exported to): {filename}")
    
    def print_statistics(self):
        """打印详细统计信息 (Print detailed statistics)"""
        print("\n" + "=" * 60)
        print("爬取统计报告 (Crawling Statistics Report)")
        print("=" * 60)
        
        print(f"\n📊 基本统计 (Basic Statistics):")
        print(f"  - 成功爬取页面 (Successfully crawled pages): {self.stats['successful_pages']}")
        print(f"  - 访问过的URL (Visited URLs): {len(self.url_queue.visited)}")
        print(f"  - 发现的链接总数 (Total links found): {self.stats['total_links_found']}")
        
        if self.results:
            # 计算平均值 (Calculate averages)
            avg_text_length = sum(r.get('text_length', 0) for r in self.results) / len(self.results)
            avg_links = sum(r.get('link_count', 0) for r in self.results) / len(self.results)
            avg_images = sum(r.get('image_count', 0) for r in self.results) / len(self.results)
            
            print(f"\n📈 平均值统计 (Average Statistics):")
            print(f"  - 平均文本长度 (Average text length): {avg_text_length:.0f} 字符 (characters)")
            print(f"  - 平均链接数 (Average links per page): {avg_links:.1f}")
            print(f"  - 平均图片数 (Average images per page): {avg_images:.1f}")
            
            # 找出最长的页面 (Find longest page)
            longest_page = max(self.results, key=lambda x: x.get('text_length', 0))
            print(f"\n📄 最长的页面 (Longest page):")
            print(f"  - 标题 (Title): {longest_page.get('title', 'N/A')}")
            print(f"  - URL: {longest_page.get('url', 'N/A')}")
            print(f"  - 长度 (Length): {longest_page.get('text_length', 0)} 字符 (characters)")
        
        print("\n" + "=" * 60)


async def demo_advanced_crawl():
    """高级爬虫演示 (Advanced crawler demo)"""
    
    print("🚀 高性能Web爬虫 - 高级示例")
    print("🚀 High-Performance Web Crawler - Advanced Example")
    print("=" * 60)
    
    # 配置爬虫 (Configure crawler)
    config = CrawlerConfig(
        max_concurrent_requests=5,
        request_timeout=30,
        max_retries=3,
        delay_between_requests=0.5,
        max_depth=2,
        allowed_domains=['example.com']
    )
    
    # 起始URL (Starting URLs)
    start_urls = [
        'https://example.com'
    ]
    
    print(f"\n⚙️  配置信息 (Configuration):")
    print(f"  - 并发请求数 (Concurrent requests): {config.max_concurrent_requests}")
    print(f"  - 请求超时 (Request timeout): {config.request_timeout}秒 (seconds)")
    print(f"  - 最大深度 (Max depth): {config.max_depth}")
    print(f"  - 请求间隔 (Request delay): {config.delay_between_requests}秒 (seconds)")
    print(f"\n🎯 起始URL (Starting URLs): {start_urls}")
    print("\n开始爬取... (Starting crawl...)\n")
    
    # 创建并运行爬虫 (Create and run crawler)
    async with AdvancedCrawler(config) as crawler:
        await crawler.crawl(start_urls)
        
        # 保存结果 (Save results)
        await crawler.save_results('advanced_results.json')
        crawler.export_to_csv('advanced_results.csv')
        
        # 打印统计信息 (Print statistics)
        crawler.print_statistics()
        
        # 打印前几条结果示例 (Print first few results as example)
        if crawler.results:
            print("\n📋 结果示例 (Sample Results):")
            print("-" * 60)
            for i, result in enumerate(crawler.results[:3], 1):
                print(f"\n{i}. {result.get('title', 'No Title')}")
                print(f"   URL: {result.get('url', '')}")
                print(f"   描述 (Description): {result.get('description', 'N/A')[:100]}...")
                print(f"   H1标题 (H1 headings): {result.get('h1_count', 0)}")
                print(f"   链接数 (Links): {result.get('link_count', 0)}")
                print(f"   图片数 (Images): {result.get('image_count', 0)}")


async def demo_filtered_crawl():
    """演示带过滤器的爬取 (Demo crawl with filters)"""
    
    class FilteredCrawler(AdvancedCrawler):
        """带内容过滤的爬虫 (Crawler with content filtering)"""
        
        def extract_data(self, html: str, url: str) -> Dict:
            data = super().extract_data(html, url)
            
            # 只保存包含特定关键词的页面 (Only save pages with specific keywords)
            keywords_to_find = ['example', 'domain']
            
            title_lower = data.get('title', '').lower()
            if any(keyword in title_lower for keyword in keywords_to_find):
                data['matched_keyword'] = True
                return data
            else:
                data['matched_keyword'] = False
                return data
    
    config = CrawlerConfig(
        max_concurrent_requests=3,
        max_depth=1,
        delay_between_requests=1.0,
        allowed_domains=['example.com']
    )
    
    start_urls = ['https://example.com']
    
    print("\n" + "=" * 60)
    print("🔍 过滤爬取演示 (Filtered Crawl Demo)")
    print("=" * 60)
    
    async with FilteredCrawler(config) as crawler:
        await crawler.crawl(start_urls)
        
        # 只保存匹配的结果 (Only save matched results)
        matched_results = [r for r in crawler.results if r.get('matched_keyword')]
        
        print(f"\n总页面数 (Total pages): {len(crawler.results)}")
        print(f"匹配的页面 (Matched pages): {len(matched_results)}")


if __name__ == '__main__':
    # 运行高级爬虫演示 (Run advanced crawler demo)
    asyncio.run(demo_advanced_crawl())
    
    # 取消注释运行过滤爬取演示 (Uncomment to run filtered crawl demo)
    # asyncio.run(demo_filtered_crawl())
