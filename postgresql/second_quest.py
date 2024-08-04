import psycopg2

def mean(cursor,param: str): #param for whiscers and tails
    cursor.execute(f"""SELECT AVG({param}) AS  
    avg_{param} FROM cats;""")

def mediana(cursor,param: str):
    cursor.execute(f"""SELECT PERCENTILE_CONT(0.5) WITHIN GROUP
    (ORDER BY {param}) AS {param} FROM cats; """)

def mode(cursor,param: str):
    cursor.execute(f"""SELECT {param} FROM(SELECT {param}, COUNT(*) AS
    count_{param}, RANK() OVER(ORDER BY COUNT(*) DESC) AS
    rank FROM cats GROUP BY {param}) AS ranked_{param}
    WHERE rank = 1;""")


