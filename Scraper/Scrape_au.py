import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter

async def main():
    # 1. Setup the Pruning Filter
    # We'll use the standard arguments supported by the latest version
    pruning_filter = PruningContentFilter(
        threshold=0.45, 
        threshold_type="fixed"
    )

    # 2. Setup Markdown Generator with the filter
    md_generator = DefaultMarkdownGenerator(content_filter=pruning_filter)

    # 3. Browser & Run Configuration
    browser_cfg = BrowserConfig(headless=True, verbose=True)
    run_cfg = CrawlerRunConfig(
        markdown_generator=md_generator,
        cache_mode=CacheMode.BYPASS  # Using the Enum for cleaner code
    )

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        # Targeting Air University (Update URL as needed)
        url = "https://www.au.edu.pk/" 
        
        print(f"--- Scraping {url} ---")
        result = await crawler.arun(url=url, config=run_cfg)

        if result.success:
            filename = "air_university_data.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(result.markdown)
            
            print(f"Success! Clean data saved to {filename}")
            # Show a little snippet of what we got
            print(f"Preview: {result.markdown[:200]}...")
        else:
            print(f"Failed to scrape. Error: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())