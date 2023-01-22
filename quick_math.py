'''
File: quick_math.py
File Created: Saturday, 21st January 2023 6:50:01 pm
Author: KHALIL HADJI 
-----
Copyright:  KHALIL HADJI 2023
'''
import numpy as np
import random
import math


def walk(start_point: np.ndarray, end_point: np.ndarray, steps_count: int) -> np.ndarray:
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


def bezier_curve(interpolation_points: np.ndarray, precision: int = 20) -> np.ndarray:
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
    return walk(bezier_curve(interpolation_points[:-1, :], precision=precision), bezier_curve(interpolation_points[1:, :], precision=precision), steps_count=precision)


def add_jitter(value: int, intensity: int = 20, absolute: bool = False):
    if absolute:
        coef = random.randint(0, intensity)
    else:
        coef = random.choice([-1, 1])*random.randint(-intensity, intensity)
    return value + value*coef/100


def random_control_point():
    pass


def fitts_law(current_pos: tuple, target_pos: tuple, target_width: int, min_steps: int = 200, difficulty_scaling_coef: int = 20):

    D = math.dist(current_pos, target_pos)
    return math.ceil(min_steps + difficulty_scaling_coef*math.log2((2*D/target_width) + 1))
