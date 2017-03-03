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
        # # Define one OC
        # oc = OptionsContainer()
        #
        # # Register some options
        # oc.register("markerColor"    , defer   = "color")
        # oc.register("markerFillColor", defer   = "markerColor")
        # oc.register("color"          , default = "black")
        # oc.register("lineWidth"      , default = 1)
        # oc.register("lineStyle"      , default = "solid")
        #
        # self.oc = oc


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
        # TODO create OC with deferral (deferred first/deferring first), and
        # test with multi-stage deferring/single-stage deferring (all options!)
        # TODO also test ._optionNames
        pass

    def testResolvingDefault(self):
        # TODO create OC with and without default values, with and without value
        # set
        pass


    ##############
    ## Priority ##
    ##############

    ############
    ## Values ##
    ############

    def testValues(self):
        pass

        # oc = self.oc
        #
        # # Set a single value
        # oc.set(color="red")
        # self.assertEqual(oc.values, {
        #     "color": "red",
        # })
        #
        # # Set two values at once
        # oc.set(lineWidth=1, lineStyle="solid")
        # self.assertEqual(oc.values, {
        #     "color": "red",
        #     "lineWidth": 1,
        #     "lineStyle": "solid",
        # })

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

    def testCopyValues(self):
        pass

        # oc1 = self.oc
        # oc2 = OptionsContainer(oc1)
        #
        # # Set different values and make sure they don't overwrite each other
        # oc1.set(color="red")
        # self.assertEqual(oc1.values, {"color": "red"})
        # self.assertEqual(oc2.values, {})
        #
        # oc2.set(color="green")
        # self.assertEqual(oc1.values, {"color": "red"  })
        # self.assertEqual(oc2.values, {"color": "green"})
        #
        # oc1.set(color="blue")
        # self.assertEqual(oc1.values, {"color": "blue" })
        # self.assertEqual(oc2.values, {"color": "green"})


    ###############
    ## Fallbacks ##
    ###############

    def testFallbacks(self):
        pass
        # # Verify the fallback values
        # self.assertEqual(self.oc.fallback_values(), {
        #     "color"    : "black",
        #     "lineWidth": 1,
        #     "lineStyle": "solid",
        # })

    ###########
    ## Other ##
    ###########

    def testCopying(self):
        # TODO make a copy and ensure that setting one copy does not change the
        # other
        pass




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
