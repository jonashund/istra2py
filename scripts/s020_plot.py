#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

#################################################
if True:
    # Problem: zero-values of untracked grid-points disturbe the plot
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
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
    plt.savefig(os.path.join(dir_output, "01.png"))
    plt.close("all")

if True:
    # Problem: Information about "holes" gets lost while flattening
    index_frame = 5
    xx = r.x[index_frame, ...]
    eps = r.eps[index_frame, ...]

    mask = np.linalg.norm(xx, axis=-1) > 1e-6
    x = xx[mask, 0].flatten()
    y = xx[mask, 1].flatten()
    z = eps[mask, 0].flatten()
    f, ax = plt.subplots(1, 2, sharex=True, sharey=True)
    ax[0].tripcolor(x, y, z)
    ax[1].tricontourf(
        x, y, z, 20
    )  # choose 20 contour levels, just to show how good its interpolation is
    ax[1].plot(x, y, "ko ", markersize=0.2)
    ax[0].plot(x, y, "ko ", markersize=0.2)
    plt.savefig(os.path.join(dir_output, "02.png"))
