from protoplot.engine.options_container import OptionsContainer
from protoplot.engine.tag import make_tags_list
from protoplot.engine.item_metaclass import ItemMetaclass  # @UnusedImport
 
class Item(metaclass=ItemMetaclass):
    '''
    Represents an item in the item hierarchy. Items typically contain other
    items and item containers.

    An Item has an "options" property, which represents the options explicitly
    set for this instance, and a "set" method as a shortcut for setting these
    options.    

    In Item instance can also have one or multiple tags, and separate sets of
    options for each each tag (similar to CSS classes). 

    Each Item subclass (!) also has an "options" property (also type
    OptionsContainer), which represents the default options for all instances of
    that class, and a "set" method as a shortcut for setting these options.
    
    To implement an item, create a subclass of Item. Then, configure its options
    by calling .options.register.
    '''
    def __init__(self, **kwargs):
        '''
        All kwargs will be used as options, except:
          * tag => use as tag(s)
        '''

        # Create the tag ist and remove the tag argument from kwargs.        
        if 'tag' in kwargs:
            self.tags = make_tags_list(kwargs['tag'])
            del kwargs['tag']
        else:
            self.tags = []
        
        # Create the instance-level options and initialize them from the
        # remaining kwargs. Note that the subclass-level options are created by
        # the metaclass.
        self.options = OptionsContainer(self.__class__.options)
        self.options.set(**kwargs)

        # Add the instance-level set method. See __set for an explanation. 
        self.set = self.__set

    @classmethod
    def set(cls, **kwargs):
        '''
        A setter shortcut for the subclass-level options.
        '''
        cls.options.set(**kwargs)

    def __set(self, **kwargs):
        '''
        A setter shortcut for the instance-level options.
        
        This can't be called "set" because there is already a class method with
        the same name and Python does not have separate namespaces for class
        methods and instance methods. Therefore, this method will be assigned to
        the name of "set" in the instance namespace by the constructor.
        '''
        self.options.set(**kwargs)
