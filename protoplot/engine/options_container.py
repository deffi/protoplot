import warnings

# Resolving order: templates first, then fallbacks

# TODO cache the resolving results

class _Entry:
    def __init__(self, name, default = None, inherit = None, defer = None):
        # TODO do we need the name here? It's also stored in the
        # OptionsContainer.values dict.
        self.name    = name

        self.default = default

        self.inherit = inherit
        self.defer   = defer

class OptionsContainer():
    '''
    An enhanced key/value storage.

    An options container is supposed to be associated with an object ("item"),
    potentially in a hierarchy of objects.

    Compared to dict, OptionsContainer has the following features:
      * It maintains a list of known keys.
      * Each known key can have a fallback that is used in lieu of the value if
        the value has not been set for this key.

    Setting the value for an unknown key is possible, but will elicit a warning.
    # TODO not?

    The fallback is exactly one of the following:
      * Default value
        If no value has been set for the key, the default value will be
        returned. For example, the key "color" might have a default value of
        "black" or "#000000".
      * Inherit
        If no value has been set for the key, another container (the "parent
        container") will be tested. The parent container is supposed to be the
        options container associated with a parent item of of the item that is
        associated with this container, but can be None if the associated item
        is not part of a hierarchy, or is the root of the hierarchy. For
        example, the key "fontSize" might inherit the same key from the parent.
        The "color" key for an options container associated with a border might
        inherit the parent's "borderColor" key.
      * Defer
        If no value has been set for the key, the value for another key in the
        same container will be returned. If no value for the other key has been
        set, the other key's fallback will be checked, just as for direct
        accesses to the other key. For example, the key "markerFaceColor" might
        defer to "markerColor", which might defer to "color", which might have
        a default or inherited value.
    The default fallback is a default value of None.

    To register a key, call the register method, specifying the name of the key
    and the fallback option.

    To set a value for a key (or for multiple keys), call the set method,
    passing the keys and values as kwargs.

    To retrieve options, use the fallback_values() method to retrieve the
    fallback values and the values property to retrieve the values that have
    actually been set.
    TODO improve: only calculate the fallback if no value has been set. Also,
    templates should be evaluated by this class.
    '''
    def __init__(self, other = None):
        # Use the entries of /other/ (if specified) or initialize to an empty
        # dict.
        if other is None:
            self._entries = {}
        else:
            self._entries = other._entries

        self._values = {}

    def register(self, name, default = None, inherit = None, defer = None):
        self._entries[name] = _Entry(name, default, inherit, defer)

    def set(self, **args):
        for key, value in args.items():
            if key in self._entries:
                self._values[key] = value
            else:
                warnings.warn("Ignoring unknown option {}".format(key))

    def _resolve_entry(self, name, templates, parent_values):
        # 1: Value
        if name in self._values:
            return self._values[name]

        # 2: Templates (only explicitly set values, no fallbacks or defaults)
        for template in templates:
            if name in template._values:
                return template._values[name]

        # 3: Fallbacks
        entry = self._entries[name]
        # TODO current


        # 4: Defaults

        pass

    def values(self):
        # A copy of the values
        return dict(self._values)

    def resolve(self, templates = None, parent_values = None):
        '''
        Returns a dict(name: value).

        templates is a list of OptionsContainer in decreasing order of priority
        parent_values is a dict(name: value)
        '''

        return {
            name, _resolve_entry(name, templates, parent_values)
            for name in self._entries.keys()
        }

    # TODO remove? Or should it return the number of set values?
    #def __len__(self):
    #    return len(self.entries)
