import asyncio
import os
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy

async def deep_crawl_air_university():
    # 1. Browser Configuration
    browser_conf = BrowserConfig(
        headless=True, 
        verbose=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    # 2. Deep Crawl Strategy
    deep_strategy = BFSDeepCrawlStrategy(
        max_depth=2, 
        include_external=False,
        max_pages=100
    )

    # 3. Run Configuration
    run_conf = CrawlerRunConfig(
        deep_crawl_strategy=deep_strategy,
        cache_mode=CacheMode.BYPASS,
        semaphore_count=5,  # Prevents browser crashes
        page_timeout=60000, 
        stream=True         # This makes it return an async generator
    )

    print("--- Starting Deep Crawl from Zero ---")
    
    output_folder = "air_university_data"
    os.makedirs(output_folder, exist_ok=True)
    
    async with AsyncWebCrawler(config=browser_conf) as crawler:
        # We use 'async for' because stream=True returns an async_generator
        count = 0
        async for result in await crawler.arun(
            url="https://www.au.edu.pk/", 
            config=run_conf
        ):
            if result.success:
                count += 1
                filename = f"page_{count}.md"
                filepath = os.path.join(output_folder, filename)
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"# URL: {result.url}\n\n")
                    f.write(result.markdown)
                
                print(f"[{count}] Saved: {result.url}")
            else:
                print(f"Failed to crawl a page: {result.error_message}")

if __name__ == "__main__":
    try:
        asyncio.run(deep_crawl_air_university())
    except KeyboardInterrupt:
        print("\nScraping stopped by user.")