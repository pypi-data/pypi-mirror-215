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
"""Brusselator system."""
from typing import Any
import numpy as np
from pydszoo import integrate_ode

parameters_periodic = {'a': 1.0, 'b': 2.1}


def dudt(time: float,  # pylint: disable=unused-argument
         values: np.ndarray,
         parameters: dict) -> np.ndarray:
    """Return temporal evolution of the Brusselator.

    Args:
        time: Time stamp (not used)
        values: Numpy array with variables
        parameters: System parameters

    Returns:
        Numpy array with time derivatives
    """
    dx_dt = parameters['a'] + values[0] ** 2 * values[1] - (parameters['b'] + 1) * values[0]
    dy_dt = parameters['b'] * values[0] - values[0] ** 2 * values[1]
    return np.array((dx_dt, dy_dt))


def create_initial_condition() -> np.ndarray:
    """Create initial conditions for Brusselator system.

    Returns:
        Numpy array with values [u, v]
    """
    return np.array((2.0 * np.random.random(), 3.0 * np.random.random()))


def integrate(initial_condition: np.ndarray = create_initial_condition(),
              time_array: np.ndarray = np.linspace(0, 20, 500),
              parameters: Any = None) -> np.ndarray:
    """Integrate Brusselator system.

    Args:
        initial_condition: numpy array with initial values
        time_array: numpy array with time steps at which to return data
        parameters: numpy array with system parameters

    Returns:
        Numpy array with solution
    """
    if not parameters:
        parameters = parameters_periodic
    return integrate_ode(dudt, initial_condition, time_array, parameters)
