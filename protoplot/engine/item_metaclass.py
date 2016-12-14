from protoplot.engine.options_container import OptionsContainer

class ItemMetaclass(type):
    '''
    Adds the following to each class that uses this metaclass:
      * An "options" attribute of type OptionsContainer
      * TBD: A __getattr__ that returns a template of the same class
    '''
    def __new__(cls, name, bases, attrs):
        attrs['options'] = OptionsContainer()
        return super().__new__(cls, name, bases, attrs)
