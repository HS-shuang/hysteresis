# -*- coding: utf-8 -*-
# @Time: 2021/11/19 19:27
# @Author: HS

import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
from scipy.optimize import least_squares


def energy(theta, rido, psi):
    return -rido * np.cos(psi - theta) + np.sin(theta) ** 2


def d_energy(theta, rido, psi):
    return -rido * np.sin(psi - theta) + np.sin(2 * theta)


def dd_energy(theta, rido, psi):
    return rido * np.cos(psi - theta) + 2 * np.cos(2 * theta)


def rou(psi):
    return np.sin(psi) ** 2


def loss(t0, rido, psi, t_bounds):
    if dd_energy(t0, rido, psi=psi) < 0:
        t0 -= 1
        if t0 < t_bounds[0] or t0 > t_bounds[1]:
            t0 -= t_bounds[0]
            t0 %= t_bounds[1]
    return d_energy(t0, rido, psi=psi)


def get_t0(rido, psi, x0=0, t_bounds=[-np.inf, np.inf]):
    t0 = least_squares(loss, x0=x0, bounds=t_bounds, args=(rido, psi, t_bounds), max_nfev=200).x
    return t0, energy(t0, rido, psi), d_energy(t0, rido, psi), dd_energy(t0, rido, psi)

def m(psi, t0):
     return np.cos(psi - t0)

# def theta_f1(psi, H):
#     y = energy(x1, H, psi)
#     return x1[y == min(y)][0]
#
#
# def theta_f2(psi, H):
#     y = energy(x2, H, psi)
#     return x2[y == min(y)][0]
#
#
#
#
#
# def m2(psi, H):
#     return np.cos(psi - theta_f2(psi, H)) * rou(psi) * np.sin(psi)
#
#
# def F1(psi, H):
#     return integrate.quad(m1, 0, np.pi, args=(psi, H))[0]
#
#
# def F2(psi, H):
#     return integrate.quad(m2, 0, np.pi, args=(psi, H))[0]
#
