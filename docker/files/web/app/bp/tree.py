from flask import Blueprint, render_template, redirect, url_for

from app import app

tree = Blueprint('tree', __name__)

@tree.route('/')
def index():
    results = app.search.search(
        index=app.config.get('INDEX_MAIN', 'mcs'),
        body={'size': 0, 'aggs': {'makers': {'terms': {'field': 'vendor.keyword'}}}})
    #import json; print(json.dumps(results))
    return render_template('tree/index.html', results=results)


@tree.route('/vendor/<name>', defaults={'start': 0})
@tree.route('/vendor/<name>/<int:start>')
def vendor(name, start=0):
    results = app.search.search(
        index=app.config.get('INDEX_MAIN', 'mcs'),
        body={'from': start, 'size': app.config.get('PAGINATION', 20), 'query': {'term': {'vendor.keyword': name}}})
    #import json; print(json.dumps(results))
    return render_template('tree/vendor.html', results=results, name=name, start=start)
