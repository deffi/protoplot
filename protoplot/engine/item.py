from protoplot.engine.options_container import OptionsContainer
from protoplot.engine.tag import make_tags_list
 
class ItemMetaclass(type):
    '''
    Adds the following to each class that uses this metaclass:
      * An "options" attribute of type OptionsContainer
      * A "set" method that calls options.set  
      * TBD: A __getattr__ that returns a template of the same class
    '''
    def __new__(cls, name, bases, attrs):
        attrs['options'] = OptionsContainer()
        return super().__new__(cls, name, bases, attrs)

    def set(cls, **kwargs):  # @NoSelf
        cls.options.set(**kwargs)

class Item(metaclass=ItemMetaclass):
    '''
    Represents an object in a heterogeneous hierarchy.
    
    It has:
      * A set of "tags" (like CSS classes)
      * A set of "options", which can be set through the set() method and
        accessed as OptionsContainer through the options property. Options can
        also be passed to the constructor.
    
    The Item class itself also has a set of options that  
    '''
    def __init__(self, **kwargs):
        '''
        All kwargs will be used as options, except:
          * tag => use as tag(s)
        '''
        
        if 'tag' in kwargs:
            self.tags = make_tags_list(kwargs['tag'])
            del kwargs['tag']
        else:
            self.tags = []
         
        self.options = OptionsContainer(self.__class__.options)
        self.options.set(**kwargs)

        # So we can have an instance method and a class method of the same name 
        self.set = self.__set

    def __set(self, **kwargs):
        self.options.set(**kwargs)
