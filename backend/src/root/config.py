import pathlib

# FastAPI
API_HOST = 'localhost'
API_PORT = 8000

# Исходные данные из csv
DIR_NAME = 'data'
FILE_NAME = 'posts.csv'
PATH_CSV = pathlib.Path(__file__).parent.parent.parent / DIR_NAME / FILE_NAME

# ElasticSearch
# ES_PARAMS = {'scheme': 'https://',
#              'host': 'localhost',
#              'port': 9200}

ES_PARAMS = {'scheme': 'https://',
             'host': 'elastic-container',
             'port': 9200}

ES_MAPPING_POSTS = {"properties": {"text": {"type": "text"}}}
ES_SETTINGS_POSTS = {"number_of_shards": 1, "number_of_replicas": 0}
ES_RESPONSE_SIZE = 20

# Postgres
# PG_PARAMS = {"host": "0.0.0.0",
#              "port": "5433",
#              "dbname": "mytest",
#              "user": "myuser",
#              "password": "mypassword"}

PG_PARAMS = {"host": "postgres-container",
             "port": "5432",
             "dbname": "mytest",
             "user": "myuser",
             "password": "mypassword"}

SQL_CREATE_TABLE = """
    CREATE TABLE posts(
        id SERIAL PRIMARY KEY,
        text TEXT,
        created_date TIMESTAMP,
        rubrics TEXT
        )
    """

SQL_DROP_TABLE = "DROP TABLE IF EXISTS posts"

SQL_COPY = """
    COPY posts(text, created_date, rubrics) 
    FROM STDIN 
    WITH
        CSV
        HEADER
        DELIMITER AS ','
    """

SQL_GET_DATA = """
    SELECT *
    FROM posts
    WHERE id IN %s
    ORDER BY created_date DESC
    """

SQL_SELECT_FOR_ELASTIC = """
    SELECT id, text 
    FROM posts
    """

SQL_INSERT_POST = """
    INSERT INTO posts(text, created_date, rubrics)
    VALUES (%s, %s, %s) 
    RETURNING *
    """

SQL_UPDATE_POST = """
    UPDATE posts
    SET text = %s, 
        created_date = %s,
        rubrics = %s
    WHERE id = %s
    RETURNING *
    """

SQL_DELETE_POST = """
    DELETE FROM posts 
    WHERE id = %s
    """

SQL_GET_POST = """
    SELECT *
    FROM posts WHERE id = %s
    """
