"""
Module containing tests for GaussFit class.
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
from .. import gauss


def test_GaussFit():
    """Simple general test"""
    gauss_1 = gauss.GaussFit("gauss_data.txt")
    gauss_1()
    assert gauss_1.sq_root_error <= 10
    file_path = Path.cwd() / "minifit-results" / "gauss_fit_gauss_data_1.pdf"
    assert file_path.exists(), f"File {file_path} does not exist"


def test_popt_GaussFit():
    gauss_1 = gauss.GaussFit("gauss_data.txt")
    gauss_1()
    assert check_list_within_percentage(
        gauss_1.popt, (4.97587424, 20.00233527, 2.84768795), 1
    )
    assert (
        check_list_within_percentage(
            gauss_1.popt, (4.97587424 * 1.1, 20.00233527, 2.84768795), 1
        )
        is not True
    )
    # first element differes by 10%, arrays should not be considered equal if precison is set to 1%


def test_GaussFit_model_function():
    gauss_1 = gauss.GaussFit("exp.dat")
    with pytest.raises(TypeError):
        gauss_1.model_function(-1)
    with pytest.raises(TypeError):
        gauss_1.model_function(1, 2, 3, 4, 5)
    assert gauss_1.model_function(22, 44, 66, 22) == 0.8058881111043039
