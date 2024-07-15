#!/bin/bash

# Start the server
gunicorn unky_rick.wsgi:application --config gunicorn.conf.py


# Wait for the server to be ready
until curl -s http://localhost:$PORT/health_check; do
  echo "Waiting for the server to be ready..."
  sleep 5
done

# Start the scheduler in the background
echo "Starting scheduler..."
nohup python path/to/scheduler.py &

# Run tests
pytest
