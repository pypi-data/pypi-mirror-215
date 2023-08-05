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
"""Integration utility functions."""
from typing import Callable
import numpy as np
from scipy.integrate import solve_ivp


def integrate_ode(dudt: Callable[[float, np.ndarray, np.ndarray], np.ndarray],
                  initial_condition: np.ndarray,
                  time_array: np.ndarray,
                  parameters: dict) -> np.ndarray:
    """Integrate system of ordinary differential equations with specified initial condition.

    Args:
        dudt: Callable that provides time derivatives of variables
        initial_condition: numpy array with initial values
        time_array: numpy array with time steps at which to return data
        parameters: numpy array with system parameters

    Returns:
        Numpy array with solution
    """
    sol = solve_ivp(dudt,
                    [0, time_array[-1]],
                    initial_condition,
                    t_eval=time_array,
                    args=[parameters],
                    rtol=1e-7,
                    atol=1e-10)
    if not sol.success:
        raise Exception("Integration failed!")
    return sol.y.T


def integrate_pde(dudt: Callable[[float, np.ndarray, np.ndarray], np.ndarray],
                  initial_condition: np.ndarray,
                  time_array: np.ndarray,
                  parameters: dict) -> np.ndarray:
    """Integrate system of partial differential equations with specified initial condition.

    Args:
        dudt: Callable that provides time derivatives of variables
        initial_condition: numpy array with initial values
        time_array: numpy array with time steps at which to return data
        parameters: numpy array with system parameters

    Returns:
        Numpy array with solution
    """
    initial_condition = np.reshape(
        initial_condition, (np.prod(parameters["num_grid_points"])))
    solution = integrate_ode(dudt, initial_condition, time_array, parameters)
    return np.reshape(solution, (len(time_array), *parameters["num_grid_points"]))
