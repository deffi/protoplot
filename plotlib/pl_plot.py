import numbers

from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter

from plotlib import Item, Container, Series, BarSeries, Text, Legend, BarLayout
from plotlib.pl_util import select

# TODO empty plots

inch = 2.54

# TODO clean up: some options get a default in the constructor, some are tested
# for presence in plot()
class Plot(Item):
    def __init__(self):
        super().__init__()
        
        self.series = Container(Series)
        self.bar_series = Container(BarSeries)
        self.text = Container(Text)
        self.legend = Legend()

        self.options(font_size=8)
        self.options(size=(16, 8))
        self.options(dpi=300)
        self.options(grid=True)
        self.options(bar_labels=None)
        self.options(bar_stacked=False)

        self.legend.options(numpoints = 1)
        
        self.callbacks = []
    
    def add_callback(self, callback):
        self.callbacks.append(callback)

    def _render_series(self, ax, xshift = None):
        num_series = len(self.series)
        
        if xshift is None:
            xoffsets = [0] * num_series
        elif isinstance(xshift, list):
            if len(xshift) != num_series:
                raise ValueError("Length of xshift does not match number of series")
            xoffsets = xshift
        elif isinstance(xshift, numbers.Number):
            # 4 series: [-1.5, -0.5, 0.5, 1.5] * xshift
            # 5 series: [-2, -1, 0, 1, 2] * xshift
            # n series: 
            xoffsets = [(i - (num_series-1)/2) * xshift for i in range(num_series)]
        else:
            raise ValueError("Unsupported xshift: %s" % repr(xshift))
        
        for series, xoffset in zip(self.series, xoffsets):
            series.render(ax, self.series, xoffset)

    def _render_bar_series(self, ax, bar_labels):
        if len(self.bar_series) == 0:
            return
        
        opts = self.effective_options(None)
        
        stacked = opts['bar_stacked']
        bar_layout = BarLayout(self.bar_series, stacked, 1.0, 1.5)

        last_top = [0] * bar_layout.num_groups
        for index, bar_series in enumerate(self.bar_series):
            last_top = bar_series.render(ax, self.bar_series, bar_layout, index, last_top)
     
        if bar_labels is not None:
            plt.xticks([i + 0.5 for i in range(len(bar_labels))], bar_labels)

    def _render_text(self, ax):
        for text in self.text:
            text.render(ax, self.text)

    def _render_legend(self, ax):
        self.legend.render(ax)



    def render(self):
        opts = self.effective_options(None)
        #print(opts)
        
        size       = opts['size'] 
        dpi        = opts['dpi']
        font_size  = opts['font_size']
        bar_labels = opts['bar_labels']
        
        width = size[0]
        height = size[1]
        plt.rc('font', size = font_size)
        plt.rc('figure', dpi = 150, figsize = (width / inch, height / inch))
        plt.rc('savefig', dpi = dpi)
        plt.rc('legend', fontsize = font_size)
        
        fig = plt.figure()
        ax = fig.add_subplot(111)

        self._render_series    (ax, opts.get('xshift'))
        self._render_bar_series(ax, bar_labels)
        self._render_text      (ax)
        self._render_legend    (ax)


        # TODO this stinks, we should not have to list them all here
        if 'xlabel' in opts                 : ax.set_xlabel(opts['xlabel'])
        if 'ylabel' in opts                 : ax.set_ylabel(opts['ylabel'])
        if 'xlim'   in opts and opts['xlim']: ax.set_xlim  (opts['xlim'  ])
        if 'ylim'   in opts and opts['ylim']: ax.set_ylim  (opts['ylim'  ])
        # TODO this stinks, we should be able to specify the "which" parameter (major/minor/both)
        if 'grid'   in opts: ax.grid      (opts['grid'  ])
        if 'xgrid'  in opts: ax.xaxis.grid(opts['xgrid' ])
        if 'ygrid'  in opts: ax.yaxis.grid(opts['ygrid' ])

        if 'xticks' in opts: ax.xaxis.set_ticks(opts['xticks'])
        if 'yticks' in opts: ax.yaxis.set_ticks(opts['yticks'])

        if 'xlog'   in opts and opts['xlog']: ax.set_xscale("log", nonposx='clip')
        if 'ylog'   in opts and opts['ylog']: ax.set_yscale("log", nonposx='clip')

        if 'x_ticks_visible' in opts:
            for tick in ax.get_xticklines():
                tick.set_visible(opts['x_ticks_visible'])
        if 'y_ticks_visible' in opts:
            for tick in ax.get_yticklines():
                tick.set_visible(opts['y_ticks_visible'])
        
        if 'x_format' in opts:
            ax.xaxis.set_major_formatter(FuncFormatter(opts['x_format']))
        if 'y_format' in opts:
            ax.yaxis.set_major_formatter(FuncFormatter(opts['y_format']))
            
        for callback in self.callbacks:
            callback(ax)

        return fig

    def show(self):
        self.render()
        plt.show()
    
    def save(self, file_name):
        print("Saving to %s" % file_name)
        fig = self.render()
        fig.savefig("../output/" + file_name, bbox_inches='tight')
