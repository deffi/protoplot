from protoplot.engine import Item

class Text(Item):
    def __init__(self, position=None, text=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Data: position, text

        self.options.register("color"    , True , None)
        self.options.register("anchor"   , False, "center")

        self.position = position
        self.text = text
