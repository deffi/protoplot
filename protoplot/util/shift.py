import numbers

def offset(shift_spec, count):
    # No shift at all - all values are 0
    if shift_spec is None:
        return [0] * count
    
    # Specified as a list - the list length must match the count. The values are
    # the same as specified in the list.
    elif isinstance(shift_spec, list):
        if len(shift_spec) != count:
            raise ValueError("Length of shift_spec does not match count")
        return list(shift_spec)
    
    # Specified as an increment - the values are increasing with a step size of
    # count, and symmetrical around 0.
    elif isinstance(shift_spec, numbers.Number):
        # 4 series: [-1.5, -0.5, 0.5, 1.5] * xshift
        # 5 series: [-2, -1, 0, 1, 2] * xshift
        # n series: 
        return [(i - (count-1)/2) * shift_spec for i in range(count)]
    
    else:
        raise ValueError("Unsupported shift_spec: {}".format(repr(shift_spec)))
