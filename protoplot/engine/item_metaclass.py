class ItemMetaclass(type):
    '''
    Adds the following to each class that uses this metaclass:
      * A __getitem__ that returns a template of the same class
    '''
    def __new__(cls, name, bases, attrs):
        result = super().__new__(cls, name, bases, attrs)
        result.__templates = {}
        return result

    def __getitem__(cls, tag):  # @NoSelf
        # If there is no template for this tag yet, add one 
        if tag not in cls.__templates:
            cls.__templates[tag] = cls()
            
        # Return the template for this tag
        return cls.__templates[tag]

    @property
    def all(cls):  # @NoSelf
        return cls[""]