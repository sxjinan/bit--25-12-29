#!/usr/bin/env python3
"""
Example usage script for the web crawler
"""

from crawler import WebCrawler
import json
import sys


def crawl_example_site():
    """Example: Crawl example.com"""
    print("Example 1: Crawling example.com")
    print("-" * 50)
    
    crawler = WebCrawler(
        start_url="http://example.com",
        max_depth=1,
        max_pages=10,
        max_workers=3,
        delay=1.0,
        respect_robots=True,
        same_domain_only=True
    )
    
    results = crawler.crawl()
    
    print(f"\nCrawled {len(results)} pages")
    for result in results:
        print(f"  - {result['url']} (Status: {result['status_code']})")
    
    return results


def crawl_with_custom_settings(url: str):
    """Example: Crawl with custom settings"""
    print(f"\nCrawling {url} with custom settings")
    print("-" * 50)
    
    crawler = WebCrawler(
        start_url=url,
        max_depth=2,
        max_pages=30,
        max_workers=5,
        delay=0.5,
        respect_robots=True,
        same_domain_only=True
    )
    
    results = crawler.crawl()
    
    # Display statistics
    stats = crawler.get_statistics()
    print("\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    return results


def save_results_to_json(results: list, filename: str = "crawl_results.json"):
    """Save crawl results to JSON file"""
    try:
        # Remove content field for smaller file size
        simplified_results = [
            {
                'url': r['url'],
                'status_code': r['status_code'],
                'size': r['size'],
                'depth': r['depth'],
                'content_type': r['content_type']
            }
            for r in results
        ]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(simplified_results, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to {filename}")
    except Exception as e:
        print(f"Error saving results: {e}")


def main():
    """Main function with examples"""
    print("="*60)
    print("Web Crawler Examples")
    print("="*60)
    
    # Example 1: Simple crawl
    results = crawl_example_site()
    
    # Save results
    if results:
        save_results_to_json(results, "example_results.json")
    
    # Example 2: Custom URL from command line
    if len(sys.argv) > 1:
        custom_url = sys.argv[1]
        print("\n" + "="*60)
        results = crawl_with_custom_settings(custom_url)
        if results:
            save_results_to_json(results, "custom_results.json")
    
    print("\n" + "="*60)
    print("Crawling completed!")
    print("="*60)


if __name__ == "__main__":
    main()
