import unittest

from protoplot.engine.item import Item

class Test(unittest.TestCase):
    def setUp(self):
        class Plot(Item):
            pass

        Plot.options.register("color", False)

        class Series(Item):
            pass

        Series.options.register("color", True)
        Series.options.register("lineWidth", False)
        Series.options.register("lineStyle", False)

        self.assertEqual(len(Plot.options), 1)
        self.assertEqual(len(Series.options), 3)

        self.Plot = Plot
        self.Series = Series

    def tearDown(self):
        pass

    def testOptions(self):
        my_series = self.Series()
        
        self.Series.set(color="red")
        my_series.set(color="green")

        self.assertEqual(self.Series.options.values["color"], "red"  )
        self.assertEqual(my_series  .options.values["color"], "green")
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
