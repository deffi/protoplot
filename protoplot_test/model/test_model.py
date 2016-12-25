import unittest

from protoplot.model import Axis, Legend, Plot, Point, Series, Text

class Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testModel(self):
        plot=Plot()
        plot.series.add(x=[0, 1, 2, 3, 4], y=[1, 1, 1, 1, 1] , tag="constant")
        plot.series.add(x=[0, 1, 2, 3, 4], y=[0, 1, 2, 3, 4] , tag="linear")
        plot.series.add(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16], tag="quadratic")



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()