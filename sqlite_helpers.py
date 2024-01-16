import sqlite3
import datetime
import logging
import time
from args import get_args
# SQL HELPER FUNCTIONS


args = get_args()


def create_table(database: str):
    logging.debug(f"Attempting to create table with SQLite in {database}")
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        with conn:
            c.execute(""" CREATE TABLE IF NOT EXISTS urls
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                url TEXT,
                alias TEXT UNIQUE,
                timestamp TIME
                ) """)
    except sqlite3.DatabaseError as e:
        logging.exception(f"SQLite database error inserting urls")
        raise
    except Exception as e:
        logging.exception(
            f"General exception creating table with sqlite with {database} database")
        raise


def insert_url(database: str, url: str, alias: str):
    logging.debug(
        f"Attempting to insert url with SQLite. Database: {database}, url: {url}, alias: {alias}")
    try:
        time = datetime.datetime.now()
        conn = sqlite3.connect(database)
        c = conn.cursor()
        with conn:
            c.execute("INSERT INTO urls (url, alias, timestamp) VALUES (?, ?, ?)", (
                url, alias, time))
    except sqlite3.DatabaseError as e:
        logging.exception(f"SQLite database error inserting urls")
        raise
    except Exception as e:
        logging.exception(
            f"General exception inserting url with sqlite.")
        raise


def delete_alias(database: str, alias: str):
    logging.debug(
        f"Attempting to delete alias with SQLite. Database: {database}, alias: {alias}")
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        with conn:
            c.execute("DELETE from urls WHERE alias=?", (alias,))
            return c.rowcount > 0
    except sqlite3.DatabaseError as e:
        logging.exception(f"SQLite database error inserting urls")
        raise
    except Exception as e:
        logging.exception(
            f"General exception deleting alias in sqlite")
        raise


def list_urls(database: str):
    logging.debug(f"Attempting to list urls with SQLite in {database}")
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        with conn:
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
            return db_array
    except sqlite3.DatabaseError as e:
        logging.exception(f"SQLite database error listing urls")
        raise
    except Exception as e:
        logging.exception(
            f"General exception listing urls in sqlite")
        raise


def list_alias_url(database: str):
    logging.debug(
        f"Attempting to list alias and urls with SQLite in {database}")
    conn = sqlite3.connect(database)
    c = conn.cursor()
    try:
        with conn:
            c.execute("SELECT url, alias from urls")
        result = c.fetchall()
        db_array = []
        for row in result:
            data = {
                "url": row[0],
                "alias": row[1],
            }
            db_array.append(data)
        return db_array
    except sqlite3.DatabaseError as e:
        logging.exception(
            f"SQLite database error listing alias and urls")
        raise
    except Exception as e:
        logging.exception(
            f"General exception listing url and alias in sqlite")
        raise


def alias_to_url(database: str, alias: str):
    logging.debug(f"Attempting to find url with alias {alias} in {database}")
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        with conn:
            c.execute("SELECT url from urls WHERE alias=?", (alias,))
        result = c.fetchone()
        if result:
            return (result[0])
        else:
            raise ValueError((f"No URL found for alias: {alias}"))
    except sqlite3.DatabaseError as e:
        logging.exception(f"SQLite database error finding alias")
        raise
    except Exception as e:
        logging.exception(
            f"General exception converting alias to url in sqlite")
        raise


logging.Formatter.converter = time.gmtime

logging.basicConfig(
    format="%(asctime)s.%(msecs)03dZ %(levelname)s:%(name)s:%(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=logging.ERROR - (args.verbose*10),
)
