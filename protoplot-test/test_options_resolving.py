import unittest
 
from protoplot.engine.item import Item
from protoplot.engine.item_container import ItemContainer

class TestOptionsResolving(unittest.TestCase):
    ##################
    ## Test fixture ##
    ##################
    
    def setUp(self):
        class Legend(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.options.register("a", True)  # Inherit
                self.options.register("b", False) # Same name, don't inherit
                self.options.register("e", False) # Different name
        
        class Series(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.options.register("a", True)  # Inherit
                self.options.register("b", False) # Same name, don't inherit
                self.options.register("d", False) # Different name

        class Plot(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.options.register("a", False)
                self.options.register("b", False)
                self.options.register("c", False)
 
                self.series = ItemContainer(Series)
                self.legend = Legend()
 
        plot=Plot()
        plot.series.add()
        plot.series.add()
        plot.series.add()
 
        self.Legend = Legend
        self.Plot = Plot
        self.Series = Series
        self.plot = plot

    def tearDown(self):
        pass


    ###################
    ## Single source ##
    ###################

    def testSpecific(self):
        self.plot                .set(a=1)
        self.plot.legend         .set(a=2)
        self.plot.series.items[0].set(a=3)
        self.plot.series.items[1].set(a=4)
        self.plot.series.items[2].set(a=5)

        resolved = self.plot.resolve_options()

        self.assertEqual(resolved[self.plot                ]["a"], 1)
        self.assertEqual(resolved[self.plot.legend         ]["a"], 2)
        self.assertEqual(resolved[self.plot.series.items[0]]["a"], 3)
        self.assertEqual(resolved[self.plot.series.items[1]]["a"], 4)
        self.assertEqual(resolved[self.plot.series.items[2]]["a"], 5)
        
 
    def testClassTemplateAll(self):
        self.Plot  .all.set(a=1)
        self.Series.all.set(a=2)
        self.Legend.all.set(a=3)
 
        resolved = self.plot.resolve_options()

        #self.assertEqual(resolved[self.plot                ]["a"], 1)
        #self.assertEqual(resolved[self.plot.legend         ]["a"], 2)
        #self.assertEqual(resolved[self.plot.series.items[0]]["a"], 3)
        #self.assertEqual(resolved[self.plot.series.items[1]]["a"], 3)
        #self.assertEqual(resolved[self.plot.series.items[2]]["a"], 3)
 
    def testClassTemplateByTag(self):
        pass
    
    def testContainerTemplateAll(self):
        pass
    
    def testContainerTemplateByTag(self):
        pass
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
