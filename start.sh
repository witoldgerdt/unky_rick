#!/bin/bash

# Ensure PYTHONPATH includes the project directory
# export PYTHONPATH=$PYTHONPATH:/opt/render/project/src

# Set the DJANGO_SETTINGS_MODULE environment variable
# export DJANGO_SETTINGS_MODULE=unky_rick.settings

# Clear any cached Python files
# find . -name "*.pyc" -exec rm -f {} \;

# Start the server using Gunicorn in the background
echo "Starting applicatiion..."
gunicorn unky_rick.wsgi:application --config gunicorn.conf.py

# Wait for the server to be ready
# until curl -s http://localhost:$PORT/health_check; do
#   echo "Waiting for the server to be ready..."
#   sleep 5
# done

# Reset the test database
# python manage.py reset_test_db

# Start the scheduler in the background
# echo "Starting scheduler..."
# python analyze_platform/scheduler.py

# Run tests
pytest 
