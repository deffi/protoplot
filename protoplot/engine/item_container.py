from protoplot.engine.options_container import OptionsContainer

class ItemContainer:
    '''
    A container for items.
    
    Has: 
      * A default item class
      * An 'options' property of type OptionsContainer
        This OptionsContainer represents default options for all contained items
      * An 'add' method
        This method create
      * A 'last' item, representing the last item added 
    '''
    def __init__(self, itemClass):
        super().__init__()
        
        self.itemClass = itemClass
        self.options = OptionsContainer(itemClass.options)
        self.items = []
        self.last = None
        
    def add(self, *args, **kwargs):
        item = self.itemClass(*args, **kwargs)
        self.items.append(item)
        self.last = item
        return item

    def set(self, **kwargs):
        self.options.set(**kwargs)
