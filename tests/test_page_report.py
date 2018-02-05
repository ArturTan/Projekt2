import sys
import unittest
from page_report import page_report

class TestReportCase(unittest.TestCase):

    def test_page_report(self):
        name_of_file = "today.log"
        page_report("./tests/" + name_of_file)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("Buffer mode needed")
        output = sys.stdout.getvalue().strip()

        self.assertEqual(output, '''"clearcode.cc/careers",6\n"clearcode.cc",1\n"www.clearcode.cc",1''')
