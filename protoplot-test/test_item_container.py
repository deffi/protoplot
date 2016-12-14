import unittest

from protoplot.engine.item import Item
from protoplot.engine.item_container import ItemContainer

class TestItemContainer(unittest.TestCase):
    def setUp(self):
        class Series(Item):
            pass

        Series.options.register("color", True)
        Series.options.register("lineWidth", False)
        Series.options.register("lineStyle", False)

        self.Series = Series

        self.series_container = ItemContainer(self.Series)

    def tearDown(self):
        pass

    def testOptions(self):
        self.series_container.set(color = "black")
        
        self.assertEqual(self.series_container.options.values["color"], "black")

    def testItemCreation(self):
        self.series_container.add(color = "red")
        self.series_container.add(color = "green")

        self.assertEqual(self.series_container.items[0].options.values["color"], "red")
        self.assertEqual(self.series_container.items[1].options.values["color"], "green")

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
