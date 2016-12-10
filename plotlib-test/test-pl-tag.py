import unittest

from plotlib import pl_tag as tag

class Test(unittest.TestCase):
    def testTag(self):
        tags = tag.make_tags_list(["foo", "bar", "baz"])
        self.assertEqual(tags, ["foo", "bar", "baz"])

        tags = tag.make_tags_list("qux,quux,quuux")
        self.assertEqual(tags, ["qux", "quux", "quuux"])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
