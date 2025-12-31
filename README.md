# 高性能Web爬虫 / High-Performance Web Crawler

北京理工大学小学期高性能web爬虫实战

A concurrent web crawler implementation in Python with advanced features for efficient web scraping.

## Features

- **并发抓取 (Concurrent Fetching)**: Multi-threaded architecture for high-performance crawling
- **URL去重 (URL Deduplication)**: Efficient tracking of visited URLs
- **深度控制 (Depth Control)**: Configurable crawling depth
- **Robots.txt支持 (Robots.txt Compliance)**: Respects website crawling policies
- **域名过滤 (Domain Filtering)**: Option to restrict crawling to same domain
- **速率限制 (Rate Limiting)**: Configurable delay between requests
- **错误处理 (Error Handling)**: Robust error handling and logging
- **自定义请求头 (Custom Headers)**: User-agent and header customization

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sxjinan/bit--25-12-29.git
cd bit--25-12-29
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from crawler import WebCrawler

# Create a crawler instance
crawler = WebCrawler(
    start_url="http://example.com",
    max_depth=2,           # Maximum crawling depth
    max_pages=50,          # Maximum number of pages to crawl
    max_workers=5,         # Number of concurrent workers
    delay=0.5,             # Delay between requests (seconds)
    respect_robots=True,   # Respect robots.txt
    same_domain_only=True  # Only crawl same domain
)

# Start crawling
results = crawler.crawl()

# Get statistics
stats = crawler.get_statistics()
print(stats)
```

### Command Line Usage

Run the example script:
```bash
python example.py
```

Crawl a specific URL:
```bash
python example.py http://example.com
```

Run the main crawler:
```bash
python crawler.py
```

### Advanced Usage

```python
from crawler import WebCrawler

# Create crawler with custom settings
crawler = WebCrawler(
    start_url="https://example.com",
    max_depth=3,
    max_pages=100,
    max_workers=10,
    delay=1.0,
    respect_robots=True,
    same_domain_only=False,  # Crawl external links
    timeout=15
)

# Start crawling
results = crawler.crawl()

# Process results
for result in results:
    print(f"URL: {result['url']}")
    print(f"Status: {result['status_code']}")
    print(f"Size: {result['size']} bytes")
    print(f"Depth: {result['depth']}")
    print("-" * 50)
```

## Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `start_url` | str | Required | Starting URL for crawling |
| `max_depth` | int | 2 | Maximum depth to crawl |
| `max_pages` | int | 100 | Maximum number of pages to crawl |
| `max_workers` | int | 5 | Number of concurrent worker threads |
| `delay` | float | 0.5 | Delay between requests (seconds) |
| `respect_robots` | bool | True | Whether to respect robots.txt |
| `same_domain_only` | bool | True | Only crawl URLs from same domain |
| `timeout` | int | 10 | Request timeout (seconds) |

## Output

The crawler returns a list of dictionaries containing:
- `url`: The crawled URL
- `status_code`: HTTP status code
- `content`: Page HTML content
- `content_type`: Content-Type header
- `size`: Content size in bytes
- `depth`: Crawling depth level

## Logging

The crawler automatically creates a `crawler.log` file with detailed logging information including:
- URLs being crawled
- Errors and warnings
- Crawling progress
- Statistics

## Architecture

```
crawler.py
├── WebCrawler class
│   ├── URL Queue Management
│   ├── Worker Threads
│   ├── URL Deduplication
│   ├── Robots.txt Parser
│   └── Link Extraction
└── Main execution
```

## Requirements

- Python 3.6+
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.0
- urllib3 >= 2.0.0

## License

MIT License

## Contributors

Beijing Institute of Technology - Winter Semester Project

## Notes

- 请遵守网站的robots.txt和服务条款 (Please respect robots.txt and website terms of service)
- 合理设置爬取间隔,避免对目标服务器造成负担 (Set appropriate delays to avoid overloading servers)
- 仅用于学习和研究目的 (For educational and research purposes only)
