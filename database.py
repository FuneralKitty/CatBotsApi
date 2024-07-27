import configparser
import psycopg2

def get_db_config(filename='config.ini', section='database'):
    parser = configparser.ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db

def connect():
    config = get_db_config()
    conn = psycopg2.connect(**config)
    return conn