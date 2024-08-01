import psycopg2
from config import *


def main():
    try:
        # Connect to the PostgreSQL database
        with psycopg2.connect(database=database, user=user, password=password, port=port) as connection:
            with connection.cursor() as cursor:
                # Fetch the PostgreSQL version
                cursor.execute('SELECT version()')
                version = cursor.fetchone()
                print(f"PostgreSQL version: {version[0]}")

                # Delete existing records from cat_colors_info
                cursor.execute("DELETE FROM cat_colors_info")

                # Insert color count data into cat_colors_info
                cursor.execute("""
                    INSERT INTO cat_colors_info (color, count)
                    SELECT color, COUNT(*)
                    FROM cats
                    GROUP BY color
                """)

                # Commit the transaction
                connection.commit()

    except psycopg2.Error as e:
        print(f"Database error: {e}")

    finally:
        if connection:
            connection.close()
            print('PostgreSQL connection is closed')


if __name__ == '__main__':
    main()
