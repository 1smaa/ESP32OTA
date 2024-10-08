def check_for_keys(*args) -> bool:
    '''
    Checks if all the specified keys are present within the dictionary
    '''
    d=args[0]
    if(not isinstance(d,dict)): return False
    for s in args[1:]:
        if (s not in d.keys()): return False
    return True