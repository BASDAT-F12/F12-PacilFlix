import uuid

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

### DAFTAR TAYANGAN
import psycopg2
from psycopg2 import sql

def get_top10_tayangan_global():
    schema = "pacilflix"
    select_query = sql.SQL("""
    WITH total_series_duration AS (
        SELECT 
            e.id_series,
            SUM(e.durasi) AS total_duration
        FROM 
            {}.{} e
        GROUP BY 
            e.id_series
    ),
    accumulated_watch_time AS (
        SELECT
            rn.id_tayangan,
            rn.username,
            SUM(EXTRACT(EPOCH FROM (rn.end_date_time - rn.start_date_time)) / 60) AS total_watch_time
        FROM
            {}.{} rn
        GROUP BY
            rn.id_tayangan, rn.username
    ),
    recent_views AS (
        SELECT 
            awt.id_tayangan,
            awt.username,
            COALESCE(f.durasi_film, tsd.total_duration, 0) AS durasi,
            awt.total_watch_time,
            COALESCE(f.durasi_film, tsd.total_duration, 0) * 0.7 AS threshold_minutes
        FROM 
            accumulated_watch_time awt
        LEFT JOIN 
            {}.{} f ON awt.id_tayangan = f.id_tayangan
        LEFT JOIN 
            {}.{} e ON awt.id_tayangan = e.id_series
        LEFT JOIN 
            {}.{} t ON awt.id_tayangan = t.id
        LEFT JOIN 
            total_series_duration tsd ON awt.id_tayangan = tsd.id_series
        WHERE 
            awt.total_watch_time >= COALESCE(f.durasi_film, tsd.total_duration, 0) * 0.7
    ),
    valid_views AS (
        SELECT
            id_tayangan,
            COUNT(*) AS view_count
        FROM
            recent_views
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
        STRING_AGG(DISTINCT e.sub_judul, ', ') AS episode_sub_judul,
        STRING_AGG(DISTINCT e.url_video, ', ') AS episode_url_video,
        STRING_AGG(DISTINCT e.release_date::text, ', ') AS episode_release_date,
        v.view_count,
        CASE
            WHEN f.id_tayangan IS NOT NULL THEN 'film'
            ELSE 'series'
        END AS type
    FROM
        valid_views v
    LEFT JOIN
        {}.{} t ON v.id_tayangan = t.id
    LEFT JOIN
        {}.{} f ON t.id = f.id_tayangan
    LEFT JOIN
        {}.{} e ON t.id = e.id_series
    GROUP BY
        t.id, t.judul, t.sinopsis, t.asal_negara, t.sinopsis_trailer, t.url_video_trailer, t.release_date_trailer, f.url_video_film, f.release_date_film, v.view_count, f.id_tayangan
    ORDER BY
        v.view_count DESC
    LIMIT 10;
    """).format(
        sql.Identifier(schema), sql.Identifier('episode'),
        sql.Identifier(schema), sql.Identifier('riwayat_nonton'),
        sql.Identifier(schema), sql.Identifier('film'),
        sql.Identifier(schema), sql.Identifier('episode'),
        sql.Identifier(schema), sql.Identifier('tayangan'),
        sql.Identifier(schema), sql.Identifier('tayangan'),
        sql.Identifier(schema), sql.Identifier('film'),
        sql.Identifier(schema), sql.Identifier('episode')
    )
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(select_query)
        res = cur.fetchall()
        return [{
            'id': str(row[0]),
            'judul': row[1],
            'sinopsis': row[2],
            'asal_negara': row[3],
            'sinopsis_trailer': row[4],
            'url_video_trailer': row[5],
            'release_date_trailer': row[6],
            'url_video_film': row[7],
            'release_date_film': row[8],
            'episode_sub_judul': row[9],
            'episode_url_video': row[10],
            'episode_release_date': row[11],
            'view_count': row[12],
            'type': row[13]
        } for row in res]
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def get_all_movies():
    schema = "pacilflix"
    select_query = sql.SQL(
        """ SELECT t.id, t.judul, t.sinopsis_trailer, t.url_video_trailer, t.release_date_trailer
            FROM {}.{} t
            JOIN {}.{} f ON t.id = f.id_tayangan""") \
        .format(
        sql.Identifier(schema), sql.Identifier("tayangan"),
        sql.Identifier(schema), sql.Identifier("film")
    )
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(select_query)
        films = cur.fetchall()
        return [{'id': str(film[0]), 'judul': film[1], 'sinopsis_trailer': film[2], 'url_video_trailer': film[3], 'release_date_trailer': film[4]} for film in films]
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
            """) \
        .format(
        sql.Identifier(schema), sql.Identifier("tayangan"),
        sql.Identifier(schema), sql.Identifier("series"),
    )
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(select_query)
        res = cur.fetchall()
        return [{'id': str(row[0]), 'judul': row[1], 'sinopsis_trailer': row[2], 'url_video_trailer': row[3], 'release_date_trailer': row[4]} for row in res]
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

### DETAIL TAYANGAN

def get_movie_data(id):
    schema = "pacilflix"
    select_query = sql.SQL(
        """ SELECT 
            t.id, 
            t.judul, 
            t.sinopsis, 
            t.asal_negara, 
            f.url_video_film, 
            f.release_date_film, 
            f.durasi_film,
            AVG(u.rating) AS average_rating,
            COUNT(DISTINCT rn.username) AS total_view_count,
            STRING_AGG(DISTINCT c1.nama, ', ') AS penulis_skenario,
            STRING_AGG(DISTINCT c2.nama, ', ') AS sutradara,
            STRING_AGG(DISTINCT c3.nama, ', ') AS pemain,
            STRING_AGG(DISTINCT gt.genre, ', ') AS genre
            FROM
                {}.{} t
            LEFT JOIN
                {}.{} f ON t.id = f.id_tayangan
            LEFT JOIN
                {}.{} u ON t.id = u.id_tayangan
            LEFT JOIN
                {}.{} rn ON t.id = rn.id_tayangan
            LEFT JOIN
                {}.{} mst ON t.id = mst.id_tayangan
            LEFT JOIN
                {}.{} ps ON mst.id_penulis_skenario = ps.id
            LEFT JOIN
                {}.{} c1 ON ps.id = c1.id
            LEFT JOIN
                {}.{} prt ON t.id = prt.id_tayangan
            LEFT JOIN
                {}.{} s ON t.id_sutradara = s.id
            LEFT JOIN
                {}.{} c2 ON s.id = c2.id
            LEFT JOIN
                {}.{} mtt ON t.id = mtt.id_tayangan
            LEFT JOIN
                {}.{} p ON mtt.id_pemain = p.id
            LEFT JOIN
                {}.{} c3 ON p.id = c3.id
            LEFT JOIN 
                {}.{} gt ON t.id = gt.id_tayangan
            WHERE
                t.id = %s
            GROUP BY
                t.id, t.asal_negara, f.url_video_film, f.release_date_film, f.durasi_film;
        """).format(
            sql.Identifier(schema), sql.Identifier('tayangan'),
            sql.Identifier(schema), sql.Identifier('film'),
            sql.Identifier(schema), sql.Identifier('ulasan'),
            sql.Identifier(schema), sql.Identifier('riwayat_nonton'),
            sql.Identifier(schema), sql.Identifier('menulis_skenario_tayangan'),
            sql.Identifier(schema), sql.Identifier('penulis_skenario'),
            sql.Identifier(schema), sql.Identifier('contributors'),
            sql.Identifier(schema), sql.Identifier('persetujuan'),
            sql.Identifier(schema), sql.Identifier('sutradara'),
            sql.Identifier(schema), sql.Identifier('contributors'),
            sql.Identifier(schema), sql.Identifier('memainkan_tayangan'),
            sql.Identifier(schema), sql.Identifier('pemain'),
            sql.Identifier(schema), sql.Identifier('contributors'),
            sql.Identifier(schema), sql.Identifier('genre_tayangan')
     )

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(select_query, (id,))
        film = cur.fetchone()
        if film:
            genres = film[12].split(',') if film[12] else []
            penulis_skenario = film[9].split(',') if film[9] else []
            pemain = film[11].split(',') if film[11] else []
            return {
                'id_tayangan': str(film[0]),
                'judul': film[1],
                'sinopsis': film[2],
                'asal_negara': film[3],
                'url_video_film': film[4],
                'release_date_film': film[5],
                'durasi_film': film[6],
                'average_rating': film[7],
                'total_view_count': film[8],
                'penulis_skenario': penulis_skenario,
                'sutradara': film[10],
                'pemain': pemain,
                'genres': genres
            }
        else:
            return None
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def get_series_data(id):
    schema = "pacilflix"
    select_query = sql.SQL("""
    SELECT 
        s.id_tayangan, 
        t.judul, 
        t.asal_negara,
        t.sinopsis, 
        AVG(u.rating) AS average_rating,
        STRING_AGG(DISTINCT gt.genre, ', ') AS genres,
        STRING_AGG(DISTINCT c1.nama, ', ') AS penulis_skenario,
        STRING_AGG(DISTINCT c2.nama, ', ') AS sutradara,
        STRING_AGG(DISTINCT c3.nama, ', ') AS pemain,
        STRING_AGG(DISTINCT e.sub_judul, ', ') AS episode_judul,
        STRING_AGG(DISTINCT e.durasi::text, ', ') AS episode_durasi
    FROM 
        {}.{} s
    LEFT JOIN
        {}.{} t ON t.id = s.id_tayangan
    LEFT JOIN 
        {}.{} u ON s.id_tayangan = u.id_tayangan
    LEFT JOIN 
        {}.{} gt ON s.id_tayangan = gt.id_tayangan
    LEFT JOIN 
        {}.{} mst ON s.id_tayangan = mst.id_tayangan
    LEFT JOIN 
        {}.{} ps ON mst.id_penulis_skenario = ps.id
    LEFT JOIN 
        {}.{} c1 ON ps.id = c1.id
    LEFT JOIN 
        {}.{} prt ON s.id_tayangan = prt.id_tayangan
    LEFT JOIN 
        {}.{} st ON t.id_sutradara = st.id
    LEFT JOIN 
        {}.{} c2 ON st.id = c2.id
    LEFT JOIN 
        {}.{} mtt ON s.id_tayangan = mtt.id_tayangan
    LEFT JOIN 
        {}.{} p ON mtt.id_pemain = p.id
    LEFT JOIN 
        {}.{} c3 ON p.id = c3.id
    LEFT JOIN 
        {}.{} e ON s.id_tayangan = e.id_series
    WHERE 
        s.id_tayangan = %s
    GROUP BY 
        s.id_tayangan, t.judul, t.asal_negara, t.sinopsis;  
    """).format(
        sql.Identifier(schema), sql.Identifier('series'),
        sql.Identifier(schema), sql.Identifier('tayangan'),
        sql.Identifier(schema), sql.Identifier('ulasan'),
        sql.Identifier(schema), sql.Identifier('genre_tayangan'),
        sql.Identifier(schema), sql.Identifier('menulis_skenario_tayangan'),
        sql.Identifier(schema), sql.Identifier('penulis_skenario'), 
        sql.Identifier(schema), sql.Identifier('contributors'),
        sql.Identifier(schema), sql.Identifier('persetujuan'),
        sql.Identifier(schema), sql.Identifier('sutradara'),
        sql.Identifier(schema), sql.Identifier('contributors'),
        sql.Identifier(schema), sql.Identifier('memainkan_tayangan'),
        sql.Identifier(schema), sql.Identifier('pemain'),
        sql.Identifier(schema), sql.Identifier('contributors'),
        sql.Identifier(schema), sql.Identifier('episode')
    )
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(select_query, (id,))
        series = cur.fetchone()
        if series:
            genres = series[5].split(',') if series[5] else []
            penulis_skenario = series[6].split(',') if series[6] else []
            pemain = series[8].split(',') if series[8] else []
            episode_judul = series[9].split(',') if series[9] else []
            episode_durasi = series[10].split(',') if series[10] else []
            
            return {
                'id_tayangan': str(series[0]),
                'judul': series[1],
                'asal_negara': series[2],
                'sinopsis': series[3],
                'average_rating': series[4],
                'genres': genres,
                'penulis_skenario': penulis_skenario,
                'sutradara': series[7],
                'pemain': pemain,
                'episode_judul': episode_judul,
                'episode_durasi': episode_durasi            
            }
        else:
            return None
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def get_episode_data(id, subtitle):
    schema = "pacilflix"
    select_query = sql.SQL("""
    WITH specific_episode AS (
        SELECT 
            e.id_series,
            e.sub_judul,
            e.sinopsis,
            e.durasi,
            e.url_video,
            e.release_date
        FROM 
            {}.{} e
        WHERE
            e.id_series = %s
            AND e.sub_judul = %s
    ),
    other_episodes AS (
        SELECT 
            e.id_series,
            STRING_AGG(e.sub_judul, ', ') AS other_sub_juduls
        FROM 
            {}.{} e
        WHERE
            e.id_series = %s
            AND e.sub_judul != %s
        GROUP BY
            e.id_series
    )
    SELECT 
        se.id_series,
        t.judul AS series_judul,
        se.sub_judul,
        se.sinopsis,
        se.durasi,
        se.url_video,
        se.release_date,
        oe.other_sub_juduls
    FROM 
        specific_episode se
    LEFT JOIN
        other_episodes oe ON se.id_series = oe.id_series
    LEFT JOIN
        {}.{} t ON se.id_series = t.id;
    """).format(
        sql.Identifier(schema), sql.Identifier('episode'),
        sql.Identifier(schema), sql.Identifier('episode'),
        sql.Identifier(schema), sql.Identifier('tayangan')
    )

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(select_query, (id, subtitle, id, subtitle))
        episode = cur.fetchone()
        if episode:
            other_sub_juduls = episode[7].split(',') if episode[7] else []
            return {
                'id_series': str(episode[0]),
                'series_judul': episode[1],
                'sub_judul': episode[2],
                'sinopsis': episode[3],
                'durasi': episode[4],
                'url_video': episode[5],
                'release_date': episode[6],
                'other_sub_juduls': other_sub_juduls
            }
        else:
            return None
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def store_viewing_history(username, id_tayangan, start_date_time, end_date_time):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        insert_query = sql.SQL(
            """ INSERT INTO pacilflix.riwayat_nonton (username, id_tayangan, start_date_time, end_date_time)
                VALUES (%s, %s, %s, %s);
            """)
        cur.execute(insert_query, (username, id_tayangan, start_date_time, end_date_time))
        conn.commit()
        return "Riwayat nonton berhasil disimpan."
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

### PENCARIAN

def get_search_result(query):
    schema = "pacilflix"
    search_pattern = '%' + query.lower() + '%'
    
    film_query = sql.SQL(
        """SELECT 
                f.id_tayangan AS id, 
                t.judul, 
                t.sinopsis_trailer, 
                t.url_video_trailer, 
                t.release_date_trailer,
                'film' AS type
            FROM 
                {}.{} f
            JOIN 
                {}.{} t ON f.id_tayangan = t.id
            WHERE 
                LOWER(t.judul) LIKE %s"""
    ).format(
        sql.Identifier(schema), sql.Identifier("film"),
        sql.Identifier(schema), sql.Identifier("tayangan")
    )
    
    series_query = sql.SQL(
        """SELECT 
                s.id_tayangan AS id, 
                t.judul, 
                t.sinopsis_trailer, 
                t.url_video_trailer, 
                t.release_date_trailer,
                'series' AS type
            FROM 
                {}.{} s
            JOIN 
                {}.{} t ON s.id_tayangan = t.id
            WHERE 
                LOWER(t.judul) LIKE %s"""
    ).format(
        sql.Identifier(schema), sql.Identifier("series"),
        sql.Identifier(schema), sql.Identifier("tayangan")
    )
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Execute film query
        cur.execute(film_query, (search_pattern,))
        films = cur.fetchall()
        
        # Execute series query
        cur.execute(series_query, (search_pattern,))
        series = cur.fetchall()
        
        # Combine results and format
        results = []
        for tayangan in films + series:
            results.append({
                'id': str(tayangan[0]),
                'judul': tayangan[1],
                'sinopsis_trailer': tayangan[2],
                'url_video_trailer': tayangan[3],
                'release_date_trailer': tayangan[4],
                'type': tayangan[5]
            })
        
        return results
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

### ULASAN

def insert_review(id_tayangan, username, rating, review):
    schema = "pacilflix"
    insert_query = sql.SQL("""
    INSERT INTO {}.{} (id_tayangan, username, rating, deskripsi, timestamp)
    VALUES (%s, %s, %s, %s, %s)
    """).format(
        sql.Identifier(schema), sql.Identifier('ulasan')
    )
    
    timestamp = 'NOW()'
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(insert_query, (id_tayangan, username, rating, review, timestamp))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return "Anda sudah memberikan review untuk tayangan ini."
    finally:
        cur.close()
        conn.close()
    return "Review berhasil ditambahkan."
    

def get_reviews(id_tayangan):
    schema = "pacilflix"
    select = sql.SQL("""
    SELECT
        u.id_tayangan, u.username, u.rating, u.deskripsi, u.timestamp
    FROM
        {}.{} u
    WHERE
        u.id_tayangan = %s
    ORDER BY
        u.timestamp; 
    """).format(
        sql.Identifier(schema), sql.Identifier("ulasan")
    )
    conn = get_db_connection()
    cur = conn.cursor()
    
    try: 
        cur.execute(select, (id_tayangan,))
        reviews = cur.fetchall()
        return [{
            'id_tayangan': str(review[0]),
            'username': review[1],
            'rating': review[2],
            'deskripsi': review[3],
            'timestamp': review[4]
        } for review in reviews]
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

### BAGIAN KONTRIBUTOR

def get_all_contributors():
    schema = "pacilflix"
    select_query = sql.SQL(
        """ SELECT c.id, c.nama, c.jenis_kelamin, c.kewarganegaraan,
                    COALESCE(p.tipe, '') AS penulis_skenario,
                    COALESCE(pe.tipe, '') AS pemain,
                    COALESCE(s.tipe, '') AS sutradara
            FROM {}.{} c
            LEFT JOIN (
                SELECT id, 'Penulis Skenario' AS tipe
                FROM {}.{}
            ) p ON c.id = p.id
            LEFT JOIN (
                SELECT id, 'Pemain' AS tipe
                FROM {}.{}
            ) pe ON c.id = pe.id
            LEFT JOIN (
                SELECT id, 'Sutradara' AS tipe
                FROM {}.{}
            ) s ON c.id = s.id
        """).format(
        sql.Identifier(schema), sql.Identifier("contributors"),
        sql.Identifier(schema), sql.Identifier("penulis_skenario"),
        sql.Identifier(schema), sql.Identifier("pemain"),
        sql.Identifier(schema), sql.Identifier("sutradara")
    )
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(select_query)
        contributors = cur.fetchall()
        return [{
            'id': str(contributor[0]),
            'nama': contributor[1],
            'jenis_kelamin': 'Laki-laki' if contributor[2] == 0 else 'Perempuan',
            'kewarganegaraan': contributor[3],
            'tipe': ', '.join([contributor[i] for i in range(4, 7) if contributor[i]])
        } for contributor in contributors]
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()




