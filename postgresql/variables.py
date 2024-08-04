import psycopg2

средняя длина хвоста,
медиана длин хвостов,
мода длин хвостов,
средняя длина усов,
медиана длин усов,
мода длин усов

cats_stat:

Table "public.cats_stat"
         Column         |   Type
------------------------+-----------
 tail_length_mean       | numeric
 tail_length_median     | numeric
 tail_length_mode       | integer[]
 whiskers_length_mean   | numeric
 whiskers_length_median | numeric
 whiskers_length_mode   | integer[]

(mean), медиана (median) и мода (mode)