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
        self.points = ItemContainer(self.MockPoint)

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

    def testTemplates(self):
        points = self.points
        
        # Same template is same, different templates are different
        self.assertIs   (points["foo"], points["foo"])
        self.assertIsNot(points["foo"], points["bar"])
 
    def testAll(self):
        points = self.points

        # Special access using .all
        self.assertIs(points.all, points[""])

    def testSet(self):
        points = self.points
         
        points.set(color = "red")
         
        self.assertEqual(points.all.options["color"], "red")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
