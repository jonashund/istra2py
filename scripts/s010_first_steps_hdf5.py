#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

np.set_printoptions(
    linewidth=160,
    precision=4,
    # suppress=False,
)

import h5py
import os

path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    "data",
    "export",
    "series_step_0.hdf5",
)

f = h5py.File(path, "r")

print(f.keys())
print()

coords = f["coordinates"]
displacements = f["displacements"]
strain = f["strains"]

print(coords.keys())
print()
print(displacements.keys())
print()
print(strain.keys())
print()

import numpy as np

matrix = strain["strain_p1"]
val = np.array(matrix).flatten()
