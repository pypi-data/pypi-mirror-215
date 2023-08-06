"""Removes trailing zeros

This script removes trailing zeros
"""
def remove_trailing_0_fcn(number):
    """This function differentiates a list wrt time.

    Parameters
    ----------
    number : float
        input number with trailing zeros


    Returns
    -------
    int
        number with decimal point and trailing zeros removed
    """
    diff_number = number -int(number)
    if diff_number == 0:
        number = int(number)
    
    return number