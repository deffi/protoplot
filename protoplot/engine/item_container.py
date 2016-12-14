from protoplot.engine.options_container import OptionsContainer

class ItemContainer:
    '''
    A homogeneous container for items.
    
    An ItemContainer contains any number of instances of a specific subclass of
    Item, called the ItemContainer's item class. An instance can be added to the
    container by calling the container's add method.

    As a convenience, an ItemContainer has a "last" property, representing the
    last item added to the container (None if no item has been added so far).
    
    An item container has an "options" property, which represents the default
    options for all items in this container, and a "set" method as a shortcut
    for setting these options.    
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
