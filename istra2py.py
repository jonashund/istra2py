#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class Reader:
    def __init__(self, path_dir, file_ending=".hdf5"):

        names = []
        for file in os.listdir(path_dir):
            if file.endswith(file_ending):
                names.append(file)
        names.sort()
        print(names)
