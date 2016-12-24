from protoplot.engine import Item

class Legend(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.options.register("visible" , False, True)        
        self.options.register("location", False, "right-of")

#         if 'loc' in opts:
#             handles, labels = ax.get_legend_handles_labels()
#             
#             if 'transform' in opts:
#                 transform = self.options['transform']
#                 del self.options['transform']
#                 handles, labels = transform(handles, labels)
#                 
#             ax.legend(handles, labels, **self.options)
