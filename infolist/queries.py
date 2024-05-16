import psycopg2
from psycopg2 import sql

def get_db_connection():
    # connection = psycopg2.connect(
    #     dbname="pacilflix",
    #     user="postgres",
    #     password = "noovader1",
    #     host="localhost",
    #     port="5432"
        # local vinka
        # dbname="vinka.alrezky",
        # user="postgres",
        # password="VeryVerySecret",
        # host="localhost",
        # port="5432"
    #)
    # database deployment
    connection = psycopg2.connect(dbname="postgres",
        user="postgres.witvydzeryxcceqwiqhn",
        password="FasilkomPacil22",
        host="aws-0-ap-southeast-1.pooler.supabase.com",
        port="5432")
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
        
def get_top10_tayangan_lokal(country):
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
    WHERE
        t.asal_negara = {}
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
        sql.Identifier(schema),sql.Identifier("episode"),
        country
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
        """ SELECT t.id, t.judul, t.sinopsis, t.sinopsis_trailer, t.url_video_trailer , t.release_date_trailer
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
        return [{'id': film[0],'judul': film[1], 'sinopsis': film[2], 'sinopsis_trailer': film[3], 'url_video_trailer': film[4], 'release_date_trailer': film[5]} for film in films]
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
        
def get_all_series():
    schema = "pacilflix"
    select_query = sql.SQL(
        """ SELECT t.judul, t.sinopsis_trailer, t.url_video trailer, t.release_date_trailer
            FROM {}.{} t
            JOIN {}.{} s ON t.id = s.id_tayangan
            LEFT JOIN {}.{} e ON t.id_episode = e.id""")\
            .format(
        sql.Identifier(schema), sql.Identifier("tayangan"),
        sql.Identifier(schema), sql.Identifier("series"),
        sql.Identifier(schema), sql.Identifier("episode")
        )
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(select_query)
        res = cur.fetchall()
        return [dict(res) for series in res]
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



### ULASAN



### BAGIAN KONTRIBUTOR
