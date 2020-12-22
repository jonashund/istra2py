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

####################################################
# Reduce redundancy


def plot_grid(ax, x_matrix, y_matrix):
    # Unsused!
    ax.plot(
        x_matrix, y_matrix, "k-", lw=0.5, alpha=0.5,
    )
    ax.plot(
        x_matrix.T, y_matrix.T, "k-", lw=0.5, alpha=0.5,
    )


def plot_points(ax, x, y):
    # x and y can be of vector or matrix shape
    ax.plot(x, y, "ko ", markersize=0.4)


####################################################
# Select data

r = istra2py.ExportReader(os.path.join("data", "export"))
r.read()

dir_output = os.path.join(os.path.dirname(__file__), "plots")
os.makedirs(dir_output, exist_ok=True)

# Select frames
index_frame_xy = 1
index_frame_val = 1

figsize = (15, 15)

# Select coordinates and data
xx = r.x[index_frame_xy, ...]
val = r.eps[index_frame_val, ..., 1]

###################################
# Create flat data

# Identify positions of DIC-grid-points where identification failed
# i.e. where coordinates are near zero
mask = np.linalg.norm(xx, axis=-1) > 1e-12

# Select data loosing grid
x_flat = xx[mask, 0]
y_flat = xx[mask, 1]
z_flat = val[mask]

###################################
# Interpolate flat data on new grid

x = np.linspace(x_flat.min(), x_flat.max(), 1000)
y = np.linspace(y_flat.min(), y_flat.max(), 1000)
# grid the data.
z = griddata((x_flat, y_flat), z_flat, (x[None, :], y[:, None]), method="linear")

#################################################


if True:
    name = "01_interpolated_contourf.png"
    # Problem: zero-values of untracked grid-points disturbe the plot

    fig, ax = plt.subplots(1, 1, figsize=figsize)

    cs = ax.contourf(x, y, z, cmap="viridis",)
    fig.colorbar(cs, ax=ax, shrink=0.9, format="%.0e")
    # cs = ax.contour(x, y, z, cmap="viridis",)

    # Plot grid based on discretization
    plot_points(ax=ax, x=x_flat, y=y_flat)

    # ax.grid(c="k", ls="-", alpha=0.5)
    plt.savefig(os.path.join(dir_output, name))
    plt.close("all")


if True:
    name = "02_flat_tripcolor.png"
    # Problem: Information about "holes" gets lost while flattening

    f, ax = plt.subplots(1, 1, figsize=figsize)

    ax.tripcolor(x_flat, y_flat, z_flat)

    plot_points(ax=ax, x=x_flat, y=y_flat)

    plt.savefig(os.path.join(dir_output, name))
    plt.close("all")


if True:
    name = "03_flat_tricontourf.png"
    # Problem: Information about "holes" gets lost while flattening

    f, ax = plt.subplots(1, 1, figsize=figsize)

    ax.tricontourf(x_flat, y_flat, z_flat, 10)

    plot_points(ax=ax, x=x_flat, y=y_flat)

    plt.savefig(os.path.join(dir_output, name))
    plt.close("all")


if True:
    name = "04_manually_contourf.png"
    fig, ax = plt.subplots(1, 1, figsize=figsize)

    # This slice is identified manually.
    # This procedure does only work in special cases
    plotable_slice = np.s_[1:-2, 1:-2, :]
    plotable_slice = np.s_[1:-2, 1:-2, :]

    x = xx[plotable_slice][:, :, 0]
    y = xx[plotable_slice][:, :, 1]
    val = val[plotable_slice[0:-1]][:, :]

    cs = ax.contourf(x, y, val, cmap="viridis",)

    # Plot grid based on discretization
    # plot_grid(ax=ax, x_matrix=x, y_matrix=y)
    plot_points(ax=ax, x=x, y=y)

    fig.colorbar(cs, ax=ax, shrink=0.9, format="%.0e")
    plt.savefig(os.path.join(dir_output, name))
    plt.close("all")
