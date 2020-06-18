#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scipy.interpolate import griddata

import matplotlib.pyplot as plt
import matplotlib
import istra2py
import os
import numpy as np

font = {"family": "monospace", "weight": "bold", "size": 22}
matplotlib.rc("font", **font)

np.set_printoptions(
    linewidth=160,
    precision=4,
    # suppress=False,
)

r = istra2py.ExportReader(os.path.join("data", "export"))
# r._list_available_keys()
r.read()

dir_output = os.path.join(os.path.dirname(__file__), "plots")
os.makedirs(dir_output, exist_ok=True)

# Select frame
index_frame = 1
xx = r.x[0, ...]
val = r.x[index_frame, ...]

# Identify positions of DIC-grip-points where identification failed, i.e. where coordinates are near zero
mask = np.linalg.norm(xx, axis=-1) > 1e-12

# Select data losing grid
x_flat = xx[mask, 0]
y_flat = xx[mask, 1]
z_flat = val[mask, 1]

# Interpolate on new grid
x = np.linspace(x_flat.min(), x_flat.max(), 1000)
y = np.linspace(y_flat.min(), y_flat.max(), 1000)
# grid the data.
z = griddata((x_flat, y_flat), z_flat, (x[None, :], y[:, None]), method="linear")

#################################################
figsize = (15, 15)

if True:
    # Problem: zero-values of untracked grid-points disturbe the plot

    fig, ax = plt.subplots(1, 1, figsize=figsize)

    cs = ax.contourf(x, y, z, cmap="viridis",)

    # Plot grid based on discretization
    ax.plot(
        x, y, "k-", lw=0.5, alpha=0.5,
    )
    ax.plot(
        x.T, y.T, "k-", lw=0.5, alpha=0.5,
    )
    # ax.grid(c="k", ls="-", alpha=0.5)
    fig.colorbar(cs, ax=ax, shrink=0.9, format="%.0e")
    plt.savefig(os.path.join(dir_output, "01.png"))
    plt.close("all")


if True:
    # Problem: Information about "holes" gets lost while flattening

    x, y, z = x_flat, y_flat, z_flat

    f, ax = plt.subplots(1, 2, sharex=True, sharey=True, figsize=figsize)

    ax[0].tripcolor(x.flatten(), y.flatten(), z.flatten())
    ax[1].tricontourf(
        x, y, z, 20
    )  # choose 20 contour levels, just to show how good its interpolation is
    ax[1].plot(x, y, "ko ", markersize=0.2)
    ax[0].plot(x, y, "ko ", markersize=0.2)
    plt.savefig(os.path.join(dir_output, "02.png"))


if True:

    fig, ax = plt.subplots(1, 1, figsize=figsize)

    plotable_slice = np.s_[:, 1:-2, 1:-2, :]

    x = r.x[plotable_slice][0, :, :, 0]
    y = r.x[plotable_slice][0, :, :, 1]
    val = r.x[plotable_slice][1, :, :, 1]

    cs = ax.contourf(x, y, val, cmap="viridis",)

    # Plot grid based on discretization
    ax.plot(
        x, y, "k-", lw=0.5, alpha=0.5,
    )
    ax.plot(
        x.T, y.T, "k-", lw=0.5, alpha=0.5,
    )

    # ax.grid(c="k", ls="-", alpha=0.5)
    fig.colorbar(cs, ax=ax, shrink=0.9, format="%.0e")
    plt.savefig(os.path.join(dir_output, "00.png"))
    plt.close("all")
