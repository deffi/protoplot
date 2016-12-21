from protoplot.engine.tag import match_tags

class ItemMetaclass(type):
    '''
    Adds the following to each class that uses this metaclass:
      * A __getitem__ that returns a template of the same class
    '''
    def __new__(cls, name, bases, attrs):
        result = super().__new__(cls, name, bases, attrs)
        result.__templates = {}
        return result


    ###############
    ## Templates ##
    ###############

    # Note that these methods are the same as in ItemContainer.
    # The set method could also be defined as a @classmethod in Item, but is
    # defined here for uniformity with ItemContainer.  

    def __getitem__(cls, tag):  # @NoSelf
        # If there is no template for this tag yet, add one 
        if tag not in cls.__templates:
            cls.__templates[tag] = cls()
            
        # Return the template for this tag
        return cls.__templates[tag]

    @property
    def all(cls):  # @NoSelf
        return cls[""]

    def set(cls, **kwargs):  # @NoSelf
        '''
        A setter shortcut for the default template
        '''
        cls[""].set(**kwargs)

    def matching_templates(cls, tags):  # @NoSelf
        '''
        Returns a list of applicable templates for an object with the specified
        tags, in increasing order of preference.
        '''
        keys = match_tags(cls.__templates.keys(), tags)
        return [cls.__templates[key] for key in keys]
