movies_query = """
            SELECT
            fw.id uuid,
            fw.title,
            fw.rating AS imdb_rating,
            fw.description,
            array_agg(DISTINCT jsonb_build_object ('uuid', g.id, 'name', g.name)) AS genre,
            array_agg(DISTINCT jsonb_build_object ('uuid', p.id, 'full_name', p.full_name)) FILTER (WHERE pfw.role = 'actor') AS actors,
            array_agg(DISTINCT jsonb_build_object ('uuid', p.id, 'full_name', p.full_name)) FILTER (WHERE pfw.role = 'writer') AS writers,
            array_agg(DISTINCT jsonb_build_object ('uuid', p.id, 'full_name', p.full_name)) FILTER (WHERE pfw.role = 'director') AS directors
            FROM content.film_work fw
            LEFT JOIN content.person_film_work AS pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person AS p ON p.id = pfw.person_id
            LEFT JOIN content.genre_film_work AS gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre AS g ON g.id = gfw.genre_id
            WHERE greatest(fw.modified, p.modified, g.modified) > '%s'
            GROUP BY fw.id
            ORDER BY greatest(fw.modified, max(p.modified), max(g.modified)) ASC;
"""

persons_query = """
            SELECT
            id uuid,
            full_name
            FROM content.person
            WHERE modified > '%s'
            ORDER BY modified ASC
"""

genres_query = """
            SELECT
            id uuid,
            name
            FROM content.genre
            WHERE modified > '%s'
            ORDER BY modified ASC
"""
