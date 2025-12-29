# 高性能Web爬虫 (High-Performance Web Crawler)

北京理工大学小学期高性能web爬虫实战项目

## 项目简介 (Project Overview)

这是一个基于Python异步编程的高性能Web爬虫框架，使用`asyncio`和`aiohttp`实现并发爬取，具有以下特点：

This is a high-performance web crawler framework based on Python asynchronous programming, using `asyncio` and `aiohttp` for concurrent crawling, with the following features:

### 主要特性 (Key Features)

- ✅ **异步并发** (Async Concurrency): 使用asyncio实现高并发请求，显著提升爬取速度
- ✅ **URL去重** (URL Deduplication): 自动去除重复URL，避免重复爬取
- ✅ **智能重试** (Smart Retry): 支持失败重试和指数退避策略
- ✅ **速率限制** (Rate Limiting): 内置速率限制器，实现礼貌爬取
- ✅ **深度控制** (Depth Control): 支持设置爬取深度，避免无限爬取
- ✅ **域名过滤** (Domain Filtering): 可限制只爬取特定域名
- ✅ **数据提取** (Data Extraction): 使用BeautifulSoup提取页面数据
- ✅ **结果保存** (Result Storage): 支持JSON格式保存爬取结果
- ✅ **错误处理** (Error Handling): 完善的异常处理和日志记录
- ✅ **可扩展性** (Extensibility): 易于继承和自定义数据提取逻辑

## 安装 (Installation)

### 1. 克隆项目 (Clone the project)

```bash
git clone https://github.com/sxjinan/bit--25-12-29.git
cd bit--25-12-29
```

### 2. 安装依赖 (Install dependencies)

```bash
pip install -r requirements.txt
```

## 快速开始 (Quick Start)

### 基本使用 (Basic Usage)

```python
import asyncio
from crawler import WebCrawler, CrawlerConfig

async def main():
    # 配置爬虫
    config = CrawlerConfig(
        max_concurrent_requests=10,  # 最大并发请求数
        request_timeout=30,           # 请求超时时间（秒）
        max_retries=3,                # 最大重试次数
        delay_between_requests=1.0,   # 请求间隔（秒）
        max_depth=2,                  # 最大爬取深度
        allowed_domains=['example.com']  # 限制爬取的域名
    )
    
    # 起始URL
    start_urls = ['https://example.com']
    
    # 运行爬虫
    async with WebCrawler(config) as crawler:
        await crawler.crawl(start_urls)
        await crawler.save_results('results.json')

if __name__ == '__main__':
    asyncio.run(main())
```

### 运行示例 (Run Examples)

项目包含了完整的示例代码：

```bash
python example_usage.py
```

## 配置说明 (Configuration)

### CrawlerConfig 参数 (Parameters)

| 参数 (Parameter) | 类型 (Type) | 默认值 (Default) | 说明 (Description) |
|-----------------|------------|----------------|-------------------|
| `max_concurrent_requests` | int | 10 | 最大并发请求数 (Max concurrent requests) |
| `request_timeout` | int | 30 | 请求超时时间（秒）(Request timeout in seconds) |
| `max_retries` | int | 3 | 最大重试次数 (Max retry attempts) |
| `delay_between_requests` | float | 1.0 | 请求间隔（秒）(Delay between requests) |
| `user_agent` | str | "HighPerformanceWebCrawler/1.0" | User-Agent字符串 |
| `respect_robots_txt` | bool | True | 是否遵守robots.txt (Whether to respect robots.txt) |
| `max_depth` | int | 3 | 最大爬取深度 (Max crawl depth) |
| `allowed_domains` | List[str] | [] | 允许爬取的域名列表 (List of allowed domains) |

## 高级用法 (Advanced Usage)

### 自定义数据提取 (Custom Data Extraction)

```python
from crawler import WebCrawler, CrawlerConfig
from bs4 import BeautifulSoup
from typing import Dict

class CustomCrawler(WebCrawler):
    def extract_data(self, html: str, url: str) -> Dict:
        """自定义数据提取逻辑"""
        soup = BeautifulSoup(html, 'lxml')
        
        # 提取特定数据
        title = soup.find('h1').get_text() if soup.find('h1') else ''
        
        return {
            'url': url,
            'title': title,
            'custom_field': 'custom_value'
        }

# 使用自定义爬虫
async with CustomCrawler(config) as crawler:
    await crawler.crawl(start_urls)
```

## 性能优化建议 (Performance Optimization Tips)

1. **调整并发数** (Adjust Concurrency): 根据目标网站和网络状况调整`max_concurrent_requests`
2. **合理设置延迟** (Set Reasonable Delay): 使用`delay_between_requests`避免触发反爬机制
3. **限制爬取深度** (Limit Depth): 使用`max_depth`控制爬取范围
4. **域名过滤** (Domain Filtering): 使用`allowed_domains`避免爬取无关网站
5. **异常处理** (Exception Handling): 确保网络异常不会导致整个爬虫崩溃

## 项目结构 (Project Structure)

```
bit--25-12-29/
├── crawler.py           # 核心爬虫实现
├── example_usage.py     # 使用示例
├── requirements.txt     # 项目依赖
├── .gitignore          # Git忽略文件
└── README.md           # 项目文档
```

## 技术栈 (Technology Stack)

- **Python 3.7+**: 编程语言
- **asyncio**: 异步I/O框架
- **aiohttp**: 异步HTTP客户端
- **BeautifulSoup4**: HTML解析
- **lxml**: 高性能XML/HTML解析器

## 注意事项 (Important Notes)

⚠️ **合法使用提醒** (Legal Usage Warning):

1. 请遵守目标网站的`robots.txt`协议
2. 请遵守网站的服务条款
3. 不要对网站造成过大负担
4. 尊重网站的知识产权
5. 仅用于学习和研究目的

Please:
- Respect the target website's `robots.txt` protocol
- Comply with the website's terms of service
- Do not overload the website
- Respect intellectual property rights
- Use for learning and research purposes only

## 许可证 (License)

本项目仅用于教育和学习目的。

This project is for educational and learning purposes only.

## 贡献 (Contributing)

欢迎提交Issue和Pull Request！

Issues and Pull Requests are welcome!

## 作者 (Author)

北京理工大学小学期项目 (Beijing Institute of Technology Short Semester Project)
