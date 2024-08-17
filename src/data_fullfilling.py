import psycopg
from typing import Optional, Any, List, Tuple, Dict
from src.arithmetic_for_cats import mean, mediana, mode

valid_attributes: List[str] = ['name', 'color', 'tail_length', 'whiskers_length']

def save_stats(cursor: psycopg.Cursor, stats: Tuple[float, float, List[float], float, float, List[float]]) -> None:
    cursor.execute("""
    INSERT INTO cats_stat(
        tail_length_mean, tail_length_median, tail_length_mode,
        whiskers_length_mean, whiskers_length_median, whiskers_length_mode
    ) VALUES (
        %s, %s, %s, %s, %s, %s
    )
    """, stats)

def table_exists(cursor: psycopg.Cursor, table_name: str) -> bool:
    cursor.execute("""
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_name = %s
    );
    """, (table_name,))
    return cursor.fetchone()[0]

def cat_colors_create_data(DB_CONFIG: Dict[str, Any]) -> None:
    connection: Optional[psycopg.Connection] = None

    try:
        with psycopg.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT version()')
                version: Tuple[str] = cursor.fetchone()
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

def fullfill_cat_options(DB_CONFIG: Dict[str, Any]) -> None:
    try:
        with psycopg.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                tail_length_mean: float = mean(cursor, 'tail_length')
                tail_length_median: float = mediana(cursor, 'tail_length')
                tail_length_mode: float = mode(cursor, 'tail_length')

                whiskers_length_mean: float = mean(cursor, 'whiskers_length')
                whiskers_length_median: float = mediana(cursor, 'whiskers_length')
                whiskers_length_mode: float = mode(cursor, 'whiskers_length')

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

def add_info_db(pool, data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT name FROM cats WHERE name = %s", (data['name'],))
                existing_cat: Optional[Tuple[str]] = cur.fetchone()

                if existing_cat:
                    return ({'error': 'Cat already exists'}, 409)

                cur.execute("""
                        INSERT INTO cats (name, color, tail_length, whiskers_length)
                        VALUES (%s, %s, %s, %s)
                    """, (data['name'], data['color'], data['tail_length'], data['whiskers_length']))
                conn.commit()
                return ({'message': 'Cat added successfully'}, 201)
    except Exception as e:
        return ({'error': str(e)}, 500)

def get_parsed_data(pool, attribute: str, order: str, offset: int, limit: int) -> Tuple[Dict[str, Any], int]:
    if attribute not in valid_attributes:
        return ({'error': 'Invalid attribute'}, 400)
    if order not in ['asc', 'desc']:
        return ({'error': 'Invalid order'}, 400)

    db_request: str = f"""
                SELECT name, color, tail_length, whiskers_length
                FROM cats
                ORDER BY {attribute} {order}
                OFFSET %s LIMIT %s
                """
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(db_request, (offset, limit))
                cats: List[Tuple[str, str, float, float]] = cur.fetchall()
                if not cats:
                    return ({'error': 'No cats found'}, 404)

                data: List[Dict[str, Any]] = [
                    {'name': cat[0], 'color': cat[1], 'tail_length': cat[2], 'whiskers_length': cat[3]}
                    for cat in cats
                ]
                return (data, 200)
    except Exception as e:
        return ({'error': str(e)}, 500)
