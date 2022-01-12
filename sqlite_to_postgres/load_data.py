import logging
import os
import sqlite3
import sys

import environ
import psycopg2
from dataclass import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor, execute_values

env = environ.Env()
environ.Env.read_env(os.path.join('.env'))

SIZE_ROWS = 20
SQL_FILE_NAME = 'db.sqlite'

logging.basicConfig(filename='log.log', filemode='w')


class SQLiteLoader:

    def __init__(self, connection) -> None:
        self.connection = connection
        self.connection.row_factory = sqlite3.Row

    def load_movies(self, field):
        logging.info(f'{__name__} {field}')
        try:
            cur = self.connection.cursor()
            cur.execute(f"""SELECT * FROM {field}""")
            while True:
                data = []
                rows = cur.fetchmany(SIZE_ROWS)
                for item in rows:
                    if item:
                        data.append(ARRAY_TABLES[field][0](**item))
                    else:
                        break
                yield data
        except (Exception, sqlite3.Error) as error:
            logging.error(f'{__name__} {error}')


class PostgresSaver:
    def __init__(self, connection) -> None:
        self.connection = connection

    def save_all_data(self, list_data, sql):
        cursor = self.connection.cursor()
        execute_values(cursor, sql, list_data)
        cursor.close()


ARRAY_TABLES = {
    'film_work': (
        FilmWork,
        'INSERT INTO content.film_work (id, title, description, creation_date, certificate,'
        'file_path, rating, type, created_at, updated_at) VALUES %s', ),
    'genre': (
        Genre,
        'INSERT INTO content.genre (id, name, description, created_at, updated_at) VALUES %s', ),
    'genre_film_work': (
        GenreFilmWork,
        'INSERT INTO content.genre_film_work (id, film_work_id, genre_id, created_at) VALUES %s'
        'ON CONFLICT (film_work_id, genre_id) DO NOTHING', ),
    'person': (
        Person,
        'INSERT INTO content.person (id, full_name, birth_date, created_at, updated_at) VALUES %s', ),
    'person_film_work': (
        PersonFilmWork,
        'INSERT INTO content.person_film_work (id, film_work_id, person_id, role, created_at)'
        'VALUES %s ON CONFLICT (film_work_id, person_id) DO NOTHING', ),
}


def objects_to_list(data):
    list_data = []
    for item in data:
        list_data.append(item.get_list())
    return list_data


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""

    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    for key in ARRAY_TABLES.keys():

        try:
            cursor = pg_conn.cursor()
            cursor.execute(f"""TRUNCATE content.{key} CASCADE""")
            cursor.close()
        except (Exception, psycopg2.Error) as error:
            logging.error(f'{key} {error}')
            continue

        for data in sqlite_loader.load_movies(key):

            if not data:
                break

            try:
                postgres_saver.save_all_data(objects_to_list(data), ARRAY_TABLES[key][1])
                pg_conn.commit()
            except (Exception, psycopg2.Error) as error:
                logging.error(f'{key} {error}')
                continue


if __name__ == '__main__':

    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        SQL_FILE_NAME = sys.argv[1]

    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', 5432),
    }

    try:
        sqlite_conn = sqlite3.connect(SQL_FILE_NAME)
        pg_conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)

        load_from_sqlite(sqlite_conn, pg_conn)

    except (Exception, psycopg2.Error) as error:
        logging.error(f'{error}')

    finally:
        sqlite_conn.close()
        pg_conn.close()
