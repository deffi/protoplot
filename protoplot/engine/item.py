from protoplot.engine.options_container import OptionsContainer
from protoplot.engine.tag import make_tags_list
from protoplot.engine.item_metaclass import ItemMetaclass  # @UnusedImport
from protoplot.engine.item_container import ItemContainer

# TODO options should be resolved in the proper order. Here's the proposed
# resulting order for series:
#                            my_series .set(...)
#                  my_plot  .series.all.set(...)
#         my_page .plots.all.series.all.set(...)
#         Page.all.plots.all.series.all.set(...)
#                  Plot .all.series.all.set(...)
#                            Series.all.set(...)
# For testability, a resolved option should store probably store a complete list
# of values in order of priority.
 
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
    and define a register_options method to register the options, like so:
        self.options.register("color", False, "black")
    Note that the Item constructor, which runs before the Item subclass
    constructor, sets the initial options. The options must already be
    registered at this point, so this cannot be done by the Item subclass
    constructor. 
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
        self.register_options()
        self.options.set(**kwargs)

        # Add the instance-level set method. See __set for an explanation. 
        self.set = self.__set


    ##############
    ## Children ##
    ##############

    def children(self):
        return [(name, attribute)
            for name, attribute in self.__dict__.items()
            if isinstance(attribute, Item)]

    def containers(self):
        return [(name, attribute)
            for name, attribute in self.__dict__.items()
            if isinstance(attribute, ItemContainer)]


    #############
    ## Options ##
    #############

    def register_options(self):
        raise NotImplementedError(
            "Item subclasses must implement the register_options method")

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

    def resolve_options(self, templates = None, indent="", verbose = False):
        def p(*args, **kwargs):
            if verbose:
                print(indent, *args, **kwargs)
                
        # TODO do we need parent here? Probably for inheriting.

        p("Resolve options for", self)
        p("* Templates:", templates)
        p("* Tags:", self.tags)

        # Determine the applicable templates: the ones kindly selected by our
        # parent, plus the matching templates from our own class.  
        templates = templates or []
        templates = templates + type(self).matching_templates(self.tags) 

        # Determine the options for self
        own_options = {}
        own_options.update(self.options.fallback_values())
        for template in templates + [self]:
            own_options.update(template.options.values)
        #print(indent+"* Own options: {}".format(own_options))

        # Determine the options for direct children (recursively)
        children_options = {}
        for name, child in self.children():
            p("* Child", name)
            child_templates = [
                getattr(template, name)
                for template in templates
            ]
            children_options.update(child.resolve_options(child_templates, indent = indent+"  ", verbose = verbose ))

        # Determine the options for children in containers (recursively)
        containers_options = {}
        for name, container in self.containers():
            p("* Container", name, container)
            template_containers = [
                getattr(template, name)
                for template in templates + [self]
            ]
            p("* Template_containers", template_containers)
            
            for child in container.items:
                # Select the matching templates for the child
                child_templates = []
                for container in template_containers:
                    child_templates += container.matching_templates(child.tags) 
                
                containers_options.update(child.resolve_options(child_templates, indent = indent+"  ", verbose = verbose))

        result = {}
        result[self] = own_options
        result.update(children_options)
        result.update(containers_options)
        return result
