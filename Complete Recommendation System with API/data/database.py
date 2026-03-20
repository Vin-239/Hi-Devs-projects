import sqlite3

DB_FILE = "rec_sys.db"

def get_conn():
    # standard sqlite connection, row_factory makes it behave like dicts
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row 
    return conn