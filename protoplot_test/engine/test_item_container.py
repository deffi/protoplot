import unittest

from protoplot.engine.item_container import ItemContainer

class TestItemContainer(unittest.TestCase):
    ##################
    ## Test fixture ##
    ##################
    
    def setUp(self):
        # A class that mimics an Item subclass
        class MockPoint:
            def __init__(self, **kwargs):
                self.options = {}
                self.options.update(kwargs)
                
            def set(self, **kwargs):
                self.options.update(kwargs)

        self.MockPoint = MockPoint
        self.points = ItemContainer(MockPoint)

    def tearDown(self):
        pass


    ###########
    ## Items ##
    ###########

    def testItemCreation(self):
        points = self.points

        # The add method creates instances of the item class, passing arguments
        # to the constructor
        points.add(x=11)
        points.add(x=22)

        # We must now have 2 items
        self.assertEqual(len(points.items), 2)

        # The class of the items must match the item class (MockPoint)
        self.assertIsInstance(points.items[0], self.MockPoint)
        self.assertIsInstance(points.items[1], self.MockPoint)

        # The value passed on creation must be set correctly
        self.assertEqual(points.items[0].options["x"], 11)
        self.assertEqual(points.items[1].options["x"], 22)

    def testLast(self):
        points = self.points

        # After adding an item, the last property must be the recently added
        # item.
        points.add(x=33)
        self.assertIs(points.last, points.items[0])
        points.add(x=44)
        self.assertIs(points.last, points.items[1])
        points.add(x=55)
        self.assertIs(points.last, points.items[2])

        # The value passed on creation must be set correctly
        self.assertEqual(points.items[0].options["x"], 33)
        self.assertEqual(points.items[1].options["x"], 44)
        self.assertEqual(points.items[2].options["x"], 55)


    ###############
    ## Templates ##
    ###############

    def testContainerTemplates(self):
        # See also: TestItem.testClassTemplates
        MockPoint = self.MockPoint
        points    = self.points

        # Templates must be instances of the container's item class.
        self.assertIsInstance(points["foo"], MockPoint)

        # Accesses to the template with the same name must always return the
        # same template.
        self.assertIs(points["foo"], points["foo"])
        self.assertIs(points[""]   , points[""]   )

        # Accesses to templates with different names must return different
        # templates.
        self.assertIsNot(points["foo"], points["bar"])

        # Accesses to .all must always return the same template, which must be
        # the same as the template with the empty name.
        self.assertIs(points.all, points.all)
        self.assertIs(points.all, points[""])


    def testSetShortcut(self):
        # Test the .set shortcut of the container. Note that the container's
        # item class (MockPoint) is not actually an Item instance, and its
        # options attribute is a dict rather than an options container.

        points = self.points

        points.all.set(color = "red")
        self.assertEqual(points.all.options["color"], "red")

        points.set(color = "green")
        self.assertEqual(points.all.options["color"], "green")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
