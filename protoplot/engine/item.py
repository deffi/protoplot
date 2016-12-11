# from plotlib.pl_options_container import OptionsContainer 
# from plotlib.pl_tag import make_tags_list
# 
# class ItemMetaclass(type):
#     '''
#     Adds an attribute "options" of type OptionsContainer to each class 
#     '''
#     def __new__(cls, name, bases, attrs):
#         attrs['options'] = OptionsContainer()
#         return super().__new__(cls, name, bases, attrs)
 
class Item:#(metaclass=ItemMetaclass):
    '''
    Represents an object in a heterogeneous hierarchy.
    
    It has:
      * A set of "tags" (like CSS classes)
      * A set of options, which can be set through the set() method and accessed
        through the options() method. Options can also be passed to the
        constructor.
    
    The Item class itself also has a set of options that  
    '''
#     def __init__(self, **kwargs):
#         '''
#         All kwargs will be used as options, except:
#           * tag => use as tags
#         '''
#         
#         # TODO should be self._tags or self.tags?
#         if 'tag' in kwargs:
#             self._tags = make_tags_list(kwargs['tag'])
#             del kwargs['tag']
#         else:
#             self._tags = []
#         
#         self.options = OptionsContainer()
#         self.options.update(kwargs)
#     
#     def effective_options(self, container):
#         opts = dict()
#         
#         # Default options for the class
#         opts.update(self.__class__.options.for_tags(self._tags))
#         
#         # Default options for the container of this item
#         if container is not None:
#             opts.update(container.options.for_tags(self._tags))
#         
#         # Options of this item instance
#         opts.update(self.options.for_tags(self._tags))
# 
#         return opts
