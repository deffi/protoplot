def make_tags_list(arg):
    '''
    Creates a list of strings from the input.
    
    Accepts the following format:
      * A list of strings
      * A string of comma-separated values
    '''
    if isinstance(arg, list):
        # TODO verify that the list contains valid tags (strings or recursive
        # call?)
        # TODO allow all iterables, at least tuple
        return arg
    elif isinstance(arg, str):
        # TODO strip off whitespace
        # TODO allow splitting on whitespace
        # TODO remove empty
        return arg.split(",")
    else:
        raise ValueError("Unsupported tags specification: %s" % repr(arg))

def match_tags(selectors, item_tags):
    '''
    Returns a list of selectors which match the item_tags, in increasing order
    of priority.
    '''
    
    result = []
    
    # First of all, the default selector (so it has the lowest priority)
    if "" in selectors:
        result.append("") 
    
    # Now all remaining selectors 
    for selector in selectors:
        if selector != "":
            if selector in item_tags:
                result.append(selector)

    return result
