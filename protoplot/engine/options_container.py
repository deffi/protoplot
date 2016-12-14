import warnings

class _Entry:
    def __init__(self, name, inherit):
        self.name    = name
        self.inherit = inherit

class OptionsContainer():
    def __init__(self, other = None):
        #super().__init__(*args, **kwargs) # For dict superclass
        # TODO should we store a reference to the "other" OC instead?
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
    