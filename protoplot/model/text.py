from protoplot.engine import Item

class Text(Item):
    def __init__(self, position=None, text=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Data: position, text
        self.position = position
        self.text = text

    def register_options(self):
        self.options.register("color"    , True , None)
        self.options.register("anchor"   , False, "center")

