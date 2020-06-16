#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import istra2py
import os


r = istra2py.EvaluationReader(os.path.join("data", "evaluation"))
# r._list_available_keys()
r.read()

import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1, figsize=(45, 45))

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
