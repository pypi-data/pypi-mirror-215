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
Module containing LennardJonesFit class for curve fitting with Lennard-Jones.
"""

import random
import numpy as np  # pylint: disable=W0611
import matplotlib
from .fit_base import FitBase, log

matplotlib.use("Agg")


class LennardJonesFit(FitBase):
    """
    This class makes curve fitting using Lennard-Jones potential formula.
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
        shift
            (bool) If true, shifts the data
        """

        self.common_init(filename, **kwargs)
        self.type_of_fit = "Lennard-Jones potential"
        self.label_type = "lennard_jones_fit"

    def model_function(self, x, *args, **kwargs):
        """Depends on the module."""
        r = x
        if len(args) != 2:
            raise TypeError("Wrong amount of guess parameters passed")
        sigma, epsilon = args
        return 4 * epsilon * ((sigma / r) ** 12 - (sigma / r) ** 6)

    def default_guess(self, context):
        """Default guess adequate for the model function."""
        guess = [1, 1]

        return guess

    def random_guess(self, context):
        """
        Random guess adequate for the model function with constraints
        chosen by the user.
        """
        if self.auto_range is None:

            guess = [random.uniform(-60, 60), random.uniform(-60, 60)]
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
        name_temp = ("sigma", "epsilon")
        for el in range(2):
            log(f"\t {name_temp[el]}: {popt[el]:2.8f}")
