# CLAUDE.md - Agent Instructions

## Project Overview
- LEGO scraper workflow for collecting, processing, and optimizing product data and images
- Python-based ETL pipeline with Cloudflare R2 storage integration
- Environment variables required for Cloudflare configuration

## Command-Line Usage
- Run scraper: `python main.py --scrape [--max-pages N]`
- Process URLs: `python main.py --process-urls [--max-workers N] [--use-proxies] [--timeout N]`
- Analyze data: `python main.py --analyze`
- Extract data: `python main.py --extract-data`
- Generate SEO: `python main.py --generate-seo PRODUCT_ID`
- Generate article: `python main.py --generate-article PRODUCT_ID [--language en|nl] [--save-prompt-only]`
- Optimize images: `python main.py --optimize-images PRODUCT_ID [--upload-to-cloudflare]`
- List processed: `python main.py --list-processed`

## Code Style Guidelines
- Python 3.8+ with type hints (Optional, Dict, List)
- Use argparse for command-line arguments
- Structured error handling with try/except blocks and detailed error messages
- Comprehensive logging with print statements (consider structured logging)
- Environment variables for configuration (Cloudflare credentials, S3 settings)
- File organization: JSON for metadata storage, separate directories for products/images
- Function-based architecture with clear responsibilities
- Concurrent processing using ThreadPoolExecutor
- Robust file and directory handling with os.path functions