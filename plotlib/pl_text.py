from plotlib import Item

class Text(Item):
    def __init__(self, position, text, **options):
        super().__init__(**options)
        self.position = position
        self.text = text

    def render(self, ax, container):
        opts = self.effective_options(container)
            
        x, y = self.position
        ax.text(x, y, self.text, **opts)
