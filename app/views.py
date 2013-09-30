from flask import render_template, request, redirect, url_for, session

from pygular import regexp_match, regexp_match_json, request_wants_json

from forms import RegExForm
from app import app
import datetime, json


def regexp_page():
    form = RegExForm(request.form)
    if form.validate_on_submit() or session.get("messages"):
        if session.get("messages"):
            message = json.loads(session["messages"])
            form.regex.data = message["re"]
            form.test.data = message["test_string"]
            del session["messages"]
        if request_wants_json():
            return regexp_match_json(form)
        else:
            match = regexp_match(form)
            return render_template('home.html', form=form, match_list=match.match_groups, match_text=match.match_text, warn=match.warn)
    else:
        return render_template('home.html', form=form, match_list="", match_text="", warn="")

# @app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    return regexp_page()


@app.route('/example')
def example():
    date = datetime.datetime.now().strftime("%d/%m/%Y")
    re = "(?P<month>\\d{1,2})\\/(?P<day>\\d{1,2})\\/(?P<year>\\d{4})"
    test_string = "Today's date is " + date + "."
    messages = json.dumps({"re": re, "test_string": test_string})
    session['messages'] = messages
    return redirect(url_for('.index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404