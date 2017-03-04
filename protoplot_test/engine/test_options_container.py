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
        # An options container without any registered options must resolve to
        # an empty dict.

        oc = OptionsContainer()

        self.assertEqual(oc.resolve(), dict())

    def testResolvingNoValues(self):
        # If not values are set, all values must resolve to notSpecified.

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
        # Test setting values (single value, or multiple values in one call) and
        # overwriting previously-set values.

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
        # Create an options container with a number of options. The name of the
        # option indicates in which of the options containers the value will be
        # set.
        oc = OptionsContainer()
        oc.register("a")   # Set in template a
        oc.register("b")   # Set in template b
        oc.register("ab")  # Set in both templates
        oc.register("x")   # Set in this options container
        oc.register("xa")  # Set in this options container and template a
        oc.register("xb")  # Set in this options container and template b
        oc.register("xab") # Set in this options container and both templates

        # Create the templates - they are copies of the options container
        template_a = OptionsContainer(oc)
        template_b = OptionsContainer(oc)
        templates = [template_a, template_b]

        # In all options containers, set the respective options.
        oc        .set(x = "x", xa = "x", xb = "x", xab = "x")
        template_a.set(a = "a", ab = "a", xa = "a", xab = "a")
        template_b.set(b = "b", ab = "b", xb = "b", xab = "b")

        # Without templates
        self.assertEqual(oc.resolve(), {
            "a"  : notSpecified,
            "b"  : notSpecified,
            "ab" : notSpecified,
            "x"  : "x",
            "xa" : "x",
            "xb" : "x",
            "xab": "x",
        })

        # With only template a
        self.assertEqual(oc.resolve(templates = [template_a]), {
            "a"  : "a",
            "b"  : notSpecified,
            "ab" : "a",
            "x"  : "x",
            "xa" : "x",
            "xb" : "x",
            "xab": "x",
        })

        # With only template b
        self.assertEqual(oc.resolve(templates = [template_b]), {
            "a"  : notSpecified,
            "b"  : "b",
            "ab" : "b",
            "x"  : "x",
            "xa" : "x",
            "xb" : "x",
            "xab": "x",
        })

        # With both templates
        self.assertEqual(oc.resolve(templates = [template_a, template_b]), {
            "a"  : "a",
            "b"  : "b",
            "ab" : "a",
            "x"  : "x",
            "xa" : "x",
            "xb" : "x",
            "xab": "x",
        })

        # With both templates (inverse order)
        self.assertEqual(oc.resolve(templates = [template_b, template_a]), {
            "a"  : "a",
            "b"  : "b",
            "ab" : "b",
            "x"  : "x",
            "xa" : "x",
            "xb" : "x",
            "xab": "x",
        })

    def testResolvingTemplateShorthand(self):
        # Shorthand is not implemented
        pass

    def testResolvingInherited(self):
        # Define an OC and register options
        # Options: v - value set, i - inherit, p - parent value set
        # Inherit is True for values including "i".
        oc = OptionsContainer()
        oc.register("vip", inherit = True)
        oc.register("vi" , inherit = True)
        oc.register("vp" )
        oc.register("v"  )
        oc.register("ip" , inherit = True)
        oc.register("i"  , inherit = True)
        oc.register("p"  )

        # Set the values of this options container (values including "v")
        oc.set(vip = "this")
        oc.set(vi  = "this")
        oc.set(vp  = "this")
        oc.set(v   = "this")

        # Set the parent values (values including "p")
        parent_values = {
            "vip": "parent",
            "vp" : "parent",
            "ip" : "parent",
            "p"  : "parent",
        }

        # Resolve without inherited values
        self.assertEqual(oc.resolve(), {
            "vip": "this",
            "vi" : "this",
            "vp" : "this",
            "v"  : "this",
            "ip" : notSpecified,
            "i"  : notSpecified,
            "p"  : notSpecified,
        })

        # Resolve with inherited values
        self.assertEqual(oc.resolve(inherited=parent_values), {
            "vip": "this",
            "vi" : "this",
            "vp" : "this",
            "v"  : "this",
            "ip" : "parent",
            "i"  : notSpecified,  # Parent has the value, but value is not inherited
            "p"  : notSpecified,  # Value is inherited, but parent does not have the value
        })

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
