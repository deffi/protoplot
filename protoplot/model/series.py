from protoplot.engine import Item

class Series(Item):
    def __init__(self, x=None, y=None, data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Data: x, y, lower, upper, color, markercolor, markerfacecolor,
        #   markeredgecolor, fillstyle, label, 

        self.x = x
        self.y = y
        self.data = data

    def register_options(self):
        self.options.register("color"    , True , None)
        
        self.options.register("lineVisible", False, True)
        self.options.register("lineColor", False, None)
        self.options.register("lineStyle", False, "solid")

        self.options.register("markerVisible", False, True)
        self.options.register("markerColor", False, None)
        self.options.register("markerFillColor", False, None)
        self.options.register("markerLineColor", False, None)
        self.options.register("markerFillStyle", False, None)
        self.options.register("markerFilled", False, True)
        self.options.register("marker", False, None)
        self.options.register("markerSize", False, 4)

        self.options.register("label", False, True)
        self.options.register("showInLegend", False, True)
        self.options.register("legendKey", False, None)
        self.options.register("legendNumPoints", False, 1)

