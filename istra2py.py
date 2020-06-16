#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import numpy as np
import pprint
import h5py


class Istra2pyException(Exception):
    pass


class ReaderDirectory:
    def __init__(self, path_dir):
        self.path_dir = path_dir
        self._file_ending = ".hdf5"

        self._file_names_unsorted = self._find_files_in_dir()
        self._file_names = self._sort_file_names()
        self.paths_files = [os.path.join(path_dir, name) for name in self._file_names]

        self.nbr_files = len(self.paths_files)

    def list_available_keys(self, file_index=1):
        with h5py.File(self.paths_files[file_index], "r") as first_file:
            d = {key: [k for k in first_file[key].keys()] for key in first_file.keys()}
            pprint.pprint(d)
            return d

    def _sort_file_names(self, verbose=True):
        # Find numbers directly before file ending
        regex = re.compile(r"(\d+)" + self._file_ending)
        numbers = [int(regex.findall(name)[0]) for name in self._file_names_unsorted]
        ordered_indices = np.array(numbers).argsort()

        file_names_sorted = np.array(self._file_names_unsorted)[
            ordered_indices
        ].tolist()

        if verbose:
            print("Sorted files are")
            pprint.pprint(file_names_sorted)
            print()

        return file_names_sorted

    def _find_files_in_dir(self, verbose=True):

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

        if verbose:
            print("Found the following files")
            pprint.pprint(names)
            print()

        return names


class Reader:
    def __init__(self, path_dir_acquisition=None, path_dir_evaluation=None):
        if path_dir_acquisition:
            self.acquisition = AcquisitionReader(path_dir=path_dir_acquisition).read()
        if path_dir_evaluation:
            self.evaluation = EvaluationReader(path_dir=path_dir_evaluation).read()


class AcquisitionReader(ReaderDirectory):
    def read(self,):
        key_main = "correlation_load_series_camera_1"
        key_images = "camera_pos_1"
        dtype_image = np.uint8

        nbr_files = self.nbr_files
        with h5py.File(self.paths_files[0], "r") as first_file:
            nbr_pix_x, nbr_pix_y = first_file[key_main][key_images].shape

        print("Extracted attributes:")
        basics = {
            "Traverse force": ".traverse_force",
            "Traverse displacement": ".traverse_displ",
            "Images": ".images",
        }
        pprint.pprint(basics)
        print()

        print("Indices of basics are: [nbr_files, nbr_x, nbr_y, nbr_components] with")
        print("nbr_files = ", nbr_files)
        print("nbr_pix_x = ", nbr_pix_x)
        print("nbr_pix_y = ", nbr_pix_y)

        self.traverse_force = np.zeros((nbr_files, 1), dtype=np.float64)
        self.traverse_displ = np.zeros((nbr_files, 1), dtype=np.float64)
        self.images = np.zeros((nbr_files, nbr_pix_x, nbr_pix_y), dtype=dtype_image)

        for index_path, path in enumerate(self.paths_files):
            hdf5 = h5py.File(path, "r")

            analog = hdf5[key_main]["analog_channels"][0]
            self.traverse_force[index_path, 0] = analog[0]  # Is this correct?
            self.traverse_displ[index_path, 0] = analog[1]  # Is this correct?

            image = hdf5[key_main][key_images]
            self.images[index_path, :, :] = image

            hdf5.close()
        return self


class EvaluationReader(ReaderDirectory):
    def read(self,):
        nbr_files = self.nbr_files

        with h5py.File(self.paths_files[0], "r") as first_file:
            nbr_x, nbr_y = first_file["coordinates"]["coordinate_x"].shape

        print("Extracted attributes:")
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
        return self


if __name__ == "__main__":
    r_e = EvaluationReader(os.path.join("data", "evaluation"))
    r_e.read()
    r_a = AcquisitionReader(os.path.join("data", "acquisition"))
    r_a.read()
    r = Reader(
        path_dir_acquisition=os.path.join("data", "acquisition"),
        path_dir_evaluation=os.path.join("data", "evaluation"),
    )
