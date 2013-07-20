from flask import jsonify, request
import re, cgi


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
    flags = {'L': re.L, 'm': re.M, 's': re.S, 'u': re.U, 'i': re.I, 'x': re.X}
    re_flags = 0
    if s:
        for option in s:
            re_flags = re_flags | flags[option]
    return re_flags


def capture_groups(regexp, text):
    matchlist = regexp.finditer(text)
    match_return = []

    # TODO: This feels wrong. Can it be done more elegantly? Too tired now to figure it out.
    if matchlist:
        for match in matchlist:
            newmatch = []
            if match.groups():
                for sub_match in match.groups():
                    if sub_match:
                        newmatch.append(cgi.escape(sub_match))
            match_return.append(newmatch)
    match_return = [x for x in match_return if x != []]
    return match_return


def regexp_highlight(regexp, text, html_class="match"):
    """
    Return the given string with all string sections matched by the given regular expression wrapped in a
    span with a highlight class, and all necessary characters escaped.
    """
    # I would have liked to do this with re.split, but I don't think it would work properly with capture groups.
    matchlist = regexp.finditer(text)
    span_list = []
    newtext = []
    for match in matchlist:
        span_list.append(match.span())

    # Reverse span_list so we can pop
    span_list.reverse()

    # TODO: I would like to remove the repetition of "if not span_list". Too tired now to think about it.
    for i, c in enumerate(text):
        if not span_list:
            return "".join(newtext) + cgi.escape(text[i:])
        if i == span_list[-1][1]:
            newtext.append('</span>')
            span_list.pop()
        if not span_list:
            return "".join(newtext) + cgi.escape(text[i:])
        if i == span_list[-1][0]:
            newtext.append('<span class="' + html_class + '">')
        if c == '\n':
            newtext.append("<br />")
        else:
            newtext.append(cgi.escape(c))
    return "".join(newtext)


def regexp_match_json(form):
    """
    Return a JSON object consisting of a string of formatted html with all sections of the original text
    matching the given regular expression wrapped in a span with a highlight class, and all newlines
    converted to breaks; a list of all match groups; and any warnings.
    """
    pattern = form.data['regex']
    options = form.data['options']
    test_string = form.data['test']

    warn = ""
    options = option_parse(options)

    try:
        compiled = re.compile(pattern, options)
        capture_list = capture_groups(compiled, test_string)
        fulltext = regexp_highlight(compiled, test_string)
        return jsonify(match_groups=capture_list, match_text=fulltext, warn=warn)
    except Exception:
        warn = "Invalid expression"
        return jsonify(match_groups=[], match_text=cgi.escape(test_string), warn=warn)