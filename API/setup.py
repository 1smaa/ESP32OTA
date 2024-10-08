import sqlite3

DB=sqlite3.connect("API/data/entities.db")
cursor=DB.cursor()
cursor.execute('''CREATE TABLE entities (
    id INTEGER, -- Not a key in this case
    digest CHAR(64) NOT NULL, -- SHA256 digests are 64 characters long in hex
    timestamp INTEGER NOT NULL, -- Storing timestamp as an integer (e.g., Unix timestamp)
    link TEXT NOT NULL -- Using TEXT for storing strings
);
''')
DB.commit()
cursor.close()
DB.close()