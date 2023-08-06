"""
Module containing tests for MorseFit class.
"""

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

# pylint: skip-file

import pytest
from .common import check_list_within_percentage
from pathlib import Path
from .. import user_defined


def user_poly(x, *args, **kwargs):
    a, b, c, d, e, f, g, h = args
    return (
        a * x**7
        + b * x**6
        + c * x**5
        + d * x**4
        + e * x**3
        + f * x**2
        + g * x
        + h
    )


a_range = (
    (-2.67143698 - 50, -2.67143698 + 50),
    (29.75271303 - 50, 29.75271303 + 50),
    (-141.51011815 - 50, -141.51011815 + 50),
    (373.56237563 - 50, 373.56237563 + 50),
    (-593.05923681 - 50, -593.05923681 + 50),
    (568.07666599 - 50, 568.07666599 + 50),
    (-304.20455678 - 50, -304.20455678 + 50),
    (-39.28501939 - 50, -39.28501939 + 50),
)


def test_UserFit():
    """Simple general test"""
    user_1 = user_defined.UserFit(
        "example.dat",
        model=user_poly,
        num_param=8,
        auto_guess=True,
        precision=0.01,
        auto_range=a_range,
    )
    user_1()
    assert user_1.sq_root_error <= 1
    file_path = Path.cwd() / "minifit-results" / "user_fit_example_1.pdf"
    assert file_path.exists(), f"File {file_path} does not exist"


def test_popt_UserFit():
    user_1 = user_defined.UserFit(
        "example.dat",
        model=user_poly,
        num_param=8,
        auto_guess=True,
        precision=0.01,
        auto_range=a_range,
    )
    user_1()
    # auto_guess=True, popt will be slightly different each time while staying in chosen precison range
    assert check_list_within_percentage(
        user_1.popt,
        (
            -2.74664485,
            30.45219915,
            -144.19263652,
            379.07860216,
            -599.65868604,
            572.65983488,
            -305.92227695,
            -39.01681137,
        ),
        1,
    )
    assert (
        check_list_within_percentage(
            user_1.popt,
            (
                -2.67143698 * 1.10,
                29.75271303,
                -141.51011815,
                373.56237563,
                -593.05923681,
                568.07666599,
                -304.20455678,
                -39.28501939,
            ),
            1,
        )
        is not True
    )
    # first element differes by 10%, arrays should not be considered equal if precison is set to 1%
