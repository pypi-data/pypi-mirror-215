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
"""Lorenz system."""
from typing import Any

import numpy as np
from pydszoo import integrate_ode

parameters_chaos = {'sigma': 10.0, 'rho': 28.0, 'beta': 8.0/3.0}


def dudt(time: float,  # pylint: disable=unused-argument
         values: np.ndarray,
         parameters: dict) -> np.ndarray:
    """Return temporal evolution of the Lorenz system.

    Args:
        time: Time stamp (not used)
        values: Numpy array with variables
        parameters: System parameters

    Returns:
        Numpy array with time derivatives
    """
    xprime = parameters['sigma'] * (values[1] - values[0])
    yprime = -values[0] * values[2] + parameters['rho'] * values[0] - values[1]
    zprime = values[0] * values[1] - parameters['beta'] * values[2]
    return np.array([xprime, yprime, zprime])


def create_initial_condition() -> np.ndarray:
    """Create initial conditions for Lorenz system.

    Returns:
        Numpy array with values [u, v, w]
    """
    return np.array((10.0+np.random.randn(),
                     1.0+np.random.randn(),
                     np.random.randn()))


def integrate(initial_condition: np.ndarray = create_initial_condition(),
              time_array: np.ndarray = np.linspace(0, 50, 10000),
              parameters: Any = None) -> np.ndarray:
    """Integrate Lorenz system.

    Args:
        initial_condition: numpy array with initial values
        time_array: numpy array with time steps at which to return data
        parameters: numpy array with system parameters

    Returns:
        Numpy array with solution
    """
    if not parameters:
        parameters = parameters_chaos
    return integrate_ode(dudt, initial_condition, time_array, parameters)
