'''
File: quick_math.py
File Created: Saturday, 21st January 2023 6:50:01 pm
Author: KHALIL HADJI 
-----
Copyright:  KHALIL HADJI 2023
'''
import numpy as np
import random


def walk(start_point: np.ndarray, end_point: np.ndarray, steps_count: int = 50) -> np.ndarray:
    """walking is generating uniform steps coordinates from starting to finishing point according to a step count 

    Args:
        start_point (np.ndarray): coordinates of the starting point [x,y]
        end_point (np.ndarray): coordinates of the ending point [x,y]
        steps_count (int, optional): how many points will be generated between start and finish. Defaults to 50.

    Returns:
        numpy.ndarray: all steps coordinates including start and finish
    """
    steps = np.array([np.linspace(0, 1, steps_count)])
    return start_point + steps.T*(end_point - start_point)


def bezier_curve(interpolation_points: np.ndarray) -> np.ndarray:
    """implementation of recursive formula for any degree n = Card(interpolation_points)-1.

    TODO: Maybe also implement the explicite formula of the bezier curve for more efficiency
    formula from wikipedia : https://en.wikipedia.org/wiki/B%C3%A9zier_curve#General_definition 

    Args:
        interpolation_points (np.ndarray): all points to fit to a bezier curve (including start and finish)

    Returns:
        np.ndarray: points coordinates that forms the bezier curve  
    """
    if interpolation_points.shape == (1, 2):
        return interpolation_points
    return walk(bezier_curve(interpolation_points[:-1, :]), bezier_curve(interpolation_points[1:, :]))


def random_control_point():
    pass
