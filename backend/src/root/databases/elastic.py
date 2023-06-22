# https://dylancastillo.co/elasticsearch-python/
# https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/overview.html
# https://elasticsearch-py.readthedocs.io/en/v8.7.1/
# https://medium.com/nuances-of-programming/%D0%BD%D0%B0%D1%87%D0%B0%D0%BB%D0%BE-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%8B-%D1%81-elasticsearch-%D0%B2-python-%D1%87%D0%B0%D1%81%D1%82%D1%8C-2-412796dcb213
# https://hevodata.com/learn/elasticsearch-to-postgresql/
# https://medium.com/@toluaina/real-time-integration-of-postgresql-with-elasticsearch-with-pgsync-9425ffa9b4e9
# https://medium.com/@sumukhi.cv/load-csv-data-into-elasticsearch-using-python-11e14b4d4c99

# Timeout connection
# https://github.com/elastic/elasticsearch-py/issues/1992?ysclid=liun9em59w862998142
# https://9to5answer.com/connection-timeout-with-elasticsearch

# elastic_transport.ConnectionError - подождать


from elasticsearch import Elasticsearch
from .. import config as cfg


class Elastic:
    def __init__(self, params):
        self.client = Elasticsearch([params],
                                    timeout=30,
                                    max_retries=10,
                                    retry_on_timeout=True)

    def on_startup(self):
        self.client.indices.delete(index='posts', ignore_unavailable=True)
        self.client.indices.refresh()
        self.client.indices.create(index='posts',
                                   mappings=cfg.ES_MAPPING_POSTS,
                                   settings=cfg.ES_SETTINGS_POSTS)

    def search(self, text):
        response = self.client.search(index="posts",
                                      query={"match": {'text': text}},
                                      size=cfg.ES_RESPONSE_SIZE)
        ids = [hit['_id'] for hit in response['hits']['hits']]
        return tuple(ids)

    def on_shutdown(self):
        self.client.transport.close()


if __name__ == "__main__":
    es = Elastic(cfg.ES_PARAMS)
    print(es.client.ping())
