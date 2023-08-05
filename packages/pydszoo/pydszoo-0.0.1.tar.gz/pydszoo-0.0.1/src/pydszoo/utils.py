# Copyright © 2022 Felix P. Kemeth.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the “Software”), to deal in the Software without
# restriction, including without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# =============================================================================================
"""Utility functions."""
import numpy as np


def enforce_boundaries(values: np.ndarray,
                       boundary_conditions: list,
                       num_grid_points: list) -> np.ndarray:
    """Enforce no flux boundary conditions on input array.

    Args:
        values: Numpy array with snapshot data
        boundary_conditions: List of boundary conditions per dimension
        num_grid_points: List of numbers of spatial grid points

    Returns:
        values with enforced boundary conditions
    """
    if len(boundary_conditions) == 1:
        return enforce_boundaries_1d(values, boundary_conditions, num_grid_points)
    if len(boundary_conditions) == 2:
        return enforce_boundaries_2d(values, boundary_conditions, num_grid_points)
    raise NotImplementedError('Boundary condition not implemented.')


def enforce_boundaries_1d(values: np.ndarray,
                          boundary_conditions: list,
                          num_grid_points: list) -> np.ndarray:
    """Enforce boundary conditions on two dimensions.

    Args:
        values: Numpy array with snapshot data
        boundary_conditions: List of boundary conditions per dimension
        num_grid_points: List of numbers of spatial grid points

    Returns:
        values with enforced boundary conditions
    """
    if boundary_conditions[0] == 'no-flux':
        values = np.pad(values, (int(num_grid_points[0]/4), int(num_grid_points[0]/4)), 'reflect')
        return values
    if boundary_conditions[0] == 'periodic':
        values = np.pad(values, (int(num_grid_points[0]/4), int(num_grid_points[0]/4)), 'wrap')
        return values
    raise NotImplementedError('Boundary condition not implemented.')


def enforce_boundaries_2d(values: np.ndarray,
                          boundary_conditions: list,
                          num_grid_points: list) -> np.ndarray:
    """Enforce boundary conditions on two dimensions.

    Args:
        values: Numpy array with snapshot data
        boundary_conditions: List of boundary conditions per dimension
        num_grid_points: List of numbers of spatial grid points

    Returns:
        values with enforced boundary conditions
    """
    if all(condition == 'no-flux' for condition in boundary_conditions):
        return enforce_no_flux_boundaries_2d(values, *num_grid_points)
    if ((boundary_conditions[0] == 'periodic') and (boundary_conditions[1] == 'no-flux')):
        return enforce_no_flux_boundaries_x(values, num_grid_points[0])
    raise NotImplementedError('Boundary condition not implemented.')


def enforce_no_flux_boundaries_2d(values: np.ndarray,
                                  num_grid_points_x: int,
                                  num_grid_points_y: int) -> np.ndarray:
    """Enforce no flux boundary conditions on two dimensions.

    Args:
        values: Numpy array with snapshot data
        num_grid_points_y: Numbers of spatial grid points in the x direction
        num_grid_points_y: Numbers of spatial grid points in the y direction

    Returns:
        values with enforced boundary conditions
    """
    # x direction
    values[0:num_grid_points_x] = values[num_grid_points_x:2*num_grid_points_x]
    values[-num_grid_points_x:] = values[-2 * num_grid_points_x:-num_grid_points_x]
    # y direction
    values[::num_grid_points_y] = values[1::num_grid_points_y]
    values[num_grid_points_y - 1::num_grid_points_y] = \
        values[num_grid_points_y - 2::num_grid_points_y]
    return values


def enforce_no_flux_boundaries_x(values: np.ndarray,
                                 num_grid_points_x: int) -> np.ndarray:
    """Enforce no flux boundary conditions on x dimension.

    Args:
        values: Numpy array with snapshot data
        num_grid_points_y: Numbers of spatial grid points in the x direction

    Returns:
        values with enforced boundary conditions
    """
    values[0:num_grid_points_x] = values[num_grid_points_x:2 * num_grid_points_x]
    values[-num_grid_points_x:] = values[-2 * num_grid_points_x:-num_grid_points_x]
    return values
