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
"""Kardar–Parisi–Zhang system."""
from typing import Any
import numpy as np
from findiff import FinDiff

from pydszoo import integrate_pde, pde_utils
from pydszoo.utils import enforce_boundaries


def get_parameters_small_d() -> dict:
    """Get exemplary parameters for Allen-Cahn system.

    Returns:
       Dictionary with parameters for two-dimensional system.
    """
    num_grid_points = 512
    spatial_dimensions = 90
    parameters = {
        'a': -0.1,
        'D': 0.1,
        'num_grid_points': [num_grid_points],
        'spatial_dimensions': [spatial_dimensions],
        'boundary_conditions': ['periodic'],
        'd_dx': FinDiff(0, spatial_dimensions/num_grid_points, 1),
        'dd_dxx': FinDiff(0, spatial_dimensions/num_grid_points, 2)
    }
    return parameters


def dudt(time: float,  # pylint: disable=unused-argument
         values: np.ndarray,
         parameters: np.ndarray) -> np.ndarray:
    """Return temporal evolution of the KPZ equation.

    Args:
        time: Time stamp (not used)
        values: Numpy array with variables
        parameters: System parameters

    Returns:
        Numpy array with time derivatives
    """
    values = enforce_boundaries(
        values, parameters["boundary_conditions"], parameters["num_grid_points"])
    flow = parameters["D"]*parameters["dd_dxx"](values) - \
        np.sqrt(2*parameters["D"])*parameters["a"]*(1+(1.0/2.0)*parameters["d_dx"](values)**2)
    return flow[int(parameters["num_grid_points"][0]/4):-int(parameters["num_grid_points"][0]/4)]


def create_initial_condition(parameters: dict) -> np.ndarray:
    """Create initial conditions for KPZ system.

    Args:
        parameters: Dictionary with parameters.

    Returns:
        Numpy array with spatial profile
    """
    length_x = parameters["spatial_dimensions"][0]
    num_grid_points_x = parameters["num_grid_points"][0]
    x_array = np.linspace(0, length_x, num_grid_points_x, endpoint=False)
    return pde_utils.create_profile_1d(x_array, 15.0, 'random',
                                       parameters["boundary_conditions"][0])


def integrate(initial_condition: Any = None,
              time_array: np.ndarray = np.linspace(0, 20, 500),
              parameters: Any = None) -> np.ndarray:
    """Integrate KPZ system.

    Args:
        initial_condition: numpy array with initial values
        time_array: numpy array with time steps at which to return data
        parameters: numpy array with system parameters

    Returns:
        Numpy array with solution
    """
    if not parameters:
        parameters = get_parameters_small_d()
    if not initial_condition:
        initial_condition = create_initial_condition(parameters)

    return integrate_pde(dudt, initial_condition, time_array, parameters)
