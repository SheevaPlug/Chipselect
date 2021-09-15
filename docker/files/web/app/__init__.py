from flask import Flask
from elasticsearch import Elasticsearch

app = Flask(__name__)
app.config.from_object('app.config')
app.search = Elasticsearch(app.config.get('ELASTICSEARCH_NODES', ['localhost']))


from app import routes
