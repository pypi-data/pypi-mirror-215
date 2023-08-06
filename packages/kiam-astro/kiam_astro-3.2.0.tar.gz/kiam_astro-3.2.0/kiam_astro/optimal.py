"""
This Python module is a part of the KIAM Astrodynamics Toolbox developed in
Keldysh Institute of Applied Mathematics (KIAM), Moscow, Russia.

The module provides routines to solve optimal control problems.

The toolbox is licensed under the MIT License.

For more information see GitHub page of the project:
https://github.com/shmaxg/KIAMToolbox
"""

import os
import pathlib
import sys

pcf = str(pathlib.Path(__file__).parent.resolve())
pwd = os.getcwd()
sys.path.extend([pcf])

import FKIAMToolbox
import numpy

def solve_r2bp_pontr_energy_irm_u_rv(x0: numpy.ndarray, x1: numpy.ndarray, tof: float, nrevs: int, atol_in: float = 1e-12, rtol_in: float = 1e-12, atol_ex: float = 1e-10, rtol_ex: float = 1e-10):
    """
    Solve standard energy-optimal control problem by Pontryagin principle in two-body problem,
    position-velocity variables in ideally-regulated engine model, using control acceleration as control variable.

    Parameters:
    -----------

    `x0` : numpy.ndarray, shape (6,)

    Initial phase state. Stucture: [x, y, z, vx, vy, vz].

    `x1` : numpy.ndarray, shape (6,)

    Target phase state. Stucture: [x, y, z, vx, vy, vz].

    `tof` : float

    The time of flight.

    `nrevs` : int

    The number of revolutions.

    `atol_in` : float

    Absolute tolerance when integrating the internal equations (equations of motion). Default is 1e-12.

    `rtol_in` : float

    Relative tolerance when integrating the internal equations (equations of motion). Default is 1e-12.

    `atol_ex` : float

    Absolute tolerance when integrating the external equations (equations of differential continuation). Default is 1e-10.

    `rtol_ex` : float

    Relative tolerance when integrating the internal equations (equations of differential continuation). Default is 1e-10.

    Returns:
    --------

    `zopt` : numpy.ndarray, shape (6,)

    The optimized vector of initial conjugate variables. Structure: [lamx, lamy, lamz, lamvx, lamvy, lamvz].
    The optimization is done by using a Newton method with adaptive step.

    `zend` : numpy.ndarray, shape (6,)

    The non-optimized vector of initial conjugate variables obtained by differential correction procedure. Structure: [lamx, lamy, lamz, lamvx, lamvy, lamvz].

    `res` : numpy.ndarray, shape (6,)

    The residue between the target position and velocity and obtained by using `zopt` conjugate variables.

    `jac` : numpy.ndarray, shape (6, 6)

    The Jacobian of the residue function at `zopt`.

    Examples:
    ---------
    ```
    x0 = numpy.array([1.0, 0.0, 0.0, 0.0, 1.0, 0.0])

    x1 = numpy.array([1.5, 0.0, 0.0, 0.0, sqrt(1.5), 0.0])

    tof = 3 * pi

    nrevs = 1

    zopt, zend, res, jac = solve_r2bp_pontr_energy_irm_u_rv(x0, x1, tof, nrevs)
    ```
    """
    FKIAMToolbox.optimalcontrol.atol_in = atol_in
    FKIAMToolbox.optimalcontrol.rtol_in = rtol_in
    FKIAMToolbox.optimalcontrol.atol_ex = atol_ex
    FKIAMToolbox.optimalcontrol.rtol_ex = rtol_ex
    zopt, zend, res, jac = FKIAMToolbox.optimalcontrol.solve_energy_optimal_problem(x0, x1, tof, nrevs)
    return zopt, zend, res, jac

def propagate_r2bp_pontr_energy_irm_u_rv(tspan: numpy.ndarray, y0: numpy.ndarray, atol: float = 1e-12, rtol: float = 1e-12, mu: float = 1.0, mu0: float = 1.0):
    """
    Propagate extended by conjugate variables equations of motion.
    Two-body problem, energy-optimal control, ideally-regulated engine model, thrust acceleration as control function, position and velocity as variables.

    Parameters:
    -----------

    `tspan` : numpy.ndarray, shape (n,)

    The times at which the solution should be obtained.

    `y0` : numpy.ndarray, shape (12,), (156,), (168,)

    The initial state.

    Structure options:

    1. [rvect, vvect, lamr, lamv]

    2. [rvect, vvect, lamr, lamv, stm]

    3. [rvect, vvect, lamr, lamv, stm, dxdtau]

    where stm is the state transition matrix and dxdtau is derivative of [rvect, vvect, lamr, lamv] with respect to continuation parameter tau (gravitational parameter mu = mu0 + (1 - mu0) * tau).

    `atol` : float

    Absolute tolerance when integrating the equations. Default is 1e-12.

    `rtol` : float

    Relative tolerance when integrating the equations. Default is 1e-12.

    `mu` : float

    Gravitational parameter of the central body. Default is 1.0.

    `mu0` : float

    Initial value of the gravitational parameter in differential continuation process.
    This parameter is required only if dxdtau is among the dependent variables (len(y0) == 168).
    Otherwise the value is ignored.

    Returns:
    --------

    `T` : numpy.ndarray, shape (n,)

    The times at which the solution is obtained. Equals to tspan.

    `Y` : numpy.ndarray, shape (m, n)

    The integrated solutions. Each column correspond to a vector y at the correspondent time t in T.

    Examples:
    ---------
    ```
    x0 = numpy.array([1.0, 0.0, 0.0, 0.0, 1.0, 0.0])

    z0 = numpy.array([1.0, 0.0, 0.0, 0.0, 1.0, 0.0])

    tof = 3 * pi

    T, Y = propagate_r2bp_pontr_energy_irm_u_rv(numpy.linspace(0.0, tof, 10000), numpy.concatenate((x0, z0)))
    ```
    """

    neq = len(y0)

    if neq == 12:
        stmreq, gradmureq = False, False
    elif neq == 156:
        stmreq = True
        gradmureq = False
    elif neq == 168:
        stmreq = True
        gradmureq = False
    else:
        raise Exception('Wrong number of dependent variables.')

    T, Y = FKIAMToolbox.propagationmodule.propagate_r2bp_pontr_eopt_irm_u_rv(tspan, y0, neq, atol, rtol, mu, mu0, stmreq, gradmureq)

    return T, Y
