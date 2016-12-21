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

    def _resolve_options_self(self, container):
        # TODO we probably want "template containers" here, which would
        # container type(self) and the container.
        # TODO we currently iterate over the tags and select matching templates,
        # but we have to do it the other way: iterate over templates and check
        # if their selector matches one of our tags, so we can use regular
        # expressions or functions as selectors. However, we still have to make
        # sure that the "all" template has lower precedence than (is overridden
        # by) the named ones. 

        # Gather a list of applicable templates
        applicable_templates = []
        my_class = type(self)
        applicable_templates.append(my_class.all)
        for tag in self.tags:
            applicable_templates.append(my_class[tag])
        if container is not None:
            applicable_templates.append(container.all)
            for tag in self.tags:
                applicable_templates.append(container[tag])
        
        result = {}
        
        # Apply the options from the templates
        for template in applicable_templates:
            result.update(template.options.values)
            
        # Apply the options from this instance (after the options from the
        # templates so they take precedence).
        result.update(self.options.values)
        
        
#         result = {}
#  
#         # Default options from the class, i. e. [Class].all.options
#         result.update(type(self).all.options.values)
#          
#         # Options from the class by tag, i. e. [Class]["..."].options
#         # TODO there may be multiple matches here with no defined precedence.
#         for tag in self.tags:
#             result.update(type(self)[tag].options.values)
#          
#         # Default options from the container, i. e. items.all.options
#         if container is not None:
#             result.update(container.all.options.values)
#          
#         # Options from the container by tag, i. e. items["..."].options
#         if container is not None:
#             for tag in self.tags:
#                 result.update(container[tag].options.values)
#          
#         # Options from this instance, i. e. instance.options (set last, takes
#         # precedence over all of the others).
#         result.update(self.options.values)
        
        return result

    def _resolve_options_children(self):
        result = {}
        
        for child in self.children():
            result.update(child.resolve_options())

        return result
    
    def _resolve_options_containers(self):
        result = {}
        
        for container in self.containers():
            for item in container.items:
                result.update(item.resolve_options(container = container))
                
        return result

    def resolve_options(self, parent = None, container = None):
        # FIXME do we need parent here? Probably for inheriting.
        result = {}
        result[self] = self._resolve_options_self(container)
        result.update(self._resolve_options_children())
        result.update(self._resolve_options_containers())
        return result
