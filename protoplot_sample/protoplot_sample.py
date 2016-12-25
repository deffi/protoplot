#!/usr/bin/env python3

import warnings
 
from protoplot import Plot, Series #, excel, LogFormatter
from protoplot.util import excel
from protoplot.renderer import MplRenderer as Renderer

x = range(0, 512+1, 16)
y = [4e-4 + 2e-4 * (xx/512) for xx in x]

plot = Plot()

plot.set(xlabel='Horizontal', ylabel='Vertical')
plot.set(xlim=[0, 512+1], ylim=[3e-4, 8e-4])
plot.set(xticks=range(0, 512+1, 64))
plot.set(ylog=True)
plot.set(xshift=64)
# formatter = LogFormatter(labelOnlyBase = False)
# plot.add_callback(lambda ax: ax.yaxis.set_minor_formatter(formatter))
# plot.add_callback(lambda ax: ax.grid(which='minor'))

plot.legend.set(location='lower right')
warnings.filterwarnings('error')

# Add series
one   = plot.series.add(x, y, color = excel.red         , label = "One"  , tag = "a,left")
two   = plot.series.add(x, y, color = excel.orange      , label = "Two"  , tag = "b")
three = plot.series.add(x, y, color = excel.green       , label = "Three", tag = ["c", "left"])
four  = plot.series.add(x, y, markerFillStyle = "bottom", label = "Four" , tag = "d")

# Line style
Series          .set(lineStyle = 'none')  # Default
plot.series["d"].set(lineStyle = "solid") # Override

# Marker size
plot.series.set(markerSize=8)

# Marker fill style
plot.series        .set(markerFillStyle = 'top')
plot.series["left"].set(markerFillStyle = 'left' )
three              .set(markerFillStyle = 'right')
# four: set on creation

# Markers
plot.series["a"].set(marker = '<')
plot.series["b"].set(marker = '^')
plot.series["c"].set(marker = '>')
plot.series["d"].set(marker = 'v')

# Color
# one, two, three: set on creation
four.set(color = excel.purple)
four.set(color = excel.blue)

# Text
plot.text.set(anchor = 'center')
plot.text.add((256, 6e-4), 'Text' )

#plot.show()
Renderer().show(plot)
