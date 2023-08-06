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
Module containing MorseFit class for curve fitting with morse.
"""


import random
import matplotlib
import numpy as np  # pylint: disable=W0611
from .fit_base import FitBase, log


matplotlib.use("Agg")


class UserFit(FitBase):
    """
    This class makes curve fitting using morse potential formula.
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

        num_param:
            (int) Number of parameters of user defined model function.
        model:
            (function/callable) An object that expects (x, *args, **kwargs)
            and returns y value for given arguments
        guess:
            (tuple) Guess of the optimal parameters for the model.
        auto_guess:
            (bool) If true, tries to fit until chosen precision is reached. Default false.
        range_auto:
            (tuple) Sets boundaries for each parameter of guess.
            If not set, default range is used.
        precision:
            Used by auto_guess. Default 0.4
        shift:
            (bool) If true, shifts the data. Default false.
        """
        self.common_init(filename, **kwargs)

        self.type_of_fit = kwargs.get("type_of_fit", "User defined function")
        self.label_type = kwargs.get("label_type", "user_fit")
        num_param = kwargs.get("num_param")
        if num_param is None:
            raise ValueError(
                "Missing required parameter: num_param. How many parameters your functions has? Required for sanitazation"  # pylint: disable=C0301
            )
        self.num_param = num_param

        user_def_func = kwargs.get("model")
        if user_def_func is not None and callable(user_def_func):
            # The object is a function
            self.user_def_func = user_def_func
        else:
            # The object is not a function or is None
            raise ValueError(
                "Missing required parameter: model. With what function do you want to fit?"
            )

    def model_function(self, x, *args, **kwargs):
        """Depends on the module."""
        if len(args) != self.num_param:
            raise TypeError("Wrong amount of guess parameters passed")
        return self.user_def_func(x, *args, **kwargs)

    def default_guess(self, context):
        """Default guess adequate for the model function."""
        guess = []
        for _ in range(self.num_param):
            guess.append(1.0)
        return guess

    def random_guess(self, context):
        """
        Random guess adequate for the model function with constraints
        chosen by the user.
        """
        if self.auto_range is None:
            guess = []
            for _ in range(self.num_param):
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
        for el in range(self.num_param):
            log(f"\t {el}: {popt[el]:2.8f}")
