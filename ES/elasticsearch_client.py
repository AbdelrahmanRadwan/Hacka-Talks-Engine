from datetime import datetime
from elasticsearch import Elasticsearch


class ElasticsearchClient:

    def __init__(self):
        self.elastic_client = Elasticsearch()

    def index_record(self, json_object):
        self.elastic_client.index(index="talks", doc_type='video-talk', body=json_object)






