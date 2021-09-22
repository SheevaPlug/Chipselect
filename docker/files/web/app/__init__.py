import os

from flask import Flask
from jinja2.tests import test_mapping, test_sequence
from elasticsearch import Elasticsearch

app = Flask(__name__)
app.config.from_object(os.getenv('CONFIGFILE', 'app.config-development'))
app.search = Elasticsearch(app.config.get('ELASTICSEARCH_NODES', ['localhost']))

from app.bp.tree import tree
app.register_blueprint(tree, url_prefix='/tree')

from app import routes
