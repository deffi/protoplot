import unittest
 
from protoplot.engine.item import Item
from protoplot.engine.item_container import ItemContainer

class TestOptionsResolving(unittest.TestCase):
    ##################
    ## Test fixture ##
    ##################
    
    def setUp(self):
        class Series(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.options.register("a", True)  # Inherit
                self.options.register("b", False) # Same name, don't inherit
                self.options.register("d", False) # Different name

        class Legend(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.options.register("a", True)  # Inherit
                self.options.register("b", False) # Same name, don't inherit
                self.options.register("e", False) # Different name
        
        class Plot(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.options.register("a", False)
                self.options.register("b", False)
                self.options.register("c", False)
 
                self.series = ItemContainer(Series)
                self.legend = Legend()
 
        class Page(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.options.register("a", False)
                self.options.register("b", False)
                self.options.register("c", False)

                self.plots = ItemContainer(Plot)

        # Create instances
        page=Page()                
        plot=page.plots.add(tag="alpha")
        legend=plot.legend
        series=[
            plot.series.add(tag="one"),
            plot.series.add(tag="two"),
            plot.series.add(tag="one,two"),
        ]
 
        # Store the classes in the test case
        self.Page   = Page
        self.Plot   = Plot
        self.Legend = Legend
        self.Series = Series

        # Store the instances in the test case
        self.page   = page        
        self.plot   = plot
        self.legend = legend
        self.series = series

    def tearDown(self):
        pass


    #####################
    ## Object identity ##
    #####################

    def testObjectIdentity(self):
        # We store some objects in the test case - make sure that they are
        # identical to the correct items in the tree.
        self.assertIs(self.plot     , self.page.plots.items[0])
        self.assertIs(self.legend   , self.plot.legend)
        self.assertIs(self.series[0], self.plot.series.items[0])
        self.assertIs(self.series[1], self.plot.series.items[1])
        self.assertIs(self.series[2], self.plot.series.items[2])


    #####################
    ## Setting options ##
    #####################
    
    # The model looks like this:
    #     page
    #     '- plots...
    #        |- legend
    #        '- series...

    # To set options for an item (page, plot, legend, or series), we select it
    # by starting either with a class template or an instance. We then select
    # children directly (legend) or via container template (plots, series). A
    # class template or container template is selected either by (class or
    # container)["..."] or by (class or container).all.   
    #
    # These are the possible ways to set options for series:
    #     Page.all.plots.all.series.all.set(...)
    #     my_page .plots.all.series.all.set(...)
    #              Plot .all.series.all.set(...)
    #              my_plot  .series.all.set(...)
    #                        Series.all.set(...)
    #                        my_series .set(...)
    # For legend:
    #     Page.all.plots.all.legend.set(...)
    #     my_page .plots.all.legend.set(...)
    #              Plot .all.legend.set(...)
    #              my_plot  .legend.set(...)
    #                        Legend.all.set(...)
    #                        my_legend .set(...) - Same as my_plot.legend 
    # For plot:
    #     Page.all.plots.all.set(...)
    #     my_page .plots.all.set(...)
    #              Plot .all.set(...)
    #              my_plot  .set(...)
    # For page:
    #     Page.all.set(...)
    #     my_page .set(...)
    #
    # We can only test a item once per test, so we group the cases by how they
    # start, not by how they end (i. e. what is accessed).
    #
    # Note that we only use the default selector (.all) here - we use tag
    # selectors in the next section. Also, there is a shortcut that allows us
    # to call .set directly on a container or a class - we also test that in a
    # separate section.

    def testOptionsViaPageClass(self):
        self.Page.all.set                     (a=1)
        self.Page.all.plots.all.set           (a=2)
        self.Page.all.plots.all.legend.set    (a=3)
        self.Page.all.plots.all.series.all.set(a=4)

        resolved = self.page.resolve_options()

        self.assertEqual(resolved[self.page     ]["a"], 1)
        self.assertEqual(resolved[self.plot     ]["a"], 2)
        self.assertEqual(resolved[self.legend   ]["a"], 3)
        self.assertEqual(resolved[self.series[0]]["a"], 4)
        self.assertEqual(resolved[self.series[1]]["a"], 4)
        self.assertEqual(resolved[self.series[2]]["a"], 4)
    
    def testOptionsViaPageInstance(self):
        self.page                     .set(a=1)
        self.page.plots.all           .set(a=2)
        self.page.plots.all.legend    .set(a=3)
        self.page.plots.all.series.all.set(a=4)

        resolved = self.page.resolve_options()
        
        self.assertEqual(resolved[self.page     ]["a"], 1)
        self.assertEqual(resolved[self.plot     ]["a"], 2)
        self.assertEqual(resolved[self.legend   ]["a"], 3)
        self.assertEqual(resolved[self.series[0]]["a"], 4)
        self.assertEqual(resolved[self.series[1]]["a"], 4)
        self.assertEqual(resolved[self.series[2]]["a"], 4)
    
    def testOptionsViaPlotClass(self):
        self.Plot.all           .set(a=1)
        self.Plot.all.legend    .set(a=2)
        self.Plot.all.series.all.set(a=3)

        resolved = self.page.resolve_options()
 
        self.assertEqual(resolved[self.plot     ]["a"], 1)
        self.assertEqual(resolved[self.legend   ]["a"], 2)
        self.assertEqual(resolved[self.series[0]]["a"], 3)
        self.assertEqual(resolved[self.series[1]]["a"], 3)
        self.assertEqual(resolved[self.series[2]]["a"], 3)
    
    def testOptionsViaPlotInstance(self):
        self.plot           .set(a=1)
        self.plot.legend    .set(a=2)
        self.plot.series.all.set(a=3)
  
        resolved = self.page.resolve_options()

        self.assertEqual(resolved[self.plot     ]["a"], 1)
        self.assertEqual(resolved[self.legend   ]["a"], 2)
        self.assertEqual(resolved[self.series[0]]["a"], 3)
        self.assertEqual(resolved[self.series[1]]["a"], 3)
        self.assertEqual(resolved[self.series[2]]["a"], 3)
    
    def testOptionsViaLegendClass(self):
        self.Legend.all.set(a=1)
        
        resolved = self.page.resolve_options()
        
        self.assertEqual(resolved[self.legend]["a"], 1)
    
    def testOptionsViaLegendInstance(self):
        self.legend.set(a=1)
        
        resolved = self.page.resolve_options()
        
        self.assertEqual(resolved[self.legend]["a"], 1)
    
    def testOptionsViaSeriesClass(self):
        self.Series.all.set(a=1)

        resolved = self.page.resolve_options()
 
        self.assertEqual(resolved[self.series[0]  ]["a"], 1)
        self.assertEqual(resolved[self.series[1]  ]["a"], 1)
        self.assertEqual(resolved[self.series[2]  ]["a"], 1)
    
    def testOptionsViaSeriesInstance(self):
        self.series[0]  .set(a=1)
        self.series[1]  .set(a=2)
        self.series[2]  .set(a=3)
        
        resolved = self.page.resolve_options()
        
        self.assertEqual(resolved[self.series[0]  ]["a"], 1)
        self.assertEqual(resolved[self.series[1]  ]["a"], 2)
        self.assertEqual(resolved[self.series[2]  ]["a"], 3)


    ###############
    ## Selectors ##
    ###############

    # Test non-default selectors, i. e. ["..."] instead of (and in conjunction
    # with) the default selector (.all). Also make sure that [""] is the same
    # as .all.

    
    ###############
    ## Shortcuts ##
    ###############
    
    # Plot.set(...) for Plot.all.set(...)
    # my_plot.series(...) for my_plot.series.all.set(...)


    ###################
    ## Single source ##
    ###################

    # TODO more systematic

    def testNotSet(self):
        # TODO must be at the default value
        pass
 
    def testClassTemplateByTag(self):
        self.Series["one"].set(a=1)
        self.Series["two"].set(a=2)
 
        resolved = self.page.resolve_options()
 
        self.assertEqual(resolved[self.series[0]]["a"], 1) # one
        self.assertEqual(resolved[self.series[1]]["a"], 2) # two
        # TODO in case both tags match, which one is effective?
        self.assertIn   (resolved[self.series[2]]["a"], [1, 2]) # one,two
     
    def testContainerTemplateByTag(self):
        self.plot.series["one"].set(a=1)
        self.plot.series["two"].set(a=2)
 
        resolved = self.page.resolve_options()
 
        self.assertEqual(resolved[self.series[0]]["a"], 1) # one
        self.assertEqual(resolved[self.series[1]]["a"], 2) # two
        # TODO in case both tags match, which one is effective?
        self.assertIn   (resolved[self.series[2]]["a"], [1, 2]) # one,two

    def testAncesterClassTemplateByTag(self):
        self.Plot["alpha"].legend    .set(a=2)
        self.Plot["alpha"].series.all.set(a=3)
 
        resolved = self.page.resolve_options()
 
        self.assertEqual(resolved[self.plot.legend]["a"], 2)
        self.assertEqual(resolved[self.series[0]  ]["a"], 3)
        self.assertEqual(resolved[self.series[1]  ]["a"], 3)
        self.assertEqual(resolved[self.series[2]  ]["a"], 3)
 
    def testAncestorContainerTemplateByTag(self):
        self.page.plots["alpha"].legend    .set(a=2)
        self.page.plots["alpha"].series.all.set(a=3)
 
        resolved = self.page.resolve_options()
 
        self.assertEqual(resolved[self.plot.legend]["a"], 2)
        self.assertEqual(resolved[self.series[0]  ]["a"], 3)
        self.assertEqual(resolved[self.series[1]  ]["a"], 3)
        self.assertEqual(resolved[self.series[2]  ]["a"], 3)
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
