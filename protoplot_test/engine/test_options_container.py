import unittest

from protoplot.engine.options_container import OptionsContainer

class OptionsContainerTest(unittest.TestCase):
    def testOptionsContainer(self):
        # Define one OC
        oc = OptionsContainer()
        self.assertEqual(len(oc), 0)
        
        # Register some options
        oc.register("color"    , True , "black")
        self.assertEqual(len(oc), 1)
        oc.register("lineWidth", False, 1)
        self.assertEqual(len(oc), 2)
        oc.register("lineStyle", False, "solid")

        # Define another OC
        oc2 = OptionsContainer(oc)

        # Verify the options count
        self.assertEqual(len(oc), 3)
        self.assertEqual(len(oc2), 3)

        # Set some values in the first OC
        oc.set(color="red")
        self.assertEqual(oc.values, {"color": "red"})
        oc.set(lineWidth=1, lineStyle="solid")
        self.assertEqual(oc.values, {"color": "red", "lineWidth": 1, "lineStyle": "solid"})
        with self.assertWarnsRegex(Warning, "^Setting unknown option markerSize$"):
            oc.set(markerSize=4)
        self.assertEqual(oc.values, {"color": "red", "lineWidth": 1, "lineStyle": "solid", "markerSize": 4})

        # Set one value in the second OC
        oc2.set(color="green")
        self.assertEqual(oc2.values, {"color": "green"})

        # Verify the defaults
        self.assertEqual(oc.fallback_values(), {
            "color"    : "black",
            "lineWidth": 1,
            "lineStyle": "solid",
        })

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
