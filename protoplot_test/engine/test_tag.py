import unittest

from protoplot.engine.tag import make_tags_list

class TestTag(unittest.TestCase):
    '''
    Tests the creation of a tag list. Tag lists can be specified different ways.
    '''

    def testMakeTagsListFromList(self):
        # Empty list
        tags = make_tags_list([])
        self.assertEqual(tags, [])

        # Single tag as list
        tags = make_tags_list(["foo"])
        self.assertEqual(tags, ["foo"])

        # Multiple tags as list
        tags = make_tags_list(["foo", "bar", "baz"])
        self.assertEqual(tags, ["foo", "bar", "baz"])

        # Multiple tags as nested lists
        tags = make_tags_list(["foo", ["bar", "baz"]])
        self.assertEqual(tags, ["foo", "bar", "baz"])

    def testMakeTagsFromString(self):
        # Empty string
        tags = make_tags_list("")
        self.assertEqual(tags, [])

        # Single tag as string
        tags = make_tags_list("foo")
        self.assertEqual(tags, ["foo"])

        # Multiple tags as comma-separated string
        tags = make_tags_list("foo,bar,baz")
        self.assertEqual(tags, ["foo", "bar", "baz"])

        # Multiple tags as space-separated string
        tags = make_tags_list("foo bar baz")
        self.assertEqual(tags, ["foo", "bar", "baz"])

        # Multiple tags as comma-and-semicolon-separated string
        tags = make_tags_list("foo,bar;baz")
        self.assertEqual(tags, ["foo", "bar", "baz"])

        # Multiple tags as comma-separated string
        tags = make_tags_list("foo,bar,baz")
        self.assertEqual(tags, ["foo", "bar", "baz"])

        # Multiple tags as comma-separated string with extra whitespace
        tags = make_tags_list("foo  ,  bar,  baz  ,  ")
        self.assertEqual(tags, ["foo", "bar", "baz"])

        # Multiple tags as comma-separated string with extra commas
        tags = make_tags_list(",foo,,bar,")
        self.assertEqual(tags, ["foo", "bar"])

    def testMakeTagsFromMixed(self):
        # List with comma-separated string
        tags = make_tags_list(["foo", "bar,baz"])
        self.assertEqual(tags, ["foo", "bar", "baz"])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    