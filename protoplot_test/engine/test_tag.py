import unittest

from protoplot.engine.tag import make_tags_list

class TestTag(unittest.TestCase):
    def testMakeTagsList(self):
        tags = make_tags_list(["foo", "bar", "baz"])
        self.assertEqual(tags, ["foo", "bar", "baz"])

        tags = make_tags_list("qux,quux,quuux")
        self.assertEqual(tags, ["qux", "quux", "quuux"])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    