"""
Module containing tests for ExponentialFit class.
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
from .. import exp


def test_ExponentialFit():
    """Simple general test"""
    exp_1 = exp.ExponentialFit("exp.dat")
    exp_1()
    assert exp_1.sq_root_error <= 20
    file_path = Path.cwd() / "minifit-results" / "exp_fit_exp_1.pdf"
    assert file_path.exists(), f"File {file_path} does not exist"


def test_popt_ExponentialFit():
    exp_1 = exp.ExponentialFit("exp.dat")
    exp_1()
    assert check_list_within_percentage(
        exp_1.popt, (2.70136445, 0.48028958, 0.79216127), 1
    )
    assert (
        check_list_within_percentage(
            exp_1.popt, (2.70136445 * 1.1, 0.48028958, 0.79216127), 1
        )
        is not True
    )
    # first element differes by 10%, arrays should not be considered equal if precison is set to 1%


def test_ExponentialFit_model_function():
    exp_1 = exp.ExponentialFit("exp.dat")
    with pytest.raises(TypeError):
        exp_1.model_function(-1)
    with pytest.raises(TypeError):
        exp_1.model_function(1, 2, 3, 4, 5)
    assert exp_1.model_function(3, 4, 2, -1000) == 613.7151739709404
