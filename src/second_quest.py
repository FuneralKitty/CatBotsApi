import psycopg
from second_quest_arithmetic import *
from config import DB_CONFIG


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
         with psycopg.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                tail_length_mean = mean(cursor, 'tail_length')
                tail_length_median = mediana(cursor, 'tail_length')
                tail_length_mode = mode(cursor, 'tail_length')

                whiskers_length_mean = mean(cursor, 'whiskers_length')
                whiskers_length_median = mediana(cursor, 'whiskers_length')
                whiskers_length_mode = mode(cursor, 'whiskers_length')

                cursor.execute("DELETE FROM cats_stat")

                save_stats(cursor, (
                    tail_length_mean, tail_length_median, [tail_length_mode],
                    whiskers_length_mean, whiskers_length_median, [whiskers_length_mode]
                ))

                connection.commit()

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    second_quest()