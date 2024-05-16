import psycopg2
from psycopg2 import sql

def get_db_connection():
    connection = psycopg2.connect(
    #     dbname="pacilflix",
    #     user="postgres",
    #     password = "noovader1",
    #     host="localhost",
    #     port="5432")
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

### DAFTAR TAYANGAN 
def get_top10_tayangan_global():
    schema = "pacilflix"
    select_query = sql.SQL("""
    WITH recent_views AS (
		SELECT 
			rn.id_tayangan,
			rn.username,
			rn.start_date_time,
			rn.end_date_time,
			COALESCE(f.durasi_film, e.durasi, 0) AS durasi,
			EXTRACT(EPOCH FROM (rn.end_date_time - rn.start_date_time)) / 60 AS watched_minutes,
			COALESCE(f.durasi_film, e.durasi, 0) * 0.7 AS threshold_minutes
		FROM 
			{}.{} rn
		LEFT JOIN 
			{}.{} f ON rn.id_tayangan = f.id_tayangan
		LEFT JOIN 
			{}.{} e ON rn.id_tayangan = e.id_series
		LEFT JOIN 
			{}.{} t ON rn.id_tayangan = t.id
		WHERE 
			rn.start_date_time >= NOW() - INTERVAL '7 days'
    ),
	valid_views AS (
		SELECT
			id_tayangan,
			COUNT(*) AS view_count
		FROM
			recent_views
		WHERE
			watched_minutes >= threshold_minutes
		GROUP BY
			id_tayangan
	)
	SELECT 
		t.id,
		t.judul,
		t.sinopsis,
		t.asal_negara,
		t.sinopsis_trailer,
		t.url_video_trailer,
		t.release_date_trailer,
		COALESCE(f.url_video_film, '') AS url_video_film,
		COALESCE(f.release_date_film, NULL) AS release_date_film,
		COALESCE(e.sub_judul, '') AS episode_sub_judul,
		COALESCE(e.url_video, '') AS episode_url_video,
		COALESCE(e.release_date, NULL) AS episode_release_date,
		v.view_count
	FROM
		valid_views v
	LEFT JOIN
		{}.{} t ON v.id_tayangan = t.id
	LEFT JOIN
		{}.{} f ON t.id = f.id_tayangan
	LEFT JOIN
		{}.{} e ON t.id = e.id_series
	ORDER BY
		v.view_count DESC;
    LIMIT 10
	""")\
    .format(
        sql.Identifier(schema),sql.Identifier("riwayat_nonton"),
        sql.Identifier(schema),sql.Identifier("film"),
        sql.Identifier(schema),sql.Identifier("episode"),
        sql.Identifier(schema),sql.Identifier("tayangan"),
        sql.Identifier(schema),sql.Identifier("tayangan"),
        sql.Identifier(schema),sql.Identifier("film"),
        sql.Identifier(schema),sql.Identifier("episode")
    )
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(select_query)
        res = cur.fetchall()
        return [dict(row) for row in res]
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
    
def get_all_movies():
    schema = "pacilflix"
    select_query = sql.SQL(
        """ SELECT t.id, t.judul, t.sinopsis_trailer, t.url_video_trailer , t.release_date_trailer
            FROM {}.{} t
            JOIN {}.{} f ON t.id = f.id_tayangan""")\
        .format(
        sql.Identifier(schema), sql.Identifier("tayangan"),
        sql.Identifier(schema), sql.Identifier("film")
        )
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(select_query)
        films = cur.fetchall()
        return [{'id': film[0],'judul': film[1], 'sinopsis_trailer': film[2], 'url_video_trailer': film[3], 'release_date_trailer': film[4]} for film in films]
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
        
def get_all_series():
    schema = "pacilflix"
    select_query = sql.SQL(
        """ SELECT t.id, t.judul, t.sinopsis_trailer, t.url_video_trailer, t.release_date_trailer
            FROM {}.{} t
            JOIN {}.{} s ON t.id = s.id_tayangan
            """)\
            .format(
        sql.Identifier(schema), sql.Identifier("tayangan"),
        sql.Identifier(schema), sql.Identifier("series"),
        )
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(select_query)
        res = cur.fetchall()
        return [{'id': row[0], 'judul': row[1], 'sinopsis_trailer': row[2], 'url_video_trailer': row[3], 'release_date_trailer': row[4]} for row in res]
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

### DETAIL TAYANGAN

def get_detail_movie(id):
    pass

### PENCARIAN

def get_search_result(query): 
    schema = "pacilflix"
    select_query = sql.SQL(
        """ SELECT 
                id, judul, sinopsis_trailer, url_video_trailer, release_date_trailer
            FROM
                {}.{}
            WHERE
                LOWER(judul) LIKE LOWER({});
            """)\
            .format(
            sql.Identifier(schema), sql.Identifier("tayangan"),
            sql.Literal('%'+ query + '%')
        )
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(select_query)
        tayangans = cur.fetchall()
        return [{'id': tayangan[0], 'judul': tayangan[1], 'sinopsis_trailer': tayangan[2], 'url_video_trailer': tayangan[3], 'release_date_trailer': tayangan[4]} for tayangan in tayangans]
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

### ULASAN



### BAGIAN KONTRIBUTOR
