import sqlite3
import datetime

conn = sqlite3.connect(":memory:")

c = conn.cursor()

# SQL HELPER FUNCTIONS


def create_table():
    c.execute(""" CREATE TABLE IF NOT EXISTS urls
              (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              url TEXT,
              alias TEXT,
              timestamp TIME
              ) """)


def insert_url(url: str, alias: str):
    time = datetime.datetime.now()
    with conn:
        c.execute("INSERT INTO urls (url, alias, timestamp) VALUES (?, ?, ?)", (
                  url, alias, time))


def delete_url(url: str):
    with conn:
        c.execute("DELETE from urls WHERE url=?", (url,))


def delete_alias(alias: str):
    with conn:
        c.execute("DELETE from urls WHERE alias=?", (alias,))


def list_urls():
    c.execute("SELECT url from urls")
    print(c.fetchall())


def list_alias_url():
    c.execute("SELECT url, alias from urls")
    print(c.fetchall())


def alias_to_url(alias: str):
    c.execute("SELECT url from urls WHERE alias=?", (alias,))
    print(c.fetchone())


# TESTING
'''create_table()

insert_url("https://www.google.com/", "Google")
insert_url("https://github.com/", "GitHub")
insert_url("https://youtube.com/", "YouTube")
list_urls()  # Gives all urls

delete_url("https://www.google.com/")
list_urls()  # should not contain google.com

delete_alias("YouTube")
list_alias_url()  # should not contain youtube

alias_to_url("GitHub")  # should return github.com'''
