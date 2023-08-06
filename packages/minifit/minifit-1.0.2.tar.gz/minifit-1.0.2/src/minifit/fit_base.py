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
Module containing logger and FitBase class.
"""

from abc import ABC, abstractmethod
import warnings
from pathlib import Path
from scipy.optimize import curve_fit
import matplotlib.pyplot as pyplot
import numpy as np


def log(str1):
    """Logger"""
    if str1 == "~":
        print("~" * 100)
    elif str1 == "=":
        print("=" * 100)
    elif str1 == "-":
        print("-" * 100)
    elif str1 == " ":
        print(" ")
    else:
        print(f"\t{str1}")


# pylint: disable=unnecessary-pass,attribute-defined-outside-init


class FitBase(ABC):
    """
    Base class for all fitting classes
    """

    def common_init(self, filename, **kwargs):
        """
        Common constructor
        """
        self.type_of_fit = (
            "FitBase instance attribute - needs to be overwritten"
        )
        self.label_type = (
            "FitBase instance attribute - needs to be overwritten"
        )
        path_data = Path("./minifit-data/" + filename)
        path_cwd = Path.cwd()
        if path_data.exists() is not True and path_cwd.exists is not True:
            raise FileNotFoundError(
                f"\"Couldn't find {filename} in minifit-data"
            )

        self.filename = filename

        if kwargs.get("guess") is None:
            self.guess = None
        else:
            self.guess = kwargs.get("guess")

        # self.guess = kwargs.get("guess", None)

        if kwargs.get("auto_guess") is True:
            self.auto_guess = True
            self.auto_range = kwargs.get("auto_range", None)
        else:
            self.auto_guess = False
            self.auto_range = None

        if kwargs.get("precision") is not None:
            self.precision = kwargs.get("precision")
        else:
            self.precision = 0.4
        # self.precision = kwargs.get("precision",  0.4)

        if kwargs.get("shift") is None:
            self.shift = False
        else:
            self.shift = kwargs.get("shift")
        # self.precision = kwargs.get("shift",  False)

        if path_data.exists() is True:
            self.filename = filename
            self.read_data(str(path_data))
        else:
            self.filename = filename
            self.read_data(str(path_cwd))

        self.popt = None
        self.pcov = None
        self.abs_sum_diff = np.inf
        self.sq_root_error = np.inf

    def read_data(self, filename):
        """Reads data from each column then shifts the data."""
        cols = None
        with open(filename) as file:
            for line in file:
                if not line.startswith("#"):
                    data = [float(x) for x in line.split()]
                    if cols is not None:
                        cols = np.vstack((cols, data))
                    else:
                        cols = np.array(data)
        self.xdata = cols[:, 0]
        self.ydata = cols[:, 1:]

        self.shift_data = self.ydata[-1, :].copy()
        if self.shift is True:
            self.ydata -= self.ydata[-1, :]
        else:
            self.shift_data[self.shift_data != 0] = 0.0

    @abstractmethod
    def model_function(self, x, *args, **kwargs):
        """Depends on the module."""
        return None

    @abstractmethod
    def default_guess(self, context):
        """Default guess adequate for the model function."""

    @abstractmethod
    def random_guess(self, context):
        """
        Random guess adequate for the model function with constraints
        chosen by the user.
        """

    @abstractmethod
    def print_info(self, popt):
        """
        Print info about popt in the format adequate for the model function.
        """

    def context_setter(self, xdata, ydata):
        """
        If overwritten can return data useful for setting guess in random_gues and default_guess
        """
        return [xdata, ydata]

    def optimize(self, xdata, ydata, ind):
        """Finds the optimal parameters and corresponding errors."""

        guess = self.default_guess(self.context_setter(xdata, ydata))
        if self.guess is not None:
            guess = self.guess
        if self.auto_guess is False:
            self.popt, self.pcov = curve_fit(
                self.model_function, xdata, ydata, p0=guess
            )
        else:
            flag = True
            while flag:
                try:
                    self.abs_sum_diff = np.inf
                    self.sq_root_error = np.inf
                    guess = self.random_guess(
                        self.context_setter(xdata, ydata)
                    )

                    self.popt, self.pcov = curve_fit(
                        self.model_function, xdata, ydata, p0=guess
                    )
                    diff = self.model_function(xdata, *self.popt) - ydata
                    self.abs_sum_diff = np.sum(abs(diff))
                    self.sq_root_error = self.sq_root_error = np.sqrt(
                        np.dot(diff, diff)
                    )
                except RuntimeError:
                    log(
                        "Unable to fit with the current guess. Trying again with a new one..."
                    )
                finally:
                    if (
                        self.sq_root_error < self.precision
                        and self.abs_sum_diff < self.precision
                    ):
                        flag = False

        log("Guess:")
        log(guess)
        log("Optimization succesful")

        log("Optimized fitting parameters:")

        self.print_info(self.popt)

        log("Differences between fit and data points:")
        diff = self.model_function(xdata, *self.popt) - ydata

        log("\t Data  \t\tModel\t      Difference")
        for x, y, z in zip(
            ydata, self.model_function(xdata, *self.popt), diff
        ):
            log(
                f"\t {x+self.shift_data[ind]:6.8f} {y+self.shift_data[ind]:6.8f}  {z:e}"
            )

        log("Covariance matrix:")
        print(f"{self.pcov}")
        self.abs_sum_diff = np.sum(abs(diff))
        log(f"Absolute sum of differences:  {self.abs_sum_diff:2.3e}")
        self.sq_root_error = np.sqrt(np.dot(diff, diff))
        log(f"Square root error:            {self.sq_root_error:2.3e}")

    def show(self, xdata, ydata, ind):
        """Saves graph of the results as pdf."""
        trial_x = np.linspace(xdata[0], xdata[-1], 1000)
        model_y = (
            self.model_function(trial_x, *self.popt) + self.shift_data[ind]
        )

        pyplot.figure()
        pyplot.plot(
            xdata, ydata + self.shift_data[ind], label="Data", marker="o"
        )
        pyplot.plot(trial_x, model_y, "r-", ls="--", label=self.label_type)
        pyplot.legend()
        pyplot.show()

        base = Path(self.filename)
        name = base.stem
        outname = self.label_type + "_" + name + "_" + str(ind + 1) + ".pdf"
        save_results_to = "./minifit-results/"
        log(f"Saving results to directory: {save_results_to}")
        mf_results = str(Path.cwd()) + "/minifit-results"
        if Path(mf_results).exists() is not True:
            Path(mf_results).mkdir()
        pyplot.savefig(save_results_to + outname)

    def __call__(self):
        """Calls optimize() and then show() for chosen data."""
        warnings.filterwarnings("ignore")

        log("=")
        log("MiniFit module for curve fitting with the least squares method")
        log(f"Using: {self.type_of_fit}")

        log("=")
        log(" ")
        log(f"Reading data from input file {self.filename}")
        log(" ")
        log(f"Input file contains {self.ydata.shape[1]} different states.")
        log("~")
        for ind in range(self.ydata.shape[1]):
            log(f"Fitting curve for state {ind+1}:")
            log("-")
            try:
                self.optimize(self.xdata, self.ydata[:, ind], ind)
                self.show(self.xdata, self.ydata[:, ind], ind)
            except RuntimeError:
                log(f"Optimization failed for data set {ind+1}")

            log("Done.")
            log("~")
