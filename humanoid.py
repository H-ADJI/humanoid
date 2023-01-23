'''
File: humanoid.py
File Created: Saturday, 21st January 2023 6:49:28 pm
Author: KHALIL HADJI 
-----
Copyright:  KHALIL HADJI 2023
'''
from playwright.sync_api import Page
from quick_math import add_jitter, bezier_curve
import math
import random
import typing
import numpy as np
import time


class HumanoidMouse():
    def __init__(self, page: Page) -> None:
        self.page = page
        self.mouse_position = (add_jitter(
            page.viewport_size['width']/2, intensity=10), 1)
        page.mouse.move(*self.mouse_position)

    def _click_position(self, target_selector: str):
        target_box = self.page.locator(selector=target_selector).bounding_box()
        click_pos_x = add_jitter(
            target_box['x'] + target_box['width']/2, intensity=25)
        click_pos_y = add_jitter(
            target_box["y"] + target_box["height"]/2, intensity=25)
        return click_pos_x, click_pos_y

    def _gen_control_points(self, start: tuple, finish: tuple):
        control_points = []
        lower_x, upper_x = min(start[0], finish[0]), max(start[0], finish[0])
        lower_y, upper_y = min(start[1], finish[1]), max(start[1], finish[1])
        for _ in range(3):
            x = random.randint(math.ceil(lower_x), math.ceil(upper_x))
            y = random.randint(math.ceil(lower_y), math.ceil(upper_y))
            control_points.append((x, y))
        control_points.sort(key=lambda x: math.dist(start, x))
        return control_points

    def _cursor_path(self, target_selector: str):
        """
        Args:
            target_selector (str): xpath / css
        """
        target_pos = self._click_position(target_selector=target_selector)
        interpolation_points = [self.mouse_position]
        interpolation_points.extend(self._gen_control_points(
            start=self.mouse_position, finish=target_pos))
        interpolation_points.append(target_pos)
        interpolation_points = np.array(interpolation_points)
        steps = math.ceil(math.dist(self.mouse_position,
                          target_pos)/(len(interpolation_points)-1))
        return bezier_curve(interpolation_points=interpolation_points, precision=steps)

    def _mouse_move(self, selector: str):
        path = self._cursor_path(target_selector=selector)
        for i, point in enumerate(path):
            self.page.mouse.move(x=point[0], y=point[1])
        self.mouse_position = point

    def click(self, selector, delay: int = 200, button: typing.Literal["left", "right", "middle"] = "left"):

        self._mouse_move(selector=selector)
        self.page.mouse.click(
            x=self.mouse_position[0], y=self.mouse_position[1], delay=delay, button=button)
