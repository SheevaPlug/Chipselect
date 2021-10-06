INDEX_MAIN = 'mcs'
SECRET_KEY = '95dee991891bf6d17effcf80e613fa2334de50ea6a9d9410a5b646efafb6a54e'
ELASTICSEARCH_NODES = ['localhost']
PAGINATION = 20
OPENSEARCH_PARAMS = {
    'hosts': [{'host': 'localhost', 'port': 9200}], 
    'http_auth': ('admin', 'admin'),
    'use_ssl': True,
    'verify_certs': False,
    'ssl_show_warn': False,
}
