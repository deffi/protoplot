import unittest
 
from protoplot.engine.item import Item
from protoplot.engine.item_container import ItemContainer


# TODO there should be different defaults for different items
# TODO set Plot.all.a and plot[0].a, the latter must have precedence.

class TestOptionsResolving(unittest.TestCase):
    '''
    The model looks like this:
        page            (Page)
        '- plots...        (ItemContainer with Plot)
           |- legend          (Legend)
           '- series...       (ItemContainer with Series)
 
    To set options for an item (page, plot, legend, or series), we select it
    by starting either with a class template or an instance. We then select
    children directly (legend) or via container template (plots, series). A
    class template or container template is selected either by (class or
    container)["..."] or by (class or container).all.   
    
    These are the possible ways to set options for series:
        Page.all.plots.all.series.all.set(...)
        my_page .plots.all.series.all.set(...)
                 Plot .all.series.all.set(...)
                 my_plot  .series.all.set(...)
                           Series.all.set(...)
                           my_series .set(...)
    For legend:
        Page.all.plots.all.legend.set(...)
        my_page .plots.all.legend.set(...)
                 Plot .all.legend.set(...)
                 my_plot  .legend.set(...)
                           Legend.all.set(...)
                           my_legend .set(...) - Same as my_plot.legend 
    For plot:
        Page.all.plots.all.set(...)
        my_page .plots.all.set(...)
                 Plot .all.set(...)
                 my_plot  .set(...)
    For page:
        Page.all.set(...)
        my_page .set(...)
    
    We use the following tree for the test (with tags in parentheses):
        page                             self.page
        '- plots
           |- plot (alpha)               self.plots[0]
           |  |- legend                  self.legends[0]
           |  '- series
           |     |- series (one)         self.series[0][0]
           |     |- series (two)         self.series[0][1]
           |     '- series (one, two)    self.series[0][2]
           '- plot (beta)                self.plots[1]
              |- legend                  self.legends[1]
              '- series
                 |- series (one)         self.series[1][0]
                 |- series (two)         self.series[1][1]
                 '- series (one, two)    self.series[1][2]
    '''

    ##################
    ## Test fixture ##
    ##################
    
    def setUp(self):
        class Series(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                
            def register_options(self):
                self.options.register("a", "defaultA", inherit = True) # Inherit
                self.options.register("b", "defaultB") # Same name, don't inherit
                self.options.register("d", "defaultD") # Different name

        class Legend(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                
            def register_options(self):
                self.options.register("a", "defaultA", inherit = True) # Inherit
                self.options.register("b", "defaultB") # Same name, don't inherit
                self.options.register("e", "defaultE") # Different name
        
        class Plot(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                self.series = ItemContainer(Series)
                self.legend = Legend()
 
            def register_options(self):
                self.options.register("a", "defaultA", inherit = True)
                self.options.register("b", "defaultB")
                self.options.register("c", "defaultC")
 
        class Page(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                self.plots = ItemContainer(Plot)
                
            def register_options(self):
                self.options.register("a", "defaultA")
                self.options.register("b", "defaultB")
                self.options.register("c", "defaultC")

        # Create instances
        page=Page()                
        plots=[
            page.plots.add(tag="alpha"),
            page.plots.add(tag="beta" ),
        ]
        legends=[
            plots[0].legend,
            plots[1].legend,
        ]
        series=[
            [
                plots[0].series.add(tag="one"),
                plots[0].series.add(tag="two"),
                plots[0].series.add(tag="one,two"),
            ],
            [
                plots[1].series.add(tag="one"),
                plots[1].series.add(tag="two"),
                plots[1].series.add(tag="one,two"),
            ]
        ]
 
        # Store the classes in the test case
        self.Page   = Page
        self.Plot   = Plot
        self.Legend = Legend
        self.Series = Series

        # Store the instances in the test case
        self.page    = page        
        self.plots   = plots
        self.legends = legends
        self.series  = series

    def tearDown(self):
        pass


    #####################
    ## Object identity ##
    #####################

    def testObjectIdentity(self):
        # We store some objects in the test case - make sure that they are
        # identical to the correct items in the tree.
        self.assertIs(self.plots[0]    , self.page.plots.items[0])
        self.assertIs(self.plots[1]    , self.page.plots.items[1])
        self.assertIs(self.legends[0]  , self.plots[0].legend)
        self.assertIs(self.legends[1]  , self.plots[1].legend)
        self.assertIs(self.series[0][0], self.plots[0].series.items[0])
        self.assertIs(self.series[0][1], self.plots[0].series.items[1])
        self.assertIs(self.series[0][2], self.plots[0].series.items[2])
        self.assertIs(self.series[1][0], self.plots[1].series.items[0])
        self.assertIs(self.series[1][1], self.plots[1].series.items[1])
        self.assertIs(self.series[1][2], self.plots[1].series.items[2])


    #####################
    ## Default options ##
    #####################

    # If no options have been set, all options must have their default value.

    def testNotSet(self):
        resolved = self.page.resolve_options()

        self.assertEqual(resolved[self.page]["a"], "defaultA")
 
        self.assertEqual(resolved[self.plots[0]]["a"], "defaultA")
        self.assertEqual(resolved[self.plots[1]]["a"], "defaultA")
 
        self.assertEqual(resolved[self.legends[0]]["a"], "defaultA")
        self.assertEqual(resolved[self.legends[1]]["a"], "defaultA")
 
        self.assertEqual(resolved[self.series[0][0]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[0][1]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[0][2]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[1][0]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[1][1]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[1][2]]["a"], "defaultA")
    
 
    ###############################################################
    ## Setting options via item instance using default selectors ##
    ###############################################################

    # This is the most basic case, starting from an instance and selecting the
    # children via their containers. Note that we only use the default selector
    # (.all) here - we test tag selectors in another section. Also, there is a
    # shortcut that allows us to call .set directly on a container or a class -
    # we also test that in a separate section.
    #
    # We can only use each item once per test, so we group the cases by how they
    # start, not by how they end (i. e. what is accessed).

    def testOptionsViaPageInstance(self):
        self.page                     .set(a=1)
        self.page.plots.all           .set(a=2)
        self.page.plots.all.legend    .set(a=3)
        self.page.plots.all.series.all.set(a=4)

        resolved = self.page.resolve_options()
        
        self.assertEqual(resolved[self.page        ]["a"], 1)
        self.assertEqual(resolved[self.plots[0]    ]["a"], 2)
        self.assertEqual(resolved[self.plots[1]    ]["a"], 2)
        self.assertEqual(resolved[self.legends[0]  ]["a"], 3)
        self.assertEqual(resolved[self.legends[1]  ]["a"], 3)
        self.assertEqual(resolved[self.series[0][0]]["a"], 4)
        self.assertEqual(resolved[self.series[0][1]]["a"], 4)
        self.assertEqual(resolved[self.series[0][2]]["a"], 4)
        self.assertEqual(resolved[self.series[1][0]]["a"], 4)
        self.assertEqual(resolved[self.series[1][1]]["a"], 4)
        self.assertEqual(resolved[self.series[1][2]]["a"], 4)

    def testOptionsViaPlotInstance(self):
        self.plots[0]           .set(a=1)
        self.plots[0].legend    .set(a=2)
        self.plots[0].series.all.set(a=3)
        self.plots[1]           .set(a=4)
        self.plots[1].legend    .set(a=5)
        self.plots[1].series.all.set(a=6)
  
        resolved = self.page.resolve_options()

        self.assertEqual(resolved[self.plots[0]    ]["a"], 1)
        self.assertEqual(resolved[self.plots[1]    ]["a"], 4)
        self.assertEqual(resolved[self.legends[0]  ]["a"], 2)
        self.assertEqual(resolved[self.legends[1]  ]["a"], 5)
        self.assertEqual(resolved[self.series[0][0]]["a"], 3)
        self.assertEqual(resolved[self.series[0][1]]["a"], 3)
        self.assertEqual(resolved[self.series[0][2]]["a"], 3)
        self.assertEqual(resolved[self.series[1][0]]["a"], 6)
        self.assertEqual(resolved[self.series[1][1]]["a"], 6)
        self.assertEqual(resolved[self.series[1][2]]["a"], 6)

    def testOptionsViaLegendInstance(self):
        self.legends[0].set(a=1)
        self.legends[1].set(a=2)
        
        resolved = self.page.resolve_options()
        
        self.assertEqual(resolved[self.legends[0]]["a"], 1)
        self.assertEqual(resolved[self.legends[1]]["a"], 2)
    
    def testOptionsViaSeriesInstance(self):
        self.series[0][0].set(a=1)
        self.series[0][1].set(a=2)
        self.series[0][2].set(a=3)
        self.series[1][0].set(a=4)
        self.series[1][1].set(a=5)
        self.series[1][2].set(a=6)
        
        resolved = self.page.resolve_options()
        
        self.assertEqual(resolved[self.series[0][0]]["a"], 1)
        self.assertEqual(resolved[self.series[0][1]]["a"], 2)
        self.assertEqual(resolved[self.series[0][2]]["a"], 3)
        self.assertEqual(resolved[self.series[1][0]]["a"], 4)
        self.assertEqual(resolved[self.series[1][1]]["a"], 5)
        self.assertEqual(resolved[self.series[1][2]]["a"], 6)

    
    ###############################################################
    ## Setting options via item subclass using default selectors ##
    ###############################################################

    # This is the case where we start from a class instance to select all
    # instances of this class using the default selector (.all; again, selection
    # by tag is tested in another section). Since we only test test the default
    # selector (.all), there is only one set call per test, even for plots and
    # series, where we have multiple instances and where there were multiple set
    # calls in the "via instance" section.

    def testOptionsViaPageClass(self):
        self.Page.all.set                     (a=1)
        self.Page.all.plots.all.set           (a=2)
        self.Page.all.plots.all.legend.set    (a=3)
        self.Page.all.plots.all.series.all.set(a=4)

        resolved = self.page.resolve_options()

        self.assertEqual(resolved[self.page        ]["a"], 1)
        self.assertEqual(resolved[self.plots[0]    ]["a"], 2)
        self.assertEqual(resolved[self.plots[1]    ]["a"], 2)
        self.assertEqual(resolved[self.legends[0]  ]["a"], 3)
        self.assertEqual(resolved[self.legends[1]  ]["a"], 3)
        self.assertEqual(resolved[self.series[0][0]]["a"], 4)
        self.assertEqual(resolved[self.series[0][1]]["a"], 4)
        self.assertEqual(resolved[self.series[0][2]]["a"], 4)
        self.assertEqual(resolved[self.series[1][0]]["a"], 4)
        self.assertEqual(resolved[self.series[1][1]]["a"], 4)
        self.assertEqual(resolved[self.series[1][2]]["a"], 4)
    
    def testOptionsViaPlotClass(self):
        self.Plot.all           .set(a=1)
        self.Plot.all.legend    .set(a=2)
        self.Plot.all.series.all.set(a=3)

        resolved = self.page.resolve_options()
 
        self.assertEqual(resolved[self.plots[0]    ]["a"], 1)
        self.assertEqual(resolved[self.plots[1]    ]["a"], 1)
        self.assertEqual(resolved[self.legends[0]  ]["a"], 2)
        self.assertEqual(resolved[self.legends[1]  ]["a"], 2)
        self.assertEqual(resolved[self.series[0][0]]["a"], 3)
        self.assertEqual(resolved[self.series[0][1]]["a"], 3)
        self.assertEqual(resolved[self.series[0][2]]["a"], 3)
        self.assertEqual(resolved[self.series[1][0]]["a"], 3)
        self.assertEqual(resolved[self.series[1][1]]["a"], 3)
        self.assertEqual(resolved[self.series[1][2]]["a"], 3)
    
    def testOptionsViaLegendClass(self):
        self.Legend.all.set(a=1)
        
        resolved = self.page.resolve_options()
        
        self.assertEqual(resolved[self.legends[0]]["a"], 1)
        self.assertEqual(resolved[self.legends[1]]["a"], 1)
    
    def testOptionsViaSeriesClass(self):
        self.Series.all.set(a=1)

        resolved = self.page.resolve_options()
 
        self.assertEqual(resolved[self.series[0][0]]["a"], 1)
        self.assertEqual(resolved[self.series[0][1]]["a"], 1)
        self.assertEqual(resolved[self.series[0][2]]["a"], 1)
        self.assertEqual(resolved[self.series[1][0]]["a"], 1)
        self.assertEqual(resolved[self.series[1][1]]["a"], 1)
        self.assertEqual(resolved[self.series[1][2]]["a"], 1)
    
    
    ###################################################################
    ## Setting options via item instance using non-default selectors ##
    ###################################################################

    # Test non-default selectors, i. e. ["..."] instead of (and in conjunction
    # with) the default selector (.all).
    #
    # We first start at a container (specifically, the plots container in the
    # page instance) and select series in the plots using all combinations of
    # the default selector and tag selectors: no tag selectors (only default
    # selectors), tag selector for plots, tag selector for series, and tag
    # selectors for plots and series.
    #
    # In each case, we test that the option of the selected series was indeed
    # set, and that the one for the non-selected series are not selected (i. e.
    # are at their default value).
    
    def testSelectors_container_none(self):
        self.page.plots.all.series.all.set(a=1)

        resolved = self.page.resolve_options()
        
        self.assertEqual(resolved[self.series[0][0]]["a"], 1)
        self.assertEqual(resolved[self.series[0][1]]["a"], 1)
        self.assertEqual(resolved[self.series[0][2]]["a"], 1)
        self.assertEqual(resolved[self.series[1][0]]["a"], 1)
        self.assertEqual(resolved[self.series[1][1]]["a"], 1)
        self.assertEqual(resolved[self.series[1][2]]["a"], 1)

    def testSelectors_container_plot(self):
        self.page.plots["alpha"].series.all.set(a=1)

        resolved = self.page.resolve_options()
        
        self.assertEqual(resolved[self.series[0][0]]["a"], 1)
        self.assertEqual(resolved[self.series[0][1]]["a"], 1)
        self.assertEqual(resolved[self.series[0][2]]["a"], 1)
        self.assertEqual(resolved[self.series[1][0]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[1][1]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[1][2]]["a"], "defaultA")

    def testSelectors_container_series(self):
        self.page.plots.all.series["one"].set(a=1)

        resolved = self.page.resolve_options()
        
        self.assertEqual(resolved[self.series[0][0]]["a"], 1)
        self.assertEqual(resolved[self.series[0][1]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[0][2]]["a"], 1)
        self.assertEqual(resolved[self.series[1][0]]["a"], 1)
        self.assertEqual(resolved[self.series[1][1]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[1][2]]["a"], 1)

    def testSelectors_container_plotAndSeries(self):
        self.page.plots["alpha"].series["one"].set(a=1)

        resolved = self.page.resolve_options()
        
        self.assertEqual(resolved[self.series[0][0]]["a"], 1)
        self.assertEqual(resolved[self.series[0][1]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[0][2]]["a"], 1)
        self.assertEqual(resolved[self.series[1][0]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[1][1]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[1][2]]["a"], "defaultA")


    ###################################################################
    ## Setting options via item subclass using non-default selectors ##
    ###################################################################

    # Same as before, but we start at the Plot class instead of the plots
    # container in the page instance.

    def testSelectors_class_none(self):
        self.Plot.all.series.all.set(a=1)
 
        resolved = self.page.resolve_options()
         
        self.assertEqual(resolved[self.series[0][0]]["a"], 1)
        self.assertEqual(resolved[self.series[0][1]]["a"], 1)
        self.assertEqual(resolved[self.series[0][2]]["a"], 1)
        self.assertEqual(resolved[self.series[1][0]]["a"], 1)
        self.assertEqual(resolved[self.series[1][1]]["a"], 1)
        self.assertEqual(resolved[self.series[1][2]]["a"], 1)

    def testSelectors_class_plot(self):
        self.Plot["alpha"].series.all.set(a=1)
 
        resolved = self.page.resolve_options()
         
        self.assertEqual(resolved[self.series[0][0]]["a"], 1)
        self.assertEqual(resolved[self.series[0][1]]["a"], 1)
        self.assertEqual(resolved[self.series[0][2]]["a"], 1)
        self.assertEqual(resolved[self.series[1][0]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[1][1]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[1][2]]["a"], "defaultA")

    def testSelectors_class_series(self):
        self.Plot.all.series["one"].set(a=1)
 
        resolved = self.page.resolve_options()
         
        self.assertEqual(resolved[self.series[0][0]]["a"], 1)
        self.assertEqual(resolved[self.series[0][1]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[0][2]]["a"], 1)
        self.assertEqual(resolved[self.series[1][0]]["a"], 1)
        self.assertEqual(resolved[self.series[1][1]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[1][2]]["a"], 1)

    def testSelectors_class_plotAndSeries(self):
        self.Plot["alpha"].series["one"].set(a=1)
 
        resolved = self.page.resolve_options()
         
        self.assertEqual(resolved[self.series[0][0]]["a"], 1)
        self.assertEqual(resolved[self.series[0][1]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[0][2]]["a"], 1)
        self.assertEqual(resolved[self.series[1][0]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[1][1]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[1][2]]["a"], "defaultA")


    ###############
    ## Shortcuts ##
    ###############
    
    # Both item subclasses and item containers offer two shortcuts.

    # First shortcut: the .all method is the same as the default selector
    # ([""]):
    #     Plot.all          is the same as    Plot[""]
    #     page.plots.all    is the same as    page.plots[""]

    def testAllShortcutClass(self):
        self.assertIs(self.Page.all, self.Page[""])
        self.assertIs(self.Plot.all, self.Plot[""])
        self.assertIs(self.Legend.all, self.Legend[""])
        self.assertIs(self.Series.all, self.Series[""])

    def testAllShortcutContainer(self):
        self.assertIs(self.page.plots.all, self.page.plots[""])
        self.assertIs(self.plots[0].series.all, self.plots[0].series[""])
        self.assertIs(self.plots[1].series.all, self.plots[1].series[""])


    # Second shortcut: the .set method forwards to the template selected by said
    # default selector:
    #     Plot.set(...)          is the same as    Plot.all.set(...)
    #     page.plots.set(...)    is the same as    page.plots.all.set(...)

    def testSetShorcutClass(self):
        self.Plot.set(a=1)  # Shortcut for self.Plot.all.set

        resolved = self.page.resolve_options()

        self.assertEqual(resolved[self.plots[0]]["a"], 1)
        self.assertEqual(resolved[self.plots[1]]["a"], 1)

    def testSetShortcutContainer(self):
        self.page.plots.set(a=2) # Shortcut for self.page.plots.all.set

        resolved = self.page.resolve_options()
        
        self.assertEqual(resolved[self.plots[0]]["a"], 2)
        self.assertEqual(resolved[self.plots[1]]["a"], 2)


    #################
    ## Inheritance ##
    #################

    def testInheritanceFromObject(self):
        # Initially, nothing is set
        resolved = self.page.resolve_options()
        self.assertEqual(resolved[self.page        ]["a"], "defaultA")
        self.assertEqual(resolved[self.plots[0]    ]["a"], "defaultA")
        self.assertEqual(resolved[self.plots[1]    ]["a"], "defaultA")
        self.assertEqual(resolved[self.series[0][0]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[0][1]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[0][2]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[1][0]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[1][1]]["a"], "defaultA")
        self.assertEqual(resolved[self.series[1][2]]["a"], "defaultA")

        # The a parameter is inherited from page to plots (single-stage
        # inheritance) and series (multi-stage inheritance).
        self.page.set(a = 11)
        self.plots[1].set(a = 22)
        resolved = self.page.resolve_options()
        self.assertEqual(resolved[self.page        ]["a"], 11)  # Set
        self.assertEqual(resolved[self.plots[0]    ]["a"], 11)  # Inherited from page
        self.assertEqual(resolved[self.plots[1]    ]["a"], 22)  # Set
        self.assertEqual(resolved[self.series[0][0]]["a"], 11)  # Inherited from page
        self.assertEqual(resolved[self.series[0][1]]["a"], 11)  # Inherited from page
        self.assertEqual(resolved[self.series[0][2]]["a"], 11)  # Inherited from page
        self.assertEqual(resolved[self.series[1][0]]["a"], 22)  # Inherited from plots[1]
        self.assertEqual(resolved[self.series[1][1]]["a"], 22)  # Inherited from plots[1]
        self.assertEqual(resolved[self.series[1][2]]["a"], 22)  # Inherited from plots[1]

        # Set page.a again. Make sure that this does not change plot[1] and its
        # series, which have been set explicitly (albeit earlier)
        self.page.set(a = 33)
        resolved = self.page.resolve_options()
        self.assertEqual(resolved[self.page        ]["a"], 33)  # Set
        self.assertEqual(resolved[self.plots[0]    ]["a"], 33)  # Inherited from page
        self.assertEqual(resolved[self.plots[1]    ]["a"], 22)  # Set
        self.assertEqual(resolved[self.series[0][0]]["a"], 33)  # Inherited from page
        self.assertEqual(resolved[self.series[0][1]]["a"], 33)  # Inherited from page
        self.assertEqual(resolved[self.series[0][2]]["a"], 33)  # Inherited from page
        self.assertEqual(resolved[self.series[1][0]]["a"], 22)  # Inherited from plots[1]
        self.assertEqual(resolved[self.series[1][1]]["a"], 22)  # Inherited from plots[1]
        self.assertEqual(resolved[self.series[1][2]]["a"], 22)  # Inherited from plots[1]

    def testNoInheritanceFromObject(self):
        # The b parameter is defined for all item subclasses, but is not
        # inherited.
        self.page.set(b = 11)
        self.plots[1].set(b = 22)
        resolved = self.page.resolve_options()
        self.assertEqual(resolved[self.page        ]["b"], 11)  # Set
        self.assertEqual(resolved[self.plots[0]    ]["b"], "defaultB")  # Not inherited
        self.assertEqual(resolved[self.plots[1]    ]["b"], 22)  # Set
        self.assertEqual(resolved[self.series[0][0]]["b"], "defaultB")  # Not inherited
        self.assertEqual(resolved[self.series[0][1]]["b"], "defaultB")  # Not inherited
        self.assertEqual(resolved[self.series[0][2]]["b"], "defaultB")  # Not inherited
        self.assertEqual(resolved[self.series[1][0]]["b"], "defaultB")  # Not inherited
        self.assertEqual(resolved[self.series[1][1]]["b"], "defaultB")  # Not inherited
        self.assertEqual(resolved[self.series[1][2]]["b"], "defaultB")  # Not inherited

    def testInheritanceFromClassTemplate(self):
        # TODO
        # like testInheritanceFromObject, but set Page.all.a
        pass

    def testInheritanceFromContainerTemplate(self):
        # TODO
        # like testInheritanceFromObject, but set page.plots.all.a
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
