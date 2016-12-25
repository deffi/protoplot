from protoplot.engine import Item

class Text(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Data: position, text

        self.options.register("color"    , True , None)
        self.options.register("anchor"   , False, "center")
