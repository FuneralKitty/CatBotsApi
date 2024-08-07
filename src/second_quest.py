import psycopg
from second_quest_arithmetic import *

def save_stats(cursor, stats):
    cursor.execute("""
    INSERT INTO cats_stat( 
        tail_length_mean, tail_length_median, tail_length_mode,
        whiskers_length_mean, whiskers_length_median, whiskers_length_mode
    ) VALUES (
        %s, %s, %s, %s, %s, %s
    )
    """, stats)

def second_quest():
    try:
        with psycopg.connect(database='wg_forge_db', user='wg_forge', password='42a', port='5432') as connection:
            with connection.cursor() as cursor:
                # Длина хвоста
                tail_length_mean = mean(cursor, 'tail_length')
                tail_length_median = mediana(cursor, 'tail_length')
                tail_length_mode = mode(cursor, 'tail_length')

                # Длина усов
                whiskers_length_mean = mean(cursor, 'whiskers_length')
                whiskers_length_median = mediana(cursor, 'whiskers_length')
                whiskers_length_mode = mode(cursor, 'whiskers_length')

                # Сохранение данных в таблицу
                save_stats(cursor, (
                    tail_length_mean, tail_length_median, [tail_length_mode],
                    whiskers_length_mean, whiskers_length_median, [whiskers_length_mode]
                ))

                # Подтвердить изменения
                connection.commit()

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    second_quest()