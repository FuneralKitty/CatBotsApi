<<<<<<< HEAD
DB_CONFIG = {
    'dbname': 'wg_forge_db',
    'user': 'wg_forge',
    'password': '42a',
    'host': '192.168.0.111',
    'port': '5432'
}
=======
import os

DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': 'postgres',
    'port': '35432'
}
>>>>>>> dev
