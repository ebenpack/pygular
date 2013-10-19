import unittest
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
            match_groups=[[{u'month': u'10'}, {u'day': u'14'}, {u'year': u'2013'}], [{u'month': u'10'}, {u'day': u'15'}, {u'year': u'2013'}]],
            match_text=u'Today\'s date is <span class="match hilite">10/14/2013</span>.\nTomorrow\'s date is <span class="match hilite">10/15/2013</span>.',
            warn='')
        self.assertEqual(test_match, match_results)

    def test_regexp_multiple_match_groups(self):
        options = None
        pattern = u'(\d+)'
        test_string = u'a1b2c3'

        RegEx = pygular.RegEx(pattern, options, test_string)
        test_match = RegEx.regexp_match()
        match_results = pygular.Match(
            match_groups=[[{1: u'1'}], [{1: u'2'}], [{1: u'3'}]],
            match_text=u'a<span class="match hilite">1</span>b<span class="match hilite">2</span>c<span class="match hilite">3</span>',
            warn='')
        self.assertEqual(test_match, match_results)

    def test_regexp_mixed_named_unnamed_groups(self):
        options = None
        pattern = u'(a(?P<named>\d))'
        test_string = u'a1b2c3a2s'

        RegEx = pygular.RegEx(pattern, options, test_string)
        test_match = RegEx.regexp_match()
        match_results = pygular.Match(
            match_groups=[ [{1:u'a1'}, {u'named': u'1'}], [{1:u'a2'}, {u'named': u'2'}] ],
            match_text=u'<span class="match hilite">a1</span>b2c3<span class="match hilite">a2</span>s',
            warn='')
        self.assertEqual(test_match, match_results)

    def test_regexp_nested_matches(self):
        options = None
        pattern = u'(((\w)\w)(\w))'
        test_string = u'abcdef'

        RegEx = pygular.RegEx(pattern, options, test_string)
        test_match = RegEx.regexp_match()
        match_results = pygular.Match(
            match_groups=[ [{1:u'abc'}, {2: u'ab'}, {3:u'a'}, {4:u'c'}], [{1:u'def'}, {2: u'de'}, {3:u'd'}, {4:u'f'}] ],
            match_text=u'<span class="match hilite">abc</span><span class="match hilite">def</span>',
            warn='')
        self.assertEqual(test_match, match_results)

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass