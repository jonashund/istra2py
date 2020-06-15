#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import numpy as np
import pprint
import h5py


class Istra2pyException(Exception):
    pass


class Reader:
    def __init__(self, path_dir, file_ending=".hdf5"):
        self.path_dir = path_dir
        self._file_ending = file_ending

        self._file_names_unsorted = self._find_files_in_dir()

        print("Found the following files")
        pprint.pprint(self._file_names_unsorted)
        print()

        self.file_names = self._sort_file_names()

        print("Sorted files are")
        pprint.pprint(self.file_names)
        print()

        self.paths_files = [os.path.join(path_dir, name) for name in self.file_names]

    def _list_available_keys(self, file_index=0):
        with h5py.File(self.paths_files[file_index], "r") as first_file:
            d = {key: [k for k in first_file[key].keys()] for key in first_file.keys()}
            pprint.pprint(d)
            return d

    def read(self,):

        nbr_files = len(self.paths_files)
        with h5py.File(self.paths_files[0], "r") as first_file:
            nbr_x, nbr_y = first_file["coordinates"]["coordinate_x"].shape

        print("Processed basics are:")
        basics = {
            "Traverse force": ".traverse_force",
            "Traverse displacement": ".traverse_displ",
            "Coordinates": ".x",
            "Displacements": ".u",
            "Strains": ".eps",
        }
        pprint.pprint(basics)
        print()

        print("Indices of basics are: [nbr_files, nbr_x, nbr_y, nbr_components] with")
        print("nbr_files = ", nbr_files)
        print("nbr_x = ", nbr_x)
        print("nbr_y = ", nbr_y)

        self.traverse_force = np.zeros((nbr_files, 1), dtype=np.float64)
        self.traverse_displ = np.zeros((nbr_files, 1), dtype=np.float64)
        self.x = np.zeros((nbr_files, nbr_x, nbr_y, 2), dtype=np.float64)
        self.u = np.zeros((nbr_files, nbr_x, nbr_y, 2), dtype=np.float64)
        self.eps = np.zeros((nbr_files, nbr_x, nbr_y, 3), dtype=np.float64)

        for index_path, path in enumerate(self.paths_files):
            hdf5 = h5py.File(path, "r")

            analog = hdf5["add_data"]["analog_channels"][0]
            self.traverse_force[index_path, 0] = analog[0]  # Is this correct?
            self.traverse_displ[index_path, 0] = analog[1]  # Is this correct?

            coords = hdf5["coordinates"]
            self.x[index_path, :, :, 0] = coords["coordinate_x"][:, :]
            self.x[index_path, :, :, 1] = coords["coordinate_y"][:, :]

            disp = hdf5["displacements"]
            self.u[index_path, :, :, 0] = disp["displacement_x"][:, :]
            self.u[index_path, :, :, 1] = disp["displacement_y"][:, :]

            strain = hdf5["strains"]
            self.eps[index_path, :, :, 0] = strain["strain_xx"][:, :]
            self.eps[index_path, :, :, 1] = strain["strain_yy"][:, :]
            self.eps[index_path, :, :, 2] = strain["strain_xy"][:, :]

            hdf5.close()

    def _sort_file_names(self,):
        # Find numbers directly before file ending
        regex = re.compile(r"(\d+)" + self._file_ending)
        numbers = [int(regex.findall(name)[0]) for name in self._file_names_unsorted]
        ordered_indices = np.array(numbers).argsort()
        return np.array(self._file_names_unsorted)[ordered_indices].tolist()

    def _find_files_in_dir(self,):
        names = []
        for file in os.listdir(self.path_dir):
            if file.endswith(self._file_ending):
                names.append(file)
        names.sort()

        if not names:
            raise Istra2pyException(
                "No files with ending {} found in {}".format(
                    self._file_ending, self.path_dir
                )
            )

        return names


if __name__ == "__main__":
    r = Reader("data")
    # r._list_available_keys()
    r.read()

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1, figsize=(45, 45))

    plotable_slice = np.s_[:, 1:-2, 1:-2, :]

    x = r.x[plotable_slice][0, :, :, 0]
    y = r.x[plotable_slice][0, :, :, 1]
    val = r.x[plotable_slice][-1, :, :, 1]

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
