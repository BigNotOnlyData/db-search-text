from enum import Enum

# API_HOST = 'localhost'
API_HOST = 'api-container'
API_PORT = '8000'
API_URL = f'http://{API_HOST}:{API_PORT}/search'


class Tabs(str, Enum):
    search = "Поиск"
    create = "Создать"
    update = "Обновить"
    delete = "Удалить"
