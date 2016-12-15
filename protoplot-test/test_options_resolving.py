import unittest
 
from protoplot.engine.item import Item
from protoplot.engine.item_container import ItemContainer

class Series(Item):
    pass

Series.options.register("color", True)
Series.options.register("lineWidth", False)
Series.options.register("lineStyle", False)

class TestOptionsResolving(unittest.TestCase):
    def setUp(self):
        pass
 
    def tearDown(self):
        pass
 
    def testOptionsResolving(self):
        pass
 
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
