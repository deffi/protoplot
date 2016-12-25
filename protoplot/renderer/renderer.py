# from matplotlib.ticker import FuncFormatter

# 
# from plotlib import Item, Container, Series, BarSeries, Text, Legend, BarLayout
# from plotlib.pl_util import select
# 
# # TODO empty plots
 
import matplotlib.pyplot as plt

from protoplot.util.shift import offset 

inch = 2.54

class MplRenderer:
    def __init__(self):
        pass

    def _render_series(self, ax, series, options, x_offset, y_offset):
        series_options = options[series]

        print(series_options)

        opts = {}
        opts['color'] = series_options['color']  
        opts['markerfacecolor'] = series_options['markerFillColor']
        opts['markeredgecolor'] = series_options['markerLineColor']
        opts['label'] = series_options['label']

        # TODO for logarithmic plots, the offset is to be applied to the
        # position after applying the logarithm.
        x = [sx + x_offset for sx in series.x]
        y = [sy + y_offset for sy in series.y]

        # TODO we need to do separate plots for different sets of point options,
        # and potentially another one for the series options (for the legend).
        # Note that for fillstyle == 'none', we may not pass a markerfacecolor.
        ax.plot(x, y, **opts)
        # ax.errorbar (xx, yy, yerr=[lower, upper], linestyle="", color=color)        

    def _render_legend(self, ax, legend, options):
        legend_options = options[legend]

        location = legend_options['location']

        opts = {}
        opts['loc'] = location

        if location is not None:
            ax.legend(**opts)
        

#         if 'loc' in opts:
#             handles, labels = ax.get_legend_handles_labels()
#             
#             if 'transform' in opts:
#                 transform = self.options['transform']
#                 del self.options['transform']
#                 handles, labels = transform(handles, labels)
#                 
#             ax.legend(handles, labels, **self.options)

        
    def _render_plot(self, plot, options):
        plot_options = options[plot]
        print(plot_options)

        size       = plot_options['size'] or (16, 10) 
        dpi        = plot_options['dpi']
        #font_size  = plot_options['font_size']
        #bar_labels = plot_options['bar_labels']
         
        width = size[0]
        height = size[1]
#         plt.rc('font', size = font_size)
#         plt.rc('figure', dpi = 150, figsize = (width / inch, height / inch))
#         plt.rc('savefig', dpi = dpi)
#         plt.rc('legend', fontsize = font_size)
         
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # FIXME this must be in the model
        xoffset = offset(plot_options['xshift'], len(plot.series.items))
        yoffset = offset(plot_options['yshift'], len(plot.series.items))

        for series, xoff, yoff in zip(plot.series.items, xoffset, yoffset):
            self._render_series(ax, series, options, xoff, yoff)

        self._render_legend(ax, plot.legend, options)

        #for text in plot.text.items:
        #    self._render_text(ax, text, options)
 
# 
#         # TODO this stinks, we should not have to list them all here
#         if 'xlabel' in opts                 : ax.set_xlabel(opts['xlabel'])
#         if 'ylabel' in opts                 : ax.set_ylabel(opts['ylabel'])

        xlim = plot_options['xlim']
        ylim = plot_options['ylim']
        if xlim: ax.set_xlim(xlim)
        if ylim: ax.set_ylim(ylim)

        # TODO this stinks, we should be able to specify the "which" parameter (major/minor/both)
        grid  = plot_options['grid']
        xgrid = plot_options['xgrid']
        ygrid = plot_options['ygrid']
        
        if grid  is not None: ax.grid      (grid )
        if xgrid is not None: ax.xaxis.grid(xgrid)
        if ygrid is not None: ax.yaxis.grid(ygrid)
 
        if (plot_options['xlog']): ax.set_xscale("log", nonposx='clip')
        if (plot_options['ylog']): ax.set_yscale("log", nonposy='clip')
 
        #ax.xaxis.set_ticks(plot_options['xticks'])
        #ax.yaxis.set_ticks(plot_options['yticks'])
 
#         if 'x_ticks_visible' in opts:
#             for tick in ax.get_xticklines():
#                 tick.set_visible(opts['x_ticks_visible'])
#         if 'y_ticks_visible' in opts:
#             for tick in ax.get_yticklines():
#                 tick.set_visible(opts['y_ticks_visible'])
#         
#         if 'x_format' in opts:
#             ax.xaxis.set_major_formatter(FuncFormatter(opts['x_format']))
#         if 'y_format' in opts:
#             ax.yaxis.set_major_formatter(FuncFormatter(opts['y_format']))
             
        return fig

    def render(self, plot):
        options = plot.resolve_options()
        return self._render_plot(plot, options)
    
    def show(self, plot):
        self.render(plot)
        plt.show()
    
    def save(self, plot, file_name):
        print("Saving to %s" % file_name)
        fig = self.render(plot)
        fig.savefig(file_name, bbox_inches='tight')
