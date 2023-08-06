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
Module containing PolyFit class for curve fitting with polynomials.
"""
import random
import matplotlib
import numpy as np  # pylint: disable=W0611
from .fit_base import FitBase, log


matplotlib.use("Agg")


class PolyFit(FitBase):
    """
    This class makes a polynomial curve fitting.
    Order of the polynomial can be chosen.
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
        order:
            (int) Order of the polynomial. Optional. Default 1
        """

        if kwargs.get("order") is None:
            log("=")
            log("Order of the polynomial wasn't given. Using default (1)")
            self.order = 1
        else:
            self.order = kwargs.get("order")
        self.common_init(filename, **kwargs)
        self.type_of_fit = "Polynomials"
        self.label_type = "polynomial_fit"

    def model_function(self, x, *args, **kwargs):
        """Depends on the module."""
        if len(args) != self.order + 1:
            raise TypeError("Wrong amount of guess parameters passed")
        val = 0.0
        # a + b*x + c*x^2 + etc.
        for exp in range(self.order + 1):
            val += args[exp] * x**exp
        return val

    def default_guess(self, context):
        """Default guess adequate for the model function."""
        guess = []
        for _ in range(self.order + 1):
            guess.append(1.0)
        return guess

    def random_guess(self, context):
        """
        Random guess adequate for the model function with constraints
        chosen by the user.
        """
        if self.auto_range is None:
            guess = []
            for _ in range(self.order + 1):
                guess.append(random.uniform(-150, 150))

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
        for el in range(self.order + 1):
            log(f"\t {el}: {self.popt[el]:2.8f}")
