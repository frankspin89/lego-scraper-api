#!/usr/bin/env python3
"""
API server for the LEGO scraper workflow.
This provides HTTP endpoints to trigger the various scraper functions.
"""

import os
import json
import time
import logging
from datetime import datetime
from functools import wraps
from threading import Thread
from flask import Flask, request, jsonify

# Import the scraper functionality
# Assuming your main script is named main.py and has these functions
from main import (
    scrape_new_products,
    process_urls,
    analyze_raw_data,
    extract_additional_data,
    generate_seo_content,
    generate_seo_articles,
    optimize_images,
    list_processed_urls,
    setup_directories
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('logs', 'api.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Dictionary to store job status
jobs = {}

def async_task(f):
    """Decorator to run a function asynchronously with job tracking."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        job_id = str(int(time.time()))
        
        def task():
            jobs[job_id] = {
                "status": "running",
                "started_at": datetime.now().isoformat(),
                "function": f.__name__,
                "args": args,
                "kwargs": kwargs
            }
            
            try:
                result = f(*args, **kwargs)
                jobs[job_id]["status"] = "completed"
                jobs[job_id]["completed_at"] = datetime.now().isoformat()
                jobs[job_id]["result"] = result
            except Exception as e:
                logger.exception(f"Error in async task {job_id}: {str(e)}")
                jobs[job_id]["status"] = "failed"
                jobs[job_id]["error"] = str(e)
                jobs[job_id]["completed_at"] = datetime.now().isoformat()
        
        thread = Thread(target=task)
        thread.start()
        
        return jsonify({
            "job_id": job_id,
            "status": "started",
            "message": f"{f.__name__} job started"
        })
    
    return wrapped

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get the status of a specific job."""
    if job_id not in jobs:
        return jsonify({"error": "Job not found"}), 404
    
    return jsonify(jobs[job_id])

@app.route('/jobs', methods=['GET'])
def list_jobs():
    """List all jobs."""
    return jsonify(jobs)

@app.route('/scrape', methods=['POST'])
@async_task
def api_scrape_new_products():
    """Endpoint to start scraping new products."""
    data = request.json or {}
    max_pages = data.get('max_pages')
    
    logger.info(f"Starting scrape job with max_pages={max_pages}")
    result = scrape_new_products(max_pages)
    return result

@app.route('/process-urls', methods=['POST'])
@async_task
def api_process_urls():
    """Endpoint to process URLs."""
    data = request.json or {}
    max_workers = data.get('max_workers', 3)
    use_proxies = data.get('use_proxies', False)
    timeout = data.get('timeout', 30)
    
    logger.info(f"Starting process URLs job with max_workers={max_workers}, use_proxies={use_proxies}, timeout={timeout}")
    result = process_urls(max_workers, use_proxies, timeout)
    return result

@app.route('/analyze', methods=['POST'])
@async_task
def api_analyze_raw_data():
    """Endpoint to analyze raw data."""
    logger.info("Starting analysis job")
    result = analyze_raw_data()
    return result

@app.route('/extract-data', methods=['POST'])
@async_task
def api_extract_additional_data():
    """Endpoint to extract additional data."""
    logger.info("Starting data extraction job")
    result = extract_additional_data()
    return result

@app.route('/generate-seo', methods=['POST'])
@async_task
def api_generate_seo_content():
    """Endpoint to generate SEO content for a product."""
    data = request.json or {}
    product_id = data.get('product_id')
    
    if not product_id:
        return jsonify({"error": "Missing required parameter: product_id"}), 400
    
    logger.info(f"Starting SEO content generation for product_id={product_id}")
    result = generate_seo_content(product_id)
    return result

@app.route('/generate-article', methods=['POST'])
@async_task
def api_generate_seo_articles():
    """Endpoint to generate SEO articles for a product."""
    data = request.json or {}
    product_id = data.get('product_id')
    language = data.get('language', 'en')
    save_prompt_only = data.get('save_prompt_only', False)
    
    if not product_id:
        return jsonify({"error": "Missing required parameter: product_id"}), 400
    
    logger.info(f"Starting article generation for product_id={product_id}, language={language}")
    result = generate_seo_articles(product_id, language, save_prompt_only)
    return result

@app.route('/optimize-images', methods=['POST'])
@async_task
def api_optimize_images():
    """Endpoint to optimize images for a product."""
    data = request.json or {}
    product_id = data.get('product_id')
    upload_to_cloudflare = data.get('upload_to_cloudflare', False)
    
    if not product_id:
        return jsonify({"error": "Missing required parameter: product_id"}), 400
    
    logger.info(f"Starting image optimization for product_id={product_id}, upload_to_cloudflare={upload_to_cloudflare}")
    result = optimize_images(product_id, upload_to_cloudflare)
    return result

@app.route('/list-processed', methods=['GET'])
def api_list_processed():
    """Endpoint to list processed URLs."""
    logger.info("Listing processed URLs")
    result = list_processed_urls()
    return jsonify(result)

if __name__ == '__main__':
    # Ensure all directories exist
    setup_directories()
    
    # Start the Flask server
    app.run(host='0.0.0.0', port=5000)