from flask import Flask, render_template, request, jsonify
import re


app = Flask(__name__)

def option_parse(s):
    opt_list = s.replace("options=" , " ").replace("&", " ").split()
    opt_list = "".join(opt_list)
    # If the 'x' flag is set, it needs to go first
    if 'x' in opt_list:
        opt_list = opt_list.replace("x","")
        opt_list = "x" + opt_list
    if opt_list:
        return "(?" + opt_list +")"
    else:
        return ""

def span_wrap(s):
    return '<span class="match">' + s.group() + '</span>'

def regexp_higlight(regexp, text, opt_list):
    return re.sub(opt_list + regexp, span_wrap, text)

@app.route('/regexp')
def regexp_eval():
    regexp = str(request.args.get('regexp'))
    options = str((request.args.get('options')))
    test = str(request.args.get('test'))

    warn=""
    opt_list = ""
    opt_list = option_parse(options)

    if not regexp and not test:
        return jsonify(result = "", fulltext = "")
    if not regexp:
        return jsonify(result = "", fulltext = test)
    if not test:
        return jsonify(result = "", fulltext = "")
    else:
        try:
            m = re.findall(opt_list + regexp, test)
            return jsonify(result = m, fulltext = regexp_higlight(regexp, test, opt_list), warn=warn)
        except Exception:
            warn = "Invalid expression"
            return jsonify(result = [], fulltext = test, warn=warn)

#    re.DOTALL
#   re.UNICODE
#   re.IGNORECASE
#   re.MULTILINE


@app.route('/', methods=['GET', 'POST'])
def regexp_main():
    return render_template('home.html', body="Hello World!")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(debug=True)
