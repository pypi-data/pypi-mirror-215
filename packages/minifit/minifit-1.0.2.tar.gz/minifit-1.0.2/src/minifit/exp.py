# -*- coding: utf-8 -*-
# Copyright (C) 2023-- Michał Kopczyński
#
# This file is part of MiniFit.
#
# MiniFit is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# MiniFit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
"""
Module containing ExponentialFit class for curve fitting with exponentials.
"""

import random
import numpy as np
import matplotlib
from .fit_base import FitBase, log

matplotlib.use("Agg")


class ExponentialFit(FitBase):
    """
    This class makes an exponential curve fitting.
    It reads data from a file given as the first argument.
    The data file must contain at least two columns.
    The first column represents x values,
    the second and following columns are the y values.
    """

    def __init__(self, filename, **kwargs):
        """
        **Arguments:**

        filename:
            (string) Name of the file that contains data.

        **Keyword arguments:**

        guess:
            (tuple) Guess of the optimal parameters for the model.
        """

        self.common_init(filename, **kwargs)
        self.type_of_fit = "Exponential"
        self.label_type = "exp_fit"

    def default_guess(self, context):
        """Default guess adequate for the model function."""
        guess = [1, 2, 1]

        return guess

    def random_guess(self, context):
        """
        Random guess adequate for the model function with constraints
        chosen by the user.
        """
        if self.auto_range is None:

            guess = [
                random.uniform(-60, 60),
                random.uniform(-60, 60),
                random.uniform(-60, 60),
            ]
        else:
            guess = [
                random.uniform(min_val, max_val)
                for min_val, max_val in self.auto_range
            ]

        return guess

    def print_info(self, popt):
        """
        Print info about popt in the format adequate for the model function.
        """
        name_temp = ("a", "b", "c")
        for el in range(3):
            log(f"\t {name_temp[el]}: {popt[el]:2.8f}")

    def model_function(self, x, *args, **kwargs):
        """Depends on the module."""
        if len(args) != 3:
            raise TypeError("Wrong amount of guess parameters passed")
        a, b, c = args
        return a * np.exp(b * x) + c
