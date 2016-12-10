def identical(series):
    '''
    series is a list of series (each series is a list)
    Returns True if the series are identical 
    '''
    for l in series[1:]:
        if l != series[0]:
            return False
    return True

def average_list(l):
    return sum(l) / len(l)

def average_series(series):
    # Series:
    #   [[1, 11, 111], 
    #    [3, 33, 333]]
    # Transposed:
    #   [[  1,   3],
    #    [ 11,  33],
    #    [111, 333]]
    # Average:
    #   [2, 22, 222]
    
    transposed = zip(*series)
    
    average = [average_list(r) for r in transposed]
    
    return average

def combine(records, function, separate = []):
    if len(separate) == 0:
        return function(records)
    elif len(separate) == 1:
        separate = separate[0]
        separate_values = set(getattr(r, separate) for r in records)
        
        result = []
        for value in separate_values:
            recs = [r for r in records if getattr(r, separate) == value]
            result.append(function(recs))

        return result
    else:
        raise NotImplemented("Multiple separate values")

def is_multiple(x):
    return isinstance(x, tuple) or isinstance(x, list)

def is_single(x):
    return isinstance(x, float) or isinstance(x, int)

def filter_none(values):
    # Values:
    #     [11, 22, 0, 44, 0], [111, 222, 333, 0, 0]
    # zip(*_):
    #     (11, 111), (22, 222), (0, 333), (44, 0), (0, 0)
    # [vv for vv in _ if all(v is not None for v in vv)] 
    #     (11, 111), (22, 222)
    # zip(*_):
    #     (11, 22), (111, 222)
    values = zip(*values)
    values = [vv for vv in values if all(v is not None for v in vv)]
    values = zip(*values)
    return values

def select(selector, data):
    if hasattr(selector, "__call__"):
        result = selector(data)
    elif isinstance(selector, str) and selector[0]=='.':
        code = "data"+selector
        globs = {}
        locs = {'data': data}
        result = eval(code, globs, locs) # FIXME safe?
    elif isinstance(selector, str) and hasattr(data, selector):
        result = getattr(data, selector)
    else:
        result = None

    if hasattr(result, "__call__"):
        return result()
    else:
        return result
