#!/bin/bash

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

export $(grep -v '^#' .env | xargs)

psql -U $POSTGRES_USER -d postgres -c "CREATE DATABASE $POSTGRES_DB;"

psql -U $POSTGRES_USER -d $POSTGRES_DB -f ./data.sql


flask run --host=0.0.0.0 --port=8000 --reload