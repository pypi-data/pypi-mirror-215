from typing import Union

def sum(x: Union[int, float], y: Union[int, float]):
    """
    Sum two numbers

    INPUT
        x: int or float
        y: int or float
    
    OUTPUT: int or float
    """
    
    return x + y

def average(x: Union[int, float], y: Union[int, float]):
    """
    Get average from two numbers.

    INPUT
        x: int or float
        y: int or float
    
    OUTPUT: float
    """
    
    return (x + y) / 2

def power(x: Union[int, float], y: Union[int, float]):
    """
    Generate power of a number by another number.

    INPUT
        x: int or float
        y: int or float
    
    OUTPUT: int or float
    """

    return x**y
