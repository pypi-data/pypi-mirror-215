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
"""Auxiliary functions."""

import numpy as np
from scipy.sparse import csr_matrix


# pylint: disable=too-many-statements
def create_stencil_2d(num_grid_point_x: int,
                      num_grid_points_y: int,
                      ninepoint: bool = True) -> csr_matrix:
    """Create 2nd order finite difference stencil in two dimensions.

    Args:
        num_grid_points_x: integer with the number of grid points along
                              the x axis
        num_grid_points_y: integer with the number of grid points along
                              the y axis
        ninepoint: if to use 9pt stencil instead of 5pt stencil

    Returns:
        Finite difference stencil as csr matrix
    """
    stencil_data = np.empty(5 * num_grid_point_x * num_grid_points_y)
    stencil_data[0:num_grid_point_x * num_grid_points_y].fill(-4.0)
    idxs = np.empty(num_grid_point_x * num_grid_points_y)
    idxs[0:num_grid_point_x * num_grid_points_y] = np.arange(
        0, num_grid_point_x * num_grid_points_y
    )
    idxscol = np.empty(num_grid_point_x * num_grid_points_y)
    idxscol[0:num_grid_point_x * num_grid_points_y] = np.arange(
        0, num_grid_point_x * num_grid_points_y
    )
    stencil_data[
        num_grid_point_x * num_grid_points_y: 5 * num_grid_point_x * num_grid_points_y
    ].fill(1.0)
    idxscolright = np.empty(num_grid_point_x * num_grid_points_y)
    idxscolright = np.arange(0, num_grid_point_x * num_grid_points_y) + 1.0
    idxscolright[
        np.where(
            idxscolright / num_grid_points_y
            - np.trunc(idxscolright / num_grid_points_y)
            == 0
        )
    ] = (
        idxscolright[
            np.where(
                idxscolright / num_grid_points_y
                - np.trunc(idxscolright / num_grid_points_y)
                == 0
            )
        ]
        - num_grid_points_y
    )
    idxscolright[np.where(idxscolright == -num_grid_points_y)] = 0
    idxscolleft = np.empty(num_grid_point_x * num_grid_points_y)
    idxscolleft = np.arange(0, num_grid_point_x * num_grid_points_y) - 1
    idxscolleft[
        np.where(
            (idxscolleft + 1.0) / num_grid_points_y
            - np.trunc((idxscolleft + 1.0) / num_grid_points_y)
            == 0
        )
    ] = (
        idxscolleft[
            np.where(
                (idxscolleft + 1.0) / num_grid_points_y
                - np.trunc((idxscolleft + 1.0) / num_grid_points_y)
                == 0
            )
        ]
        + num_grid_points_y
    )
    idxscoltop = np.empty(num_grid_point_x * num_grid_points_y)
    idxscoltop = np.arange(0, num_grid_point_x * num_grid_points_y) - num_grid_points_y
    idxscoltop[np.where(idxscoltop < 0)] = (
        num_grid_point_x * num_grid_points_y + idxscoltop[np.where(idxscoltop < 0)]
    )
    idxscolbottom = np.empty(num_grid_point_x * num_grid_points_y)
    idxscolbottom = (
        np.arange(0, num_grid_point_x * num_grid_points_y) + num_grid_points_y
    )
    idxscolbottom[np.where(idxscolbottom >= num_grid_point_x * num_grid_points_y)] = (
        idxscolbottom[np.where(idxscolbottom >= num_grid_point_x * num_grid_points_y)]
        - num_grid_point_x * num_grid_points_y
    )
    idxtmp = idxs
    for _ in range(0, 4):
        idxs = np.append(idxs, idxtmp)
    idxscol = np.append(idxscol, idxscolright)
    idxscol = np.append(idxscol, idxscolleft)
    idxscol = np.append(idxscol, idxscoltop)
    idxscol = np.append(idxscol, idxscolbottom)
    if ninepoint:
        stencil_data = np.empty(9 * num_grid_point_x * num_grid_points_y)
        stencil_data[0: num_grid_point_x * num_grid_points_y].fill(-20.0)
        stencil_data[
            num_grid_point_x
            * num_grid_points_y: 5
            * num_grid_point_x
            * num_grid_points_y
        ].fill(4.0)
        stencil_data[
            5
            * num_grid_point_x
            * num_grid_points_y: 9
            * num_grid_point_x
            * num_grid_points_y
        ].fill(1.0)
        for _ in range(0, 4):
            idxs = np.append(idxs, idxtmp)
        idxscol9 = np.empty(num_grid_point_x * num_grid_points_y)
        idxscol9 = (
            np.arange(0, num_grid_point_x * num_grid_points_y) - num_grid_points_y - 1
        )  # left top
        idxscol9[np.where(idxscol9 < 0)] = (
            num_grid_point_x * num_grid_points_y + idxscol9[np.where(idxscol9 < 0)]
        )
        idxscol9[
            np.where(
                (idxscol9 + float(num_grid_points_y) + 1.0) / num_grid_points_y
                - np.trunc(
                    (idxscol9 + float(num_grid_points_y) + 1.0) / num_grid_points_y
                )
                == 0
            )
        ] = (
            idxscol9[
                np.where(
                    (idxscol9 + float(num_grid_points_y) + 1.0) / num_grid_points_y
                    - np.trunc(
                        (idxscol9 + float(num_grid_points_y) + 1.0) / num_grid_points_y
                    )
                    == 0
                )
            ]
            + num_grid_points_y
        )
        idxscol9[np.where(idxscol9 >= num_grid_point_x * num_grid_points_y)] = (
            idxscol9[np.where(idxscol9 >= num_grid_point_x * num_grid_points_y)]
            - num_grid_point_x * num_grid_points_y
        )
        idxscol9[0] = num_grid_point_x * num_grid_points_y - 1
        idxscol = np.append(idxscol, idxscol9)
        idxscol9 = (
            np.arange(0, num_grid_point_x * num_grid_points_y) - num_grid_points_y + 1
        )  # right top
        idxscol9[-1] = num_grid_point_x * num_grid_points_y - 2 * num_grid_points_y
        idxscol9[np.where(idxscol9 < 0)] = (
            num_grid_point_x * num_grid_points_y + idxscol9[np.where(idxscol9 < 0)]
        )
        idxscol9[
            np.where(
                (idxscol9 + float(num_grid_points_y)) / num_grid_points_y
                - np.trunc((idxscol9 + float(num_grid_points_y)) / num_grid_points_y)
                == 0
            )
        ] = (
            idxscol9[
                np.where(
                    (idxscol9 + float(num_grid_points_y)) / num_grid_points_y
                    - np.trunc(
                        (idxscol9 + float(num_grid_points_y)) / num_grid_points_y
                    )
                    == 0
                )
            ]
            - num_grid_points_y
        )
        idxscol9[np.where(idxscol9 < 0)] = (
            idxscol9[np.where(idxscol9 < 0)] + num_grid_point_x * num_grid_points_y
        )
        idxscol9[-1] = num_grid_point_x * num_grid_points_y - 2 * num_grid_points_y
        idxscol = np.append(idxscol, idxscol9)
        idxscol9 = (
            np.arange(0, num_grid_point_x * num_grid_points_y) + num_grid_points_y - 1
        )  # left bottom
        idxscol9[np.where(idxscol9 >= num_grid_point_x * num_grid_points_y)] = (
            idxscol9[np.where(idxscol9 >= num_grid_point_x * num_grid_points_y)]
            - num_grid_point_x * num_grid_points_y
        )
        idxscol9[
            np.where(
                (idxscol9 - float(num_grid_points_y) + 1.0) / num_grid_points_y
                - np.trunc(
                    (idxscol9 - float(num_grid_points_y) + 1.0) / num_grid_points_y
                )
                == 0
            )
        ] = (
            idxscol9[
                np.where(
                    (idxscol9 - float(num_grid_points_y) + 1.0) / num_grid_points_y
                    - np.trunc(
                        (idxscol9 - float(num_grid_points_y) + 1.0) / num_grid_points_y
                    )
                    == 0
                )
            ]
            + num_grid_points_y
        )
        idxscol9[np.where(idxscol9 >= num_grid_point_x * num_grid_points_y)] = (
            idxscol9[np.where(idxscol9 >= num_grid_point_x * num_grid_points_y)]
            - num_grid_point_x * num_grid_points_y
        )
        idxscol9[0] = 2 * num_grid_points_y - 1
        idxscol = np.append(idxscol, idxscol9)
        idxscol9 = (
            np.arange(0, num_grid_point_x * num_grid_points_y) + num_grid_points_y + 1
        )  # right bottom
        idxscol9[np.where(idxscol9 >= num_grid_point_x * num_grid_points_y)] = (
            idxscol9[np.where(idxscol9 >= num_grid_point_x * num_grid_points_y)]
            - num_grid_point_x * num_grid_points_y
        )
        idxscol9[
            np.where(
                (idxscol9 - float(num_grid_points_y)) / num_grid_points_y
                - np.trunc((idxscol9 - float(num_grid_points_y)) / num_grid_points_y)
                == 0
            )
        ] = (
            idxscol9[
                np.where(
                    (idxscol9 - float(num_grid_points_y)) / num_grid_points_y
                    - np.trunc(
                        (idxscol9 - float(num_grid_points_y)) / num_grid_points_y
                    )
                    == 0
                )
            ]
            - num_grid_points_y
        )
        idxscol9[np.where(idxscol9 < 0)] = (
            idxscol9[np.where(idxscol9 < 0)] + num_grid_point_x * num_grid_points_y
        )
        idxscol9[-1] = 0
        idxscol = np.append(idxscol, idxscol9)
    stencil = csr_matrix(
        (stencil_data, (idxs, idxscol)),
        shape=(
            num_grid_point_x * num_grid_points_y,
            num_grid_point_x * num_grid_points_y,
        ),
        dtype=float,
    )
    if ninepoint:
        stencil = stencil / 6.0
    return stencil
