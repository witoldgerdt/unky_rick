#!/bin/bash

set -e

# Parse DATABASE_URL to extract components
DB_URL=$DATABASE_URL
DB_USER=$(echo $DB_URL | sed -e 's/^.*\/\/\(.*\):.*@.*$/\1/')
DB_PASSWORD=$(echo $DB_URL | sed -e 's/^.*\/\/.*:\(.*\)@.*$/\1/')
DB_HOST=$(echo $DB_URL | sed -e 's/^.*@\(.*\):.*\/.*$/\1/')
DB_PORT=$(echo $DB_URL | sed -e 's/^.*:\(.*\)\/.*$/\1/' -e 's/\/.*$//')
DB_NAME=$(echo $DB_URL | sed -e 's/^.*\/\(.*\)$/\1/')

PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "
CREATE TABLE IF NOT EXISTS data_status (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  status BOOLEAN NOT NULL DEFAULT TRUE
);
"
