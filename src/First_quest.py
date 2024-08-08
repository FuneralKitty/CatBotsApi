import psycopg


def table_exists(cursor, table_name):
    cursor.execute("""
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_name = %s
    );
    """, (table_name,))
    return cursor.fetchone()[0]


def first_quest(DB_CONFIG):
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


if __name__ == '__main__':
    first_quest()
