import unittest

from protoplot.engine.options_container import OptionsContainer, notSpecified

# TODO Tests:
#   * Copy an options container and modify either => modifications may not
#     affect the copy

class OptionsContainerTest(unittest.TestCase):
    ##################
    ## Test fixture ##
    ##################

    def setUp(self):
        pass


    ###############
    ## Resolving ##
    ###############

    def testResolvingNoOptions(self):
        oc = OptionsContainer()

        self.assertEqual(oc.resolve(), dict())

    def testResolvingNoValues(self):
        oc = OptionsContainer()

        oc.register("color")
        oc.register("width")
        oc.register("pattern")

        self.assertEqual(oc.resolve(), {
            "color"  : notSpecified,
            "width"  : notSpecified,
            "pattern": notSpecified,
        })

    def testResolvingValue(self):
        # Define an OC and register options
        oc = OptionsContainer()
        oc.register("color")
        oc.register("width")
        oc.register("pattern")

        # Set a single value
        oc.set(color = "red")
        # Set multiple values at once
        oc.set(width = 2, pattern = "solid")

        self.assertEqual(oc.resolve(), {
            "color"  : "red",
            "width"  : 2,
            "pattern": "solid",
        })

        # Overwrite two values
        oc.set(color="green", width = 3)

        self.assertEqual(oc.resolve(), {
            "color"  : "green",
            "width"  : 3,
            "pattern": "solid",
        })

    def testResolvingShorthand(self):
        # Shorthand is not implemented
        pass

    def testResolvingTemplate(self):
        # TODO create two template and test:
        #   * value set in this OC
        #   * value set in one or the other templates
        #   * value set in both templates
        #   * value set in this OC and one or the other templates
        #   * value set in this OC and both templates
        # In all cases where appropriate, test both priority orders

        pass

    def testResolvingTemplateShorthand(self):
        # Shorthand is not implemented
        pass

    def testResolvingInherited(self):
        # TODO set some inherited values and test with/without overriding by
        # value
        pass

    def testResolvingDeferred(self):
        # Define an OC and register options
        oc = OptionsContainer()
        oc.register("markerFillColor"      , defer = "markerColor")
        oc.register("color"                                       )
        oc.register("markerBackgroundColor", defer = "markerColor")
        oc.register("markerColor"          , defer = "color")
        oc.register("markerLineColor"      , defer = "markerColor")

        optionNames = oc._optionNames();
        self.assertLess(optionNames.index("markerColor"), optionNames.index("markerFillColor"      ))
        self.assertLess(optionNames.index("markerColor"), optionNames.index("markerLineColor"      ))
        self.assertLess(optionNames.index("markerColor"), optionNames.index("markerBackgroundColor"))
        self.assertLess(optionNames.index("color")      , optionNames.index("markerColor"          ))

        self.assertEqual(oc.resolve(), {
            "markerBackgroundColor": notSpecified,
            "markerFillColor"      : notSpecified,
            "markerLineColor"      : notSpecified,
            "markerColor"          : notSpecified,
            "color"                : notSpecified,
        })

        # Set markerBackgroundColor, it must not affect anything else
        oc.set(markerBackgroundColor = "red")
        self.assertEqual(oc.resolve(), {
            "markerBackgroundColor": "red",
            "markerFillColor"      : notSpecified,
            "markerLineColor"      : notSpecified,
            "markerColor"          : notSpecified,
            "color"                : notSpecified,
        })

        # Set color, it must affect direct (markerColor) and indirect
        # (markerFillColor, markerLineColor) deferring.
        oc.set(color = "yellow")
        self.assertEqual(oc.resolve(), {
            "markerBackgroundColor": "red",
            "markerFillColor"      : "yellow",
            "markerLineColor"      : "yellow",
            "markerColor"          : "yellow",
            "color"                : "yellow",
        })

        # Set markerFillColor, it must now have that value
        oc.set(markerFillColor = "green")
        self.assertEqual(oc.resolve(), {
            "markerBackgroundColor": "red",
            "markerFillColor"      : "green",
            "markerLineColor"      : "yellow",
            "markerColor"          : "yellow",
            "color"                : "yellow",
        })

        # Set markerColor, it must affect markerLineColor (the only one without
        # explicit value so far)
        oc.set(markerColor = "blue")
        self.assertEqual(oc.resolve(), {
            "markerBackgroundColor": "red",
            "markerFillColor"      : "green",
            "markerLineColor"      : "blue",
            "markerColor"          : "blue",
            "color"                : "yellow",
        })

        # Set markerLineColor (now everything has an explicit value)
        oc.set(markerLineColor = "indigo")
        self.assertEqual(oc.resolve(), {
            "markerBackgroundColor": "red",
            "markerFillColor"      : "green",
            "markerLineColor"      : "indigo",
            "markerColor"          : "blue",
            "color"                : "yellow",
        })

    def testResolvingDefault(self):
        # Define an OC and register options
        oc = OptionsContainer()
        oc.register("color"  , default = "black")
        oc.register("width"  , default = 1)
        oc.register("pattern", default = "solid")

        self.assertEqual(oc.resolve(), {
            "color"  : "black",
            "width"  : 1,
            "pattern": "solid",
        })

        # Set some (but not all) values
        oc.set(width = 3)
        oc.set(pattern = "dashed")

        self.assertEqual(oc.resolve(), {
            "color"  : "black",  # Still at its default value
            "width"  : 3,
            "pattern": "dashed",
        })

        pass


    ##############
    ## Priority ##
    ##############


    ###########
    ## Other ##
    ###########

    def testCopying(self):
        oc1 = OptionsContainer()
        oc1.register("color")
        oc1.register("width")
        oc1.register("pattern")

        oc2 = OptionsContainer(oc1)

        # Set different values and make sure they don't overwrite each other
        oc1.set(color="red")
        self.assertEqual(oc1.resolve(pruneNotSpecified = True), {"color": "red"})
        self.assertEqual(oc2.resolve(pruneNotSpecified = True), {})

        oc2.set(color="green")
        self.assertEqual(oc1.resolve(pruneNotSpecified = True), {"color": "red"})
        self.assertEqual(oc2.resolve(pruneNotSpecified = True), {"color": "green"})

        oc1.set(color="blue")
        self.assertEqual(oc1.resolve(pruneNotSpecified = True), {"color": "blue"})
        self.assertEqual(oc2.resolve(pruneNotSpecified = True), {"color": "green"})

    def testUnknownOptions(self):
        pass

        # oc = self.oc
        #
        # # Set an unknown option
        # with self.assertWarnsRegex(Warning, "^Setting unknown option markerSize$"):
        #     oc.set(markerSize=4)
        #
        # # The value must have been set
        # self.assertEqual(oc.values, {
        #     "markerSize": 4
        # })




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
