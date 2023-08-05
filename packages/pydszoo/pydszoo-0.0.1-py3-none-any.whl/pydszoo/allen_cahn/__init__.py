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
"""Allen-Cahn system."""
from typing import Any
import numpy as np

from pydszoo import integrate_pde
from pydszoo.fun import create_stencil_2d
from pydszoo.utils import enforce_boundaries
from pydszoo.pde_utils import create_profile_1d


def get_parameters_small_d() -> dict:
    """Get exemplary parameters for Allen-Cahn system.

    Returns:
       Dictionary with parameters for two-dimensional system.
    """
    parameters = {
        'a': -0.1,
        'D': 0.1,
        'num_grid_points': [512, 512],
        'spatial_dimensions': [90, 90],
        'boundary_conditions': ['periodic', 'no-flux'],
        'stencil': create_stencil_2d(512, 512)
    }
    return parameters


def dudt(time: float,  # pylint: disable=unused-argument
         values: np.ndarray,
         parameters: dict) -> np.ndarray:
    """Return temporal evolution of the Allen-Cahn system.

    Args:
        time: Time stamp (not used)
        values: Numpy array with variables
        parameters: System parameters

    Returns:
        Numpy array with time derivatives
    """
    values = enforce_boundaries(
        values, parameters["boundary_conditions"], parameters["num_grid_points"])
    dx_i = [parameters["spatial_dimensions"][i]/parameters["num_grid_points"][i]
            for i in range(len(parameters["num_grid_points"]))]
    assert len(set(dx_i)) == 1

    return parameters['D']*parameters['stencil'].dot(values) / (dx_i[0]**2) - \
        (values-parameters['a']) * (values**2-1)


def create_initial_condition(parameters: dict, initial_condition: str) -> np.ndarray:
    """Create initial conditions for Allen-Cahn system.

    Args:
        parameters: Dictionary with parameter values
        initial_condition: String specifying the desired initial conditions

    Returns:
        Numpy array with values [u, v]
    """
    assert len(parameters["spatial_dimensions"]) == 2
    assert len(parameters["boundary_conditions"]) == 2
    assert len(parameters["num_grid_points"]) == 2
    assert parameters["boundary_conditions"][1] == 'no-flux'

    length_x, length_y = parameters["spatial_dimensions"]
    num_grid_points_x, _ = parameters["num_grid_points"]
    x_array = np.linspace(0, length_x, num_grid_points_x, endpoint=False)
    # y_array = np.linspace(0, length_y, num_grid_points_y, endpoint=False)

    profile = create_profile_1d(x_array, length_y/6.0, initial_condition,
                                parameters["boundary_conditions"][0])

    delta_y = length_y/parameters["num_grid_points"][1]
    phi = np.zeros(parameters["num_grid_points"])

    for index_x in range(parameters["num_grid_points"][0]):
        for index_y in range(parameters["num_grid_points"][1]):
            residual = np.sqrt((delta_y*(index_y-profile[index_x]))**2)
            phi[index_x][index_y] = \
                np.tanh((profile[index_x]-residual)/(np.sqrt(2.0*parameters['D'])))
    return phi


def integrate(initial_condition: Any = None,
              time_array: np.ndarray = np.linspace(0, 20, 500),
              parameters: Any = None) -> np.ndarray:
    """Integrate Allen-Cahn system.

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
        initial_condition = create_initial_condition(parameters, 'random')
    return integrate_pde(dudt, initial_condition, time_array, parameters)
