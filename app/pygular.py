from flask import jsonify, request
import re


def request_wants_json():
    """
    Return HTML where appropriate, and JSON otherwise.
    http://flask.pocoo.org/snippets/45/
    """
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
           request.accept_mimetypes[best] > \
           request.accept_mimetypes['text/html']


def option_parse(s):
    """
    Parse the option string passed in query string format and return an option string formatted for Python regular
    expression evaluation.
    """
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
    """
    Replace newline character with break tag.
    """
    return s.replace('\n', '<br />')


def span_wrap(s, html_class="match"):
    """
    Return the given string wrapped in a span, with the given class.
    """
    # html_class is included to make this function more general, but we need to have the default class "match" in order
    # to work with re.sub(). This optional class parameter may be removed later if this function isn't needed
    # elsewhere.
    return '<span class="' + html_class + '">' + s.group() + '</span>'


def regexp_highlight(regexp, text, opt_list):
    """
    Return the given string with all string sections matched by the given regular expression wrapped in a
    span with a highlight class.
    """
    return re.sub(opt_list + regexp, span_wrap, text)


def regexp_match(request):
    """
    Return a string of formatted html with all sections of the original text matching the given regular expression
    wrapped in a span with a highlight class, and all newlines converted to breaks.
    """
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