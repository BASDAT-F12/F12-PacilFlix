import psycopg2
from psycopg2 import sql

# Fungsi untuk membuat koneksi ke database
def create_connection():
    conn = psycopg2.connect(
        # local vinka
        # dbname="vinka.alrezky",
        # user="postgres",
        # password="VeryVerySecret",
        # host="localhost"
        dbname="railway",
        user="postgres",
        password="ZLAWBQxRhNoDzvIaLJHXSjgVvzwFeqpx",
        host="monorail.proxy.rlwy.net",
        port="48577"
    )
    return conn

# Fungsi untuk mengeksekusi kueri tanpa hasil kembali
def execute_query(query, params=None):
    conn = create_connection()
    cur = conn.cursor()
    try:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def register_user(username, password, country):
    schema = "pacilflix"
    table = "pengguna"
    insert_query = sql.SQL("""
        INSERT INTO {}.{} (username, password, negara_asal) 
        VALUES (%s, %s, %s)
    """).format(sql.Identifier(schema), sql.Identifier(table))

    execute_query(insert_query, (username, password, country))

def login_user(username, password):
    schema = "pacilflix"
    table = "pengguna"
    select_query = sql.SQL("""
        SELECT * FROM {}.{} 
        WHERE username = %s AND password = %s
    """).format(sql.Identifier(schema), sql.Identifier(table))

    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute(select_query, (username, password))
        user = cur.fetchone()
        if user:
            return True  # Pengguna ditemukan, berhasil login
        else:
            return False  # Pengguna tidak ditemukan atau password salah
    except psycopg2.Error as e:
        raise e
    finally:
        cur.close()
        conn.close()
