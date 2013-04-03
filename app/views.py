from flask import render_template, request
from pygular import regexp_match, request_wants_json
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/regexp')
def regexp():
    if request_wants_json():
        return regexp_match(request)
    else:
        pass


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404