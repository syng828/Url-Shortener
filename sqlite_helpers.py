import sqlite3
import datetime

# SQL HELPER FUNCTIONS


def create_table(database: str):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    with conn:
        c.execute(""" CREATE TABLE IF NOT EXISTS urls
              (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              url TEXT,
              alias TEXT UNIQUE,
              timestamp TIME
              ) """)


def insert_url(database: str, url: str, alias: str):
    time = datetime.datetime.now()
    conn = sqlite3.connect(database)
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO urls (url, alias, timestamp) VALUES (?, ?, ?)", (
                  url, alias, time))


def delete_alias(database: str, alias: str):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    with conn:
        c.execute("DELETE from urls WHERE alias=?", (alias,))


def list_urls(database: str):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT * from urls")
    result = c.fetchall()
    db_array = []
    for row in result:
        data = {
            "id": row[0],
            "url": row[1],
            "alias": row[2],
            "created_at": row[3]
        }
        db_array.append(data)


def list_alias_url(database: str):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    with conn:
        c.execute("SELECT url alias from urls")
    return (c.fetchall())


def alias_to_url(database: str, alias: str):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    with conn:
        c.execute("SELECT url from urls WHERE alias=?", (alias,))
    return (c.fetchone())
