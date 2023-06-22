# Проблемы
## Общие
+ При создании нового проекта в Pycharm в виртуальном окружении были видны все глобальные 
пакеты, установленные до этого. Для того, чтобы в новом окружение 
было чисто потребовалось `deactivate`, а затем `activate` виртуальное окружение:
`.\venv\Scripts\activate`
+ Возникли ошибки относительного импорта при импорте модулей python. Решено изменением структуры файлов,
вынося `main.py` выше всех модулей как [здесь](https://napuzba.com/attempted-relative-import-with-no-known-parent-package/)


## PostgreSQL
+ PgAdmin 4 не запускался. Помог запуск от имени администратора.
+ В csv файле не было id, которое должно быть в БД. При создании таблицы БД в поле id 
указал свойство SERIAL, которое автоматически проставляло id.
+ Для импорта данных из csv в postgress использовал метод `copy_expert` адаптера `psycopg2`, 
с указанием имен столбцов.
+ Если копировать через PgAdmin, то скрипт надо прописывать в shell (psql) например
`\copy readers from 'C:\Users\Rodion\Desktop\Readers.csv' delimiter ';' csv header`
	- `"` - двойная кавычка вокруг пути выдавала ошибку
	- Путь к файлу должен быть на латинице

## Elasticsearch
+ По видимому в России нельзя скачать *Elasticsearch*. Для работы с ним использовал *Docker* с 
образами из *Docker Hub*, так как образы с официального сайта *Elasticsearch* не работали. 
Также использовал *Kibana*. В `docker-compose.yml` важно указать в `enviroments`
*Kibana* `ELASTICSEARCH_HOSTS=http://elastic-container:9200`. Без него при запуске *Kibana* 
просила токен авторизации. (В итоге реализация без *Kibana*, так как с ней тормозило)
+ Периодически запросы к *Elasticsearch* выдавали ошибку Timeout Connection. Решено
добавлением параметров `Elasticsearch([params],
                                    timeout=30,
                                    max_retries=10,
                                    retry_on_timeout=True)`
+ Elasticsearch, при старте FastAPI, выдавал `elastic_transport.ConnectionError`.
Elasticsearch долго подключался, со временем соединение устанавливалось - решение в цикле while проверять подключение 
и только потом работать с FastAPI 

	```
	while not app.sync.es.client.ping():
	    time.sleep(15)
	app.sync.on_startup()
	```
+ При добавлении или удалении данных в Elasticsearch, не все новые данные сразу отображались 
при их запросе. Помогло применение метода `es.indices.refresh()`

## Docker
+ Если локально на компе установлен Postgres (мой случай), то чтобы обращаться к контейнеру 
с Postgres через комп, надо указать порт Postgres отличный от того, что прослушивается локально.
В моем случае на компе Postgres был на порту 5432, а в контейнере установил 5433:5432 - означает,
что порт в контейнере 5432 Postgres, пробрасывается на локальный хост на порт 5433.
+ [Windows] Сервис *Vmmem* (отвечает за виртуальную машину линукс в докере) в диспетчере задача 
грузил оперативную память на 3.5 Gb и сильно тормозил комп. Помогло создание файла `.wslconfig`
в *User profile* c кодом как [здесь](https://thegeekpage.com/docker-vmmem-process-takes-too-much-memory/)
	```
    [wsl2] 
    memory=2GB 
    processors=2
	```





