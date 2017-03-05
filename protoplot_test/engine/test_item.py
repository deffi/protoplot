import unittest

from protoplot.engine.item import Item
from protoplot.engine.item_container import ItemContainer

class TestItem(unittest.TestCase):
    '''
    Tests the basic functionality of items. Options resolving is tested
    separately due to the high numer of test cases.

    The model looks like this:
        Plot
        |- legend    (Legend)
        '- series    (ItemContainer with Series)

    The following options are defined:
      * Plot:   color
      * Legend: color (inherited)
      * Series: color (inherited), lineWidth, lineStyle
    '''

    ##################
    ## Test fixture ##
    ##################

    def setUp(self):
        class Series(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def register_options(self):
                self.options.register("color", inherit=True)
                self.options.register("lineWidth")
                self.options.register("lineStyle")

        class Legend(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def register_options(self):
                self.options.register("color", inherit=True)

        class Plot(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                self.legend = Legend()
                self.series = ItemContainer(Series)

            def register_options(self):
                self.options.register("color")

        self.Legend = Legend
        self.Plot   = Plot
        self.Series = Series

    def tearDown(self):
        pass


    #########
    ## Tag ##
    #########
        
    def testTag(self):
        # Tests creating an item instance with different methods of specifying
        # tags. More ways to specify a tag list are tested in test_tag.

        Series = self.Series

        # No tag specification
        series = Series()
        self.assertEqual(series.tags, [])

        # Multiple tags as comma-separated string
        series = Series(tag="foo,bar")
        self.assertEqual(series.tags, ["foo", "bar"])

        # Multiple tags as list of strings
        series = Series(tag=["foo", "bar"])
        self.assertEqual(series.tags, ["foo", "bar"])


    ##############
    ## Children ##
    ##############

    def testChildren(self):
        plot = self.Plot()
        self.assertEqual(plot.children(), [("legend", plot.legend)])
    
    def testContainers(self):
        plot = self.Plot()
        self.assertEqual(plot.containers(), [("series", plot.series)])


    ###############
    ## Templates ##
    ###############

    def testClassTemplates(self):
        # See also: TestItemContainer.testContainerTemplates

        Series = self.Series

        # Templates must be instances of the same class.
        self.assertIsInstance(Series["foo"], Series)

        # Accesses to the template with the same name must always return the
        # same template, which must be an instance of the same class.
        self.assertIs(Series["foo"], Series["foo"])
        self.assertIs(Series[""]   , Series[""]   )

        # Accesses to templates with different names must return different
        # templates.
        self.assertIsNot(Series["foo"], Series["bar"])

        # Accesses to .all must always return the same template, which must be
        # the same as the template with the empty name.
        self.assertIs(Series.all, Series.all)
        self.assertIs(Series.all, Series[""])

    def testSetShortcut(self):
        # Test the .set shortcut of the Item subclass.

        Series = self.Series

        Series.all.set(color = "red")
        self.assertEqual(Series.all.options.resolve()["color"], "red")

        Series.set(color = "green")
        self.assertEqual(Series.all.options.resolve()["color"], "green")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
