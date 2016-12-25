from protoplot.engine import Item, ItemContainer
#from protoplot.model import Legend, Series, Text
from protoplot.model.legend import Legend
from protoplot.model.series import Series
from protoplot.model.text import Text

class Plot(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.options.register("backgroundColor", True, "white")

        self.options.register("xlabel", False, "")
        self.options.register("ylabel", False, "")
        self.options.register("xlim", False, None)
        self.options.register("ylim", False, None)
        self.options.register("xlog", False, None)
        self.options.register("ylog", False, None)
        self.options.register("xshift", False, None)
        self.options.register("yshift", False, None)
        self.options.register("xticks", False, None)
        self.options.register("xticks", False, None)
 
        self.series = ItemContainer(Series)
        self.text   = ItemContainer(Text)
        self.legend = Legend()

        # Options for plot:
        #   * Rendering: dpi (should be in the page? what if there is none?),
        #     size
        #   * Layout: fontSize, barStacked, x/yShift? x/yLabel? (oder zu Axis?)
        #   * colorScheme
        
    
        # Option types:
        #   * x/yShift: array, list, unit, function
        #   * format: format string or formatter function