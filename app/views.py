from flask import render_template, request
from pygular import regexp_eval
from app import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('home.html')


@app.route('/regexp')
def regexp():
    return regexp_eval(request)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404