from protoplot.engine import Item

class Point(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def register_options(self):
        self.options.register("color"    , True , None)
        
        self.options.register("lineVisible", False, True)
        self.options.register("lineColor", False, None)
        self.options.register("lineStyle", False, "solid")

        self.options.register("markerVisible", False, True)
        self.options.register("markerColor", False, None)
        self.options.register("markerFillColor", False, None)
        self.options.register("markerLineColor", False, None)
        self.options.register("markerFilled", False, True)
        self.options.register("markerShape", False, None)
        self.options.register("markerSize", False, 4)
