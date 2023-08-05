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
"""PDE utility functions."""
from typing import Callable
import numpy as np


def create_profile_1d_random(x_array: np.ndarray,
                             y_mean: float = 15.0,
                             profile_basis_function: Callable = np.sin) -> np.ndarray:
    """Create random profile.

    Args:
        x_array: Numpy array with x coordinates
        y_mean: Mean amplitude of profile
        profile_basis_function: Basis function to use

    Returns:
        Numpy array with profile
    """
    amplitude0 = y_mean + np.random.randn()
    amplitudes = np.array([2, 2, 2, 2, 1, 0.2]) * np.random.random(6) * y_mean/15.0
    frequencies = np.array(
        [int(np.random.randint(1, 2)),
         int(np.random.randint(2, 4)),
         int(np.random.randint(4, 8)),
         int(np.random.randint(8, 16)),
         int(np.random.randint(16, 32)),
         int(np.random.randint(32, 64))])
    profile = amplitude0
    for amplitude, frequency in zip(amplitudes, frequencies):
        profile += amplitude*profile_basis_function(2*np.pi*frequency*x_array/x_array[-1])
    return profile


def create_profile_1d_sergio_orig(x_array: np.ndarray,
                                  y_mean: float = 15.0,
                                  profile_basis_function: Callable = np.sin) -> np.ndarray:
    """Create rules based profile.

    Args:
        x_array: Numpy array with x coordinates
        y_mean: Mean amplitude of profile
        profile_basis_function: Basis function to use

    Returns:
        Numpy array with profile
    """
    profile = y_mean + \
        profile_basis_function(x_array*22*np.pi/x_array[-1]) * y_mean/15.0 + \
        profile_basis_function(x_array*12*np.pi/x_array[-1]) * y_mean/15.0 + \
        profile_basis_function(x_array*8*np.pi/x_array[-1]) * y_mean/15.0
    return profile


def create_profile_1d(x_array: np.ndarray,
                      y_mean: float,
                      profile_type: str,
                      boundary_conditions: str) -> np.ndarray:
    """Create a profile in one spatial dimension.

    Args:
        x_array: Numpy array with x coordinates
        y_mean: Mean amplitude of profile
        profile_type: Type of profile that should be created
        boundary_conditions: Boundary conditions

    Returns:
        Numpy array with profile
    """
    if boundary_conditions == 'no-flux':
        profile_basis_function = np.cos
    elif boundary_conditions == 'periodic':
        profile_basis_function = np.sin
    else:
        raise ValueError(
            f"Boundary conditions must either be no-flux or periodic, "
            f"but are {boundary_conditions}")

    if profile_type == 'sergio_orig':
        profile = create_profile_1d_sergio_orig(x_array, y_mean, profile_basis_function)
    elif profile_type == 'random':
        profile = create_profile_1d_random(x_array, y_mean, profile_basis_function)
    else:
        raise NotImplementedError(f'Initial condition {profile_type} not implemented!')
    return profile
