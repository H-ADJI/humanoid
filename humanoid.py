'''
File: humanoid.py
File Created: Saturday, 21st January 2023 6:49:28 pm
Author: KHALIL HADJI 
-----
Copyright:  KHALIL HADJI 2023
'''
from playwright.sync_api import sync_playwright, Page
from quick_math import add_jitter, fitts_law, bezier_curve
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

    def _gen_control_points(self):
        x = add_jitter(self.page.viewport_size['width']/2, intensity=30)
        y = add_jitter(self.page.viewport_size['height']/2, intensity=30)
        return x, y

    def _cursor_path(self, target_selector: str):
        """use Fitts law of human-computer interaction difficulty index
        Source: https://en.wikipedia.org/wiki/Fitts%27s_law#Bits_per_second:_model_innovations_driven_by_information_theory

        Args:
            target_selector (str): xpath / css
        """
        target_pos = self._click_position(target_selector=target_selector)
        target_box = self.page.locator(selector=target_selector).bounding_box()
        target_width = min(target_box['height'], target_box['width'])
        difficulty_index = fitts_law(current_pos=self.mouse_position,
                                     target_pos=target_pos, target_width=target_width)
        control_points = [self.mouse_position]
        for _ in range(5):
            control_points.append(self._gen_control_points())
        control_points.append(target_pos)
        interpolation_points = np.array(control_points)
        return bezier_curve(interpolation_points=interpolation_points, precision=difficulty_index)

    def _mouse_move(self, selector: str):
        path = self._cursor_path(target_selector=selector)
        path_size = len(path)
        for i, point in enumerate(path):
            if i > path_size*0.8:
                time.sleep(0.05)

            self.page.mouse.move(x=point[0], y=point[1])
        self.mouse_position = point

    def click(self, selector, delay: int = 200, button: typing.Literal["left", "right", "middle"] = "left"):
        
        self._mouse_move(selector=selector)
        self.page.mouse.click(
            x=self.mouse_position[0], y=self.mouse_position[1], delay=delay, button=button)
