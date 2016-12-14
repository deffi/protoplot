import warnings

class _Entry:
    def __init__(self, name, inherit):
        self.name    = name
        self.inherit = inherit

class OptionsContainer():
    '''
    A collection of options in the form of key/value pairs.
    
    The options container maintains a list of known keys. Options with other
    keys may be added, but this will elicit a warning.
    '''
    def __init__(self, other = None):
        if other is None:
            self.entries = {}
        else:
            self.entries = other.entries
        self.values = {}

    def register(self, name, inherit):
        self.entries[name] = _Entry(name, inherit)

    def set(self, **args):
        for key, value in args.items():
            if not key in self.entries:
                warnings.warn("Setting unknown option {}".format(key))
            
            self.values[key] = value

    def __len__(self):
        return len(self.entries)
    