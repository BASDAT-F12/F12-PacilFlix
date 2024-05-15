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
        
        #local farrel
        # dbname="paciflix",
        # user = "postgres",
        # password = "noovader1",
        # host="localhost",
        # port="5432"

        # database deployment
        dbname="postgres",
        user="postgres.witvydzeryxcceqwiqhn",
        password="FasilkomPacil22",
        host="aws-0-ap-southeast-1.pooler.supabase.com",
        port="5432"
    )
    return conn

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
            return True  # Pengguna not found, login successfull
        else:
            return False  # Pengguna not found or password is wrong
    except psycopg2.Error as e:
        raise e
    finally:
        cur.close()
        conn.close()
