"""
This module contains the Equalizer class, which is used to compare two objects.
The comparison is done by recursively comparing the attributes of the objects.
"""
import numpy as np
from .utils import type_to_params


class Equalizer:
    def __init__(self, epsilon: float):
        self.epsilon = epsilon

    def equalize(self, first, second):
        """
        Compare two objects
        """
        if first is None and second is None:
            return True
        if isinstance(first, (int, str, bool)):
            return first == second
        if isinstance(first, (float, np.float64)):
            return abs(first - second) < self.epsilon
        if isinstance(first, list):
            return all(
                self.equalize(first_item, second_item)
                for first_item, second_item in zip(first, second)
            )
        params = type_to_params(type(first))
        for attr, value in vars(first).items():
            if attr not in params:
                continue
            if not self.equalize(value, getattr(second, attr)):
                return False

        return True
