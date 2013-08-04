# TODO: Need to write tests. Some possiblilities below.

import unittest
from app import app

from coverage import coverage
cov = coverage(branch = True, omit = ['flask/*', 'tests.py'])
cov.start()

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_regexp_highlight(self):
        pass

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print "\n\nCoverage Report:\n"
    cov.report()
    # print "HTML version: " + os.path.join(basedir, "tmp/coverage/index.html")
    # cov.html_report(directory = 'tmp/coverage')
    cov.erase()

# (?P<first_name>\w+) (?P<last_name>\w+)
# First Last
# 	Match 1:
# 		first_name.  First
#		last_name.  Last
#
# (\d+)\.?
# a1b2c3
# 	Match 1:
# 		1. 1
# 	Match 2:
# 		1. 2
# 	Match 3:
# 		1. 3
#
#
# (a(1))\.?
# a1b2c3a1
# 	Match 1:
# 		1. a1
# 		2. 1
# 	Match 2:
# 		1. a1
# 		2. 1
#
#
# (a(?P<named>\d))\.?
# a1b2c3a2s
# 	Match 1:
# 		1. a1
# 		named. 1
# 	Match 2:
# 		1. a1
# 		named. 2
# [
# 	['a1', {'named': 1}],
# 	['a2', {'named': 2}]
# ]
#
# (((\w)\w)(\w))
# abcdef
# 	Match 1:
# 		1.  abc
#		2.  ab
#		3.  a
#		4.  c
#	Match 2:
#		1.  def
#		2.  de
#		3.  d
#		4.  f