#!/bin/bash

# Start the server
gunicorn unky_rick.wsgi:application --config gunicorn.conf.py

# Start the scheduler in the background
python analyze_platform/scheduler.py &

# Wait for the server to be ready
until curl -s http://localhost:$PORT/health_check; do
  echo "Waiting for the server to be ready..."
  sleep 5
done

# Run tests
pytest
