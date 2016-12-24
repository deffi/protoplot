from protoplot.engine import Item, ItemContainer
from protoplot.model.legend import Legend
from protoplot.model.series import Series

class Plot(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.options.register("backgroundColor", True, "white")
 
        self.series = ItemContainer(Series)
        self.legend = Legend()

        # Options for plot:
        #   * Rendering: dpi (should be in the page? what if there is none?),
        #     size
        #   * Layout: fontSize, barStacked, x/yShift? x/yLabel? (oder zu Axis?)
        #   * colorScheme
        
    
        # Option types:
        #   * x/yShift: array, list, unit, function
        #   * format: format string or formatter function