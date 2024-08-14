import psycopg
from src.arithmetic_for_cats import *


def save_stats(cursor, stats):
    cursor.execute("""
    INSERT INTO cats_stat(
        tail_length_mean, tail_length_median, tail_length_mode,
        whiskers_length_mean, whiskers_length_median, whiskers_length_mode
    ) VALUES (
        %s, %s, %s, %s, %s, %s
    )
    """, stats)


def table_exists(cursor, table_name):
    cursor.execute("""
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_name = %s
    );
    """, (table_name,))
    return cursor.fetchone()[0]


def cat_colors_create_data(DB_CONFIG):
    connection = None

    try:
        with psycopg.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT version()')
                version = cursor.fetchone()
                print(f"PostgreSQL version: {version[0]}")

                cursor.execute("DELETE FROM cat_colors_info")

                cursor.execute("""
                    INSERT INTO cat_colors_info (color, count)
                    SELECT color, COUNT(*)
                    FROM cats
                    GROUP BY color
                """)

                connection.commit()

    except psycopg.Error as e:
        print(f"Database error: {e}")

    finally:
        if connection:
            connection.close()
            print('PostgreSQL connection is closed')


def fullfill_cat_options(DB_CONFIG):
    try:
        with psycopg.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                tail_length_mean = mean(cursor, 'tail_length')
                tail_length_median = mediana(cursor, 'tail_length')
                tail_length_mode = mode(cursor, 'tail_length')

                whiskers_length_mean = mean(cursor, 'whiskers_length')
                whiskers_length_median = mediana(cursor, 'whiskers_length')
                whiskers_length_mode = mode(cursor, 'whiskers_length')

                cursor.execute("DELETE FROM cats_stat")

                save_stats(
                    cursor,
                    (tail_length_mean,
                     tail_length_median,
                     [tail_length_mode],
                        whiskers_length_mean,
                        whiskers_length_median,
                        [whiskers_length_mode]))

                connection.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
