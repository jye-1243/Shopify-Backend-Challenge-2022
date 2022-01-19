import sqlite3

# Initialize database
# Source: https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()