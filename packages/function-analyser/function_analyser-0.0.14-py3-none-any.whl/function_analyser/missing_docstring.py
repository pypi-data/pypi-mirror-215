def has_docstring(function):
    """
    Does a function have a docstring?
    :param function:
    :return:
    """
    return function[1].__doc__ is not None
