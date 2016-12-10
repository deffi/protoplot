from plotlib import Item
from plotlib.util import is_single, is_multiple, filter_none, select


class Series(Item):
    def __init__(self, x, y, data = None, **options):
        super().__init__(**options)
        
        if data is None:
            self._data = None
            
            # x and y are lists
            # Either x or y can be single values; in this case, it is replicated
            if is_multiple(x) and is_single(y):
                x_ = x
                y_ = [y] * len(x)
            elif is_multiple(y) and is_single(x): 
                x_ = [x] * len(y)
                y_ = y
            else:
                x_ = x
                y_ = y
                
            # Filter out "None" values
            x_, y_ = filter_none((x_, y_))
        else:
            self._data = [dt for dt in data if select(x, dt) is not None and select(y, dt) is not None] 
            
            # x and y is a selector
            x_ = [select(x, d) for d in self._data]
            y_ = [select(y, d) for d in self._data]

        self.x = x_
        self.y = y_

    def render(self, ax, container, xoffset):
        opts = self.effective_options(container)

        extra_opts = dict()
        if "lower" in opts:
            extra_opts["lower"] = opts["lower"]
            del opts["lower"]
        if "upper" in opts:
            extra_opts["upper"] = opts["upper"]
            del opts["upper"]
        
        if 'color' in opts:
            color = opts['color']
            #del opts['color']
            opts['markercolor'] = color
    
        if 'markercolor' in opts:
            markercolor = opts['markercolor']
            del opts['markercolor']
            opts['markerfacecolor'] = markercolor
            opts['markeredgecolor'] = markercolor

        # This sucks, we should be able to do this with arbitrary parameters
        if 'empty' in opts:
            # Must be a function of record
            empty = opts['empty']
            del opts['empty']
            
            if self._data is None:
                raise ValueError("If filled is specified, there must be data")
            empty = [empty(record) for record in self._data]
        else:
            empty = [False] * len(self.x)

        if 'fillstyle' in opts and opts['fillstyle'] == 'none':
            if 'markerfacecolor' in opts:
                del opts['markerfacecolor']

        xx = [x + xoffset for x in self.x]
        yy = self.y 

        # Plot the regular symbols
        xx_filled = [x for i, x in enumerate(xx) if not empty[i]]
        yy_filled = [y for i, y in enumerate(yy) if not empty[i]]
        ax.plot(xx_filled, yy_filled, **opts)
        
        # Plot the empty symbols
        xx_open = [x for i, x in enumerate(xx) if empty[i]]
        yy_open = [y for i, y in enumerate(yy) if empty[i]]
        opts_open = dict(opts)
        opts_open["fillstyle"] = "none"
        if "label"           in opts_open: del opts_open["label"]
        if "markerfacecolor" in opts_open: del opts_open["markerfacecolor"]
        ax.plot(xx_open, yy_open, **opts_open)

        if "lower" in extra_opts and "upper" in extra_opts:
            lower_func = extra_opts["lower"]
            upper_func = extra_opts["upper"]
            
            lower = [select(lower_func, d) for d in self._data]
            upper = [select(upper_func, d) for d in self._data]

            #rlower = [y-l for y, l in zip(yy, lower)]
            #rupper = [u-y for u, y in zip(upper, yy)]

            ax.errorbar (xx, yy, yerr=[lower, upper], linestyle="", color=color)

