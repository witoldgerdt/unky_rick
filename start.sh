#!/bin/bash

# Start the server
# gunicorn unky_rick.wsgi:application --workers 3 --bind 0.0.0.0:$PORT &
# gunicorn unky_rick.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --log-level debug
gunicorn unky_rick.wsgi:application --config gunicorn.conf.py

# Wait for the server to be ready
until curl -s http://localhost:$PORT/health_check; do
  echo "Waiting for the server to be ready..."
  sleep 5
done

# Run tests
pytest
