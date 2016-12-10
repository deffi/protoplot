#!/usr/bin/env python3
 
from plotlib import Plot, Series, excel, LogFormatter

x = range(0, 512+1, 16)
y = [4e-4 + 2e-4 * (xx/512) for xx in x]

plot = Plot()
plot.options(xlabel='Horizontal', ylabel='Vertical')
plot.options(xlim=[0, 512+1], ylim=[3e-4, 8e-4])
plot.options(xticks=range(0, 512+1, 64))
plot.options(ylog=True)
plot.options(xshift=64)
formatter = LogFormatter(labelOnlyBase = False)
plot.add_callback(lambda ax: ax.yaxis.set_minor_formatter(formatter))
plot.add_callback(lambda ax: ax.grid(which='minor'))

plot.legend.options(loc='center right')

# Options for all series
Series.options(linestyle = 'none')

# Options for all series of plot
plot.series.options(markersize=8, fillstyle='top')

# Options for series by tag
plot.series.options.by_tag("a")(marker = '<')
plot.series.options.by_tag("b")(marker = '^')
plot.series.options.by_tag("c")(marker = '>')
plot.series.options.by_tag("d")(marker = 'v')

# Options for series by tag - overrides defaults 
plot.series.options.by_tag("left" )(fillstyle='left' )
plot.series.options.by_tag("d")(linestyle = "solid")

# Add series - override fillstyle for one
plot.series.add(x, y, color=excel.red   , label = "One"  , tag= "a,left")
plot.series.add(x, y, color=excel.orange, label = "Two"  , tag= "b")
three = plot.series.add(x, y, color=excel.green , label = "Three", tag= ["c", "left"])
four = plot.series.add(x, y, label = "Four" , tag= "d", fillstyle='bottom')

# Options for specific series
three.options(fillstyle='right') # Override defaults
four.options(color=excel.blue) 
four.options.by_tag("d")(color=excel.purple) # Useless! It's already for a specific one.


plot.text.options(horizontalalignment='center', verticalalignment='center')
plot.text.add((256, 6e-4), 'Text' )

plot.show()
