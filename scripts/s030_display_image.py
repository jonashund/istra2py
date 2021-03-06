#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

import istra2py
import os
import numpy as np

np.set_printoptions(
    linewidth=160,
    precision=4,
    # suppress=False,
)

dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
r = istra2py.Reader(
    path_dir_acquisition=os.path.join(dir, "data", "acquisition"),
    path_dir_export=os.path.join(dir, "data", "export"),
    # path_dir_export=os.path.join("data", "export_skipping_some_frames"),
)
r.read()


img = r.acquisition.images[3]
imgplot = plt.imshow(img)

if __name__ == "__main__":
    plt.show()
