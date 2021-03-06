import warnings

class _NotSpecified:
    def __str__(self):
        return "notSpecified"

notSpecified = _NotSpecified



class _Entry:
    def __init__(self, default = notSpecified, inherit = False, defer = None):
        self.default = default
        self.inherit = inherit
        self.defer   = defer

class OptionsContainer():
    '''
    An enhanced key/value storage.

    An options container is supposed to be associated with an object ("item"),
    potentially in a hierarchy of objects.

    # TODO this documentation is very outdated

    Compared to dict, OptionsContainer has the following features:
      * It maintains a list of known keys.
      * Each known key can have a fallback that is used in lieu of the value if
        the value has not been set for this key.

    Setting the value for an unknown key is possible, but will elicit a warning.
    # TODO not?

    The fallback is exactly one of the following:
      * Default value:
        If no value has been set for the key, the default value will be
        returned. Example:
          * color with a default value of "black" or "#000000" or color.black
      * Inherit:
        If no value has been set for the key, another container (the "parent
        container") will be tested. The parent container is supposed to be the
        options container associated with a parent item of of the item that is
        associated with this container, but can be None if the associated item
        is not part of a hierarchy, or is the root of the hierarchy. Examples:
          * fontSize inheriting the parent's fontSize
          * color of a border inheriting the parent's borderColor
          * label of an X axis inheriting the parent's xLabel
          * fillColor of a marker inheriting the parent series' markerFillColor
      * Defer:
        If no value has been set for the key, the value for another key in the
        same container will be returned. If no value for the other key has been
        set, the other key's fallback will be checked, just as for direct
        accesses to the other key. Example:
          * markerFaceColor deferring to markerColor deferring to color.
            Color might have a default or inherited value.
          * Not implemented: CSS style "border: 1px solid black" (shorthand
            property)
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
        # The registered options. If other is specified, copy its registered
        # options. Otherwise, start with an ampty dict.
        if other is None:
            self._entries = {}
        else:
            self._entries = dict(other._entries)

        # The explicitly set values
        self._values = {}

        # The indirectly set values
        self._indirect_values = {}

    def register(self, name, default = notSpecified, inherit = False, defer = None):
        self._entries[name] = _Entry(default, inherit, defer)

    def set(self, **args):
        for key, value in args.items():
            if key in self._entries:
                self._values[key] = value
            else:
                warnings.warn("Ignoring unknown option {}".format(key))

    def set_indirect(self, name, value):
        if name in self._entries:
            self._indirect_values[name] = value
        else:
            warnings.warn("Ignoring unknown option {}".format(key))

    def _optionNames(self):
        '''
        Builds a list of option names in resolving order: if a defers to b, then
        b must come before a in the list.
        '''

        unsortedNames = list(self._entries.keys())
        sortedNames = []

        while unsortedNames:
            # Pick a name: take the first unsorted name and follow the deferral
            # chain to the end.
            name = unsortedNames[0]
            while self._entries[name].defer and self._entries[name].defer in unsortedNames:
                name = self._entries[name].defer

            # Add the picked name to the sorted list and remove it from the
            # unsorted list.
            sortedNames  .append(name)
            unsortedNames.remove(name)

        return sortedNames

    def _resolve_entry(self, name, templates, inherited, resolvedValues):
        # Value
        if name in self._values:
            return self._values[name]

        # Shorthand

        # Indirect
        if name in self._indirect_values:
            return self._indirect_values[name]

        # Template value (only explicitly set values, no fallbacks or defaults)
        for template in templates:
            if name in template._values:
                return template._values[name]

        # Template shorthand

        # Inherited
        if self._entries[name].inherit and name in inherited:
            return inherited[name]

        # Deferred
        deferredName = name
        while deferredName and deferredName not in resolvedValues:
            entry = self._entries[deferredName]
            deferredName = entry.defer
        if deferredName:
            return resolvedValues[deferredName]

        # Default
        entry = self._entries[name]
        return entry.default

    def resolve(self, templates = None, inherited = None, pruneNotSpecified = False):
        '''
        Returns a dict(name: value).

        templates is a list of OptionsContainer in decreasing order of priority
        inherited is a dict(name: value)
        '''

        resolvedValues = dict()

        if templates is None: templates = list()
        if inherited is None: inherited = dict()

        for name in self._optionNames():
            resolved = self._resolve_entry(name, templates, inherited, resolvedValues)

            # Add the resolved value to the result dict, unless it is
            # notSpecified and notSpecified is to be pruend.
            if not (resolved is notSpecified and pruneNotSpecified):
                resolvedValues[name] = resolved

        return resolvedValues
