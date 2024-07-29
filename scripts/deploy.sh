#!/bin/bash

# Load environment variables
source /var/www/unky_rick/venv/bin/activate
export DATABASE_URL=$(aws secretsmanager get-secret-value --secret-id prod/DATABASE_URL --query SecretString --output text | jq -r '.url')

# Navigate to the project directory
cd /var/www/unky_rick

# Install dependencies if not already installed
pip install -r requirements.txt

# Restart the Gunicorn service
sudo systemctl restart gunicorn
