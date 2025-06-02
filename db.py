import os
import psycopg2
from psycopg2.extras import RealDictCursor

PG_URL = os.getenv("PG_URL")

def query(sql, params=None):
    with psycopg2.connect(PG_URL) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchall()

