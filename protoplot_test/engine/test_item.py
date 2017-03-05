import unittest

from protoplot.engine.item import Item
from protoplot.engine.item_container import ItemContainer

class Test(unittest.TestCase):
    ##################
    ## Test fixture ##
    ##################
    
    def setUp(self):
        class Series(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def register_options(self):
                self.options.register("color"    , inherit = True)
                self.options.register("lineWidth")
                self.options.register("lineStyle")

        class Legend(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                
            def register_options(self):
                self.options.register("color", inherit = True)

        class Plot(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                self.legend = Legend()
                self.series = ItemContainer(Series)

            def register_options(self):
                self.options.register("color")
 
        self.Legend = Legend
        self.Plot = Plot
        self.Series = Series

    def tearDown(self):
        pass


    #########
    ## Tag ##
    #########
        
    def testTag(self):
        Series = self.Series

        series = Series()
        self.assertEqual(series.tags, [])

        series = Series(tag="foo")
        self.assertEqual(series.tags, ["foo"])

        series = Series(tag="foo,bar")
        self.assertEqual(series.tags, ["foo", "bar"])

        series = Series(tag=["foo", "bar"])
        self.assertEqual(series.tags, ["foo", "bar"])


    ##############
    ## Children ##
    ##############

    def testChildren(self):
        plot = self.Plot()
        
        self.assertEqual(plot.children(), [("legend", plot.legend)])
    
    def testContainers(self):
        # TODO implement
        pass


    ###############
    ## Templates ##
    ###############

    def testTemplates(self):
        Series = self.Series
        
        # Same template is same, different templates are different
        self.assertIs   (Series["foo"], Series["foo"])
        self.assertIsNot(Series["foo"], Series["bar"])

    def testAll(self):
        Series = self.Series

        # Special access using .all
        self.assertIs(Series.all, Series[""])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
