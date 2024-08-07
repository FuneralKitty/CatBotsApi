from src.First_quest import first_quest
from src.second_quest import second_quest
from src.config import DB_CONFIG

#add all flask here


if __name__ == '__main__':
    #дописать выполнение скрипта
    #дописать что будет если уже существуют
    with psycopg.connect(**DB_CONFIG) as connection:
        with self.connection as cursor:
        cursor.execute(open("schema.sql", "r").read())
    first_quest()
    second_quest()