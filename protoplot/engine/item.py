from protoplot.engine.options_container import OptionsContainer
from protoplot.engine.tag import make_tags_list
from protoplot.engine.item_metaclass import ItemMetaclass  # @UnusedImport
from protoplot.engine.item_container import ItemContainer
 
class Item(metaclass=ItemMetaclass):
    '''
    Represents an item in the tree. Items typically contain (a) other items, and
    (b) item containers.

    An Item *instance* has the following attributes:
      * An "options" property (of type OptionsContainer), which contains the
        options for this specific instance.
      * A "set" method as a shortcut for setting these options.
      * A (potentially empty) set of tags to allow selective application of
        options (a tag is similar to a class in CSS).
      
    An Item *subclass* has the following (class) attributes:
      * An item accessor which will return a template item instance for a given
        tag specification, which can be a string or the empty slice to specify
        the default template. (TODO really empty slice?)
      * An "all" property as a shortcut for [:]
      * A "set" method as a shortcut for [:].set 

    Item subclasses should call the Item constructor with all *args and **kwargs
    and configure their options in the constructor like so:
        self.options.register("color", False)
    '''
    
    def __init__(self, **kwargs):
        '''
        All kwargs will be used as options, except:
          * tag => use as tag(s)
        '''

        # Create the tag list and remove the tag argument from kwargs.        
        if 'tag' in kwargs:
            self.tags = make_tags_list(kwargs['tag'])
            del kwargs['tag']
        else:
            self.tags = []
        
        # Create the instance-level options and initialize them from the
        # remaining kwargs.
        #self.options = OptionsContainer(self.__class__.options)
        self.options = OptionsContainer()
        self.options.set(**kwargs)

        # Add the instance-level set method. See __set for an explanation. 
        self.set = self.__set


    ##############
    ## Children ##
    ##############

    def children(self):
        return [a for a in self.__dict__.values() if isinstance(a, Item)]

    def containers(self):
        return [a for a in self.__dict__.values() if isinstance(a, ItemContainer)]


    #############
    ## Options ##
    #############

    def __set(self, **kwargs):
        '''
        A setter shortcut for the instance-level options.
        
        This can't be called "set" because there is already a class method with
        the same name (defined in the metaclass) and Python does not have
        separate namespaces for class methods and instance methods. Therefore,
        this method will be assigned to the name of "set" in the instance
        namespace by the constructor.
        '''
        self.options.set(**kwargs)

    def _resolve_own_options(self):
        return self.options.values

    def _resolve_child_options(self):
        result = {}
        
        for child in self.children():
            result.update(child.resolve_options())

        return result
    
    def _resolve_container_options(self):
        result = {}
        
        for container in self.containers():
            for item in container.items:
                result.update(item.resolve_options())
                
        return result

    def resolve_options(self, parent = None, containerTemplates = []):
        result = {}
        result[self] = self._resolve_own_options()
        result.update(self._resolve_child_options())
        result.update(self._resolve_container_options())
        return result
