def get_mean(cursor, param: str):
    query = "SELECT AVG(%s) AS avg_%s FROM cats;" % (param, param)
    cursor.execute(query)
    return cursor.fetchone()[0]


def get_mediana(cursor, param: str):
    query = "SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY %s) AS median_%s FROM cats; " % (param, param)
    cursor.execute(query)
    return cursor.fetchone()[0]


def get_mode(cursor, param: str):
    cursor.execute(
        f"""SELECT {param} FROM(
                        SELECT {param}, COUNT(*) AS count_{param},
                        RANK() OVER(ORDER BY COUNT(*) DESC) AS rank
                        FROM cats GROUP BY {param}) AS ranked_{param}
                        WHERE rank = 1;"""
    )
    return cursor.fetchone()[0]
