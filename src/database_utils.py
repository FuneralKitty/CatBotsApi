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
