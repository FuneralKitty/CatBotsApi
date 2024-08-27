#!/bin/bash

# Установка виртуального окружения
echo "Создаём виртуальное окружение..."
python3 -m venv venv

# Активация виртуального окружения
echo "Активируем виртуальное окружение..."
source venv/bin/activate

# Установка зависимостей
echo "Устанавливаем зависимости..."
pip install -r requirements.txt

# Настройка переменных окружения
echo "Настраиваем переменные окружения..."
export POSTGRES_DB=wg_forge_db
export POSTGRES_USER=wg_forge
export POSTGRES_PASSWORD=42a
export HOST=localhost
export PORT=5432
export FLASK_ENV=development

# Инициализация базы данных
echo "Создаём базу данных..."
psql -U $POSTGRES_USER -d postgres -c "CREATE DATABASE $POSTGRES_DB;"

# Применение SQL скрипта для инициализации данных
echo "Применяем SQL скрипт для инициализации данных..."
psql -U $POSTGRES_USER -d $POSTGRES_DB -f ./data.sql

# Запуск приложения
echo "Запускаем приложение..."
flask run --host=0.0.0.0 --port=8000 --reload