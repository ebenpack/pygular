from collections import namedtuple
from flask import jsonify
import re, cgi

Match = namedtuple('Match', ['match_groups', 'match_text', 'warn'])

class RegEx(object):
    def __init__(self, pattern, options, test_string):
        self.pattern = pattern
        self.options = options
        self.test_string = test_string
        self.warn = ""
        self.flags = self.compile_flags()
        self.compiled = self.compile_re()
        if self.compiled:
            self.matchlist = list(self.compiled.finditer(self.test_string))

    def compile_flags(self):
        flags = {'L': re.L, 'm': re.M, 's': re.S, 'u': re.U, 'i': re.I, 'x': re.X}
        re_flags = 0
        if self.options:
            for option in self.options:
                re_flags = re_flags | flags[option]
        return re_flags

    def compile_re(self):
        try:
            compiled = re.compile(self.pattern, self.flags)
            return compiled
        except re.error:
            self.warn = "Invalid expression"
            self.match = Match([], cgi.escape(self.test_string), self.warn)


    def serialize_capture_groups(self):
        """
        Returns a list of all match groups. A match group consists of a list of matches, which are dictionaries mapping
        the match number (or name if it is a named match) to the matched text.
        """

        serialized = []

        # Is there any situation where two or more names would map to the same group number
        # (i.e. group numbers not unique)? If so, this would be problematic.
        groupindex = {v:k for k,v  in self.compiled.groupindex.items()}

        if self.matchlist:
            for match in self.matchlist:
                newmatch = []
                if not match.groups():
                    continue
                else:
                    for i, match in enumerate(match.groups(), start=1):
                        if groupindex and i in groupindex:
                            newmatch.append({"title":groupindex[i], "value":match})
                        else:
                            newmatch.append({"title":i,"value": match})
                    serialized.append({"match": newmatch})
        return serialized


    def regexp_highlight(self, html_class="match hilite"):
        """
        Return the given string with all string sections matched by the given regular expression wrapped in a
        span with a highlight class, and all necessary characters escaped.
        """

        span_list = []
        newtext = []

        for match in self.matchlist:
            span_list.append(match.span())

        if not span_list:
            return cgi.escape(self.test_string)

        cursor = 0
        for span in span_list:
            newtext.append(cgi.escape(self.test_string[cursor:span[0]]))
            newtext.extend(["<span class='{}'>".format(html_class), cgi.escape(self.test_string[span[0]:span[1]]),"</span>"])
            cursor = span[1]
        newtext.append(cgi.escape(self.test_string[cursor:]))
        return "".join(newtext)


    def regexp_match(self):
        """
        Return a named tuple consisting of a string of formatted html with all sections of the original text
        matching the given regular expression wrapped in a span with a highlight class, and all newlines
        converted to breaks; a list of all match groups; and any warnings.
        """

        if self.compiled:
            capture_list = self.serialize_capture_groups()
            fulltext = self.regexp_highlight()
            self.match = Match(capture_list, fulltext, self.warn)
            return self.match
        else:
            return self.match

    def regexp_match_json(self):
        """
        Return a JSON object consisting of a string of formatted html with all sections of the original text
        matching the given regular expression wrapped in a span with a highlight class, and all newlines
        converted to breaks; a list of all match groups; and any warnings.
        """

        self.regexp_match()
        return jsonify(matchgroups=self.match.match_groups,matchtext=self.match.match_text, warning=self.match.warn )
