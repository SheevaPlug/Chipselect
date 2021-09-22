from flask import Blueprint, render_template, redirect, url_for

from app import app

tree = Blueprint('tree', __name__)

@tree.route('/')
def index():
    return render_template(
        'tree/index.html',
        results=app.search.search(
            index='mcs',
            body={'size': 0, 'aggs': {'makers': {'terms': {'field': 'vendor.keyword'}}}}))


@tree.route('/vendor/<name>')
def vendor(name):
    return render_template(
        'tree/vendor.html',
        results=app.search.search(
            index='mcs',
            body={'query': {'term': {'vendor.keyword': name}}}))
