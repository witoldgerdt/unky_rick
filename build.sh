#!/usr/bin/env bash
set -o errexit  # Exit on error

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# A new migration to reflect any change
python manage.py makemigrations analyze_platform
python manage.py migrate analyze_platform

