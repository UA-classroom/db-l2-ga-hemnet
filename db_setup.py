import os

import psycopg2
#import psycopg2.extras
from psycopg2.extras import RealDictCursor

from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_NAME = os.getenv("DATABASE_NAME")
PASSWORD = os.getenv("PASSWORD")


def get_connection():
    """
    Function that returns a single connection
    In reality, we might use a connection pool, since
    this way we'll start a new connection each time
    someone hits one of our endpoints, which isn't great for performance
    """
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        user="postgres",  # change if needed
        password=PASSWORD,
        host="localhost",  # change if needed
        port="5432",  # change if needed
    )


def create_tables():
    """
    A function to create the necessary tables for the project.
    """
    con = get_connection()

    # Implement
    
  
    cur = con.cursor()
    # create tables
    with open("db_setup.sql", "r") as f:
        sql_commands = f.read()

    for command in sql_commands.split(";"):
        cmd = command.strip()
        if cmd:  # ignore empty commands
            cur.execute(cmd)

    #con.commit()
    #con.close()
    
    # insert basicdata
    with open("insert_base.sql", "r") as f:
        sql_commands = f.read()

    for command in sql_commands.split(";"):
        cmd = command.strip()
        if cmd:  # ignore empty commands
            cur.execute(cmd)

    con.commit()
    cur.close()
    con.close()
    

def get_items(con):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM items;")
            items = cursor.fetchall()
    return items 


if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")
