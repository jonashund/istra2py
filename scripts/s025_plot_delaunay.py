#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
import istra2py
import os
import numpy as np
import scipy.spatial


font = {"family": "monospace", "weight": "bold", "size": 22}
matplotlib.rc("font", **font)

np.set_printoptions(
    linewidth=160,
    precision=4,
    # suppress=False,
)


def plot_points(ax, x, y):
    # x and y can be of vector or matrix shape
    ax.plot(x, y, "ko ", markersize=0.4)


####################################################
# Select data

r = istra2py.ExportReader(os.path.join("data", "export"))
r.read()

dir_output = os.path.join(os.path.dirname(__file__), "plots_delaunay")
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

# Identify positions of DIC-grip-points where identification failed
# i.e. where coordinates are near zero
mask = np.linalg.norm(xx, axis=-1) > 1e-12

# Select data loosing grid
x_flat = xx[mask, 0]
y_flat = xx[mask, 1]
z_flat = val[mask]


points = np.concatenate((x_flat[:, None], y_flat[:, None]), axis=1)

d = scipy.spatial.Delaunay(points)

triangles = d.simplices


max_length = 30  # Todo: get this parameter algorithmically e.g. take mean of 100 random triangle edges
pairs_points_in_triangle = [[0, 1], [1, 2], [2, 0]]


mask_smaller = np.ones(len(triangles), dtype=np.bool)
for i, simp in enumerate(triangles):
    for pair in pairs_points_in_triangle:
        diff = points[simp[pair[0]]] - points[simp[pair[1]]]
        if np.linalg.norm(diff) > max_length:
            mask_smaller[i] = False

triangles_small = triangles[mask_smaller]

if not triangles_small.size == 0:
    plt.triplot(points[:, 0], points[:, 1], triangles_small)
    plt.plot(points[:, 0], points[:, 1], "o")


if True:
    name = "01_tricontourf.png"

    f, ax = plt.subplots(1, 1, figsize=figsize)

    # ax.tricontourf(X=x_flat, Y=y_flat, triangles=triangles_small, Z=z_flat, N=10)
    ax.tricontourf(x_flat, y_flat, triangles_small, z_flat, 10)

    plot_points(ax=ax, x=x_flat, y=y_flat)

    plt.savefig(os.path.join(dir_output, name))
    plt.close("all")

# if True:
#     name = "04_manually_contourf.png"
#     fig, ax = plt.subplots(1, 1, figsize=figsize)
#
#     # This slice is identified manually.
#     # This procedure does only work in special cases
#     plotable_slice = np.s_[1:-2, 1:-2, :]
#     plotable_slice = np.s_[1:-2, 1:-2, :]
#
#     x = xx[plotable_slice][:, :, 0]
#     y = xx[plotable_slice][:, :, 1]
#     val = val[plotable_slice[0:-1]][:, :]
#
#     cs = ax.contourf(x, y, val, cmap="viridis",)
#
#     # Plot grid based on discretization
#     # plot_grid(ax=ax, x_matrix=x, y_matrix=y)
#     plot_points(ax=ax, x=x, y=y)
#     ax.plot(x, y, "ko ", markersize=0.4)
#
#     fig.colorbar(cs, ax=ax, shrink=0.9, format="%.0e")
#     plt.savefig(os.path.join(dir_output, name))
#     plt.close("all")
