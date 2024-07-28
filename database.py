import configparser
import psycopg2
from psycopg2 import OperationalError, sql

class Database:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.host = config['database']['host']
        self.user = config['database']['user']
        self.password = config['database']['password']
        self.port = config['database']['port']
        self.dbname = config['database']['dbname']

        self.cur = None
        self.conn = None

    def establish_connection(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.cur = self.conn.cursor()
            print("Connection established successfully.")
        except psycopg2.Error as e:
            print("Error:", e)
            raise

    def close_connection(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
        print("Connection closed successfully.")

db = Database()

try:
    db.establish_connection()
    db.cur.execute("SELECT name, color, tail_length FROM cats")
    results = db.cur.fetchall()
    for row in results:
        print(row)
except psycopg2.Error as e:
    print("Error executing query:", e)
finally:
    db.close_connection()