import os

from flask import Flask
from jinja2.tests import test_mapping, test_sequence
from opensearchpy import OpenSearch

app = Flask(__name__)
app.config.from_object(os.getenv('CONFIGFILE', 'app.config-development'))
#app.search = Elasticsearch(app.config.get('ELASTICSEARCH_NODES', ['localhost']))
opensearch_params = app.config.get('OPENSEARCH_PARAMS', {
    'hosts': [{'host': 'localhost', 'port': 9200}], 
    'http_auth': ('admin', 'admin'),
    'use_ssl': True,
    'verify_certs': False,
    'ssl_show_warn': False,
})
app.search = OpenSearch(**opensearch_params)

from app.bp.tree import tree
app.register_blueprint(tree, url_prefix='/tree')

from app import routes
