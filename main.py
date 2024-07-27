from database import connect

if __name__ == '__main__':
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT * FROM cats LIMIT 2;')
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()



    docker run --name \
-e POSTGRES_DB=wg_forge_db \
-e POSTGRES_USER=wg_forge \
-e POSTGRES_PASSWORD=42a \
 -p 5433:5432 \
-d postgres