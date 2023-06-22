import psycopg2.extras
from elasticsearch import helpers

from .. import config as cfg
from ..api.schemas import Record
from .elastic import Elastic
from .postgres import open_connection, Postgres


class Synchronizer:
    """
    Класс для совместных операций Postgres и Elastic
    """

    def __init__(self, db: Postgres, es: Elastic) -> None:
        self.db = db
        self.es = es

    @staticmethod
    def _gendata(cursor: psycopg2.extras.RealDictCursor) -> dict:
        for row in cursor:
            yield {"_index": "posts",
                   "_id": row['id'],
                   "_source": {"text": row['text']}
                   }

    def on_startup(self) -> None:
        self.db.on_startup()
        self.es.on_startup()

        with open_connection(self.db.params) as conn:
            with conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(cfg.SQL_SELECT_FOR_ELASTIC)
                    helpers.bulk(self.es.client, self._gendata(cur))
                    self.es.client.indices.refresh(index="posts")

    def on_shutdown(self) -> None:
        self.es.on_shutdown()

    def get_data_by_search(self, text: str) -> list:
        if ids := self.es.search(text):
            data = self.db.get_data(ids)
        else:
            data = []
        return data

    def create_post(self, body: Record):
        with open_connection(self.db.params) as conn:
            with conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    data = (body.text, str(body.created_date), body.rubrics)
                    cur.execute(cfg.SQL_INSERT_POST, data)
                    new_post = cur.fetchone()
                    self.es.client.index(index="posts",
                                         id=new_post['id'],
                                         document={'text': new_post['text']})
                    return new_post

    def update_post(self, body: Record):
        with open_connection(self.db.params) as conn:
            with conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    data = (body.text, str(body.created_date), body.rubrics, body.id)
                    cur.execute(cfg.SQL_UPDATE_POST, data)
                    new_post = cur.fetchone()
                    self.es.client.update(index="posts",
                                          id=new_post['id'],
                                          body={'doc': {'text': new_post['text']}})
                    return new_post

    def delete_post(self, id_):
        with open_connection(self.db.params) as conn:
            with conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(cfg.SQL_DELETE_POST, (id_,))
                    self.es.client.delete(index="posts", id=id_)

    def get_post(self, id_):
        with open_connection(self.db.params) as conn:
            with conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(cfg.SQL_GET_POST, (id_,))
                    return cur.fetchone()


if __name__ == "__main__":
    pass
    # sync = Synchronizer()
    # sync.on_startup()
    # print(sync.es.client.count(index='posts')['count'])
    # pprint(sync.get_search('Замечательная история'))
