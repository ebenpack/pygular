import unittest
import re
from app import pygular

class RegEx(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_regexp_named_groups(self):
        options = None
        pattern = u'(?P<month>\d{1,2})\/(?P<day>\d{1,2})\/(?P<year>\d{4})'
        test_string = u'Today\'s date is 10/14/2013.\nTomorrow\'s date is 10/15/2013.'

        RegEx = pygular.RegEx(pattern, options, test_string)
        test_match = RegEx.regexp_match()
        match_results = pygular.Match(
            match_groups=[{'match': [{'value': u'10', 'title': u'month'}, {'value': u'14', 'title': u'day'},
                                     {'value': u'2013', 'title': u'year'}]},
                                     {'match': [{'value': u'10', 'title': u'month'},
                                     {'value': u'15', 'title': u'day'}, {'value': u'2013', 'title': u'year'}]}],
            match_text=u"Today's date is <span class='match hilite'>10/14/2013</span>.\nTomorrow's date is <span class='match hilite'>10/15/2013</span>.",
            warn='')
        self.assertEqual(test_match, match_results)

    def test_regexp_multiple_match_groups(self):
        options = None
        pattern = u'(\d+)'
        test_string = u'a1b2c3'

        RegEx = pygular.RegEx(pattern, options, test_string)
        test_match = RegEx.regexp_match()
        match_results = pygular.Match(
            match_groups=[{'match': [{'value': u'1', 'title': 1}]}, {'match': [{'value': u'2', 'title': 1}]},
                          {'match': [{'value': u'3', 'title': 1}]}],
            match_text=u"a<span class='match hilite'>1</span>b<span class='match hilite'>2</span>c<span class='match hilite'>3</span>",
            warn='')
        self.assertEqual(test_match, match_results)

    def test_regexp_mixed_named_unnamed_groups(self):
        options = None
        pattern = u'(a(?P<named>\d))'
        test_string = u'a1b2c3a2s'

        RegEx = pygular.RegEx(pattern, options, test_string)
        test_match = RegEx.regexp_match()
        match_results = pygular.Match(
            match_groups=[{'match': [{'value': u'a1', 'title': 1}, {'value': u'1', 'title': u'named'}]},
                          {'match': [{'value': u'a2', 'title': 1}, {'value': u'2', 'title': u'named'}]}],
            match_text=u"<span class='match hilite'>a1</span>b2c3<span class='match hilite'>a2</span>s",
            warn='')
        self.assertEqual(test_match, match_results)

    def test_regexp_nested_matches(self):
        options = None
        pattern = u'(((\w)\w)(\w))'
        test_string = u'abcdef'

        RegEx = pygular.RegEx(pattern, options, test_string)
        test_match = RegEx.regexp_match()
        match_results = pygular.Match(
            match_groups=[{'match': [{'value': u'abc', 'title': 1}, {'value': u'ab', 'title': 2},
                                     {'value': u'a', 'title': 3}, {'value': u'c', 'title': 4}]},
                                     {'match': [{'value': u'def', 'title': 1}, {'value': u'de', 'title': 2},
                                     {'value': u'd', 'title': 3}, {'value': u'f', 'title': 4}]}],
            match_text=u"<span class='match hilite'>abc</span><span class='match hilite'>def</span>",
            warn='')
        self.assertEqual(test_match, match_results)

    def test_regexp_roman_numerals(self):
        options = None
        pattern = u"^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
        test_string = u"MMMMDCCCLXXXVIII"

        RegEx = pygular.RegEx(pattern, options, test_string)
        test_match = RegEx.regexp_match()
        match_results = pygular.Match(
            match_groups=[{'match': [{'value': u'DCCC', 'title': 1}, {'value': u'LXXX', 'title': 2}, {'value': u'VIII', 'title': 3}]}],
            match_text=u"<span class='match hilite'>MMMMDCCCLXXXVIII</span>",
            warn='')
        self.assertEqual(test_match, match_results)

    def test_regexp_email(self):
        '''
        Perl Mail::RFC822::Address regex. It matches email addresses.
        '''
        options = ['x']
        pattern = u'(?:(?:\\r\\n)?[ \\t])*(?:(?:(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|"(?:[^\\"\\r\\\\]|\\\\.|(?:(?:\\r\\n)?[ \\t]))*"(?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|"(?:[^\\"\\r\\\\]|\\\\.|(?:(?:\\r\\n)?[\\t]))*"(?:(?:\\r\\n)?[ \\t])*))*@(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*))*|(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|"(?:[^\\"\\r\\\\]|\\\\.|(?:(?:\\r\\n)?[ \\t]))*"(?:(?:\\r\\n)?[ \\t])*)*\\<(?:(?:\\r\\n)?[ \\t])*(?:@(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*))*(?:,@(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*))*)*:(?:(?:\\r\\n)?[ \\t])*)?(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|"(?:[^\\"\\r\\\\]|\\\\.|(?:(?:\\r\\n)?[ \\t]))*"(?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|"(?:[^\\"\\r\\\\]|\\\\.|(?:(?:\\r\\n)?[ \\t]))*"(?:(?:\\r\\n)?[ \\t])*))*@(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*))*\\>(?:(?:\\r\\n)?[ \\t])*)|(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|"(?:[^\\"\\r\\\\]|\\\\.|(?:(?:\\r\\n)?[ \\t]))*"(?:(?:\\r\\n)?[ \\t])*)*:(?:(?:\\r\\n)?[ \\t])*(?:(?:(?:[^()<>@,;:\\\\".\\[\\]\\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|"(?:[^\\"\\r\\\\]|\\\\.|(?:(?:\\r\\n)?[ \\t]))*"(?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|"(?:[^\\"\\r\\\\]|\\\\.|(?:(?:\\r\\n)?[ \\t]))*"(?:(?:\\r\\n)?[ \\t])*))*@(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*))*|(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|"(?:[^\\"\\r\\\\]|\\\\.|(?:(?:\\r\\n)?[ \\t]))*"(?:(?:\\r\\n)?[ \\t])*)*\\<(?:(?:\\r\\n)?[ \\t])*(?:@(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*))*(?:,@(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\]\\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*))*)*:(?:(?:\\r\\n)?[ \\t])*)?(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|"(?:[^\\"\\r\\\\]|\\\\.|(?:(?:\\r\\n)?[ \\t]))*"(?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|"(?:[^\\"\\r\\\\]|\\\\.|(?:(?:\\r\\n)?[ \\t]))*"(?:(?:\\r\\n)?[ \\t])*))*@(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*))*\\>(?:(?:\\r\\n)?[ \\t])*)(?:,\\s*(?:(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|"(?:[^\\"\\r\\\\]|\\\\.|(?:(?:\\r\\n)?[ \\t]))*"(?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|"(?:[^\\"\\r\\\\]|\\\\.|(?:(?:\\r\\n)?[ \\t]))*"(?:(?:\\r\\n)?[ \\t])*))*@(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*))*|(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|"(?:[^\\"\\r\\\\]|\\\\.|(?:(?:\\r\\n)?[ \\t]))*"(?:(?:\\r\\n)?[ \\t])*)*\\<(?:(?:\\r\\n)?[ \\t])*(?:@(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*))*(?:,@(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*))*)*:(?:(?:\\r\\n)?[ \\t])*)?(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|"(?:[^\\"\\r\\\\]|\\\\.|(?:(?:\\r\\n)?[ \\t]))*"(?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|"(?:[^\\"\\r\\\\]|\\\\.|(?:(?:\\r\\n)?[ \\t]))*"(?:(?:\\r\\n)?[ \\t])*))*@(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*)(?:\\.(?:(?:\\r\\n)?[ \\t])*(?:[^()<>@,;:\\\\".\\[\\] \\000-\\031]+(?:(?:(?:\\r\\n)?[ \\t])+|\\Z|(?=[\\["()<>@,;:\\\\".\\[\\]]))|\\[([^\\[\\]\\r\\\\]|\\\\.)*\\](?:(?:\\r\\n)?[ \\t])*))*\\>(?:(?:\\r\\n)?[ \\t])*))*)?;\\s*)'

        test_string = u'testaddress@example.com'

        RegEx = pygular.RegEx(pattern, options, test_string)
        test_match = RegEx.regexp_match()
        match_results = pygular.Match(
            match_groups=[{'match': [{'value': None, 'title': 1}, {'value': None, 'title': 2},
                                     {'value': None, 'title': 3}, {'value': None, 'title': 4},
                                     {'value': None, 'title': 5}, {'value': None, 'title': 6},
                                     {'value': None, 'title': 7}, {'value': None, 'title': 8},
                                     {'value': None, 'title': 9}, {'value': None, 'title': 10},
                                     {'value': None, 'title': 11}, {'value': None, 'title': 12},
                                     {'value': None, 'title': 13}, {'value': None, 'title': 14},
                                     {'value': None, 'title': 15}, {'value': None, 'title': 16},
                                     {'value': None, 'title': 17}, {'value': None, 'title': 18},
                                     {'value': None, 'title': 19}, {'value': None, 'title': 20},
                                     {'value': None, 'title': 21}, {'value': None, 'title': 22},
                                     {'value': None, 'title': 23}, {'value': None, 'title': 24}]}],
            match_text=u"<span class='match hilite'>testaddress@example.com</span>",
            warn='')
        self.assertEqual(test_match, match_results)

# TODO: Add tests for the following:


if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass