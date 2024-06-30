from contextlib import contextmanager
from psycopg_pool import ConnectionPool

dsn = "host=localhost dbname=identity_db user=identity_db password=postgres"
dbconn_pool = ConnectionPool(dsn, min_size=3)

@contextmanager
def dblock():
    with dbconn_pool.connection() as conn:
        try:
            with conn.cursor() as cur:
                yield cur
            conn.commit()
        except:
            conn.rollback()
            raise