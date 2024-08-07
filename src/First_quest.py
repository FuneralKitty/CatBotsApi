import psycopg
from config import *

def first_quest():
    connection = None  # Инициализируем переменную connection

    try:
        # Подключение к базе данных PostgreSQL
        with psycopg.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        ) as connection:
            with connection.cursor() as cursor:
                # Получаем версию PostgreSQL
                cursor.execute('SELECT version()')
                version = cursor.fetchone()
                print(f"PostgreSQL version: {version[0]}")

                # Удаляем существующие записи из cat_colors_info
                cursor.execute("DELETE FROM cat_colors_info")

                # Вставляем данные о количестве цветов в cat_colors_info
                cursor.execute("""
                    INSERT INTO cat_colors_info (color, count)
                    SELECT color, COUNT(*)
                    FROM cats
                    GROUP BY color
                """)

                # Фиксируем транзакцию
                connection.commit()

    except psycopg.Error as e:
        print(f"Database error: {e}")

    finally:
        if connection:
            connection.close()
            print('PostgreSQL connection is closed')


if __name__ == '__main__':
    first_quest()