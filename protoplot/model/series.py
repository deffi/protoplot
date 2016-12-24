from protoplot.engine import Item

class Series(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Data: lower, upper, color, markercolor, markerfacecolor,
        #   markeredgecolor, fillstyle, label, 
        
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

        self.options.register("showInLegend", False, True)
        self.options.register("legendKey", False, None)
        self.options.register("legendNumPoints", False, 1)

