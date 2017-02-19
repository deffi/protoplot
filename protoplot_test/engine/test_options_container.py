import unittest

from protoplot.engine.options_container import OptionsContainer

class OptionsContainerTest(unittest.TestCase):
    ##################
    ## Test fixture ##
    ##################

    def setUp(self):
        # Define one OC
        oc = OptionsContainer()

        # Register some options
        oc.register("color"    , "black", inherit = True)
        oc.register("lineWidth", 1)
        oc.register("lineStyle", "solid")

        self.oc = oc


    #########################
    ## Registering options ##
    #########################

    def testCount(self):
        emptyOc = OptionsContainer()
        #self.assertEqual(len(emptyOc), 0)
        #self.assertEqual(len(self.oc), 3)

    def testCopy(self):
        oc = self.oc

        # Define a copy of the options container
        oc2 = OptionsContainer(oc)

        # Verify the options count
        # self.assertEqual(len(oc2), 3)


    ############
    ## Values ##
    ############

    def testValues(self):
        oc = self.oc

        # Set a single value
        oc.set(color="red")
        self.assertEqual(oc.values, {
            "color": "red",
        })

        # Set two values at once
        oc.set(lineWidth=1, lineStyle="solid")
        self.assertEqual(oc.values, {
            "color": "red",
            "lineWidth": 1,
            "lineStyle": "solid",
        })

    def testUnknownOptions(self):
        oc = self.oc

        # Set an unknown option
        with self.assertWarnsRegex(Warning, "^Setting unknown option markerSize$"):
            oc.set(markerSize=4)

        # The value must have been set
        self.assertEqual(oc.values, {
            "markerSize": 4
        })

    def testCopyValues(self):
        oc1 = self.oc
        oc2 = OptionsContainer(oc1)

        # Set different values and make sure they don't overwrite each other
        oc1.set(color="red")
        self.assertEqual(oc1.values, {"color": "red"})
        self.assertEqual(oc2.values, {})

        oc2.set(color="green")
        self.assertEqual(oc1.values, {"color": "red"  })
        self.assertEqual(oc2.values, {"color": "green"})

        oc1.set(color="blue")
        self.assertEqual(oc1.values, {"color": "blue" })
        self.assertEqual(oc2.values, {"color": "green"})


    ###############
    ## Fallbacks ##
    ###############

    def testFallbacks(self):
        # Verify the fallback values
        self.assertEqual(self.oc.fallback_values(), {
            "color"    : "black",
            "lineWidth": 1,
            "lineStyle": "solid",
        })


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
