from protoplot.engine.tag import match_tags

class ItemContainer:
    '''
    A homogeneous container for items.
    
    An ItemContainer contains any number of instances of a specific subclass of
    Item, called the ItemContainer's item class. An instance can be added to the
    container by calling the container's add method.

    As a convenience, an ItemContainer has a "last" property, representing the
    last item added to the container (None if no item has been added so far).

    An item container also has the following attributes:
      * An item accessor which will return a template item instance for a given
        tag specification, which can be a string or the empty slice to specify
        the default template.  TODO really empty slice?
      * An "all" property as a shortcut for [:]
      * A "set" method as a shortcut for [:].set

    itemClass must have the following properties:
      * Its constructor must be able to be called without arguments (for
        template creation)
      * It must have a set method accepting options as kwargs.
    '''
    def __init__(self, itemClass):
        super().__init__()

        # Items        
        self.itemClass = itemClass
        self.items = []
        self.last = None
        
        # Templates
        self.__templates = {}
        
    def add(self, *args, **kwargs):
        item = self.itemClass(*args, **kwargs)
        self.items.append(item)
        self.last = item
        return item


    ###############
    ## Templates ##
    ###############

    # Note that these methods are the same as in ItemMetaclass.
    # TODO We should definitely merge them somehow.
    # TODO in some places, it should say "selector" instead of "tag" 

    def __getitem__(self, tag):
        # If there is no template for this tag yet, add one 
        if tag not in self.__templates:
            self.__templates[tag] = self.itemClass()
            
        # Return the template for this tag
        return self.__templates[tag]

    @property
    def all(self):
        return self[""]

    def set(self, **kwargs):
        '''
        A setter shortcut for the default template
        '''
        self[""].set(**kwargs)

    def matching_templates(self, tags):
        '''
        Returns a list of applicable templates for an object with the specified
        tags, in increasing order of preference.
        '''
        keys = match_tags(self.__templates.keys(), tags)
        return [self.__templates[key] for key in keys]
