#!/bin/bash

set -e

# Install AWS CLI, jq for JSON parsing, and boto3 for Python
sudo yum update -y
sudo yum install -y aws-cli jq python3 python3-pip
pip3 install boto3 virtualenv

# Retrieve the DATABASE_URL from Secrets Manager using Python
cat <<EOF > get_database_url.py
import boto3
from botocore.exceptions import ClientError

def get_secret():
    secret_name = "prod/DATABASE_URL"
    region_name = "eu-central-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    return secret

if __name__ == "__main__":
    secret = get_secret()
    print(secret)
EOF

DATABASE_URL=$(python3 get_database_url.py)

# Set environment variables for database connection
export DATABASE_URL=$DATABASE_URL

# Navigate to the project directory
cd /var/www/unky_rick

# Set up virtual environment if it doesn't exist
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

# Start the Django server using Gunicorn
gunicorn --workers 3 --bind 0.0.0.0:8000 unky_rick.wsgi:application --daemon
