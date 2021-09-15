from flask import render_template

from app import app
from app.forms import SearchForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        #print(form.query.data)
        #print(app.search.search(body={'query': {'match_all': form.query.data}}))
        results = app.search.search(
            index='mcs',
            body={'query': {'query_string': {'query': form.query.data}}})
        from pprint import pprint; pprint(results)
    else:
        print(form.errors)
    return render_template('index.html', form=form, results=results)


@app.route('/show/<deviceid>')
def show(deviceid):
    result = app.search.get_source(index='mcs', id=deviceid)
    return render_template('show.html', result=result)
    
