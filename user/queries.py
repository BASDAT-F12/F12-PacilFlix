import psycopg2
from psycopg2 import sql

def get_db_connection():
    connection = psycopg2.connect(
        # dbname="pacilflix",
        # user="postgres",
        # password = "noovader1",
        # host="localhost",
        # port="5432"
        # local vinka
        # dbname="vinka.alrezky",
        # user="postgres",
        # password="VeryVerySecret",
        # host="localhost",
        # port="5432"
        # database deployment
        dbname="postgres",
        user="postgres.witvydzeryxcceqwiqhn",
        password="FasilkomPacil22",
        host="aws-0-ap-southeast-1.pooler.supabase.com",
        port="5432"
    )
    return connection


def execute_query(query, params=None):
    conn = get_db_connection()
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


def get_all_packages():
        schema = "pacilflix"
        select_query = sql.SQL(
            """ SELECT p.nama, p.harga, p.resolusi_layar, ARRAY_AGG(d.dukungan_perangkat) AS dukungan_perangkat
                FROM {}.{} p
                JOIN {}.{} d ON p.nama = d.nama_paket
                GROUP BY p.nama, p.harga, p.resolusi_layar
            """).format(
            sql.Identifier(schema), sql.Identifier("paket"),
            sql.Identifier(schema), sql.Identifier("dukungan_perangkat")
        )
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(select_query)
            packages = cur.fetchall()
            return [{'nama': package[0], 'harga': package[1], 'resolusi_layar': package[2], 'dukungan_perangkat': ', '.join(package[3])} for package in packages]
        except psycopg2.Error as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()




def buy_package(username, package_name, method, timestamp):
    schema = "pacilflix"
    insert_query = sql.SQL(
        """ INSERT INTO {}.{} (username, nama_paket, metode_pembayaran, timestamp_pembayaran)
            VALUES (%s, %s, %s, %s)
        """).format(
        sql.Identifier(schema), sql.Identifier("transaction")
    )
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(insert_query, (username, package_name, method, timestamp))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def get_active_subscription(username):
    schema = "pacilflix"
    select_query = sql.SQL(
        """ SELECT p.nama, p.harga, p.resolusi_layar, d.dukungan_perangkat, t.start_date_time, t.end_date_time
            FROM {}.{} t
            JOIN {}.{} p ON t.nama_paket = p.nama
            JOIN {}.{} d ON p.nama = d.nama_paket
            WHERE t.username = %s AND t.end_date_time > CURRENT_DATE
        """).format(
        sql.Identifier(schema), sql.Identifier("transaction"),
        sql.Identifier(schema), sql.Identifier("paket"),
        sql.Identifier(schema), sql.Identifier("dukungan_perangkat")
    )
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(select_query, (username,))
        subscription_info = cur.fetchone()
        if subscription_info:
            return {
                'nama': subscription_info[0],
                'harga': subscription_info[1],
                'resolusi_layar': subscription_info[2],
                'dukungan_perangkat': subscription_info[3],
                'tanggal_dimulai': subscription_info[4],
                'tanggal_akhir': subscription_info[5]
            }
        else:
            return None
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def get_transaction_history(username):
    schema = "pacilflix"
    select_query = sql.SQL(
        """ SELECT p.nama, t.start_date_time, t.end_date_time, t.metode_pembayaran, t.timestamp_pembayaran, p.harga
            FROM {}.{} t
            JOIN {}.{} p ON t.nama_paket = p.nama
            WHERE t.username = %s
            ORDER BY t.start_date_time DESC
        """).format(
        sql.Identifier(schema), sql.Identifier("transaction"),
        sql.Identifier(schema), sql.Identifier("paket")
    )
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(select_query, (username,))
        transactions = cur.fetchall()
        return [
            {
                'nama': row[0],
                'tanggal_dimulai': row[1].strftime('%d/%m/%Y'),
                'tanggal_akhir': row[2].strftime('%d/%m/%Y'),
                'metode_pembayaran': row[3],
                'tanggal_pembayaran': row[4].strftime('%d/%m/%Y'),
                'total_pembayaran': f"{row[5]:,} IDR"
            }
            for row in transactions
        ]
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def get_package_by_name(package_name):
    schema = "pacilflix"
    select_query = sql.SQL(
        """ SELECT p.nama, p.harga, p.resolusi_layar, ARRAY_AGG(d.dukungan_perangkat) AS dukungan_perangkat
            FROM {}.{} p
            JOIN {}.{} d ON p.nama = d.nama_paket
            WHERE p.nama = %s
            GROUP BY p.nama, p.harga, p.resolusi_layar
        """).format(
        sql.Identifier(schema), sql.Identifier("paket"),
        sql.Identifier(schema), sql.Identifier("dukungan_perangkat")
    )
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(select_query, (package_name,))
        package = cur.fetchone()
        if package:
            return {
                'nama': package[0],
                'harga': f"{package[1]:,} IDR",
                'resolusi_layar': package[2],
                'dukungan_perangkat': ', '.join(package[3])
            }
        else:
            return None
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()




