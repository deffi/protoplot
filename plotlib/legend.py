from plotlib import Item

class Legend(Item):
    def __init__(self, **options):
        super().__init__(**options)

    def render(self, ax):
        opts = self.effective_options(None)

        if 'loc' in opts:
            handles, labels = ax.get_legend_handles_labels()
            
            if 'transform' in opts:
                transform = self.options['transform']
                del self.options['transform']
                handles, labels = transform(handles, labels)
                
            ax.legend(handles, labels, **self.options)
