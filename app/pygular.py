from collections import namedtuple
from flask import jsonify, request
import re, cgi

Match = namedtuple('Match', ['match_groups', 'match_text', 'warn'])

class RegEx(object):
    def __init__(self, form):
        self.pattern = form.data['regex']
        self.options = form.data['options']
        self.test_string = form.data['test']
        self.warn = ""
        self.flags = self.compile_flags()
        self.compiled = self.compile_re()

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


    def capture_groups(self):
        """
        Returns a list of all match groups. A match group consists of a list of matches, which are dictionaries mapping
        the match number (or name if it is a named match) to the matched text.
        """

        matchlist = self.compiled.finditer(self.test_string)
        match_return = []

        # matches = regexp.findall(text)
        groupindex = self.compiled.groupindex

        # Is there any situation where two or more names would map to the same group number (i.e. group numbers not unique)?

        if matchlist:
            for i, group in enumerate(matchlist):
                newmatch = []
                if not group.groups():
                    continue
                else:
                    # Is there any situation where two or more names would map to the same group number
                    # (i.e. group numbers not unique)? If so, this would be problematic.
                    groupindex = {v:k for k, v in self.compiled.groupindex.items()}
                    for j, match in enumerate(group.groups()):
                        if groupindex and (j+1) in groupindex:
                            newmatch.append({groupindex[(j+1)]: match})
                        else:
                            # If match is None (which is returned by the match object group() method when a group is contained
                            # in a part of the pattern that did not match), just add an empty string to the match group.
                            # Alternatively, something like "<span class='alert'>No Match</span>" could be returned, but
                            # I'm not sure if that's appropriate/correct or not.
                            if not match:
                                newmatch.append({(j+1): ""})
                            else:
                                newmatch.append({(j+1): match})
                    match_return.append(newmatch)
        return match_return


    def regexp_highlight(self, html_class="match hilite"):
        """
        Return the given string with all string sections matched by the given regular expression wrapped in a
        span with a highlight class, and all necessary characters escaped.
        """
        # I would have liked to do this with re.split, but I don't think it would work properly with capture groups.
        matchlist = self.compiled.finditer(self.test_string)
        span_list = []
        newtext = []
        for match in matchlist:
            span_list.append(match.span())

        # Reverse span_list so we can pop
        span_list.reverse()

        # TODO: Can I remove the repetition of "if not span_list"?
        for i, char in enumerate(self.test_string):
            if not span_list:
                return "".join(newtext) + cgi.escape(self.test_string[i:])
            if i == span_list[-1][0]:
                newtext.append('<span class="' + html_class + '">')
            if i == span_list[-1][1]:
                newtext.append('</span>')
                span_list.pop()
                if not span_list:
                    return "".join(newtext) + cgi.escape(self.test_string[i:])
                if i == span_list[-1][0]:
                    newtext.append('<span class="' + html_class + '">')
                if i == span_list[-1][1]:
                    newtext.append('</span>')
                    span_list.pop()
            newtext.append(cgi.escape(char))
        return "".join(newtext)


    def regexp_match(self):
        """
        Return a named tuple consisting of a string of formatted html with all sections of the original text
        matching the given regular expression wrapped in a span with a highlight class, and all newlines
        converted to breaks; a list of all match groups; and any warnings.
        """
        if self.compiled:
            capture_list = self.capture_groups()
            fulltext = self.regexp_highlight()
            match = Match(capture_list, fulltext, self.warn)
            return match
        else:
            self.warn = "Invalid expression"
            match = Match([], cgi.escape(self.test_string), self.warn)
            return match

    def regexp_match_json(self):
        """
        Return a JSON object consisting of a string of formatted html with all sections of the original text
        matching the given regular expression wrapped in a span with a highlight class, and all newlines
        converted to breaks; a list of all match groups; and any warnings.
        """
        match = self.regexp_match()
        return jsonify(match_groups=match.match_groups,match_text=match.match_text, warn=match.warn )
