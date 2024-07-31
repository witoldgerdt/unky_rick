#!/bin/bash
cd /var/www/unky_rick
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=$(aws secretsmanager get-secret-value --secret-id arn:aws:secretsmanager:eu-central-1:211125541723:secret:prod/DATABASE_URL-aCWqmI --query SecretString --output text | jq -r ".database_url")
python manage.py migrate
python manage.py collectstatic --noinput
