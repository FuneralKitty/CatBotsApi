#!/bin/bash

echo "Making venv..."
python3 -m venv venv
source venv/bin/activate

python3 -m pip install --upgrade pip
pip3 install -r requirements.txt


su postgres -c "psql -c \"CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';\""
su postgres -c "psql -c \"CREATE DATABASE $POSTGRES_DB;\""
su postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;\""

# Выполнение SQL-скрипта инициализации
echo "Выполнение SQL-скрипта инициализации..."
psql --host=localhost --port=5432 --dbname=$POSTGRES_DB --username=$POSTGRES_USER --password --file=data.sql

echo "Настройка базы данных завершена."