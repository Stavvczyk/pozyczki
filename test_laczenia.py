import psycopg2

conn = psycopg2.connect(
    host="dpg-d3pa50hr0fns73afnrd0-a.frankfurt-postgres.render.com",
    database="pozyczki_db",
    user="pozyczki_db_user",
    password="3Ez2JQS6c1GJVunGJ5dz0tcCpp9P0SvY",
    port="5432"
)

cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS pozyczki(
               id SERIAL PRIMARY KEY,
               osoba TEXT NOT NULL,
               kwota TEXT NOT NULL,
               typ TEXT NOT NULL,
               data TEXT NOT NULL
               );""")

conn.commit()

cursor.close()
conn.close()

print("gotowe!")