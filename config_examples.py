"""
配置示例文件
Configuration Example File

展示不同场景下的爬虫配置
Shows crawler configurations for different scenarios
"""

from crawler import CrawlerConfig


# 场景1: 快速爬取小型网站 (Scenario 1: Fast crawl of small website)
FAST_CRAWL_CONFIG = CrawlerConfig(
    max_concurrent_requests=20,      # 高并发 (High concurrency)
    request_timeout=15,               # 较短超时 (Short timeout)
    max_retries=2,                    # 较少重试 (Fewer retries)
    delay_between_requests=0.1,       # 短延迟 (Short delay)
    max_depth=3,
    user_agent="FastCrawler/1.0"
)


# 场景2: 礼貌爬取大型网站 (Scenario 2: Polite crawl of large website)
POLITE_CRAWL_CONFIG = CrawlerConfig(
    max_concurrent_requests=3,        # 低并发 (Low concurrency)
    request_timeout=30,               # 正常超时 (Normal timeout)
    max_retries=3,                    # 正常重试 (Normal retries)
    delay_between_requests=2.0,       # 长延迟 (Long delay)
    max_depth=5,
    respect_robots_txt=True,
    user_agent="PoliteCrawler/1.0 (Educational Purpose)"
)


# 场景3: 深度爬取特定域名 (Scenario 3: Deep crawl of specific domain)
DEEP_CRAWL_CONFIG = CrawlerConfig(
    max_concurrent_requests=10,
    request_timeout=30,
    max_retries=3,
    delay_between_requests=0.5,
    max_depth=10,                     # 深度爬取 (Deep crawl)
    allowed_domains=['example.com', 'www.example.com'],
    user_agent="DeepCrawler/1.0"
)


# 场景4: 新闻网站爬取 (Scenario 4: News website crawl)
NEWS_CRAWL_CONFIG = CrawlerConfig(
    max_concurrent_requests=5,
    request_timeout=30,
    max_retries=3,
    delay_between_requests=1.0,
    max_depth=2,                      # 浅层爬取 (Shallow crawl)
    allowed_domains=['news-site.com'],
    user_agent="NewsCrawler/1.0"
)


# 场景5: 电商网站爬取 (Scenario 5: E-commerce website crawl)
ECOMMERCE_CRAWL_CONFIG = CrawlerConfig(
    max_concurrent_requests=8,
    request_timeout=30,
    max_retries=5,                    # 更多重试 (More retries)
    delay_between_requests=1.5,
    max_depth=4,
    allowed_domains=['shop.com', 'www.shop.com'],
    user_agent="EcommerceCrawler/1.0"
)


# 场景6: 学术网站爬取 (Scenario 6: Academic website crawl)
ACADEMIC_CRAWL_CONFIG = CrawlerConfig(
    max_concurrent_requests=5,
    request_timeout=45,               # 长超时（学术网站可能较慢）(Long timeout)
    max_retries=3,
    delay_between_requests=2.0,       # 礼貌爬取 (Polite crawl)
    max_depth=3,
    respect_robots_txt=True,
    user_agent="AcademicCrawler/1.0 (Research Purpose)"
)


# 场景7: 测试/开发配置 (Scenario 7: Test/Development configuration)
DEV_CRAWL_CONFIG = CrawlerConfig(
    max_concurrent_requests=2,        # 低并发便于调试 (Low concurrency for debugging)
    request_timeout=10,
    max_retries=1,
    delay_between_requests=0.5,
    max_depth=1,                      # 最小深度 (Minimal depth)
    allowed_domains=['example.com'],
    user_agent="DevCrawler/1.0"
)


def get_config(scenario: str = 'default') -> CrawlerConfig:
    """
    根据场景获取配置 (Get configuration based on scenario)
    
    Args:
        scenario: 场景名称 (Scenario name)
                 可选值 (Options): 'fast', 'polite', 'deep', 'news', 
                                   'ecommerce', 'academic', 'dev'
    
    Returns:
        CrawlerConfig: 爬虫配置对象 (Crawler configuration object)
    """
    configs = {
        'fast': FAST_CRAWL_CONFIG,
        'polite': POLITE_CRAWL_CONFIG,
        'deep': DEEP_CRAWL_CONFIG,
        'news': NEWS_CRAWL_CONFIG,
        'ecommerce': ECOMMERCE_CRAWL_CONFIG,
        'academic': ACADEMIC_CRAWL_CONFIG,
        'dev': DEV_CRAWL_CONFIG
    }
    
    return configs.get(scenario, CrawlerConfig())


# 示例：如何使用配置 (Example: How to use configurations)
if __name__ == '__main__':
    import asyncio
    from crawler import WebCrawler
    
    async def demo():
        # 使用快速爬取配置 (Use fast crawl configuration)
        config = get_config('dev')  # 使用开发配置 (Use dev config)
        
        print(f"配置信息 (Configuration):")
        print(f"  并发数 (Concurrency): {config.max_concurrent_requests}")
        print(f"  超时时间 (Timeout): {config.request_timeout}秒")
        print(f"  最大深度 (Max depth): {config.max_depth}")
        print(f"  请求间隔 (Delay): {config.delay_between_requests}秒")
        
        # 创建爬虫实例 (Create crawler instance)
        async with WebCrawler(config) as crawler:
            print("\n爬虫已配置完成 (Crawler configured successfully)")
    
    asyncio.run(demo())
