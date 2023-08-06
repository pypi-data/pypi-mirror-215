"""
Module containing functions shared by tests
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

# pylint: skip-file


def check_list_within_percentage(list1, list2, percentage):
    assert len(list1) == len(list2)

    for value1, value2 in zip(list1, list2):
        difference = abs(value1 - value2)
        max_difference = abs(percentage * value1 / 100)
        if difference > max_difference:
            return False

    return True
