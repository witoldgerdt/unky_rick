#!/bin/bash

# Navigate to the project directory
cd /var/www/unky_rick

# Update the system and install necessary packages
sudo yum update -y
sudo yum install -y python3 python3-pip

# Install virtual environment if not already installed
pip3 install virtualenv

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    virtualenv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Django migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the Django server using Gunicorn (adjust as needed for your setup)
gunicorn --workers 3 --bind 0.0.0.0:8000 unky_rick.wsgi:application --daemon