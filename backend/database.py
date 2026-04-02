import psycopg2

def get_connection():
    conn = psycopg2.connect(
        dbname="anti_ragging_db",
        user="manjotsingh",
        password="",   # leave empty (since Homebrew default)
        host="localhost",
        port="5432"
    )
    return conn