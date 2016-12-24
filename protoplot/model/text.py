from protoplot.engine import Item

class Point(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Data: position

        self.options.register("color"    , True , None)
        self.options.register("anchor"   , False, "center")
