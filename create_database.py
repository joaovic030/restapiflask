import sqlite3

connection = sqlite3.connect('banco.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id integer PRIMARY KEY, \
                name text, rating real, dailyvalue real, city text)"

create_hotel = "INSERT INTO hoteis VALUES (10, 'Hotel Amazonia', 3.2, 380, 'Rondonia')"

cursor.execute(create_table)
cursor.execute(create_hotel)

connection.commit()
connection.close()