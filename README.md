# LEGO Scraper API

This project provides a containerized API for the LEGO scraper workflow. It allows you to run scraping operations via HTTP endpoints, making it easy to integrate with n8n or other workflow automation tools.

## Features

- Dockerized API for LEGO scraper functions
- Asynchronous job processing with status tracking
- Cloudflare R2 integration for image storage
- Structured logging
- Easy installation on any server with Docker support

## API Endpoints

- `GET /health` - Health check endpoint
- `GET /jobs` - List all jobs
- `GET /jobs/<job_id>` - Get status of a specific job
- `POST /scrape` - Start scraping new products
- `POST /process-urls` - Process URLs from input file
- `POST /analyze` - Analyze raw data
- `POST /extract-data` - Extract additional data
- `POST /generate-seo` - Generate SEO content for a product
- `POST /generate-article` - Generate SEO article for a product
- `POST /optimize-images` - Optimize images for a product
- `GET /list-processed` - List processed URLs

## Installation

### Using the Installation Script

1. Clone this repository to your local machine:
   ```
   git clone https://github.com/frankspin89/lego-scraper-api.git
   ```

2. Upload to your server or run the installation script:
   ```
   sudo ./install.sh --clone https://github.com/frankspin89/lego-scraper-api.git
   ```

3. Edit the `.env` file with your credentials:
   ```
   nano /opt/lego-scraper/.env
   ```

### Manual Installation

1. Install Docker and Docker Compose on your server
2. Clone this repository
3. Create a `.env` file with your Cloudflare and OpenAI credentials
4. Run `docker-compose up -d`

## Usage with n8n

In n8n, you can create HTTP request nodes to trigger the scraper functions:

1. Add an HTTP Request node
2. Set method to POST (or GET for list operations)
3. Set URL to your server's address with the appropriate endpoint
4. Add JSON body for parameters (example: `{"product_id": "75077"}`)
5. Connect to other nodes in your workflow for processing results

## Environment Variables

- `CLOUDFLARE_ACCOUNT_ID` - Your Cloudflare account ID
- `CLOUDFLARE_ACCESS_KEY_ID` - Your Cloudflare access key
- `CLOUDFLARE_SECRET_ACCESS_KEY` - Your Cloudflare secret key
- `CLOUDFLARE_R2_BUCKET` - Your Cloudflare R2 bucket name
- `CLOUDFLARE_DOMAIN` - Your Cloudflare domain
- `OPENAI_API_KEY` - Your OpenAI API key

## Example API Requests

### Start a scraping job:
```bash
curl -X POST http://your-server:5000/scrape -H "Content-Type: application/json" -d '{"max_pages": 5}'
```

### Generate SEO content:
```bash
curl -X POST http://your-server:5000/generate-seo -H "Content-Type: application/json" -d '{"product_id": "75077"}'
```

### Check job status:
```bash
curl http://your-server:5000/jobs/1678901234
```