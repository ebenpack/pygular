from flask import jsonify
import re


def option_parse(s):
    # TODO: Parse options with regex
    opt_list = s.replace("options=", " ").replace("&", " ").split()
    opt_list = "".join(opt_list)
    # If the 'x' flag is set, it needs to go first
    if 'x' in opt_list:
        opt_list = opt_list.replace("x", "")
        opt_list = "x" + opt_list
    if opt_list:
        return "(?" + opt_list + ")"
    else:
        return ""


def html_newline(s):
    return s.replace('\n', '<br />')


def span_wrap(s, html_class="match"):
    return '<span class="' + html_class + '">' + s.group() + '</span>'


def regexp_highlight(regexp, text, opt_list):
    return re.sub(opt_list + regexp, span_wrap, text)


def regexp_eval(request):
    regexp = str(request.args.get('regexp'))
    options = str((request.args.get('options')))
    test = str(request.args.get('test'))

    warn = ""
    opt_list = option_parse(options)

    if not regexp and not test:
        return jsonify(result="", fulltext="")
    if not regexp:
        return jsonify(result="", fulltext=html_newline(test))
    if not test:
        return jsonify(result="", fulltext="")
    else:
        try:
            m = re.findall(opt_list + regexp, test)
            return jsonify(result=m, fulltext=html_newline(regexp_highlight(regexp, test, opt_list)), warn=warn)
        except Exception:
            warn = "Invalid expression"
            return jsonify(result = [], fulltext = html_newline(test), warn=warn)