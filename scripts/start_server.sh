#!/bin/bash
cd /var/www/unky_rick
source venv/bin/activate
export DATABASE_URL=$(aws secretsmanager get-secret-value --secret-id DATABASE_URL --query SecretString --output text | jq -r ".database_url")
nohup python manage.py runserver 0.0.0.0:8000 &
