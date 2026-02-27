import asyncio
import os
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter

async def main():
    # 1. Setup the "Filter" to remove noise (headers, footers, sidebars)
    # This ensures your RAG model only sees relevant university content.
    pruning_filter = PruningContentFilter(
        threshold=0.45,       # Higher = stricter filtering
        min_word_count=50,    # Ignore tiny snippets of text
        threshold_type="fixed"
    )

    # 2. Setup Markdown Generator
    md_generator = DefaultMarkdownGenerator(content_filter=pruning_filter)

    # 3. Browser & Run Configuration
    browser_cfg = BrowserConfig(headless=True, verbose=True)
    run_cfg = CrawlerRunConfig(
        markdown_generator=md_generator,
        cache_mode="bypass"  # Ensures you get fresh data
    )

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        # REPLACE THIS URL with your university's specific page (e.g., Admissions)
        url = "https://webdata.au.edu.pk/Pages/Admission/admission_schedule.aspx"
        
        print(f"--- Scraping {url} ---")
        result = await crawler.arun(url=url, config=run_cfg)

        if result.success:
            # Save the clean Markdown to a file
            filename = "university_data.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(result.markdown)
            
            print(f"Success! Clean data saved to {filename}")
            print(f"Content Length: {len(result.markdown)} characters")
        else:
            print(f"Failed to scrape. Error: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())