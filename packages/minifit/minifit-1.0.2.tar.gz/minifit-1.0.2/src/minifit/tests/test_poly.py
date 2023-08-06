"""
Module containing tests for PolyFit class.
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
from .. import poly


def test_PolyFit():
    """Simple general test"""
    poly_1 = poly.PolyFit("example.dat", order=7)
    poly_1()
    assert poly_1.sq_root_error <= 6
    file_path = Path.cwd() / "minifit-results" / "polynomial_fit_example_3.pdf"
    assert file_path.exists(), f"File {file_path} does not exist"


def test_popt_PolyFit():
    poly_1 = poly.PolyFit("example.dat", order=7)
    poly_1()
    assert check_list_within_percentage(
        poly_1.popt,
        (
            -39.0169376799999981,
            -305.9215619700000275,
            572.6581489500000544,
            -599.6565376300000025,
            379.0770024099999773,
            -144.1919395300000133,
            30.4520343900000015,
            -2.7466285300000002,
        ),
        1,
    )
    assert (
        check_list_within_percentage(
            poly_1.popt,
            (
                -39.01693768 * 1.1,
                -305.92156197,
                572.65814895,
                -599.65653763,
                379.07700241,
                -144.19193953,
                30.45203439,
                -2.74662853,
            ),
            1,
        )
        is not True
    )
    # first element differes by 10%, arrays should not be considered equal if precison is set to 1%


def test_PolyFit_model_function():
    """Tests for model function"""
    poly_1 = poly.PolyFit("exp.dat", order=7)
    with pytest.raises(TypeError):
        poly_1.model_function(-1)
    with pytest.raises(TypeError):
        poly_1.model_function(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    assert (
        poly_1.model_function(-5, -1, -2, -3, 4, 5, 0.003, 0.03, 25000)
        == -1953121981.625
    )
