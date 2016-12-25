from protoplot.engine import Item

class Axis(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.options.register("log", False, False)
        self.options.register("logBase", False, 10)
        self.options.register("min", False, None)
        self.options.register("max", False, None)
        self.options.register("format", False, None)
        
        self.options.register("majorInterval", False, None)
        self.options.register("minorInterval", False, None)
        self.options.register("majorTicks", False, True)
        self.options.register("minorTicks", False, False)
        self.options.register("majorGridVisible", False, True)
        self.options.register("minorGridVisible", False, False)
        self.options.register("majorGridColor", False, None)
        self.options.register("minorGridColor", False, None)
        self.options.register("majorGridLineStyle", False, "solid")
        self.options.register("minorGridLineStyle", False, "solid")
