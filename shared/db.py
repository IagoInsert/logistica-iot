from contextlib import contextmanager
import mysql.connector
from mysql.connector import pooling
from shared.config import MYSQL_CONFIG

_pool = None

def get_pool():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(pool_name="logistica_pool", pool_size=8, **MYSQL_CONFIG)
    return _pool

@contextmanager
def get_conn():
    conn = get_pool().get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def fetch_one(query, params=None):
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params or ())
        row = cur.fetchone()
        cur.close()
        return row

def fetch_all(query, params=None):
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params or ())
        rows = cur.fetchall()
        cur.close()
        return rows

def execute(query, params=None):
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params or ())
        last_id = cur.lastrowid
        cur.close()
        return last_id
