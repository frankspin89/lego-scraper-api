#!/bin/bash

# LEGO Scraper Installation Script
# This script sets up the LEGO scraper Docker environment on a new server

set -e

echo "===== LEGO Scraper Installation ====="
echo "This script will install Docker, Docker Compose, and set up the LEGO scraper application."

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
  echo "This script must be run as root"
  exit 1
fi

# Install Docker if not already installed
if ! command -v docker &> /dev/null; then
  echo "Installing Docker..."
  apt-get update
  apt-get install -y apt-transport-https ca-certificates curl software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
  add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
  apt-get update
  apt-get install -y docker-ce docker-ce-cli containerd.io
  systemctl enable docker
  systemctl start docker
  echo "Docker installed successfully"
else
  echo "Docker is already installed"
fi

# Install Docker Compose if not already installed
if ! command -v docker-compose &> /dev/null; then
  echo "Installing Docker Compose..."
  curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose
  echo "Docker Compose installed successfully"
else
  echo "Docker Compose is already installed"
fi

# Create application directory if it doesn't exist
APP_DIR="/opt/lego-scraper"

if [ ! -d "$APP_DIR" ]; then
  echo "Creating application directory at $APP_DIR..."
  mkdir -p "$APP_DIR"
fi

# Copy application files to the application directory
echo "Setting up application files..."
cd "$APP_DIR"

# Clone the repository if specified, or copy from current directory
if [ "$1" == "--clone" ] && [ -n "$2" ]; then
  REPO_URL="$2"
  echo "Cloning repository from $REPO_URL..."
  apt-get install -y git
  git clone "$REPO_URL" .
else
  echo "Please provide the path to your lego-scraper code or use --clone option with repository URL"
  exit 1
fi

# Create data directory structure
echo "Creating data directories..."
mkdir -p data/products data/raw data/images data/articles data/seo logs

# Create .env file from template if it doesn't exist
if [ ! -f .env ]; then
  echo "Creating .env file..."
  cat > .env << EOF
# Cloudflare R2 configuration
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_ACCESS_KEY_ID=your_access_key
CLOUDFLARE_SECRET_ACCESS_KEY=your_secret_key
CLOUDFLARE_R2_BUCKET=your_bucket_name
CLOUDFLARE_DOMAIN=your.domain.com

# OpenAI API configuration
OPENAI_API_KEY=your_openai_api_key
EOF
  echo "Please edit the .env file with your configuration"
fi

# Set file permissions
echo "Setting file permissions..."
chmod +x install.sh
chmod +x api.py

# Build and start the Docker containers
echo "Building and starting Docker containers..."
docker-compose up --build -d

# Show status of containers
echo "Checking service status..."
docker-compose ps

echo "Installation complete!"
echo "The API is now running at http://localhost:5000"
echo ""
echo "To check logs: docker-compose logs -f"
echo "To stop the service: docker-compose down"
echo ""
echo "Don't forget to update your .env file with the correct credentials!"