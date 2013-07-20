from flask import render_template, request
from pygular import regexp_match_json, request_wants_json
from forms import RegExForm
from app import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = RegExForm(request.form)
    if form.validate_on_submit():
        if request_wants_json():
            return regexp_match_json(form)
        else:
            pass
    else:
        return render_template('home.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404