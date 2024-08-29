import os
import dotenv

dotenv.load_dotenv()
DB_CONFIG = {
    "dsn_url": os.getenv("DSN"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": int(os.getenv("POSTGRES_PORT"))
}
for i in DB_CONFIG.items():
    print(type(i), i)
