from protoplot.engine import Item

# TODO define the possible locations of the legend - for example:
#
#     left-of above    left above    above    right above    right-of above
#                    .-------------------------------------.
#     left-of top    | left top      top      right top    | right-of top
#                    |                                     |
#     left-of        | left          center   right        | right-of
#                    |                                     |
#     left-of bottom | left bottom   bottom   right bottom | right-of bottom
#                    '-------------------------------------'
#     left-of below    left below    below    right below    right-of below
#
# Additionally:
#   * "auto" - inside at the corner/side with the most space 
#   * Order is irrelevant, e. g. "top left" instead of "left top"
#   * Allow "center" for one direction, e. g. "top center" or "center top"
#   * Arbitrary position with anchor
#   * Arbitrary position where 0 is left/top and 1 is right/bottom
#   * Cardinal directions, e. g. "northwest"/"nw", "northnorthwest"/"nnw"
#
# TODO transform function that returns a permutation (list of indices) (?)

class Legend(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def register_options(self):
        self.options.register("visible" , False, True)        
        self.options.register("location", False, "right-of")

