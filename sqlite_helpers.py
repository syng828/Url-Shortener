import sqlite3
import datetime

# SQL HELPER FUNCTIONS


def create_connection():
    return sqlite3.connect("urls.db")


def create_table():
    conn = create_connection()
    c = conn.cursor()
    with conn:
        c.execute(""" CREATE TABLE IF NOT EXISTS urls
              (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              url TEXT,
              alias TEXT,
              timestamp TIME
              ) """)


def insert_url(url: str, alias: str):
    time = datetime.datetime.now()
    conn = create_connection()
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO urls (url, alias, timestamp) VALUES (?, ?, ?)", (
                  url, alias, time))


def delete_url(url: str):
    conn = create_connection()
    c = conn.cursor()
    with conn:
        c.execute("DELETE from urls WHERE url=?", (url,))


def delete_alias(alias: str):
    conn = create_connection()
    c = conn.cursor()
    with conn:
        c.execute("DELETE from urls WHERE alias=?", (alias,))


def list_urls():
    conn = create_connection()
    c = conn.cursor()
    with conn:
        c.execute("SELECT url from urls")
    return (c.fetchall())


def list_alias_url():
    conn = create_connection()
    c = conn.cursor()
    with conn:
        c.execute("SELECT url alias from urls")
    return (c.fetchall())


def alias_to_url(alias: str):
    conn = create_connection()
    c = conn.cursor()
    with conn:
        c.execute("SELECT url from urls WHERE alias=?", (alias,))
    return (c.fetchone())


# TESTING
'''create_table(c)

insert_url("https://www.google.com/", "Google")
insert_url("https://github.com/", "GitHub")
insert_url("https://youtube.com/", "YouTube")
list_urls()  # Gives all urls

delete_url("https://www.google.com/")
list_urls()  # should not contain google.com

delete_alias("YouTube")
list_alias_url()  # should not contain youtube

alias_to_url("GitHub")  # should return github.com '''
