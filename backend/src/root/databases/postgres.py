import psycopg2
import psycopg2.extras

from .. import config as cfg
from ..api.schemas import Record


class open_connection:
    """
    Создаёт самозакрывающееся соединение с Postgres
    """
    def __init__(self, params):
        self.params = params
        self.connection = None

    def __enter__(self):
        self.connection = psycopg2.connect(**self.params)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class Postgres:
    """
    Класс для взаимодействия с базой данных.

    Используются 3 уровня контекстного менеджера with:
    1. Первый созданный методами класса для закрытия соединения.
    2. Второй для комита транзакции предусмотренный либой psycopg2
    3. Третий для закрытия курсора предусмотренный либой psycopg2
    """
    def __init__(self, params: dict) -> None:
        self.params = params

    def on_startup(self) -> None:
        """
        Создание первоначальных данных при первом запуске приложения
        """
        with open_connection(self.params) as conn:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(cfg.SQL_DROP_TABLE)
                    cur.execute(cfg.SQL_CREATE_TABLE)

                    with open(cfg.PATH_CSV, encoding='utf-8') as csv_file:
                        cur.copy_expert(sql=cfg.SQL_COPY, file=csv_file)

    def get_data(self, ids: tuple) -> list[Record]:
        """
        Вытаскивает из БД данные по id.
        :param ids: кортеж из id
        """
        with open_connection(self.params) as conn:
            with conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(cfg.SQL_GET_DATA, (ids,))
                    return [Record(id=row['id'],
                                   text=row['text'],
                                   created_date=row['created_date'],
                                   rubrics=row['rubrics'])
                            for row in cur]
