import psycopg2
from config import *


def fill_cat_colors(cursor):
    cursor.execute("DELETE FROM cat_colors_info")
    cursor.execute("SELECT color, COUNT(*) as count FROM cats GROUP BY color")
    color_count = cursor.fetchall()
    return color_count


def insert_into_database(cursor, count: tuple):
    for color, num in count:
        cursor.execute(
            "INSERT INTO cat_colors_info (color, count) VALUES (%s, %s)", (color, num))


def main():
    try:
        with psycopg2.connect(database=database, user=user, password=password, port=port) as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT version()')

            with connection.cursor() as cursor:
                count = fill_cat_colors(cursor)
                insert_into_database(cursor, count)
                connection.commit()

    except psycopg2.Error as e:
        print(f"Database error: {e}")

    finally:
        if connection:
            connection.close()
            print('PostgreSQL connection is closed')

if __name__ == '__main__':
    main()