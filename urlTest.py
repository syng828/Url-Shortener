import sqlite3
import datetime

conn = sqlite3.connect(":memory:")

c = conn.cursor()

# SQL HELPER FUNCTIONS


def createTable():
    tableExists = "SELECT name FROM sqlite_master WHERE type='table' AND name='Urls'"
    if not conn.execute(tableExists).fetchone():
        c.execute(""" CREATE TABLE Urls
              (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              url TEXT,
              alias TEXT,
              timestamp TIME
              ) """)


def insertUrl(url: str, alias: str):
    time = datetime.datetime.now()
    with conn:
        c.execute("INSERT INTO Urls (url, alias, timestamp) VALUES (?, ?, ?)", (
                  url, alias, time))


def deleteUrl(url: str):
    with conn:
        c.execute("DELETE from Urls WHERE url=?", (url,))


def listUrls():
    c.execute("SELECT url from Urls")
    print(c.fetchall())


def aliasToUrl(alias: str):
    c.execute("SELECT url from Urls WHERE alias=?", (alias,))
    print(c.fetchone())


# TESTING
createTable()

insertUrl("https://www.google.com/", "Google")
insertUrl("https://github.com/", "GitHub")
insertUrl("https://youtube.com/", "YouTube")
listUrls()  # Gives all urls

deleteUrl("https://www.google.com/")
listUrls()  # should not contain google.com

aliasToUrl("GitHub")  # should return github.com
