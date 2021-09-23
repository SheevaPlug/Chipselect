from flask import render_template

from app import app
from app.forms import SearchForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        results = app.search.search(
            index=app.config.get('INDEX_MAIN', 'mcs'),
            body={'query': {'query_string': {'query': form.query.data}}})
    return render_template('index.html', form=form, results=results)


@app.route('/show/<deviceid>')
def show(deviceid):
    # @todo move this into "tree" blueprint
    result = app.search.get_source(
        index=app.config.get('INDEX_MAIN', 'mcs'),
        id=deviceid)
    return render_template('show.html', result=result)
