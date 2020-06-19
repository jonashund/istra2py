#!/usr/bin/env python
# -*- coding: utf-8 -*-
import istra2py
import os
import numpy as np

dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
r = istra2py.Reader(
    # path_dir_acquisition=os.path.join(dir, "data", "acquisition"),
    path_dir_export=os.path.join(dir, "data", "export"),
    # path_dir_export=os.path.join("data", "export_skipping_some_frames"),
)
r.read(identify_images_export=False)



if True:
    print('#########################################')
    print('Check if two masks of different steps are the same')

    h1 = r.export.get_single_hdf5_file(1)
    h2 = r.export.get_single_hdf5_file(2)

    m1 = h1["coordinates"]["mask"]

    m2 = h2["coordinates"]["mask"]

    a1 = np.array(m1, dtype=np.bool)
    a2 = np.array(m2, dtype=np.bool)

    # Define what to print
    printQueue = [
        "(a1==a2).all()",
    ]

    # Print
    for val in printQueue:
        print(val)
        print(eval(val), "\n")

    print('No, of different steps differ. This was expected')


if True:
    print('#########################################')
    print('Check if masks of different quantities of same step are the same')

    h1 = r.export.get_single_hdf5_file(6)
    m1 = h1["coordinates"]["mask"]
    m2 = h1["strains"]["mask"]
    m3 = h1["displacements"]["mask"]

    a1 = np.array(m1, dtype=np.bool)
    a2 = np.array(m2, dtype=np.bool)
    a3 = np.array(m3, dtype=np.bool)



    # Define what to print
    printQueue = [
        "(a1==a2).all()",
        "(a1==a3).all()",
        "(a2==a3).all()",
    ]

    # Print
    for val in printQueue:
        print(val)
        print(eval(val), "\n")

    print('Yes, masks of same step are equal for the data tested here.')
