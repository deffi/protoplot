import unittest

from protoplot.engine.item import Item

class Test(unittest.TestCase):
    ##################
    ## Test fixture ##
    ##################
    
    def setUp(self):
        class Legend(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.options.register("color", True)
        
        class Plot(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.options.register("color", False)
 
                self.legend = Legend()
 
        class Series(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.options.register("color"    , True)
                self.options.register("lineWidth", False)
                self.options.register("lineStyle", False)
 
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


    #############
    ## Options ##
    #############

    def testOptionCount(self):
        plot   = self.Plot()
        series = self.Series()
         
        self.assertEqual(len(plot  .options), 1)
        self.assertEqual(len(series.options), 3)

    def testOptions(self):
        series1 = self.Series()
        series2 = self.Series()
          
        # Different instances have different sets of options
        series1.options.set(color="red"  , lineWidth = 1)
        series2.options.set(color="green")
        series2.options.set(lineWidth = 2)
          
        self.assertEqual(series1.options.values["color"], "red"  )
        self.assertEqual(series2.options.values["color"], "green")
  
        self.assertEqual(series1.options.values["lineWidth"], 1)
        self.assertEqual(series2.options.values["lineWidth"], 2)
    
    def testInstanceSet(self):
        series1 = self.Series()
        series2 = self.Series()
          
        # Different instances have different sets of options
        series1.set(color="red"  , lineWidth = 1)
        series2.set(color="green")
        series2.set(lineWidth = 2)
          
        self.assertEqual(series1.options.values["color"], "red"  )
        self.assertEqual(series2.options.values["color"], "green")
  
        self.assertEqual(series1.options.values["lineWidth"], 1)
        self.assertEqual(series2.options.values["lineWidth"], 2)


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

    def testTemplateOptions(self):
        Series = self.Series
        
        Series["foo"].set(color = "red"  )
        Series["bar"].set(color = "green")
        Series.all   .set(color = "black")
        
        self.assertEqual(Series["foo"].options.values, { "color": "red"   })
        self.assertEqual(Series["bar"].options.values, { "color": "green" })
        self.assertEqual(Series.all   .options.values, { "color": "black" })

    def testClassSet(self):
        Series = self.Series
        
        Series.set(color = "red")
        
        self.assertEqual(Series.all.options.values["color"], "red")

    def testNestedTemplates(self):
        # This is for the case where one items explicitly contains another. If
        # an item contains multiple items (such as series in a plot), that's
        # a case for item containers. 
        
        Plot = self.Plot
        Legend = self.Legend
        
        plot = Plot()

        Legend            .set(color = "black") # All legends (Legend.all)        
        Plot.all   .legend.set(color = "green") # Legend in any plot
        Plot["foo"].legend.set(color = "blue")  # Legend in any plot with tag 
        plot       .legend.set(color = "red")   # Legend in specific plot
        
        self.assertEqual(Legend.all        .options.values["color"], "black")
        self.assertEqual(Plot.all   .legend.options.values["color"], "green")
        self.assertEqual(Plot["foo"].legend.options.values["color"], "blue")
        self.assertEqual(plot       .legend.options.values["color"], "red")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
