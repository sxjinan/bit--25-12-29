# 高性能Web爬虫使用指南
# High-Performance Web Crawler Usage Guide

## 目录 (Table of Contents)

1. [快速开始](#快速开始-quick-start)
2. [核心概念](#核心概念-core-concepts)
3. [配置详解](#配置详解-configuration-details)
4. [自定义爬虫](#自定义爬虫-custom-crawler)
5. [最佳实践](#最佳实践-best-practices)
6. [常见问题](#常见问题-faq)
7. [性能调优](#性能调优-performance-tuning)

---

## 快速开始 (Quick Start)

### 1. 安装依赖 (Install Dependencies)

```bash
pip install -r requirements.txt
```

### 2. 基本使用示例 (Basic Usage Example)

```python
import asyncio
from crawler import WebCrawler, CrawlerConfig

async def main():
    # 创建配置
    config = CrawlerConfig(
        max_concurrent_requests=10,
        max_depth=2,
        allowed_domains=['example.com']
    )
    
    # 运行爬虫
    async with WebCrawler(config) as crawler:
        await crawler.crawl(['https://example.com'])
        await crawler.save_results('results.json')

asyncio.run(main())
```

### 3. 运行示例脚本 (Run Example Scripts)

```bash
# 基础示例
python example_usage.py

# 高级示例
python advanced_example.py

# 运行测试
python test_crawler.py
```

---

## 核心概念 (Core Concepts)

### 异步爬取 (Asynchronous Crawling)

爬虫使用Python的`asyncio`和`aiohttp`实现异步并发请求，可以同时处理多个URL，显著提升爬取速度。

The crawler uses Python's `asyncio` and `aiohttp` for asynchronous concurrent requests, allowing multiple URLs to be processed simultaneously, significantly improving crawl speed.

### URL队列管理 (URL Queue Management)

- **去重**: 自动过滤重复的URL
- **深度控制**: 限制爬取深度，避免无限爬取
- **状态追踪**: 跟踪URL的访问状态（待访问、进行中、已访问）

- **Deduplication**: Automatically filters duplicate URLs
- **Depth Control**: Limits crawl depth to avoid infinite crawling
- **State Tracking**: Tracks URL visit status (pending, in-progress, visited)

### 速率限制 (Rate Limiting)

内置速率限制器确保请求之间有适当的延迟，避免对目标服务器造成过大负担。

Built-in rate limiter ensures appropriate delays between requests to avoid overloading target servers.

---

## 配置详解 (Configuration Details)

### CrawlerConfig 类

```python
config = CrawlerConfig(
    max_concurrent_requests=10,    # 最大并发请求数
    request_timeout=30,            # 请求超时时间（秒）
    max_retries=3,                 # 失败重试次数
    delay_between_requests=1.0,    # 请求间隔（秒）
    user_agent="CustomCrawler/1.0",# User-Agent字符串
    respect_robots_txt=True,       # 是否遵守robots.txt
    max_depth=3,                   # 最大爬取深度
    allowed_domains=['example.com']# 允许的域名列表
)
```

### 参数说明 (Parameter Details)

#### max_concurrent_requests
- **默认值**: 10
- **建议范围**: 5-20
- **说明**: 控制并发请求数量。过高可能导致被封禁，过低则爬取速度慢。

#### request_timeout
- **默认值**: 30秒
- **建议范围**: 10-60秒
- **说明**: 单个请求的超时时间。根据目标网站响应速度调整。

#### max_retries
- **默认值**: 3
- **建议范围**: 2-5
- **说明**: 请求失败后的重试次数。使用指数退避策略。

#### delay_between_requests
- **默认值**: 1.0秒
- **建议范围**: 0.5-5.0秒
- **说明**: 请求之间的延迟。礼貌爬取的关键参数。

#### max_depth
- **默认值**: 3
- **建议范围**: 1-10
- **说明**: 从起始URL开始的最大爬取深度。深度0表示只爬取起始URL。

---

## 自定义爬虫 (Custom Crawler)

### 自定义数据提取

```python
from crawler import WebCrawler, CrawlerConfig
from bs4 import BeautifulSoup
from typing import Dict

class MyCustomCrawler(WebCrawler):
    def extract_data(self, html: str, url: str) -> Dict:
        """自定义数据提取逻辑"""
        soup = BeautifulSoup(html, 'lxml')
        
        # 提取特定元素
        title = soup.find('h1')
        price = soup.find('span', class_='price')
        
        return {
            'url': url,
            'title': title.get_text() if title else '',
            'price': price.get_text() if price else '',
            'custom_field': 'custom_value'
        }

# 使用自定义爬虫
config = CrawlerConfig()
async with MyCustomCrawler(config) as crawler:
    await crawler.crawl(['https://example.com'])
```

### 自定义链接过滤

```python
class FilteredCrawler(WebCrawler):
    def extract_links(self, html: str, base_url: str) -> List[str]:
        """只提取特定类型的链接"""
        links = super().extract_links(html, base_url)
        
        # 只保留包含'product'的URL
        filtered_links = [
            link for link in links 
            if 'product' in link.lower()
        ]
        
        return filtered_links
```

---

## 最佳实践 (Best Practices)

### 1. 礼貌爬取 (Polite Crawling)

```python
# ✅ 好的做法
config = CrawlerConfig(
    max_concurrent_requests=5,     # 适度的并发
    delay_between_requests=1.0,    # 合理的延迟
    respect_robots_txt=True,       # 遵守robots.txt
    user_agent="YourBot/1.0 (contact@example.com)"
)

# ❌ 不好的做法
config = CrawlerConfig(
    max_concurrent_requests=100,   # 过高的并发
    delay_between_requests=0.01,   # 几乎无延迟
    respect_robots_txt=False       # 不遵守规则
)
```

### 2. 域名限制 (Domain Restriction)

```python
# 限制只爬取特定域名
config = CrawlerConfig(
    allowed_domains=['example.com', 'www.example.com']
)
```

### 3. 深度控制 (Depth Control)

```python
# 浅层爬取：只爬取主页和一级链接
config = CrawlerConfig(max_depth=1)

# 深层爬取：探索更深的链接
config = CrawlerConfig(max_depth=5)
```

### 4. 错误处理 (Error Handling)

```python
import logging

# 配置日志级别
logging.basicConfig(level=logging.INFO)

# 爬虫会自动处理错误并记录日志
async with WebCrawler(config) as crawler:
    try:
        await crawler.crawl(start_urls)
    except Exception as e:
        print(f"爬取失败: {e}")
```

### 5. 结果保存 (Saving Results)

```python
# 保存为JSON
await crawler.save_results('results.json')

# 如果使用高级爬虫，还可以保存为CSV
crawler.export_to_csv('results.csv')
```

---

## 常见问题 (FAQ)

### Q1: 爬虫速度太慢怎么办？

**A:** 可以尝试：
1. 增加`max_concurrent_requests`（建议不超过20）
2. 减少`delay_between_requests`（注意不要太激进）
3. 减少`max_depth`，只爬取需要的深度
4. 优化`extract_data`方法，减少处理时间

### Q2: 如何避免被目标网站封禁？

**A:** 
1. 设置合理的`delay_between_requests`（至少1秒）
2. 使用适当的`user_agent`
3. 遵守`robots.txt`
4. 限制并发数量
5. 考虑使用代理IP（需自行实现）

### Q3: 如何爬取需要登录的网站？

**A:** 需要自定义爬虫并添加cookie或session管理：

```python
class AuthCrawler(WebCrawler):
    async def __aenter__(self):
        headers = {
            'User-Agent': self.config.user_agent,
            'Cookie': 'your_session_cookie_here'
        }
        timeout = aiohttp.ClientTimeout(total=self.config.request_timeout)
        self.session = aiohttp.ClientSession(headers=headers, timeout=timeout)
        return self
```

### Q4: 如何处理JavaScript渲染的页面？

**A:** 当前爬虫只能处理静态HTML。对于JavaScript渲染的页面，需要：
1. 使用Selenium或Playwright
2. 或分析网站的API请求，直接请求API

### Q5: 如何提取特定的数据？

**A:** 继承`WebCrawler`类并重写`extract_data`方法：

```python
class CustomCrawler(WebCrawler):
    def extract_data(self, html: str, url: str) -> Dict:
        soup = BeautifulSoup(html, 'lxml')
        
        # 根据你的需求提取数据
        data = {
            'url': url,
            'title': soup.find('h1').get_text(),
            # ... 更多字段
        }
        
        return data
```

---

## 性能调优 (Performance Tuning)

### 场景1: 快速爬取小型网站

```python
config = CrawlerConfig(
    max_concurrent_requests=15,
    delay_between_requests=0.3,
    max_depth=3
)
```

### 场景2: 大规模数据采集

```python
config = CrawlerConfig(
    max_concurrent_requests=10,
    delay_between_requests=1.0,
    max_depth=5,
    request_timeout=45
)
```

### 场景3: 谨慎爬取

```python
config = CrawlerConfig(
    max_concurrent_requests=3,
    delay_between_requests=2.0,
    max_depth=2,
    respect_robots_txt=True
)
```

### 性能监控

```python
import time

start_time = time.time()

async with WebCrawler(config) as crawler:
    await crawler.crawl(start_urls)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"爬取用时: {duration:.2f}秒")
    print(f"平均速度: {len(crawler.results)/duration:.2f} 页/秒")
```

---

## 注意事项 (Important Notes)

1. **法律合规**: 确保你的爬取行为符合当地法律法规
2. **服务条款**: 遵守目标网站的服务条款
3. **robots.txt**: 尊重网站的robots.txt协议
4. **负载**: 不要对网站造成过大负担
5. **数据使用**: 合理使用爬取的数据，尊重版权

---

## 技术支持 (Technical Support)

如有问题，请：
1. 查看本文档
2. 运行测试脚本验证环境
3. 查看日志输出
4. 提交Issue

---

**版本**: 1.0  
**更新日期**: 2025-12-29  
**项目**: 北京理工大学小学期高性能Web爬虫
