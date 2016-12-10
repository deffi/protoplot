from plotlib import Item

class BarLayout:
    def __init__(self, bar_series, stacked, bar_spacing, bar_group_spacing):
        if len(bar_series) == 0:
            return
        
        self.stacked = stacked
        self.bar_spacing = bar_spacing
        self.bar_group_spacing = bar_group_spacing 

        self.num_groups = max(bar_series.num_bars() for bar_series in bar_series)

        if stacked:
            group_size = 1
        else:
            group_size = len(bar_series)

        self.bar_width = 1 / (1 + (group_size - 1) * bar_spacing + bar_group_spacing)
        
    def bar_offset(self, bar_index):
        if self.stacked:
            return 0.5 * self.bar_group_spacing * self.bar_width
        else:
            return 0.5 * self.bar_group_spacing * self.bar_width + bar_index * self.bar_spacing * self.bar_width
            

# TODO in rtmc6 plot, you can specify an index here, and if you don't, it's
# auto-assigned in order. Together with bottom, this makes it possible to
# specify custom stacking.
class BarSeries(Item):
    def __init__(self, y, **options):
        super().__init__(**options)

        self.y = y

    def num_bars(self):
        return len(self.y)

    def render(self, ax, container, layout, index, last_top):
        opts = self.effective_options(container)

        offset = layout.bar_offset(index)
        
        if layout.stacked:
            bottom = last_top
        else:
            bottom = [0] * self.num_bars()

        width = layout.bar_width        
        left = [i + offset for i in range(self.num_bars())]
        
        ax.bar(left, self.y, width = width, bottom = bottom, **opts)
        
        return [b + h for b, h in zip(bottom, self.y)]
