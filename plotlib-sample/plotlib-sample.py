#!/usr/bin/env python3
 
from plotlib import Plot, excel, LogFormatter

x = range(0, 512+1, 16)
y = [4e-4 + 2e-4 * (xx/512) for xx in x]

plot = Plot()
plot.options(xlabel='Horizontal', ylabel='Vertical')
plot.options(xlim=[0, 512+1], ylim=[3e-4, 8e-4])
plot.options(xticks=range(0, 512+1, 64))
plot.options(ylog=True)
formatter = LogFormatter(labelOnlyBase = False)
plot.add_callback(lambda ax: ax.yaxis.set_minor_formatter(formatter))
plot.add_callback(lambda ax: ax.grid(which='minor'))

plot.legend.options(loc='center right')

plot.series.options(linestyle='none', markersize=8, fillstyle='right')
plot.series.add(x, y, color=excel.orange, label = "Blabla", marker = '^')

plot.text.options(horizontalalignment='center', verticalalignment='center')
plot.text.add((256, 6e-4), 'Text' )

plot.show()
